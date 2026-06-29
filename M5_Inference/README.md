# M5_Inference

Distributed hydrogeophysical inference experiment module. Evolves the CAS 521 Module 5 protocol notebook into the ExploreTitan research engine.

## Documentation

| File | Purpose |
|------|---------|
| [`MODIFICATION_DESIGN.md`](MODIFICATION_DESIGN.md) | **Implementation spec** — what changes, when, acceptance criteria |
| [`CASSINI_IMAGING_GUIDE.md`](CASSINI_IMAGING_GUIDE.md) | PDS Atlas links and download workflow for RADAR templates |
| [`PLANETARY_TOOLS.md`](PLANETARY_TOOLS.md) | **Tool install** — PDS quick-read (Tier A) + ISIS3 (Tier B) |
| [`Inference_Data/README.md`](Inference_Data/README.md) | PDS LBDR ingestion + derived inference file formats |
| [`MODULE5_ALGORITHMIC_DESIGN.md`](MODULE5_ALGORITHMIC_DESIGN.md) | Current notebook algorithm (pre-modification) |
| [`PROJECT_BASE.md`](PROJECT_BASE.md) | Scientific project base |
| [`METHOD_NOTES.md`](METHOD_NOTES.md) | Assumptions, limitations, and RQ metric mapping |
| [`RUNBOOK.md`](RUNBOOK.md) | How to execute each experiment mode and inspect outputs |
| [`DEFINITION_OF_DONE.md`](DEFINITION_OF_DONE.md) | Final acceptance checklist for ExploreTitan completeness |
| [`../DATA_SOURCES.md`](../DATA_SOURCES.md) | Data roles and external sources |

## Notebook

- [`[Base]Module5_Protocol_Simulation.ipynb`]([Base]Module5_Protocol_Simulation.ipynb) — orchestrator and visualization layer for modes `experiment_01`..`experiment_04`

## Directory layout

```
data/           → inputs (materials, environments, templates, benchmarks)
Inference_Data/ → Cassini PDS products + inference-ready derived tables
src/            → extracted Python runtime modules
experiments/    → per-experiment configs
results/        → generated outputs (gitignored)
notebooks/      → optional analysis exports
```

## Planetary data tooling

```bash
# Tier A — quick .IMG / .LBL read (recommended first)
pip install -r requirements-planetary.txt
python scripts/peek_pds.py ../Inference_Data/BIEQI69S314_D220_T071S01_V03.IMG

# Tier A + B — add ISIS3 for LBDR extraction / BIDR georef
bash scripts/install_planetary_tools.sh --full
conda activate exploretitan-planetary
```

See [`PLANETARY_TOOLS.md`](PLANETARY_TOOLS.md) for the full file-type matrix and experiment workflow.

## Implementation status

| Phase | Status |
|-------|--------|
| A — Data loaders + structure | Complete |
| B — Forward model | Complete (calibration-aware runtime path) |
| C — Centralized baseline | Complete |
| D — Distributed SCI | Complete |
| E — Communication/failure constraints | Complete |
| F — Cassini ingestion + src extract | Complete |
| G — Validation/tests/docs | Complete |
