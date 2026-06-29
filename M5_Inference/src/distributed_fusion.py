"""
Distributed posterior update and belief-fusion routines.
"""

from __future__ import annotations

from typing import Any

import networkx as nx
import numpy as np
import pandas as pd

from .evaluation import compute_local_global_gap, rmse
from .inversion import STATE_COLUMNS, initialize_local_beliefs, local_posterior_update
from .m5_network import apply_failure_step, largest_component_fraction


def _neighbors(graph: nx.Graph, node: int) -> list[int]:
    if graph.is_directed():
        return [int(n) for n in graph.successors(node)]
    return [int(n) for n in graph.neighbors(node)]


def _select_neighbors(
    candidate_neighbors: list[int],
    uncertainty: pd.Series,
    *,
    selective: bool,
    max_messages_for_node: int | None,
) -> list[int]:
    if not candidate_neighbors:
        return []
    neighbors = list(candidate_neighbors)
    if selective:
        neighbors = sorted(neighbors, key=lambda n: float(uncertainty.get(n, 0.0)), reverse=True)
    if max_messages_for_node is None:
        return neighbors
    return neighbors[: max(0, max_messages_for_node)]


def distributed_inference(
    obs_df: pd.DataFrame,
    materials_df: pd.DataFrame,
    graph: nx.Graph,
    *,
    truth_df: pd.DataFrame | None = None,
    initial_beliefs: pd.DataFrame | None = None,
    max_iter: int = 50,
    beta: float = 0.3,
    tol: float = 1e-3,
    msg_budget: int | None = None,
    selective_messaging: bool = True,
    payload_bytes: int = 56,
    seed: int = 42,
) -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, Any]]:
    """
    Run iterative distributed inference with local updates and belief fusion.
    """
    rng = np.random.default_rng(seed)
    beliefs = initial_beliefs.copy() if initial_beliefs is not None else initialize_local_beliefs(obs_df, materials_df)
    if beliefs.empty:
        return beliefs, [], {"comm_cost": 0.0, "local_global_gap": float("nan"), "converged": False}

    beliefs = beliefs.set_index("node_id").sort_index()
    active_nodes = [node for node in beliefs.index if graph.has_node(int(node))]
    beliefs = beliefs.loc[active_nodes].copy()
    if beliefs.empty:
        return beliefs.reset_index(), [], {"comm_cost": 0.0, "local_global_gap": float("nan"), "converged": False}

    for col in STATE_COLUMNS:
        beliefs[col] = pd.to_numeric(beliefs[col], errors="coerce").fillna(0.0)
    beliefs["posterior_uncertainty"] = pd.to_numeric(
        beliefs.get("posterior_uncertainty", 0.09),
        errors="coerce",
    ).fillna(0.09)

    obs_rows = obs_df.set_index("node_id")
    total_messages = 0
    trace: list[dict[str, Any]] = []
    converged = False

    for iteration in range(1, int(max_iter) + 1):
        prior_states = beliefs[STATE_COLUMNS].copy()
        local_states = beliefs.copy()

        # Step A: local update at each node.
        for node in local_states.index:
            if node in obs_rows.index:
                row = obs_rows.loc[node]
            else:
                row = pd.Series({"radar_obs": np.nan, "em_obs": np.nan, "is_observed": False})

            gain = 0.75 if bool(row.get("is_observed", False)) else 0.2
            updated = local_posterior_update(local_states.loc[node, STATE_COLUMNS].to_dict(), row, materials_df, local_gain=gain)
            for key in STATE_COLUMNS:
                local_states.at[node, key] = float(updated[key])

        # Step B: inter-agent fusion under optional communication budget.
        fused = local_states.copy()
        iter_messages = 0
        budget_left = int(msg_budget) if msg_budget is not None else None
        uncertainty = local_states["posterior_uncertainty"].copy()

        # Randomized tie-breaking prevents deterministic lockstep on identical states.
        node_order = list(local_states.index)
        rng.shuffle(node_order)
        if selective_messaging:
            node_order = sorted(node_order, key=lambda n: float(uncertainty.get(n, 0.0)), reverse=True)

        per_node_cap = None
        if budget_left is not None and len(node_order) > 0:
            per_node_cap = max(1, budget_left // len(node_order))

        for node in node_order:
            if budget_left is not None and budget_left <= 0:
                break

            neighbors = [n for n in _neighbors(graph, int(node)) if n in local_states.index and n != node]
            if not neighbors:
                continue

            selected = _select_neighbors(
                neighbors,
                uncertainty,
                selective=selective_messaging,
                max_messages_for_node=per_node_cap,
            )
            if budget_left is not None:
                selected = selected[:budget_left]
            if not selected:
                continue

            neighbor_mean = local_states.loc[selected, STATE_COLUMNS].mean(axis=0)
            self_state = local_states.loc[node, STATE_COLUMNS]
            fused.loc[node, STATE_COLUMNS] = (1.0 - beta) * self_state + beta * neighbor_mean

            iter_messages += len(selected)
            if budget_left is not None:
                budget_left -= len(selected)

            # Uncertainty falls with incoming corroboration.
            fused.at[node, "posterior_uncertainty"] = float(
                np.clip(local_states.at[node, "posterior_uncertainty"] * np.exp(-0.12 * len(selected)), 0.004, 0.25)
            )

        beliefs = fused
        total_messages += iter_messages
        max_state_change = float((beliefs[STATE_COLUMNS] - prior_states).abs().max().max())
        local_global_gap = compute_local_global_gap(beliefs.reset_index())
        cumulative_comm_cost = float(total_messages * payload_bytes)
        converged = max_state_change < float(tol)

        rmse_hydro = float("nan")
        if truth_df is not None and not truth_df.empty:
            truth_indexed = truth_df.copy().reset_index(drop=True)
            truth_indexed["node_id"] = truth_indexed.index.astype(int)
            merged = truth_indexed.merge(
                beliefs.reset_index()[["node_id", "hydrocarbon_fraction_est"]],
                on="node_id",
                how="inner",
            )
            rmse_hydro = rmse(merged["hydrocarbon_fraction"], merged["hydrocarbon_fraction_est"])

        trace.append(
            {
                "iteration": iteration,
                "messages_this_iter": int(iter_messages),
                "cumulative_messages": int(total_messages),
                "cumulative_comm_cost": cumulative_comm_cost,
                "max_state_change": max_state_change,
                "local_global_gap": local_global_gap,
                "rmse_hydrocarbon": rmse_hydro,
                "converged": converged,
            }
        )
        if converged:
            break

    output = beliefs.reset_index()
    metrics = {
        "iterations": len(trace),
        "total_messages": int(total_messages),
        "comm_cost": float(total_messages * payload_bytes),
        "local_global_gap": float(compute_local_global_gap(output)),
        "converged": bool(converged),
    }
    return output, trace, metrics


def failure_inference_sweep(
    obs_df: pd.DataFrame,
    materials_df: pd.DataFrame,
    base_graph: nx.Graph,
    *,
    truth_df: pd.DataFrame | None = None,
    removal_steps: list[float] | tuple[float, ...] = (0.05, 0.10, 0.25, 0.50),
    removal_strategy: str = "targeted",
    max_iter: int = 50,
    beta: float = 0.3,
    tol: float = 1e-3,
    msg_budget: int | None = None,
    selective_messaging: bool = True,
    payload_bytes: int = 56,
    seed: int = 42,
) -> tuple[pd.DataFrame, dict[str, list[dict[str, Any]]]]:
    """
    Apply progressive failures and run distributed inference at each step.
    """
    rows: list[dict[str, Any]] = []
    traces: dict[str, list[dict[str, Any]]] = {}
    base = base_graph.copy()

    for idx, step in enumerate(removal_steps):
        failed_graph, removed = apply_failure_step(
            base,
            removal_fraction=float(step),
            strategy=str(removal_strategy),
            seed=seed + idx,
        )
        active_nodes = sorted(int(node) for node in failed_graph.nodes())
        sub_obs = obs_df[obs_df["node_id"].isin(active_nodes)].copy()
        if sub_obs.empty:
            rows.append(
                {
                    "removal_fraction": float(step),
                    "active_nodes": 0,
                    "removed_nodes": len(removed),
                    "lcc_fraction": 0.0,
                    "rmse_hydrocarbon": float("nan"),
                    "local_global_gap": float("nan"),
                    "comm_cost": 0.0,
                    "converged": False,
                }
            )
            traces[f"{step:.3f}"] = []
            continue

        sub_truth = None
        if truth_df is not None:
            truth_with_node = truth_df.copy().reset_index(drop=True)
            truth_with_node["node_id"] = truth_with_node.index.astype(int)
            sub_truth = truth_with_node[truth_with_node["node_id"].isin(active_nodes)].copy()

        pred_df, trace, metrics = distributed_inference(
            sub_obs,
            materials_df,
            failed_graph,
            truth_df=sub_truth,
            max_iter=max_iter,
            beta=beta,
            tol=tol,
            msg_budget=msg_budget,
            selective_messaging=selective_messaging,
            payload_bytes=payload_bytes,
            seed=seed + 100 + idx,
        )

        rmse_hydro = float("nan")
        if sub_truth is not None and not sub_truth.empty:
            merged = sub_truth.merge(
                pred_df[["node_id", "hydrocarbon_fraction_est"]],
                on="node_id",
                how="inner",
            )
            rmse_hydro = rmse(merged["hydrocarbon_fraction"], merged["hydrocarbon_fraction_est"])

        rows.append(
            {
                "removal_fraction": float(step),
                "active_nodes": int(len(active_nodes)),
                "removed_nodes": int(len(removed)),
                "lcc_fraction": float(largest_component_fraction(failed_graph)),
                "rmse_hydrocarbon": rmse_hydro,
                "local_global_gap": float(metrics["local_global_gap"]),
                "comm_cost": float(metrics["comm_cost"]),
                "converged": bool(metrics["converged"]),
            }
        )
        traces[f"{step:.3f}"] = trace

    return pd.DataFrame(rows), traces

