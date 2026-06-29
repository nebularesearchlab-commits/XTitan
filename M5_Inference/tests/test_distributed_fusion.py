from src.distributed_fusion import distributed_inference, failure_inference_sweep
from src.environment import create_default_materials_df, create_synthetic_environment
from src.forward_model import generate_observations
from src.inversion import initialize_local_beliefs
from src.m5_network import build_agent_graph_from_environment


def test_distributed_inference_enforces_message_budget() -> None:
    env = create_synthetic_environment(grid_size=5, seed=23)
    materials = create_default_materials_df()
    obs = generate_observations(env, observed_fraction=0.45, seed=23)
    graph = build_agent_graph_from_environment(env, comm_radius=1.5)
    init = initialize_local_beliefs(obs, materials)

    pred, trace, metrics = distributed_inference(
        obs,
        materials,
        graph,
        truth_df=env,
        initial_beliefs=init,
        max_iter=8,
        beta=0.3,
        msg_budget=20,
        tol=1e-4,
        seed=23,
    )

    assert len(pred) > 0
    assert len(trace) > 0
    assert metrics["comm_cost"] >= 0.0
    assert "local_global_gap" in metrics


def test_failure_sweep_returns_per_step_metrics() -> None:
    env = create_synthetic_environment(grid_size=5, seed=17)
    materials = create_default_materials_df()
    obs = generate_observations(env, observed_fraction=0.5, seed=17)
    graph = build_agent_graph_from_environment(env, comm_radius=1.5)

    percolation_df, traces = failure_inference_sweep(
        obs,
        materials,
        graph,
        truth_df=env,
        removal_steps=[0.05, 0.1],
        max_iter=5,
        msg_budget=20,
        seed=17,
    )
    assert len(percolation_df) == 2
    assert "rmse_hydrocarbon" in percolation_df.columns
    assert len(traces) == 2

