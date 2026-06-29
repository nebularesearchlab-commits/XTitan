# METHOD_NOTES

Method notes for the implemented ExploreTitan workflow in `M5_Inference`.

## Architecture Mapping

- **Layer 1 Environment**: `src/environment.py` canonicalizes environment/material schemas and creates synthetic Titan grids.
- **Layer 2 Forward Model**: `src/forward_model.py` generates radar/EM observations and supports Cassini-driven calibration hints.
- **Layer 3 Inversion**: `src/inversion.py` provides centralized inversion and agent-local posterior updates.
- **Layer 4 Network + Fusion**: `src/m5_network.py` builds communication graphs; `src/distributed_fusion.py` runs belief fusion with budgets/failures.
- **Layer 5 Evaluation**: `src/evaluation.py` computes RMSE, communication, and coherence metrics.
- **Orchestration**: `src/runner.py` routes experiment modes 01-04 and the notebook calls these modules.

## Runtime and Data Rules

- Canonical runtime root is resolved to `M5_Inference` via `src/config.py`.
- Input resolution order in loaders:
  1. local synthetic files in `data/`
  2. derived Cassini files in `Inference_Data/derived/`
  3. safe fallbacks
- Titan-only guards reject non-Titan products before derived calibration is consumed.

## Research Question Mapping

- **RQ1 Accuracy**: `rmse_hydrocarbon`, `rmse_depth_km`, `rmse_porosity`.
- **RQ2 Communication**: `comm_cost`, `messages_this_iter`, `cumulative_comm_cost`, Experiment 03 communication curves.
- **RQ3 Coherence**: `local_global_gap`, `converged`, `max_state_change`, and Experiment 04 failure-step degradation.

## Assumptions and Limits

- Forward model is a calibrated synthetic proxy, not a full radiative-transfer solver.
- Sparse/empty derived burst tables fall back to safe calibration defaults.
- Raw TAB preview extraction produces echo-stat summaries, not full ISIS geometry reconstruction.
- Message payload cost is modeled consistently for comparison across runs.
