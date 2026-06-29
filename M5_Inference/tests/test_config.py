from pathlib import Path

from src.config import (
    canonical_runtime_root,
    get_runtime_paths,
    save_metrics_json,
    validate_experiment_config,
)


def test_canonical_runtime_root_prefers_m5_child(tmp_path: Path) -> None:
    base = tmp_path / "workspace"
    base.mkdir()
    child = base / "M5_Inference"
    child.mkdir()
    resolved = canonical_runtime_root(base)
    assert resolved == child.resolve()


def test_validate_experiment_config_catches_missing_fields() -> None:
    valid, errors = validate_experiment_config("experiment_02", {"seed": 42})
    assert not valid
    assert any("max_iter" in message for message in errors)


def test_save_metrics_json_creates_output_file(tmp_path: Path) -> None:
    root = tmp_path / "M5_Inference"
    root.mkdir(parents=True)
    paths = get_runtime_paths(root)
    output = save_metrics_json("unit_test.json", {"ok": True}, runtime_paths=paths)
    assert output.exists()
    assert output.read_text(encoding="utf-8").strip().startswith("{")

