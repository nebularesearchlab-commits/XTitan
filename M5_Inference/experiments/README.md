# experiments/

Per-experiment configuration and run scripts.

| Folder | Mode | Description |
|--------|------|-------------|
| `experiment_01/` | `centralized` | Centralized baseline with map artifacts and metadata |
| `experiment_02/` | `distributed_full` | Agent-local posterior updates + inter-agent belief fusion |
| `experiment_03/` | `distributed_constrained` | Message budget enforcement with comm-cost curves |
| `experiment_04/` | `network_failure` | Failure-coupled inference degradation traces |

Each folder contains `config.yaml` with paths, hyperparameters, and optional `seeds` arrays for repeated runs and summary statistics.
