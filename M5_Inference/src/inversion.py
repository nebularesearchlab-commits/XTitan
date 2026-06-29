"""
Centralized and local inversion helpers for ExploreTitan.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


STATE_COLUMNS = [
    "hydrocarbon_fraction_est",
    "subsurface_depth_km_est",
    "porosity_est",
    "dielectric_constant_est",
]


def _prior_from_materials(materials_df: pd.DataFrame) -> dict[str, float]:
    """Build physically plausible priors from available material properties."""
    density_mean = float(pd.to_numeric(materials_df["density_kg_m3"], errors="coerce").dropna().mean())
    perm_mean = float(pd.to_numeric(materials_df["permittivity"], errors="coerce").dropna().mean())
    hydro_mean = float(pd.to_numeric(materials_df["hydrocarbon_factor"], errors="coerce").dropna().mean())

    density_mean = density_mean if np.isfinite(density_mean) else 1300.0
    perm_mean = perm_mean if np.isfinite(perm_mean) else 3.1
    hydro_mean = hydro_mean if np.isfinite(hydro_mean) else 0.25

    porosity_prior = float(np.clip(1.0 - (density_mean - 700.0) / 2200.0, 0.05, 0.9))
    return {
        "hydrocarbon_fraction_est": float(np.clip(hydro_mean, 0.01, 0.95)),
        "subsurface_depth_km_est": 8.0,
        "porosity_est": porosity_prior,
        "dielectric_constant_est": float(np.clip(perm_mean, 1.6, 8.0)),
    }


def _invert_single_observation(
    radar_obs: float | None,
    em_obs: float | None,
    prior: dict[str, float],
) -> dict[str, float]:
    """
    Invert one observation pair into state variables with stable clamps.
    """
    if radar_obs is None or not np.isfinite(radar_obs):
        return dict(prior)

    radar = float(radar_obs)
    hydro = float(np.clip((radar - 0.35) / 1.5, 0.01, 0.98))
    dielectric = float(np.clip(1.6 + 3.3 * hydro, 1.6, 6.5))

    if em_obs is None or not np.isfinite(em_obs):
        depth = prior["subsurface_depth_km_est"]
    else:
        em = max(float(em_obs), 1e-4)
        depth = float(np.clip(-np.log(em) / 0.08, 0.8, 20.0))

    porosity = float(np.clip(0.7 - 0.04 * depth + 0.25 * hydro, 0.02, 0.95))
    return {
        "hydrocarbon_fraction_est": hydro,
        "subsurface_depth_km_est": depth,
        "porosity_est": porosity,
        "dielectric_constant_est": dielectric,
    }


def centralized_invert(obs_df: pd.DataFrame, materials_df: pd.DataFrame) -> pd.DataFrame:
    """
    Centralized inversion using all available observations and priors.
    """
    prior = _prior_from_materials(materials_df)
    rows = []
    for _, row in obs_df.iterrows():
        node_id = int(row["node_id"])
        inv = _invert_single_observation(row.get("radar_obs"), row.get("em_obs"), prior)
        unc = 0.025 if bool(row.get("is_observed", False)) else 0.09
        rows.append({"node_id": node_id, **inv, "posterior_uncertainty": unc})
    return pd.DataFrame(rows)


def local_posterior_update(
    current_state: dict[str, float],
    row: pd.Series,
    materials_df: pd.DataFrame,
    *,
    local_gain: float = 0.75,
) -> dict[str, float]:
    """
    Local agent update: blend previous belief with new local observation.
    """
    prior = _prior_from_materials(materials_df)
    observed_state = _invert_single_observation(row.get("radar_obs"), row.get("em_obs"), prior)

    out: dict[str, float] = {}
    for key in STATE_COLUMNS:
        old = float(current_state.get(key, prior[key]))
        new = float(observed_state[key])
        out[key] = (1.0 - local_gain) * old + local_gain * new
    return out


def initialize_local_beliefs(obs_df: pd.DataFrame, materials_df: pd.DataFrame) -> pd.DataFrame:
    """
    Initialize local beliefs before distributed fusion starts.
    """
    base = centralized_invert(obs_df, materials_df)
    if "is_observed" in obs_df.columns:
        observed = obs_df[["node_id", "is_observed"]].copy()
        base = base.merge(observed, on="node_id", how="left")
    else:
        base["is_observed"] = False
    return base

