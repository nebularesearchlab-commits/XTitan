# experiment_04 — Network failure

**Mode:** `network_failure`  
**Goal:** RMSE degradation under progressive node removal (percolation + inference).

## Config (planned)

```yaml
removal_strategy: targeted   # or random
removal_steps: [0.05, 0.10, 0.25, 0.50]
preserve_top_k: 0.10
```

Uses existing `run_percolation_test` wired to inference RMSE.

## Outputs

→ `../results/figures/exp04_percolation_rmse.png`
