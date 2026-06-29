"""
LBDR ingestion helpers for deriving calibration-friendly burst summaries.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REQUIRED_OUTPUT_COLUMNS = [
    "burst_id",
    "utc_time",
    "radar_mode",
    "beam_number",
    "sub_spacecraft_latitude_deg",
    "sub_spacecraft_longitude_deg",
    "spacecraft_altitude_km",
    "act_incidence_angle_deg",
    "act_azimuth_angle_deg",
    "pass_incidence_angle_deg",
    "sigma0_corrected",
    "sigma0_uncorrected",
    "antenna_temp_k",
    "quality_flag",
    "echo_peak_dn",
    "echo_mean_dn",
    "echo_std_dn",
    "echo_samples",
]


def _load_metadata(raw_dir: Path) -> dict[str, Any]:
    metadata_path = raw_dir / "product_metadata.json"
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing product metadata: {metadata_path}")
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def _assert_titan(metadata: dict[str, Any]) -> None:
    target = str(metadata.get("target_name", "")).strip().upper()
    if target and target != "TITAN":
        raise ValueError(f"Refusing to extract non-Titan product: {target}")


def _tab_path_from_metadata(raw_dir: Path, metadata: dict[str, Any]) -> Path:
    table_meta = metadata.get("binary_table", {})
    table_file = table_meta.get("file_name", "LBDR_02_D294_V02.TAB")
    return raw_dir / str(table_file)


def _extract_echo_stats(
    tab_path: Path,
    *,
    row_bytes: int,
    echo_start_byte: int,
    echo_items: int,
    max_rows: int,
) -> pd.DataFrame:
    """
    Fast extraction of echo summary statistics from raw fixed-length rows.
    """
    if not tab_path.exists():
        raise FileNotFoundError(f"Missing LBDR TAB file: {tab_path}")

    rows: list[dict[str, float | int | None]] = []
    start = int(echo_start_byte) - 1  # PDS offsets are 1-based.
    length = int(echo_items) * 4

    with tab_path.open("rb") as handle:
        for idx in range(max_rows):
            row = handle.read(int(row_bytes))
            if len(row) < int(row_bytes):
                break
            echo_blob = row[start : start + length]
            if len(echo_blob) != length:
                break
            echo = np.frombuffer(echo_blob, dtype="<f4").astype(np.float64)
            if echo.size == 0:
                continue

            finite = echo[np.isfinite(echo)]
            if finite.size == 0:
                continue

            rows.append(
                {
                    "burst_id": idx + 1,
                    "echo_peak_dn": float(np.max(finite)),
                    "echo_mean_dn": float(np.mean(finite)),
                    "echo_std_dn": float(np.std(finite)),
                    "echo_samples": int(finite.size),
                }
            )

    if not rows:
        return pd.DataFrame(columns=["burst_id", "echo_peak_dn", "echo_mean_dn", "echo_std_dn", "echo_samples"])
    return pd.DataFrame(rows)


def _build_preview_bursts_frame(echo_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a schema-compatible preview table from raw echo statistics.
    """
    if echo_df.empty:
        return pd.DataFrame(columns=REQUIRED_OUTPUT_COLUMNS)

    sigma_raw = echo_df["echo_mean_dn"].to_numpy(dtype=float)
    sigma_norm = (sigma_raw - sigma_raw.min()) / (sigma_raw.ptp() + 1e-9)

    preview = pd.DataFrame(
        {
            "burst_id": echo_df["burst_id"].astype(int),
            "utc_time": None,
            "radar_mode": 2,  # SAR-low placeholder for preview extraction.
            "beam_number": np.nan,
            "sub_spacecraft_latitude_deg": np.nan,
            "sub_spacecraft_longitude_deg": np.nan,
            "spacecraft_altitude_km": np.nan,
            "act_incidence_angle_deg": 35.0,
            "act_azimuth_angle_deg": np.nan,
            "pass_incidence_angle_deg": 35.0,
            "sigma0_corrected": sigma_norm,
            "sigma0_uncorrected": sigma_norm,
            "antenna_temp_k": np.nan,
            "quality_flag": 0,
            "echo_peak_dn": echo_df["echo_peak_dn"],
            "echo_mean_dn": echo_df["echo_mean_dn"],
            "echo_std_dn": echo_df["echo_std_dn"],
            "echo_samples": echo_df["echo_samples"].astype(int),
        }
    )
    return preview[REQUIRED_OUTPUT_COLUMNS]


def build_preview_bursts_from_raw(
    *,
    raw_dir: str | Path,
    derived_dir: str | Path,
    max_rows: int = 512,
    overwrite: bool = False,
) -> Path:
    """
    Extract preview bursts_inference.csv from raw TAB when derived file is missing.
    """
    raw_dir = Path(raw_dir)
    derived_dir = Path(derived_dir)
    derived_dir.mkdir(parents=True, exist_ok=True)
    output_csv = derived_dir / "bursts_inference.csv"

    if output_csv.exists() and not overwrite:
        existing = pd.read_csv(output_csv)
        if len(existing) > 0:
            return output_csv

    metadata = _load_metadata(raw_dir)
    _assert_titan(metadata)

    table_meta = metadata.get("binary_table", {})
    echo_meta = metadata.get("echo_data_column", {})
    tab_path = _tab_path_from_metadata(raw_dir, metadata)

    echo_df = _extract_echo_stats(
        tab_path,
        row_bytes=int(table_meta.get("row_bytes", 132344)),
        echo_start_byte=int(echo_meta.get("start_byte", 1273)),
        echo_items=int(echo_meta.get("items", 32768)),
        max_rows=int(max_rows),
    )
    preview_df = _build_preview_bursts_frame(echo_df)
    preview_df.to_csv(output_csv, index=False)

    # Persist ingestion metadata for traceability.
    ingest_meta = {
        "source_tab": str(tab_path),
        "rows_extracted": int(len(preview_df)),
        "max_rows_requested": int(max_rows),
        "method": "preview_echo_stats_only",
    }
    (derived_dir / "preview_ingestion.json").write_text(json.dumps(ingest_meta, indent=2), encoding="utf-8")
    return output_csv

