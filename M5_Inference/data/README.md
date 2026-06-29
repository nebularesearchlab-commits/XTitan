# data/

Input data for M5_Inference. Schemas defined in [`../DATA_SOURCES.md`](../DATA_SOURCES.md) and [`../MODIFICATION_DESIGN.md`](../MODIFICATION_DESIGN.md).

| Subfolder | Role | Phase |
|-----------|------|-------|
| `materials/` | Titan material property bounds | A |
| `environments/` | Synthetic ground truth (`TitanGrid` CSV) | A |
| `templates/cassini_radar/` | Cassini BIDR + sparsity masks | F |
| `observations/` | Forward model outputs per run | B |
| `benchmarks/dl_rmd_sample/` | Earth EM inversion sanity check | C |
| `references/` | PGDA gravity, citation files | F |

Do not commit large PDS downloads without LFS or external storage links.
