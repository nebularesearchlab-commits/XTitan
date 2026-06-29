# experiment_02 — Distributed full communication

**Mode:** `distributed_full`  
**Goal:** Compare distributed SCI + M5 to Experiment 01.

## Config (planned)

```yaml
env_path: data/environments/environment_001.csv
comm_radius: 1.5    # grid cells
preserve_top_k: 0.10
max_iter: 50
beta: 0.3           # neighbor fusion weight
```

## Outputs

→ `../results/metrics/exp02_rmse.json`, convergence trace
