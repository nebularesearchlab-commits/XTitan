from src.environment import create_default_materials_df, create_synthetic_environment
from src.forward_model import generate_observations
from src.inversion import STATE_COLUMNS, centralized_invert


def test_forward_and_centralized_inversion_shapes() -> None:
    env = create_synthetic_environment(grid_size=6, seed=11)
    materials = create_default_materials_df()

    obs = generate_observations(env, observed_fraction=0.5, seed=11)
    pred = centralized_invert(obs, materials)

    assert len(obs) == len(env)
    assert len(pred) == len(env)
    for col in STATE_COLUMNS:
        assert col in pred.columns

