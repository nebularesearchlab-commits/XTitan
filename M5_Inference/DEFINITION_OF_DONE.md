# DEFINITION_OF_DONE

ExploreTitan completion checklist for `M5_Inference`.

## Core Scientific Completeness

- [x] Experiment 01-04 are mode-routable and config-driven.
- [x] Experiment 02 runs true distributed posterior updates and inter-agent belief fusion.
- [x] Experiment 03 enforces `msg_budget` and outputs measured communication-cost curves.
- [x] Experiment 04 couples failures to inference and reports RMSE/coherence degradation.
- [x] Placeholder fields (`comm_cost`, `local_global_gap`, `converged`) are runtime-derived in distributed modes.

## Data and Physics Rigor

- [x] Canonical runtime/data resolution order is implemented.
- [x] Titan-only product guards block non-Titan calibration paths.
- [x] LBDR ingestion path includes preview extraction fallback plus quality filtering.
- [x] Forward model calibration can consume derived burst statistics when available.

## Engineering Quality

- [x] Notebook acts as orchestration/visualization layer for `src/` modules.
- [x] Core modules extracted: environment, forward model, inversion, network, fusion, evaluation, IO, runner.
- [x] Validation utilities exist for experiment configs and required schemas.
- [x] Smoke/unit tests exist for modules and runner modes.

## Reproducibility and Documentation

- [x] Standard artifact outputs (JSON, CSV, traces, figures) are produced.
- [x] Run metadata includes config, seed(s), and timestamp.
- [x] Multi-seed execution paths and summary stats are supported.
- [x] Method notes and runbook are published in this folder.
