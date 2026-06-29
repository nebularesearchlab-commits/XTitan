"""
Forward model utilities for synthetic Titan observation generation.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ForwardCalibration:
    """Calibration knobs inferred from available radar products."""

    radar_gain: float = 1.0
    incidence_penalty: float = 0.35
    em_depth_scale: float = 0.08
    radar_sigma: float = 0.05
    em_sigma: float = 0.06


def calibrate_from_bursts(
    bursts_df: pd.DataFrame | None,
    *,
    default_radar_sigma: float = 0.05,
) -> ForwardCalibration:
    """
    Derive lightweight forward-model calibration from derived LBDR bursts.
    """
    if bursts_df is None or bursts_df.empty:
        return ForwardCalibration(radar_sigma=default_radar_sigma, em_sigma=default_radar_sigma * 1.2)

    sigma0 = pd.to_numeric(bursts_df.get("sigma0_corrected"), errors="coerce").dropna()
    incidence = pd.to_numeric(bursts_df.get("act_incidence_angle_deg"), errors="coerce").dropna()

    if sigma0.empty:
        return ForwardCalibration(radar_sigma=default_radar_sigma, em_sigma=default_radar_sigma * 1.2)

    iqr = float(np.clip(sigma0.quantile(0.75) - sigma0.quantile(0.25), 0.01, 1.0))
    radar_sigma = max(default_radar_sigma, iqr * 0.2)
    em_sigma = radar_sigma * 1.2

    incidence_penalty = 0.35
    if not incidence.empty:
        mean_inc = float(np.clip(incidence.mean(), 5.0, 85.0))
        incidence_penalty = 0.15 + 0.5 * (mean_inc / 90.0)

    return ForwardCalibration(
        radar_gain=1.0,
        incidence_penalty=incidence_penalty,
        em_depth_scale=0.08,
        radar_sigma=radar_sigma,
        em_sigma=em_sigma,
    )


def _forward_radar(
    dielectric: np.ndarray,
    hydro_fraction: np.ndarray,
    incidence_deg: np.ndarray,
    calibration: ForwardCalibration,
) -> np.ndarray:
    """
    Synthetic radar backscatter proxy.

    The model rewards higher hydrocarbon fraction and dielectric contrast, while
    penalizing steep incidence angles where specular returns weaken.
    """
    incidence_factor = np.cos(np.deg2rad(incidence_deg)).clip(min=0.05)
    dielectric_term = np.sqrt(np.clip(dielectric, 1.0, None))
    hydro_term = np.clip(hydro_fraction, 0.0, 1.0)
    return calibration.radar_gain * (0.55 * dielectric_term + 0.45 * hydro_term) * (incidence_factor ** calibration.incidence_penalty)


def _forward_em(
    depth_km: np.ndarray,
    porosity: np.ndarray,
    calibration: ForwardCalibration,
) -> np.ndarray:
    """
    Synthetic EM attenuation proxy.

    Deeper and less porous regions attenuate more strongly.
    """
    depth_term = np.exp(-calibration.em_depth_scale * np.clip(depth_km, 0.0, None))
    porosity_term = np.clip(porosity, 0.01, 0.95)
    return depth_term * (0.6 + 0.4 * porosity_term)


def generate_observations(
    truth_df: pd.DataFrame,
    *,
    observed_fraction: float = 0.45,
    calibration: ForwardCalibration | None = None,
    noise_sigma: float | None = None,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetic observations from truth fields with configurable sparsity.
    """
    cal = calibration or ForwardCalibration()
    rng = np.random.default_rng(seed)

    n = len(truth_df)
    if n == 0:
        return pd.DataFrame(columns=["node_id", "radar_obs", "em_obs", "is_observed"])

    node_id = np.arange(n, dtype=int)
    depth = pd.to_numeric(truth_df["subsurface_depth_km"], errors="coerce").fillna(0.0).to_numpy()
    dielectric = pd.to_numeric(truth_df["dielectric_constant"], errors="coerce").fillna(2.0).to_numpy()
    hydro = pd.to_numeric(truth_df["hydrocarbon_fraction"], errors="coerce").fillna(0.1).to_numpy()
    rock_mass = pd.to_numeric(truth_df["rock_mass_kg_m3"], errors="coerce").fillna(1500.0).to_numpy()

    # Approximate porosity from density trend for a stable synthetic inversion target.
    porosity = np.clip(1.0 - (rock_mass - 700.0) / 2200.0, 0.01, 0.95)
    incidence = np.clip(15.0 + (truth_df["x"].to_numpy() % 9) * 2.0, 5.0, 80.0)

    radar_clean = _forward_radar(dielectric, hydro, incidence, cal)
    em_clean = _forward_em(depth, porosity, cal)

    sigma = float(noise_sigma if noise_sigma is not None else cal.radar_sigma)
    radar_obs = radar_clean + rng.normal(0.0, sigma, n)
    em_obs = em_clean + rng.normal(0.0, cal.em_sigma, n)

    observed_mask = rng.random(n) < float(np.clip(observed_fraction, 0.01, 1.0))
    radar_obs = np.where(observed_mask, radar_obs, np.nan)
    em_obs = np.where(observed_mask, em_obs, np.nan)

    return pd.DataFrame(
        {
            "node_id": node_id,
            "radar_obs": radar_obs,
            "em_obs": em_obs,
            "is_observed": observed_mask.astype(bool),
            "incidence_deg": incidence,
        }
    )

