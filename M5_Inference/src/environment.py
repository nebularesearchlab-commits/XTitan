"""
Environment and materials utilities for ExploreTitan.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_ENV_COLUMNS = {
    "x",
    "y",
    "subsurface_depth_km",
    "dielectric_constant",
    "hydrocarbon_fraction",
    "rock_mass_kg_m3",
    "temperature_K",
}

REQUIRED_MATERIAL_COLUMNS = {
    "material",
    "density_kg_m3",
    "permittivity",
    "conductivity_S_m",
    "hydrocarbon_factor",
}


def create_default_materials_df() -> pd.DataFrame:
    """
    Build default Titan material properties when no local file exists.
    """
    return pd.DataFrame(
        [
            {
                "material": "water_ice",
                "density_kg_m3": 920.0,
                "permittivity": 3.1,
                "conductivity_S_m": 1.0e-5,
                "hydrocarbon_factor": 0.1,
            },
            {
                "material": "tholin_mix",
                "density_kg_m3": 1100.0,
                "permittivity": 2.4,
                "conductivity_S_m": 8.0e-6,
                "hydrocarbon_factor": 0.45,
            },
            {
                "material": "liquid_hc",
                "density_kg_m3": 510.0,
                "permittivity": 1.9,
                "conductivity_S_m": 1.0e-7,
                "hydrocarbon_factor": 0.95,
            },
            {
                "material": "silicate_mix",
                "density_kg_m3": 2600.0,
                "permittivity": 5.8,
                "conductivity_S_m": 3.0e-4,
                "hydrocarbon_factor": 0.03,
            },
        ]
    )


def canonicalize_environment_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize legacy and new environment schemas into one canonical format.
    """
    out = df.copy()

    if "subsurface_depth_km" not in out.columns and "depth" in out.columns:
        depth_raw = pd.to_numeric(out["depth"], errors="coerce")
        scale = 0.01 if depth_raw.median(skipna=True) > 50 else 1.0
        out["subsurface_depth_km"] = depth_raw * scale

    if "rock_mass_kg_m3" not in out.columns:
        if "porosity" in out.columns:
            porosity = pd.to_numeric(out["porosity"], errors="coerce").fillna(0.3).clip(0.01, 0.95)
            out["rock_mass_kg_m3"] = 700.0 + (1.0 - porosity) * 2200.0
        else:
            out["rock_mass_kg_m3"] = 1500.0

    if "temperature_K" not in out.columns:
        out["temperature_K"] = 94.0

    for col, default in {
        "x": 0.0,
        "y": 0.0,
        "dielectric_constant": 2.4,
        "hydrocarbon_fraction": 0.2,
    }.items():
        if col not in out.columns:
            out[col] = default

    if "node_id" not in out.columns:
        out["node_id"] = np.arange(len(out), dtype=int)

    return out


def canonicalize_materials_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize legacy and new material schemas into one canonical format.
    """
    out = df.copy()

    if "material" not in out.columns and "material_class" in out.columns:
        out["material"] = out["material_class"]

    if "permittivity" not in out.columns:
        if {"dielectric_min", "dielectric_max"}.issubset(out.columns):
            out["permittivity"] = (
                pd.to_numeric(out["dielectric_min"], errors="coerce")
                + pd.to_numeric(out["dielectric_max"], errors="coerce")
            ) / 2.0
        else:
            out["permittivity"] = 2.5

    if "conductivity_S_m" not in out.columns:
        material_names = out.get("material", pd.Series(["unknown"] * len(out))).astype(str).str.lower()
        out["conductivity_S_m"] = np.where(material_names.str.contains("silicate"), 3.0e-4, 1.0e-5)

    if "hydrocarbon_factor" not in out.columns:
        material_names = out.get("material", pd.Series(["unknown"] * len(out))).astype(str).str.lower()
        out["hydrocarbon_factor"] = np.where(
            material_names.str.contains("hydrocarbon|liquid|methane"),
            0.9,
            np.where(material_names.str.contains("tholin"), 0.45, 0.1),
        )

    if "density_kg_m3" not in out.columns:
        out["density_kg_m3"] = 1200.0

    return out


def create_synthetic_environment(grid_size: int = 10, seed: int = 42) -> pd.DataFrame:
    """
    Create a synthetic Titan-like 2D environment used by baseline experiments.
    """
    rng = np.random.default_rng(seed)
    xs, ys = np.meshgrid(np.arange(grid_size), np.arange(grid_size))
    count = grid_size * grid_size

    # Generate smooth geological trends plus moderate stochastic variability.
    depth = np.clip(8.0 + 2.0 * np.sin(xs.ravel() / 3.0) + rng.normal(0.0, 0.5, count), 1.5, None)
    hydrocarbon = np.clip(0.25 + 0.35 * np.cos(ys.ravel() / 4.0) + rng.normal(0.0, 0.08, count), 0.01, 0.98)
    dielectric = np.clip(2.2 + 1.8 * hydrocarbon + rng.normal(0.0, 0.15, count), 1.6, 6.5)
    rock_mass = np.clip(1200.0 + 900.0 * (1.0 - hydrocarbon) + rng.normal(0.0, 45.0, count), 700.0, None)
    temperature = np.clip(90.0 + 2.5 * np.sin((xs.ravel() + ys.ravel()) / 6.0) + rng.normal(0.0, 0.4, count), 80.0, 110.0)

    return pd.DataFrame(
        {
            "x": xs.ravel().astype(float),
            "y": ys.ravel().astype(float),
            "subsurface_depth_km": depth,
            "dielectric_constant": dielectric,
            "hydrocarbon_fraction": hydrocarbon,
            "rock_mass_kg_m3": rock_mass,
            "temperature_K": temperature,
        }
    )


def validate_environment_df(df: pd.DataFrame) -> None:
    """Raise a clear error if an environment table is missing required columns."""
    normalized = canonicalize_environment_df(df)
    missing = REQUIRED_ENV_COLUMNS.difference(normalized.columns)
    if missing:
        raise ValueError(f"Environment data is missing required columns: {sorted(missing)}")


def validate_materials_df(df: pd.DataFrame) -> None:
    """Raise a clear error if a materials table is missing required columns."""
    normalized = canonicalize_materials_df(df)
    missing = REQUIRED_MATERIAL_COLUMNS.difference(normalized.columns)
    if missing:
        raise ValueError(f"Materials data is missing required columns: {sorted(missing)}")


def ensure_phase1_input_files(
    data_root: str | Path,
    *,
    env_filename: str = "environment_001.csv",
    materials_filename: str = "titan_materials.csv",
    seed: int = 42,
) -> tuple[Path, Path]:
    """
    Ensure baseline environment and material files exist for Experiment 01.
    """
    data_root = Path(data_root)
    env_dir = data_root / "environments"
    mat_dir = data_root / "materials"
    env_dir.mkdir(parents=True, exist_ok=True)
    mat_dir.mkdir(parents=True, exist_ok=True)

    env_path = env_dir / env_filename
    mat_path = mat_dir / materials_filename

    if not env_path.exists():
        create_synthetic_environment(seed=seed).to_csv(env_path, index=False)
    if not mat_path.exists():
        create_default_materials_df().to_csv(mat_path, index=False)

    return env_path, mat_path

