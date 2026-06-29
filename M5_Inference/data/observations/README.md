# observations/

Forward-model outputs — simulated geophysical measurements per experiment run.

**Structure:**

```
observations/
└── sim_run_001/
    ├── observations.csv      # node_id, radar, em, noise_sigma
    ├── metadata.json         # forward model params, seed, env path
    └── sparsity_mask.npy     # optional copy used for this run
```

Written by `forward_model()` in notebook Block 2 or `src/forward_model.py`.
