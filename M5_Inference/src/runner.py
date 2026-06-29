"""
Experiment runners for ExploreTitan modes 01-04.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

from .config import (
    RuntimePaths,
    ensure_results_dirs,
    get_runtime_paths,
    load_experiment_config,
    save_metrics_csv,
    save_metrics_json,
    save_trace_json,
    utc_now_iso,
    validate_experiment_config,
)
from .distributed_fusion import distributed_inference, failure_inference_sweep
from .environment import create_synthetic_environment, ensure_phase1_input_files
from .evaluation import aggregation_stats, evaluate_phase1, rmse, summarize_trace
from .forward_model import calibrate_from_bursts, generate_observations
from .inversion import centralized_invert, initialize_local_beliefs
from .io_loaders import (
    assert_titan_metadata,
    derive_noise_hint_from_bursts,
    load_environment_table,
    load_inference_bursts,
    load_materials_table,
    load_product_metadata,
)
from .m5_network import build_agent_graph_from_environment


def _resolve_path(root: Path, configured_path: str | None) -> Path | None:
    if configured_path is None:
        return None
    path = Path(configured_path)
    if path.is_absolute():
        return path
    return root / path


def _seed_list_from_config(config: dict[str, Any], fallback_seed: int) -> list[int]:
    if "seeds" in config and isinstance(config["seeds"], list) and config["seeds"]:
        return [int(seed) for seed in config["seeds"]]
    return [int(config.get("seed", fallback_seed))]


def _build_run_metadata(experiment_key: str, config: dict[str, Any], seed: int) -> dict[str, Any]:
    return {
        "experiment_key": experiment_key,
        "seed": int(seed),
        "timestamp_utc": utc_now_iso(),
        "config": config,
    }


def _validate_or_raise(experiment_key: str, config: dict[str, Any]) -> None:
    valid, errors = validate_experiment_config(experiment_key, config)
    if not valid:
        raise ValueError(f"Invalid {experiment_key} config: {'; '.join(errors)}")


def run_experiment_01(
    *,
    config: dict[str, Any] | None = None,
    runtime_paths: RuntimePaths | None = None,
    execute_m5_protocol: Callable[..., dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Experiment 01: centralized reproducible baseline with map artifacts.
    """
    paths = runtime_paths or get_runtime_paths()
    cfg = load_experiment_config(
        "experiment_01",
        default_config={
            "env_path": "data/environments/environment_001.csv",
            "materials_path": "data/materials/titan_materials.csv",
            "noise_sigma": 0.05,
            "observed_fraction": 0.45,
            "comm_radius": 1.5,
            "preserve_top_k": 0.10,
            "run_m5_topology": True,
            "seed": 42,
        },
        runtime_paths=paths,
    )
    if config:
        cfg.update(config)
    _validate_or_raise("experiment_01", cfg)
    ensure_results_dirs(paths)

    env_default, mat_default = ensure_phase1_input_files(paths.data_root, seed=int(cfg.get("seed", 42)))
    env_path = _resolve_path(paths.root, cfg.get("env_path")) or env_default
    mat_path = _resolve_path(paths.root, cfg.get("materials_path")) or mat_default

    env_df = load_environment_table(env_path)
    materials_df = load_materials_table(mat_path)

    raw_meta = load_product_metadata(paths.inference_data_root / "raw" / "CORADR_0294" / "LBDR")
    assert_titan_metadata(raw_meta)
    bursts_df = load_inference_bursts(runtime_paths=paths, require_titan=True)
    noise_hint = derive_noise_hint_from_bursts(bursts_df, fallback_sigma=float(cfg.get("noise_sigma", 0.05)))
    calibration = calibrate_from_bursts(bursts_df, default_radar_sigma=noise_hint["radar_sigma"])

    seed_values = _seed_list_from_config(cfg, fallback_seed=int(cfg.get("seed", 42)))
    run_rows: list[dict[str, Any]] = []
    first_obs_df: pd.DataFrame | None = None
    first_pred_df: pd.DataFrame | None = None
    first_metrics: dict[str, Any] | None = None

    for run_seed in seed_values:
        obs_df = generate_observations(
            env_df,
            observed_fraction=float(cfg.get("observed_fraction", 0.45)),
            calibration=calibration,
            noise_sigma=float(cfg.get("noise_sigma", noise_hint["radar_sigma"])),
            seed=int(run_seed),
        )
        pred_df = centralized_invert(obs_df, materials_df)
        metrics = evaluate_phase1(env_df, pred_df, obs_df, comm_cost=0.0, converged=True, local_global_gap=None)

        run_rows.append(
            {
                "seed": int(run_seed),
                "rmse_hydrocarbon": float(metrics["rmse_hydrocarbon"]),
                "rmse_depth_km": float(metrics["rmse_depth_km"]),
                "rmse_porosity": float(metrics["rmse_porosity"]),
                "coverage_ratio": float(metrics["coverage_ratio"]),
                "local_global_gap": float(metrics["local_global_gap"]),
            }
        )
        if first_obs_df is None:
            first_obs_df = obs_df
            first_pred_df = pred_df
            first_metrics = metrics

    m5_summary: dict[str, Any] | None = None
    if bool(cfg.get("run_m5_topology", True)) and execute_m5_protocol is not None:
        graph = build_agent_graph_from_environment(env_df, comm_radius=float(cfg.get("comm_radius", 1.5)))
        raw_m5 = execute_m5_protocol(
            graph,
            preserve_top_k=float(cfg.get("preserve_top_k", 0.1)),
            max_iter=int(cfg.get("max_iter", 50)),
            beta=float(cfg.get("beta", 0.3)),
        )
        if isinstance(raw_m5, dict):
            comparisons = raw_m5.get("stage3", {}).get("metric_comparison", {})
            preservation_values = []
            for value in comparisons.values():
                score = value.get("preservation") if isinstance(value, dict) else None
                if score is not None and np.isfinite(score):
                    preservation_values.append(float(score))
            m5_summary = {
                "compression_ratio": float(raw_m5.get("stage2", {}).get("compression_ratio", float("nan"))),
                "critical_nodes_count": int(len(raw_m5.get("stage1", {}).get("critical_nodes", []))),
                "critical_edges_count": int(len(raw_m5.get("stage1", {}).get("significant_edges", []))),
                "mean_metric_preservation": (
                    float(np.mean(preservation_values)) if preservation_values else float("nan")
                ),
            }

    merged_map = env_df.copy().reset_index(drop=True)
    merged_map["node_id"] = merged_map.index.astype(int)
    merged_map = merged_map.merge(first_obs_df, on="node_id", how="left").merge(first_pred_df, on="node_id", how="left")
    map_rows = merged_map.to_dict(orient="records")
    map_artifact = save_metrics_csv("exp01_maps.csv", map_rows, runtime_paths=paths)

    payload = {
        "run_metadata": _build_run_metadata("experiment_01", cfg, int(seed_values[0])),
        "seed_values": seed_values,
        "runs": run_rows,
        "aggregate_rmse_hydrocarbon": aggregation_stats([float(row["rmse_hydrocarbon"]) for row in run_rows]),
        "aggregate_rmse_depth_km": aggregation_stats([float(row["rmse_depth_km"]) for row in run_rows]),
        "aggregate_rmse_porosity": aggregation_stats([float(row["rmse_porosity"]) for row in run_rows]),
        "paths": {"environment_path": str(env_path), "materials_path": str(mat_path)},
        "noise_hint": noise_hint,
        "cassini_bursts_used": int(len(bursts_df)),
        "metrics": first_metrics,
        "m5_summary": m5_summary,
        "artifacts": {"maps_csv": str(map_artifact)},
    }
    metrics_path = save_metrics_json("exp01_rmse.json", payload, runtime_paths=paths)
    return {
        "env_df": env_df,
        "materials_df": materials_df,
        "obs_df": first_obs_df,
        "pred_df": first_pred_df,
        "metrics": first_metrics,
        "payload": payload,
        "metrics_path": metrics_path,
    }


def run_experiment_02(
    *,
    config: dict[str, Any] | None = None,
    runtime_paths: RuntimePaths | None = None,
) -> dict[str, Any]:
    """
    Experiment 02: true distributed posterior updates and belief fusion.
    """
    paths = runtime_paths or get_runtime_paths()
    cfg = load_experiment_config(
        "experiment_02",
        default_config={
            "env_path": "data/environments/environment_001.csv",
            "materials_path": "data/materials/titan_materials.csv",
            "comm_radius": 1.5,
            "max_iter": 50,
            "beta": 0.3,
            "tol": 1e-3,
            "observed_fraction": 0.45,
            "noise_sigma": 0.05,
            "seed": 42,
        },
        runtime_paths=paths,
    )
    if config:
        cfg.update(config)
    _validate_or_raise("experiment_02", cfg)
    ensure_results_dirs(paths)

    env_default, mat_default = ensure_phase1_input_files(paths.data_root, seed=int(cfg.get("seed", 42)))
    env_path = _resolve_path(paths.root, cfg.get("env_path")) or env_default
    mat_path = _resolve_path(paths.root, cfg.get("materials_path")) or mat_default

    env_df = load_environment_table(env_path)
    materials_df = load_materials_table(mat_path)
    bursts_df = load_inference_bursts(runtime_paths=paths, require_titan=True)
    calibration = calibrate_from_bursts(bursts_df, default_radar_sigma=float(cfg.get("noise_sigma", 0.05)))

    seed_values = _seed_list_from_config(cfg, fallback_seed=int(cfg.get("seed", 42)))
    graph = build_agent_graph_from_environment(env_df, comm_radius=float(cfg.get("comm_radius", 1.5)))

    run_rows: list[dict[str, Any]] = []
    first_obs_df: pd.DataFrame | None = None
    first_baseline_pred: pd.DataFrame | None = None
    first_distributed_pred: pd.DataFrame | None = None
    first_trace: list[dict[str, Any]] = []
    first_baseline_metrics: dict[str, Any] | None = None
    first_distributed_metrics: dict[str, Any] | None = None
    first_trace_paths: dict[str, str] | None = None
    first_coherence = float("nan")

    for run_seed in seed_values:
        obs_df = generate_observations(
            env_df,
            observed_fraction=float(cfg.get("observed_fraction", 0.45)),
            calibration=calibration,
            noise_sigma=float(cfg.get("noise_sigma", calibration.radar_sigma)),
            seed=int(run_seed),
        )

        baseline_pred = centralized_invert(obs_df, materials_df)
        initial_beliefs = initialize_local_beliefs(obs_df, materials_df)

        distributed_pred, trace, dist_metrics = distributed_inference(
            obs_df,
            materials_df,
            graph,
            truth_df=env_df,
            initial_beliefs=initial_beliefs,
            max_iter=int(cfg.get("max_iter", 50)),
            beta=float(cfg.get("beta", 0.3)),
            tol=float(cfg.get("tol", 1e-3)),
            msg_budget=None,
            selective_messaging=True,
            seed=int(run_seed),
        )

        baseline_metrics = evaluate_phase1(env_df, baseline_pred, obs_df, comm_cost=0.0, converged=True, local_global_gap=None)
        distributed_metrics = evaluate_phase1(
            env_df,
            distributed_pred,
            obs_df,
            comm_cost=float(dist_metrics["comm_cost"]),
            converged=bool(dist_metrics["converged"]),
            local_global_gap=float(dist_metrics["local_global_gap"]),
        )
        coherence_vs_baseline = rmse(
            distributed_pred.sort_values("node_id")["hydrocarbon_fraction_est"],
            baseline_pred.sort_values("node_id")["hydrocarbon_fraction_est"],
        )

        trace_suffix = "" if len(seed_values) == 1 else f"_seed{run_seed}"
        trace_csv_path = save_metrics_csv(f"exp02_convergence_trace{trace_suffix}.csv", trace, runtime_paths=paths)
        trace_json_path = save_trace_json(f"exp02_convergence_trace{trace_suffix}.json", trace, runtime_paths=paths)

        run_rows.append(
            {
                "seed": int(run_seed),
                "rmse_hydrocarbon": float(distributed_metrics["rmse_hydrocarbon"]),
                "local_global_gap": float(distributed_metrics["local_global_gap"]),
                "comm_cost": float(distributed_metrics["comm_cost"]),
                "coherence_vs_baseline_rmse": float(coherence_vs_baseline),
                "iterations": int(dist_metrics["iterations"]),
                "converged": bool(distributed_metrics["converged"]),
            }
        )

        if first_obs_df is None:
            first_obs_df = obs_df
            first_baseline_pred = baseline_pred
            first_distributed_pred = distributed_pred
            first_trace = trace
            first_baseline_metrics = baseline_metrics
            first_distributed_metrics = distributed_metrics
            first_trace_paths = {"trace_csv": str(trace_csv_path), "trace_json": str(trace_json_path)}
            first_coherence = coherence_vs_baseline

    payload = {
        "run_metadata": _build_run_metadata("experiment_02", cfg, int(seed_values[0])),
        "seed_values": seed_values,
        "runs": run_rows,
        "aggregate_rmse_hydrocarbon": aggregation_stats([float(row["rmse_hydrocarbon"]) for row in run_rows]),
        "aggregate_local_global_gap": aggregation_stats([float(row["local_global_gap"]) for row in run_rows]),
        "aggregate_comm_cost": aggregation_stats([float(row["comm_cost"]) for row in run_rows]),
        "metrics_distributed": first_distributed_metrics,
        "metrics_baseline": first_baseline_metrics,
        "coherence_vs_baseline_rmse": first_coherence,
        "trace_summary": summarize_trace(first_trace),
        "artifacts": first_trace_paths or {},
    }
    metrics_path = save_metrics_json("exp02_rmse.json", payload, runtime_paths=paths)
    return {
        "env_df": env_df,
        "obs_df": first_obs_df,
        "baseline_pred_df": first_baseline_pred,
        "distributed_pred_df": first_distributed_pred,
        "trace": first_trace,
        "payload": payload,
        "metrics_path": metrics_path,
    }


def run_experiment_03(
    *,
    config: dict[str, Any] | None = None,
    runtime_paths: RuntimePaths | None = None,
) -> dict[str, Any]:
    """
    Experiment 03: budget-constrained messaging with communication-cost curves.
    """
    paths = runtime_paths or get_runtime_paths()
    cfg = load_experiment_config(
        "experiment_03",
        default_config={
            "msg_budget": 100,
            "preserve_top_k": 0.10,
            "network_sizes": [100, 300, 500, 1000],
            "comm_radius": 1.5,
            "max_iter": 40,
            "beta": 0.3,
            "observed_fraction": 0.45,
            "noise_sigma": 0.05,
            "seed": 42,
        },
        runtime_paths=paths,
    )
    if config:
        cfg.update(config)
    _validate_or_raise("experiment_03", cfg)
    ensure_results_dirs(paths)

    msg_budget = int(cfg.get("msg_budget", 100))
    network_sizes = [int(size) for size in cfg.get("network_sizes", [100, 300, 500, 1000])]
    seed_values = _seed_list_from_config(cfg, fallback_seed=int(cfg.get("seed", 42)))
    rows: list[dict[str, Any]] = []

    for run_seed in seed_values:
        for size_idx, size in enumerate(network_sizes):
            local_seed = int(run_seed) + size_idx
            grid_size = int(math.ceil(math.sqrt(size)))
            env_df = create_synthetic_environment(grid_size=grid_size, seed=local_seed).iloc[:size].copy()

            env_tmp_path = paths.results_traces_dir / f"_tmp_env_exp03_seed{run_seed}_{size}.csv"
            env_tmp_path.parent.mkdir(parents=True, exist_ok=True)
            env_df.to_csv(env_tmp_path, index=False)
            env_df = load_environment_table(env_tmp_path)
            _, mat_default = ensure_phase1_input_files(paths.data_root, seed=local_seed)
            materials_df = load_materials_table(mat_default)

            obs_df = generate_observations(
                env_df,
                observed_fraction=float(cfg.get("observed_fraction", 0.45)),
                noise_sigma=float(cfg.get("noise_sigma", 0.05)),
                seed=local_seed,
            )
            graph = build_agent_graph_from_environment(env_df, comm_radius=float(cfg.get("comm_radius", 1.5)))
            initial = initialize_local_beliefs(obs_df, materials_df)

            pred_df, trace, dist_metrics = distributed_inference(
                obs_df,
                materials_df,
                graph,
                truth_df=env_df,
                initial_beliefs=initial,
                max_iter=int(cfg.get("max_iter", 40)),
                beta=float(cfg.get("beta", 0.3)),
                tol=float(cfg.get("tol", 1e-3)),
                msg_budget=msg_budget,
                selective_messaging=True,
                seed=local_seed,
            )
            metrics = evaluate_phase1(
                env_df,
                pred_df,
                obs_df,
                comm_cost=float(dist_metrics["comm_cost"]),
                converged=bool(dist_metrics["converged"]),
                local_global_gap=float(dist_metrics["local_global_gap"]),
            )
            rows.append(
                {
                    "seed": int(run_seed),
                    "network_size": size,
                    "msg_budget": msg_budget,
                    "rmse_hydrocarbon": metrics["rmse_hydrocarbon"],
                    "local_global_gap": metrics["local_global_gap"],
                    "comm_cost": metrics["comm_cost"],
                    "iterations": int(dist_metrics["iterations"]),
                    "converged": bool(metrics["converged"]),
                }
            )
            save_trace_json(f"exp03_trace_seed{run_seed}_{size}.json", trace, runtime_paths=paths)
            env_tmp_path.unlink(missing_ok=True)

    curve_path = save_metrics_csv("exp03_comm_accuracy_curve.csv", rows, runtime_paths=paths)
    grouped_stats: list[dict[str, Any]] = []
    if rows:
        grouped_df = pd.DataFrame(rows)
        for size, group in grouped_df.groupby("network_size"):
            grouped_stats.append(
                {
                    "network_size": int(size),
                    "rmse_hydrocarbon_mean": float(group["rmse_hydrocarbon"].mean()),
                    "rmse_hydrocarbon_std": float(group["rmse_hydrocarbon"].std(ddof=0)),
                    "local_global_gap_mean": float(group["local_global_gap"].mean()),
                    "local_global_gap_std": float(group["local_global_gap"].std(ddof=0)),
                    "comm_cost_mean": float(group["comm_cost"].mean()),
                    "comm_cost_std": float(group["comm_cost"].std(ddof=0)),
                }
            )
    summary_payload = {
        "run_metadata": _build_run_metadata("experiment_03", cfg, int(seed_values[0])),
        "seed_values": seed_values,
        "curve_points": rows,
        "grouped_by_network_size": grouped_stats,
        "rmse_stats": aggregation_stats([float(row["rmse_hydrocarbon"]) for row in rows]),
        "coherence_stats": aggregation_stats([float(row["local_global_gap"]) for row in rows]),
        "comm_cost_stats": aggregation_stats([float(row["comm_cost"]) for row in rows]),
        "artifacts": {"curve_csv": str(curve_path)},
    }
    summary_path = save_metrics_json("exp03_scaling_summary.json", summary_payload, runtime_paths=paths)
    return {
        "curve_rows": rows,
        "summary": summary_payload,
        "summary_path": summary_path,
    }


def run_experiment_04(
    *,
    config: dict[str, Any] | None = None,
    runtime_paths: RuntimePaths | None = None,
) -> dict[str, Any]:
    """
    Experiment 04: failure dynamics coupled to distributed inference performance.
    """
    paths = runtime_paths or get_runtime_paths()
    cfg = load_experiment_config(
        "experiment_04",
        default_config={
            "env_path": "data/environments/environment_001.csv",
            "materials_path": "data/materials/titan_materials.csv",
            "comm_radius": 1.5,
            "max_iter": 40,
            "beta": 0.3,
            "msg_budget": 100,
            "removal_strategy": "targeted",
            "removal_steps": [0.05, 0.10, 0.25, 0.50],
            "observed_fraction": 0.45,
            "noise_sigma": 0.05,
            "seed": 42,
        },
        runtime_paths=paths,
    )
    if config:
        cfg.update(config)
    _validate_or_raise("experiment_04", cfg)
    ensure_results_dirs(paths)

    env_default, mat_default = ensure_phase1_input_files(paths.data_root, seed=int(cfg.get("seed", 42)))
    env_path = _resolve_path(paths.root, cfg.get("env_path")) or env_default
    mat_path = _resolve_path(paths.root, cfg.get("materials_path")) or mat_default

    env_df = load_environment_table(env_path)
    materials_df = load_materials_table(mat_path)
    graph = build_agent_graph_from_environment(env_df, comm_radius=float(cfg.get("comm_radius", 1.5)))

    seed_values = _seed_list_from_config(cfg, fallback_seed=int(cfg.get("seed", 42)))
    all_rows: list[dict[str, Any]] = []
    all_traces: dict[str, list[dict[str, Any]]] = {}
    first_percolation_df: pd.DataFrame | None = None
    first_traces: dict[str, list[dict[str, Any]]] | None = None

    for run_seed in seed_values:
        obs_df = generate_observations(
            env_df,
            observed_fraction=float(cfg.get("observed_fraction", 0.45)),
            noise_sigma=float(cfg.get("noise_sigma", 0.05)),
            seed=int(run_seed),
        )
        percolation_df, traces = failure_inference_sweep(
            obs_df,
            materials_df,
            graph,
            truth_df=env_df,
            removal_steps=[float(step) for step in cfg.get("removal_steps", [0.05, 0.10, 0.25, 0.50])],
            removal_strategy=str(cfg.get("removal_strategy", "targeted")),
            max_iter=int(cfg.get("max_iter", 40)),
            beta=float(cfg.get("beta", 0.3)),
            tol=float(cfg.get("tol", 1e-3)),
            msg_budget=int(cfg.get("msg_budget", 100)),
            selective_messaging=True,
            seed=int(run_seed),
        )
        seed_rows = percolation_df.copy()
        seed_rows["seed"] = int(run_seed)
        all_rows.extend(seed_rows.to_dict(orient="records"))
        for key, trace in traces.items():
            trace_key = f"seed{run_seed}_step{key}"
            all_traces[trace_key] = trace
            save_trace_json(f"exp04_trace_{trace_key}.json", trace, runtime_paths=paths)

        if first_percolation_df is None:
            first_percolation_df = percolation_df
            first_traces = traces

    percolation_csv = save_metrics_csv("exp04_percolation_curve.csv", all_rows, runtime_paths=paths)
    grouped_stats: list[dict[str, Any]] = []
    if all_rows:
        grouped_df = pd.DataFrame(all_rows)
        for step, group in grouped_df.groupby("removal_fraction"):
            grouped_stats.append(
                {
                    "removal_fraction": float(step),
                    "rmse_hydrocarbon_mean": float(group["rmse_hydrocarbon"].mean()),
                    "rmse_hydrocarbon_std": float(group["rmse_hydrocarbon"].std(ddof=0)),
                    "local_global_gap_mean": float(group["local_global_gap"].mean()),
                    "local_global_gap_std": float(group["local_global_gap"].std(ddof=0)),
                    "comm_cost_mean": float(group["comm_cost"].mean()),
                    "comm_cost_std": float(group["comm_cost"].std(ddof=0)),
                    "lcc_fraction_mean": float(group["lcc_fraction"].mean()),
                }
            )

    payload = {
        "run_metadata": _build_run_metadata("experiment_04", cfg, int(seed_values[0])),
        "seed_values": seed_values,
        "per_step_metrics": all_rows,
        "grouped_by_removal_fraction": grouped_stats,
        "artifacts": {"percolation_csv": str(percolation_csv)},
    }
    metrics_path = save_metrics_json("exp04_percolation.json", payload, runtime_paths=paths)

    if len(seed_values) > 1 and grouped_stats:
        percolation_df_out = pd.DataFrame(grouped_stats).rename(
            columns={
                "rmse_hydrocarbon_mean": "rmse_hydrocarbon",
                "local_global_gap_mean": "local_global_gap",
            }
        )
    else:
        percolation_df_out = first_percolation_df.copy() if first_percolation_df is not None else pd.DataFrame()
    return {
        "percolation_df": percolation_df_out,
        "traces": first_traces or {},
        "payload": payload,
        "metrics_path": metrics_path,
    }

