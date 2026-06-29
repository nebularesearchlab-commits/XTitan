from pathlib import Path

from src.config import get_runtime_paths
from src.environment import create_default_materials_df, create_synthetic_environment
from src.runner import run_experiment_01, run_experiment_02, run_experiment_03, run_experiment_04


def _prepare_runtime(tmp_path: Path):
    root = tmp_path / "M5_Inference"
    (root / "data" / "environments").mkdir(parents=True, exist_ok=True)
    (root / "data" / "materials").mkdir(parents=True, exist_ok=True)
    (root / "Inference_Data" / "derived").mkdir(parents=True, exist_ok=True)
    (root / "Inference_Data" / "raw" / "CORADR_0294" / "LBDR").mkdir(parents=True, exist_ok=True)
    (root / "experiments").mkdir(parents=True, exist_ok=True)

    create_synthetic_environment(grid_size=6, seed=9).to_csv(root / "data" / "environments" / "environment_001.csv", index=False)
    create_default_materials_df().to_csv(root / "data" / "materials" / "titan_materials.csv", index=False)
    return get_runtime_paths(root)


def test_runner_modes_generate_metrics_files(tmp_path: Path) -> None:
    paths = _prepare_runtime(tmp_path)

    out1 = run_experiment_01(runtime_paths=paths, config={"run_m5_topology": False, "seed": 9})
    out2 = run_experiment_02(runtime_paths=paths, config={"max_iter": 5, "seed": 9})
    out3 = run_experiment_03(
        runtime_paths=paths,
        config={"network_sizes": [36, 49], "max_iter": 4, "msg_budget": 12, "seed": 9},
    )
    out4 = run_experiment_04(
        runtime_paths=paths,
        config={"removal_steps": [0.05, 0.1], "max_iter": 4, "msg_budget": 10, "seed": 9},
    )

    assert out1["metrics_path"].exists()
    assert out2["metrics_path"].exists()
    assert out3["summary_path"].exists()
    assert out4["metrics_path"].exists()

