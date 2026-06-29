"""
I/O loaders with canonical data resolution and Titan-only guards.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .config import RuntimePaths, get_runtime_paths
from .environment import (
    REQUIRED_ENV_COLUMNS,
    REQUIRED_MATERIAL_COLUMNS,
    canonicalize_environment_df,
    canonicalize_materials_df,
    validate_environment_df,
    validate_materials_df,
)


REQUIRED_BURST_COLUMNS = {
    "burst_id",
    "sigma0_corrected",
    "sub_spacecraft_latitude_deg",
    "sub_spacecraft_longitude_deg",
    "act_incidence_angle_deg",
}

NON_TITAN_GUARDWORDS = {"EARTH", "MOON", "MARS", "VENUS", "MERCURY"}


def resolve_input_path(
    runtime_paths: RuntimePaths,
    *,
    local_relative: str | None = None,
    derived_relative: str | None = None,
    fallback_relative: str | None = None,
) -> Path | None:
    """
    Resolve data path with strict order:
    1) local synthetic data in `data/`
    2) derived Cassini data in `Inference_Data/derived/`
    3) fallback path
    """
    if local_relative:
        local_candidate = runtime_paths.root / local_relative
        if local_candidate.exists():
            return local_candidate
    if derived_relative:
        derived_candidate = runtime_paths.inference_data_root / "derived" / derived_relative
        if derived_candidate.exists():
            return derived_candidate
    if fallback_relative:
        fallback_candidate = runtime_paths.root / fallback_relative
        if fallback_candidate.exists():
            return fallback_candidate
    return None


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV path not found: {path}")
    return pd.read_csv(path)


def load_environment_table(path: str | Path) -> pd.DataFrame:
    """Load and validate environment table used by all experiment modes."""
    raw_df = _read_csv(Path(path))
    validate_environment_df(raw_df)
    return canonicalize_environment_df(raw_df)


def load_materials_table(path: str | Path) -> pd.DataFrame:
    """Load and validate materials table used by forward/inversion functions."""
    raw_df = _read_csv(Path(path))
    validate_materials_df(raw_df)
    return canonicalize_materials_df(raw_df)


def load_product_metadata(raw_dir: str | Path) -> dict[str, Any]:
    """Load product metadata JSON from `Inference_Data/raw/...`."""
    metadata_path = Path(raw_dir) / "product_metadata.json"
    if not metadata_path.exists():
        return {}
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def assert_titan_metadata(metadata: dict[str, Any]) -> None:
    """
    Reject non-Titan products to prevent accidental Earth/Moon calibration.
    """
    if not metadata:
        return
    target = str(metadata.get("target_name", "")).strip().upper()
    if target and target != "TITAN":
        raise ValueError(f"Non-Titan product rejected by guard: target_name={target}")

    dataset = str(metadata.get("data_set_id", "")).upper()
    description = str(metadata.get("description", "")).upper()
    text = f"{dataset} {description}"
    matched = {token for token in NON_TITAN_GUARDWORDS if token in text}
    if matched and "TITAN" not in text:
        raise ValueError(f"Non-Titan dataset rejected by guard: matched={sorted(matched)}")


def _enforce_burst_columns(df: pd.DataFrame) -> None:
    missing = REQUIRED_BURST_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"bursts_inference table is missing required columns: {sorted(missing)}")


def _quality_filter_bursts(df: pd.DataFrame, min_sigma: float | None = None, max_incidence: float = 89.0) -> pd.DataFrame:
    """
    Apply quality filtering for robust calibration inputs.
    """
    out = df.copy()
    for col in ("sigma0_corrected", "act_incidence_angle_deg"):
        out[col] = pd.to_numeric(out[col], errors="coerce")

    if "quality_flag" in out.columns:
        out = out[out["quality_flag"].fillna(0).astype(float) >= 0]
    out = out[np.isfinite(out["sigma0_corrected"]) & np.isfinite(out["act_incidence_angle_deg"])]
    out = out[np.abs(out["act_incidence_angle_deg"]) <= float(max_incidence)]
    if min_sigma is not None:
        out = out[out["sigma0_corrected"] >= float(min_sigma)]
    return out.reset_index(drop=True)


def _load_candidate_bursts_csvs(derived_root: Path) -> list[Path]:
    return sorted(derived_root.rglob("bursts_inference.csv"))


def load_inference_bursts(
    derived_root: str | Path | None = None,
    *,
    require_titan: bool = True,
    min_quality_sigma: float | None = None,
    runtime_paths: RuntimePaths | None = None,
) -> pd.DataFrame:
    """
    Load the best available derived bursts table with quality filtering.

    Returns an empty DataFrame when no usable table is available.
    """
    paths = runtime_paths or get_runtime_paths()
    root = Path(derived_root) if derived_root else (paths.inference_data_root / "derived")
    if not root.exists():
        return pd.DataFrame(columns=sorted(REQUIRED_BURST_COLUMNS))

    candidates = _load_candidate_bursts_csvs(root)
    if not candidates:
        # If no derived table exists yet, attempt a preview extraction from raw LBDR.
        try:
            from .lbdr_ingestion import build_preview_bursts_from_raw

            raw_dir = paths.inference_data_root / "raw" / "CORADR_0294" / "LBDR"
            derived_dir = paths.inference_data_root / "derived" / "CORADR_0294" / "LBDR_02_D294_V02"
            build_preview_bursts_from_raw(raw_dir=raw_dir, derived_dir=derived_dir, max_rows=512)
            candidates = _load_candidate_bursts_csvs(root)
        except Exception:
            candidates = []
    if not candidates:
        return pd.DataFrame(columns=sorted(REQUIRED_BURST_COLUMNS))

    # Use the first non-empty table that passes schema and filtering checks.
    for csv_path in candidates:
        try:
            df = pd.read_csv(csv_path)
            if df.empty:
                continue
            _enforce_burst_columns(df)
            filtered = _quality_filter_bursts(df, min_sigma=min_quality_sigma)
            if filtered.empty:
                continue

            if require_titan:
                # Check product metadata near this derived directory.
                derived_product_dir = csv_path.parent
                raw_guess = (
                    paths.inference_data_root
                    / "raw"
                    / derived_product_dir.relative_to(paths.inference_data_root / "derived").parent
                    / "LBDR"
                )
                metadata = load_product_metadata(raw_guess)
                assert_titan_metadata(metadata)
            return filtered
        except Exception:
            continue

    # Fallback once more to preview extraction when all existing tables are unusable.
    try:
        from .lbdr_ingestion import build_preview_bursts_from_raw

        raw_dir = paths.inference_data_root / "raw" / "CORADR_0294" / "LBDR"
        derived_dir = paths.inference_data_root / "derived" / "CORADR_0294" / "LBDR_02_D294_V02"
        preview_csv = build_preview_bursts_from_raw(raw_dir=raw_dir, derived_dir=derived_dir, max_rows=512, overwrite=True)
        preview_df = pd.read_csv(preview_csv)
        if not preview_df.empty:
            _enforce_burst_columns(preview_df)
            return _quality_filter_bursts(preview_df, min_sigma=min_quality_sigma)
    except Exception:
        pass

    return pd.DataFrame(columns=sorted(REQUIRED_BURST_COLUMNS))


def derive_noise_hint_from_bursts(
    bursts_df: pd.DataFrame | None,
    *,
    fallback_sigma: float = 0.05,
) -> dict[str, float]:
    """
    Estimate observation noise from derived bursts when possible.
    """
    if bursts_df is None or bursts_df.empty or "sigma0_corrected" not in bursts_df.columns:
        return {"radar_sigma": fallback_sigma, "em_sigma": fallback_sigma * 1.2}

    sigma = pd.to_numeric(bursts_df["sigma0_corrected"], errors="coerce").dropna()
    if sigma.empty:
        return {"radar_sigma": fallback_sigma, "em_sigma": fallback_sigma * 1.2}

    robust_std = float(np.clip(sigma.quantile(0.75) - sigma.quantile(0.25), 0.01, 0.35))
    radar_sigma = max(fallback_sigma, robust_std * 0.25)
    return {"radar_sigma": radar_sigma, "em_sigma": radar_sigma * 1.2}


def load_optional_sparsity_mask(mask_path: str | Path | None) -> np.ndarray | None:
    """Load optional 2D sparsity mask used for observation sparsity patterns."""
    if mask_path is None:
        return None
    path = Path(mask_path)
    if not path.exists():
        return None
    if path.suffix.lower() != ".npy":
        raise ValueError(f"Unsupported sparsity mask format: {path.suffix}")
    return np.load(path)


def ensure_schema_examples() -> dict[str, list[str]]:
    """
    Return required column sets for test assertions and docs.
    """
    return {
        "environment_required_columns": sorted(REQUIRED_ENV_COLUMNS),
        "materials_required_columns": sorted(REQUIRED_MATERIAL_COLUMNS),
        "bursts_required_columns": sorted(REQUIRED_BURST_COLUMNS),
    }

