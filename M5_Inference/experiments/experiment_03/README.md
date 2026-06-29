# experiment_03 — Communication-constrained

**Mode:** `distributed_constrained`  
**Goal:** RMSE vs communication cost under M5 compression and message budget.

## Config (planned)

```yaml
msg_budget: 100     # max messages per iteration
preserve_top_k: 0.10
use_m5_compression: true
```

## Outputs

→ `../results/metrics/exp03_comm_accuracy_curve.csv`
