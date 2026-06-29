"""
Quick-read helpers for Cassini RADAR PDS3 products (BIDR .IMG, LBDR .TAB labels).

Tier A tooling — no ISIS required. For full burst extraction or map projection,
use ISIS3 (see PLANETARY_TOOLS.md).
"""

from __future__ import annotations

import re
import struct
from pathlib import Path
from typing import Any

import numpy as np

try:
    import pvl
except ImportError:  # pragma: no cover
    pvl = None


# PDS3 hex float missing sentinel used in many Cassini RADAR products (16#FF7FFFFB#).
_PDS_MISSING_FLOAT = struct.unpack(">f", bytes.fromhex("FF7FFFFB"))[0]


def _decode_label_bytes(raw: bytes) -> str:
    """PDS labels are ASCII / Latin-1 text, often padded with nulls in fixed records."""
    return raw.decode("latin-1", errors="replace").rstrip("\x00 ")


def _parse_label_text(text: str) -> dict[str, Any]:
    """Parse PDS3 label text into a dict (pvl if available, else lightweight regex)."""
    if pvl is not None:
        return pvl.loads(text)  # type: ignore[no-any-return]
    return _parse_label_fallback(text)


def _parse_label_fallback(text: str) -> dict[str, Any]:
    """Minimal parser when pvl is not installed — enough for image geometry."""
    out: dict[str, Any] = {}
    for key in (
        "PDS_VERSION_ID",
        "RECORD_BYTES",
        "LABEL_RECORDS",
        "FILE_RECORDS",
        "PRODUCT_ID",
        "TARGET_NAME",
        "DATA_SET_ID",
        "START_TIME",
        "STOP_TIME",
    ):
        m = re.search(rf"^\s*{key}\s*=\s*(.+)$", text, re.MULTILINE)
        if m:
            out[key] = m.group(1).strip().strip('"')
    img: dict[str, Any] = {}
    for key in ("LINES", "LINE_SAMPLES", "SAMPLE_TYPE", "SAMPLE_BITS", "MISSING_CONSTANT", "NOTE"):
        m = re.search(rf"^\s*{key}\s*=\s*(.+)$", text, re.MULTILINE)
        if m:
            val = m.group(1).strip().strip('"')
            if key in ("LINES", "LINE_SAMPLES", "SAMPLE_BITS"):
                img[key] = int(float(val.split()[0]))
            else:
                img[key] = val
    if img:
        out["IMAGE"] = img
    ptr = re.search(r"\^IMAGE\s*=\s*(\d+)", text)
    if ptr:
        out["^IMAGE"] = int(ptr.group(1))
    return out


def load_pds3_label(
    product_path: str | Path,
    label_path: str | Path | None = None,
) -> tuple[dict[str, Any], str]:
    """
    Load a PDS3 label from a detached .LBL file or the first fixed-length record.

    Returns (parsed_label_dict, raw_label_text).
    """
    product_path = Path(product_path)
    if label_path is not None:
        label_file = Path(label_path)
        text = label_file.read_text(encoding="latin-1", errors="replace")
        return _parse_label_text(text), text

    detached = product_path.with_suffix(".LBL")
    if detached.is_file():
        text = detached.read_text(encoding="latin-1", errors="replace")
        return _parse_label_text(text), text

    # Embedded label: read first record (default 12288 for BIDR; sniff if unknown).
    with product_path.open("rb") as f:
        head = f.read(65536)
    text_head = _decode_label_bytes(head)
    m = re.search(r"RECORD_BYTES\s*=\s*(\d+)", text_head)
    record_bytes = int(m.group(1)) if m else 12288
    with product_path.open("rb") as f:
        text = _decode_label_bytes(f.read(record_bytes))
    return _parse_label_text(text), text


def _image_start_record(label: dict[str, Any]) -> int:
    """Record index where the IMAGE array begins (^IMAGE pointer, 1-based in PDS3)."""
    if "^IMAGE" in label:
        return int(label["^IMAGE"])
    if "^image" in label:
        return int(label["^image"])
    label_records = int(label.get("LABEL_RECORDS", 1))
    return label_records + 1


def _numpy_dtype(sample_type: str, sample_bits: int) -> np.dtype:
    """Map PDS3 SAMPLE_TYPE + SAMPLE_BITS to a NumPy dtype (Cassini RADAR is big-endian)."""
    st = sample_type.upper().replace('"', "")
    if st in ("PC_REAL", "IEEE_REAL") and sample_bits == 32:
        return np.dtype(">f4")
    if st in ("PC_REAL", "IEEE_REAL") and sample_bits == 64:
        return np.dtype(">f8")
    if st in ("MSB_UNSIGNED_INTEGER", "MSB_INTEGER") and sample_bits == 16:
        return np.dtype(">u2")
    if st in ("MSB_UNSIGNED_INTEGER", "MSB_INTEGER") and sample_bits == 8:
        return np.dtype(">u1")
    raise ValueError(f"Unsupported PDS sample type: {sample_type} / {sample_bits} bits")


def read_pds3_image(
    product_path: str | Path,
    label_path: str | Path | None = None,
    *,
    max_lines: int | None = None,
    max_samples: int | None = None,
) -> tuple[np.ndarray, dict[str, Any]]:
    """
    Read a PDS3 IMAGE object from a BIDR-style .IMG file into a 2D NumPy array.

    Optional max_lines / max_samples load a crop for quick preview (saves RAM).
    Invalid / missing pixels are set to NaN.
    """
    product_path = Path(product_path)
    label, _ = load_pds3_label(product_path, label_path=label_path)

    record_bytes = int(label["RECORD_BYTES"])
    image_meta = label.get("IMAGE") or label.get("Image") or {}
    lines = int(image_meta["LINES"])
    samples = int(image_meta["LINE_SAMPLES"])
    dtype = _numpy_dtype(str(image_meta["SAMPLE_TYPE"]), int(image_meta["SAMPLE_BITS"]))

    read_lines = min(lines, max_lines) if max_lines else lines
    read_samples = min(samples, max_samples) if max_samples else samples

    start_record = _image_start_record(label)
    byte_offset = (start_record - 1) * record_bytes
    row_bytes = read_samples * dtype.itemsize

    with product_path.open("rb") as f:
        f.seek(byte_offset)
        buf = f.read(read_lines * row_bytes)

    arr = np.frombuffer(buf, dtype=dtype, count=read_lines * read_samples)
    arr = arr.reshape(read_lines, read_samples).astype(np.float64)
    arr[np.abs(arr - _PDS_MISSING_FLOAT) < 1.0] = np.nan
    arr[arr > 1e30] = np.nan
    return arr, label


def _json_safe(value: Any) -> Any:
    """Convert pvl parsed types (e.g. datetime) into JSON-serializable values."""
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def summarize_product(product_path: str | Path, label_path: str | Path | None = None) -> dict[str, Any]:
    """
    Return a JSON-friendly summary of a PDS3 product without loading the full array.
    """
    product_path = Path(product_path)
    label, raw_text = load_pds3_label(product_path, label_path=label_path)
    summary: dict[str, Any] = {
        "path": str(product_path.resolve()),
        "size_bytes": product_path.stat().st_size,
        "pds_version_id": label.get("PDS_VERSION_ID"),
        "product_id": label.get("PRODUCT_ID"),
        "target_name": label.get("TARGET_NAME"),
        "data_set_id": label.get("DATA_SET_ID"),
        "start_time": label.get("START_TIME"),
        "stop_time": label.get("STOP_TIME"),
        "record_bytes": label.get("RECORD_BYTES"),
        "file_records": label.get("FILE_RECORDS"),
    }

    image_meta = label.get("IMAGE") or label.get("Image")
    if image_meta:
        summary["image"] = {
            "lines": image_meta.get("LINES"),
            "line_samples": image_meta.get("LINE_SAMPLES"),
            "sample_type": image_meta.get("SAMPLE_TYPE"),
            "note": image_meta.get("NOTE"),
        }
        summary["product_kind"] = "pds3_image"
    elif "^TABLE" in label or "TABLE" in label:
        table = label.get("TABLE") or {}
        summary["table"] = {
            "rows": table.get("ROWS") or table.get("TABLE_ROWS"),
            "columns": table.get("COLUMNS") or table.get("TABLE_COLUMNS"),
            "row_bytes": table.get("ROW_BYTES"),
        }
        summary["product_kind"] = "pds3_table"
    else:
        summary["product_kind"] = "pds3_other"

    # Pull map bounds when present (BIDR backplanes include IMAGE_MAP_PROJECTION).
    for key in ("MINIMUM_LATITUDE", "MAXIMUM_LATITUDE", "WESTERNMOST_LONGITUDE", "EASTERNMOST_LONGITUDE"):
        m = re.search(rf"^\s*{key}\s*=\s*([-0-9.]+)", raw_text, re.MULTILINE)
        if m:
            summary.setdefault("footprint", {})[key.lower()] = float(m.group(1))

    return _json_safe(summary)


def is_titan_product(label_or_summary: dict[str, Any]) -> bool:
    """
    Return True when product metadata explicitly targets Titan.
    """
    target = str(label_or_summary.get("TARGET_NAME") or label_or_summary.get("target_name") or "").strip().upper()
    if target:
        return target == "TITAN"
    text = " ".join(
        str(label_or_summary.get(key, ""))
        for key in ("DATA_SET_ID", "data_set_id", "DESCRIPTION", "description")
    ).upper()
    if "TITAN" in text:
        return True
    for token in ("EARTH", "MOON", "MARS", "VENUS", "MERCURY"):
        if token in text:
            return False
    return False


def assert_titan_product(label_or_summary: dict[str, Any]) -> None:
    """
    Raise a clear error when a non-Titan PDS product is provided.
    """
    if not is_titan_product(label_or_summary):
        target = label_or_summary.get("TARGET_NAME") or label_or_summary.get("target_name")
        raise ValueError(f"Non-Titan PDS product rejected by guard. target={target!r}")
