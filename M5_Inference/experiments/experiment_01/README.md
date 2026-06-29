# experiment_01 — Centralized baseline

**Mode:** `centralized`  
**Goal:** Best-case RMSE ceiling — all observations to single inverter.

## Config (planned)

```yaml
env_path: data/environments/environment_001.csv
materials_path: data/materials/titan_materials.csv
alpha: 0.1          # Laplacian regularization
noise_sigma: 0.05
seed: 42
```

## Outputs

→ `../results/metrics/exp01_rmse.json`
