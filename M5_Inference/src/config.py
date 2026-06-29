"""
Configuration and artifact utilities for ExploreTitan experiments.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover - fallback parser is used when yaml unavailable
    yaml = None


@dataclass(frozen=True)
class RuntimePaths:
    """Canonical path bundle for notebook and module runtimes."""

    root: Path
    data_root: Path
    inference_data_root: Path
    experiments_root: Path
    results_root: Path
    results_metrics_dir: Path
    results_figures_dir: Path
    results_traces_dir: Path
    legacy_dataset_path: Path
    experiment_config_paths: dict[str, Path]


def canonical_runtime_root(start_path: str | Path | None = None) -> Path:
    """
    Resolve the canonical `M5_Inference` runtime root.

    Priority:
    1) current directory if it is `M5_Inference`
    2) `./M5_Inference` child from current directory
    3) current directory fallback
    """
    here = Path(start_path or Path.cwd()).resolve()
    if here.name == "M5_Inference":
        return here
    child = here / "M5_Inference"
    if child.exists() and child.is_dir():
        return child.resolve()
    return here


def get_runtime_paths(start_path: str | Path | None = None) -> RuntimePaths:
    """Build canonical runtime paths rooted at `M5_Inference`."""
    root = canonical_runtime_root(start_path)
    experiments_root = root / "experiments"
    results_root = root / "results"
    return RuntimePaths(
        root=root,
        data_root=root / "data",
        inference_data_root=root / "Inference_Data",
        experiments_root=experiments_root,
        results_root=results_root,
        results_metrics_dir=results_root / "metrics",
        results_figures_dir=results_root / "figures",
        results_traces_dir=results_root / "traces",
        legacy_dataset_path=root.parent / "SimulationDataset",
        experiment_config_paths={
            "experiment_01": experiments_root / "experiment_01" / "config.yaml",
            "experiment_02": experiments_root / "experiment_02" / "config.yaml",
            "experiment_03": experiments_root / "experiment_03" / "config.yaml",
            "experiment_04": experiments_root / "experiment_04" / "config.yaml",
        },
    )


def _parse_scalar(raw_value: str) -> Any:
    """Parse a scalar from lightweight YAML-like `key: value` text."""
    value = raw_value.split("#", 1)[0].strip()
    if not value:
        return None
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    if lower in {"none", "null"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)
        except Exception:
            return value
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def _fallback_yaml_load(raw_text: str) -> dict[str, Any]:
    """Minimal parser for flat YAML files used in experiment configs."""
    parsed: dict[str, Any] = {}
    for line in raw_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        parsed[key.strip()] = _parse_scalar(value)
    return parsed


def _safe_yaml_load(raw_text: str) -> dict[str, Any]:
    """Load YAML using pyyaml when available, else fallback parser."""
    if yaml is not None:
        try:
            loaded = yaml.safe_load(raw_text)
            return loaded if isinstance(loaded, dict) else {}
        except Exception:
            pass
    return _fallback_yaml_load(raw_text)


def load_experiment_config(
    experiment_key: str,
    default_config: dict[str, Any] | None = None,
    runtime_paths: RuntimePaths | None = None,
) -> dict[str, Any]:
    """
    Load per-experiment config from `experiments/*/config.yaml`.

    Returns defaults when config is absent or invalid.
    """
    cfg = dict(default_config or {})
    paths = runtime_paths or get_runtime_paths()
    cfg_path = paths.experiment_config_paths.get(experiment_key)
    if cfg_path is None or not cfg_path.exists():
        return cfg
    loaded = _safe_yaml_load(cfg_path.read_text(encoding="utf-8"))
    cfg.update(loaded)
    return cfg


def validate_experiment_config(experiment_key: str, config: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Validate required fields and basic ranges for experiment configs.
    """
    errors: list[str] = []

    def _require(keys: list[str]) -> None:
        for key in keys:
            if key not in config:
                errors.append(f"Missing required config key: {key}")

    if experiment_key == "experiment_01":
        _require(["env_path", "materials_path", "seed"])
    elif experiment_key == "experiment_02":
        _require(["max_iter", "beta", "comm_radius", "seed"])
    elif experiment_key == "experiment_03":
        _require(["msg_budget", "network_sizes", "seed"])
    elif experiment_key == "experiment_04":
        _require(["removal_strategy", "removal_steps", "seed"])

    max_iter = config.get("max_iter")
    if max_iter is not None and int(max_iter) <= 0:
        errors.append("max_iter must be > 0")

    beta = config.get("beta")
    if beta is not None and not (0.0 < float(beta) <= 1.0):
        errors.append("beta must be in (0, 1]")

    msg_budget = config.get("msg_budget")
    if msg_budget is not None and int(msg_budget) <= 0:
        errors.append("msg_budget must be > 0")

    strategy = config.get("removal_strategy")
    if strategy is not None and str(strategy) not in {"random", "targeted"}:
        errors.append("removal_strategy must be 'random' or 'targeted'")

    network_sizes = config.get("network_sizes")
    if network_sizes is not None:
        if not isinstance(network_sizes, list) or not network_sizes:
            errors.append("network_sizes must be a non-empty list")
        else:
            for size in network_sizes:
                if int(size) <= 0:
                    errors.append("network_sizes entries must be > 0")
                    break

    removal_steps = config.get("removal_steps")
    if removal_steps is not None:
        if not isinstance(removal_steps, list) or not removal_steps:
            errors.append("removal_steps must be a non-empty list")
        else:
            for step in removal_steps:
                value = float(step)
                if value <= 0 or value >= 1:
                    errors.append("removal_steps entries must be in (0, 1)")
                    break

    seeds = config.get("seeds")
    if seeds is not None:
        if not isinstance(seeds, list) or not seeds:
            errors.append("seeds must be a non-empty list when provided")
        else:
            for seed in seeds:
                if int(seed) < 0:
                    errors.append("seeds entries must be >= 0")
                    break

    return (len(errors) == 0, errors)


def ensure_results_dirs(runtime_paths: RuntimePaths | None = None) -> None:
    """Create standard results folders once before writing outputs."""
    paths = runtime_paths or get_runtime_paths()
    for path in (
        paths.results_root,
        paths.results_metrics_dir,
        paths.results_figures_dir,
        paths.results_traces_dir,
    ):
        path.mkdir(parents=True, exist_ok=True)


def save_metrics_json(filename: str, payload: dict[str, Any], runtime_paths: RuntimePaths | None = None) -> Path:
    """Write JSON metrics payload to results/metrics and return full path."""
    paths = runtime_paths or get_runtime_paths()
    ensure_results_dirs(paths)
    output_path = paths.results_metrics_dir / filename
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output_path


def save_metrics_csv(
    filename: str,
    rows: list[dict[str, Any]],
    columns: list[str] | None = None,
    runtime_paths: RuntimePaths | None = None,
) -> Path:
    """Write tabular metric rows as CSV in results/metrics."""
    paths = runtime_paths or get_runtime_paths()
    ensure_results_dirs(paths)
    output_path = paths.results_metrics_dir / filename
    if not rows:
        output_path.write_text("", encoding="utf-8")
        return output_path

    if columns is None:
        columns = list(rows[0].keys())

    lines = [",".join(columns)]
    for row in rows:
        values: list[str] = []
        for col in columns:
            value = row.get(col, "")
            if isinstance(value, str):
                escaped = value.replace('"', '""')
                if "," in escaped or "\n" in escaped:
                    escaped = f'"{escaped}"'
                values.append(escaped)
            else:
                values.append(str(value))
        lines.append(",".join(values))
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def save_trace_json(filename: str, trace: list[dict[str, Any]], runtime_paths: RuntimePaths | None = None) -> Path:
    """Write iteration/failure traces to results/traces as JSON."""
    paths = runtime_paths or get_runtime_paths()
    ensure_results_dirs(paths)
    output_path = paths.results_traces_dir / filename
    output_path.write_text(json.dumps(trace, indent=2, sort_keys=True), encoding="utf-8")
    return output_path


def utc_now_iso() -> str:
    """Stable UTC timestamp for run metadata."""
    return datetime.now(timezone.utc).isoformat()

