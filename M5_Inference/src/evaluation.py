"""
Evaluation metrics for ExploreTitan experiments.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd


def rmse(truth: pd.Series, pred: pd.Series) -> float:
    """Root-mean-square error with NaN-safe coercion."""
    t = pd.to_numeric(truth, errors="coerce").to_numpy()
    p = pd.to_numeric(pred, errors="coerce").to_numpy()
    mask = np.isfinite(t) & np.isfinite(p)
    if mask.sum() == 0:
        return float("nan")
    return float(np.sqrt(np.mean((t[mask] - p[mask]) ** 2)))


def compute_local_global_gap(distributed_pred_df: pd.DataFrame) -> float:
    """
    Coherence proxy: mean absolute local deviation from global hydro mean.
    """
    if distributed_pred_df.empty or "hydrocarbon_fraction_est" not in distributed_pred_df.columns:
        return float("nan")
    hydro = pd.to_numeric(distributed_pred_df["hydrocarbon_fraction_est"], errors="coerce")
    center = hydro.mean(skipna=True)
    if not np.isfinite(center):
        return float("nan")
    return float((hydro - center).abs().mean(skipna=True))


def summarize_trace(trace: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize convergence and communication trace into scalar stats."""
    if not trace:
        return {
            "iterations": 0,
            "comm_cost": 0.0,
            "converged": False,
            "final_change": float("nan"),
            "local_global_gap": float("nan"),
        }
    final = trace[-1]
    return {
        "iterations": len(trace),
        "comm_cost": float(final.get("cumulative_comm_cost", 0.0)),
        "converged": bool(final.get("converged", False)),
        "final_change": float(final.get("max_state_change", float("nan"))),
        "local_global_gap": float(final.get("local_global_gap", float("nan"))),
    }


def evaluate_phase1(
    truth_df: pd.DataFrame,
    pred_df: pd.DataFrame,
    obs_df: pd.DataFrame,
    *,
    comm_cost: float = 0.0,
    converged: bool = True,
    local_global_gap: float | None = None,
) -> dict[str, float | bool]:
    """
    Core metrics used across baseline and distributed experiment runs.
    """
    merged = truth_df.copy().reset_index(drop=True)
    merged["node_id"] = merged.index.astype(int)
    merged = merged.merge(pred_df, on="node_id", how="left")
    merged = merged.merge(obs_df[["node_id", "is_observed"]], on="node_id", how="left")

    # Resolve merge collisions when prediction frames already include `is_observed`.
    if "is_observed" not in merged.columns:
        if "is_observed_y" in merged.columns:
            merged["is_observed"] = merged["is_observed_y"]
        elif "is_observed_x" in merged.columns:
            merged["is_observed"] = merged["is_observed_x"]
        else:
            merged["is_observed"] = False

    observed_fraction = float(pd.to_numeric(merged["is_observed"], errors="coerce").fillna(0).mean())
    uncertainty = pd.to_numeric(merged.get("posterior_uncertainty"), errors="coerce")
    uncertainty_reduction = float((1.0 - uncertainty.mean() / 0.10) if uncertainty.notna().any() else 0.0)

    if local_global_gap is None or not np.isfinite(local_global_gap):
        local_global_gap = compute_local_global_gap(pred_df)

    return {
        "rmse_hydrocarbon": rmse(merged["hydrocarbon_fraction"], merged["hydrocarbon_fraction_est"]),
        "rmse_depth_km": rmse(merged["subsurface_depth_km"], merged["subsurface_depth_km_est"]),
        "rmse_porosity": rmse(
            pd.to_numeric(1.0 - (merged["rock_mass_kg_m3"] - 700.0) / 2200.0, errors="coerce"),
            merged["porosity_est"],
        ),
        "coverage_ratio": observed_fraction,
        "uncertainty_reduction": uncertainty_reduction,
        "comm_cost": float(comm_cost),
        "local_global_gap": float(local_global_gap) if local_global_gap is not None else float("nan"),
        "converged": bool(converged),
    }


def aggregation_stats(values: list[float]) -> dict[str, float]:
    """Mean/std/95% CI summary for repeated runs."""
    arr = np.array(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return {"mean": float("nan"), "std": float("nan"), "ci95": float("nan")}
    mean = float(arr.mean())
    std = float(arr.std(ddof=1)) if arr.size > 1 else 0.0
    ci95 = float(1.96 * std / math.sqrt(arr.size)) if arr.size > 1 else 0.0
    return {"mean": mean, "std": std, "ci95": ci95}

