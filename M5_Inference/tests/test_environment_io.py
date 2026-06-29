from pathlib import Path

import pandas as pd

from src.environment import create_default_materials_df, create_synthetic_environment
from src.io_loaders import (
    assert_titan_metadata,
    load_environment_table,
    load_materials_table,
)


def test_environment_and_materials_have_required_columns() -> None:
    env = create_synthetic_environment(grid_size=5, seed=7)
    mats = create_default_materials_df()
    assert "subsurface_depth_km" in env.columns
    assert "permittivity" in mats.columns


def test_csv_loaders_validate_schema(tmp_path: Path) -> None:
    env_path = tmp_path / "env.csv"
    mat_path = tmp_path / "materials.csv"

    create_synthetic_environment(grid_size=4, seed=3).to_csv(env_path, index=False)
    create_default_materials_df().to_csv(mat_path, index=False)

    env = load_environment_table(env_path)
    mats = load_materials_table(mat_path)
    assert len(env) == 16
    assert len(mats) >= 3


def test_titan_guard_rejects_non_titan_products() -> None:
    metadata = {
        "target_name": "EARTH",
        "data_set_id": "CO-RADAR-LBDR",
        "description": "Example Earth dataset",
    }
    try:
        assert_titan_metadata(metadata)
    except ValueError:
        return
    raise AssertionError("Expected non-Titan metadata to be rejected")

