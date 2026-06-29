from pathlib import Path

from src.config import get_runtime_paths
from src.environment import create_default_materials_df, create_synthetic_environment
from src.runner import run_experiment_02


def test_regression_key_metrics_are_present(tmp_path: Path) -> None:
    root = tmp_path / "M5_Inference"
    (root / "data" / "environments").mkdir(parents=True, exist_ok=True)
    (root / "data" / "materials").mkdir(parents=True, exist_ok=True)
    (root / "Inference_Data" / "derived").mkdir(parents=True, exist_ok=True)

    create_synthetic_environment(grid_size=6, seed=5).to_csv(root / "data" / "environments" / "environment_001.csv", index=False)
    create_default_materials_df().to_csv(root / "data" / "materials" / "titan_materials.csv", index=False)

    paths = get_runtime_paths(root)
    output = run_experiment_02(
        runtime_paths=paths,
        config={"max_iter": 6, "seed": 5, "seeds": [5, 6]},
    )
    payload = output["payload"]

    required = {"rmse_hydrocarbon", "coverage_ratio", "comm_cost", "local_global_gap", "converged"}
    assert required.issubset(payload["metrics_distributed"].keys())
    assert payload["aggregate_rmse_hydrocarbon"]["mean"] >= 0.0

