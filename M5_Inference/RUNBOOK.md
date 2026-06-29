# RUNBOOK

Operational guide for running ExploreTitan experiments 01-04.

## 1) Setup

```bash
cd "M5_Inference"
pip install -r requirements-planetary.txt
```

Optional full planetary stack:

```bash
bash scripts/install_planetary_tools.sh --full
conda activate exploretitan-planetary
```

## 2) Configure

Edit the mode config file under `experiments/experiment_0x/config.yaml`.

Important fields:

- `seed` and optional `seeds` (multi-seed statistics)
- `msg_budget` for Experiment 03 and 04
- `removal_steps` and `removal_strategy` for Experiment 04
- `env_path` and `materials_path` for shared baseline data

## 3) Execute in Notebook

Open `[Base]Module5_Protocol_Simulation.ipynb` and set:

- `EXPERIMENT_MODE = "experiment_01"` for centralized baseline
- `EXPERIMENT_MODE = "experiment_02"` for distributed fusion
- `EXPERIMENT_MODE = "experiment_03"` for communication-constrained runs
- `EXPERIMENT_MODE = "experiment_04"` for failure-coupled inference

Run cells in order.

## 4) Expected Artifacts

- `results/metrics/exp01_rmse.json`
- `results/metrics/exp01_maps.csv`
- `results/metrics/exp02_rmse.json`
- `results/metrics/exp02_convergence_trace*.csv`
- `results/metrics/exp03_comm_accuracy_curve.csv`
- `results/metrics/exp03_scaling_summary.json`
- `results/metrics/exp04_percolation.json`
- `results/metrics/exp04_percolation_curve.csv`
- `results/traces/exp03_trace_*.json`
- `results/traces/exp04_trace_*.json`
- `results/figures/*.png`

## 5) Validation

Run tests:

```bash
python -m pytest tests -q
```

Run a quick syntax check:

```bash
python -m compileall src
```
