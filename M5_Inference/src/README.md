# src/

Reusable ExploreTitan runtime modules extracted from the notebook workflow.

## Current modules

- [`config.py`](config.py): Canonical runtime path resolution, config validation, artifact writers.
- [`io_loaders.py`](io_loaders.py): Data-source resolution (local first, derived Cassini second), Titan-only guards, quality filters.
- [`environment.py`](environment.py): Synthetic environment generation and schema canonicalization helpers.
- [`forward_model.py`](forward_model.py): Calibration-aware radar/EM forward model.
- [`inversion.py`](inversion.py): Centralized inversion + agent-local posterior updates.
- [`m5_network.py`](m5_network.py): Agent communication graph and failure-step utilities.
- [`distributed_fusion.py`](distributed_fusion.py): Iterative belief fusion, message-budget enforcement, failure-coupled inference loops.
- [`evaluation.py`](evaluation.py): RMSE/coherence/communication metrics and aggregation stats.
- [`runner.py`](runner.py): Experiment 01-04 mode runners used by the notebook orchestrator layer.
- [`lbdr_ingestion.py`](lbdr_ingestion.py): Raw TAB preview extraction into derived `bursts_inference.csv` with provenance.
- [`pds_io.py`](pds_io.py): Tier A PDS quick-read and Titan product validation helpers.

CLI wrapper: [`../scripts/peek_pds.py`](../scripts/peek_pds.py)

Install deps: [`../requirements-planetary.txt`](../requirements-planetary.txt) and [`../environment-planetary.yml`](../environment-planetary.yml).
