# Inference_Data — Inventory & Experiment Suitability Audit

**Folder audited:** `Agentic Lab/Inference_Data/`  
**Audit date:** 2026-06-11  
**Experiment framework:** ExploreTitan / M5_Inference — distributed hydrogeophysical inference under Titan-like constraints  

**Evaluation roles** (from [`../DATA_SOURCES.md`](../DATA_SOURCES.md)):

| Role | Meaning | Used as experiment input? |
|------|---------|---------------------------|
| **A** | Subsurface ground truth | Synthetic only (`M5_Inference/data/environments/`) |
| **B** | Physics / material priors | Literature + UCSC materials CSV |
| **C** | Observation priors (Cassini σ⁰, coverage, noise) | PDS RADAR products → forward model |
| **D** | Method benchmarks (Earth EM / inference) | DL-RMD, papers — not Titan labels |
| **Ref** | Documentation / specs | Supports processing; not loaded by notebook |

**Important:** This folder is **orphan staging**. The canonical pipeline layout lives in [`../M5_Inference/Inference_Data/`](../M5_Inference/Inference_Data/) (LBDR `CORADR_0294` already catalogued there). Items marked ✅ below should be **migrated or registered** in that tree before Phase F integration.

---

## Executive summary

| Category | Count (top-level + CORADR_0077) | Total size (approx.) |
|----------|--------------------------------|----------------------|
| ✅ Suitable now (Role C or strong template) | 4 items | ~430 MB |
| ⚠️ Partially suitable (wrong band, low-res, or incomplete) | 5 items | ~440 MB |
| ❌ Not suitable for Titan experiment | 2 items | ~80 MB |
| 📚 Reference / literature only | 8+ items | ~350 KB (+ 1 MB docx) |
| 🗂️ Volume docs & catalogs (keep as spec) | CORADR_0077 tree + `.CAT` | ~32 MB |

**Bottom line:** You have **useful Titan BIDR/LBDR-related assets**, but they are **scattered**, **partially duplicated**, and **not wired** to `M5_Inference/data/templates/cassini_radar/manifest.csv` or `inference_data_manifest.yaml`. One large file (`LBDR_02_003_V01`) is **Earth calibration**, not Titan. The best immediate Titan observation asset for σ⁰ priors is the small **T16 backscatter** product (`BIBQD…`); the large **T71** file is **incidence**, not backscatter.

---

## ✅ Suitable for the experiment

These directly support Role **C** (observation priors) or surface templates that constrain synthetic worlds.

### Cassini RADAR — Titan BIDR (backscatter)

| File | Size | Flyby | Role | Why suitable |
|------|------|-------|------|--------------|
| `BIBQD18N341_D087_T016S03_V03.LBL` | 5 KB | **T16** (2006-07-22) | **C** | Detached label for σ⁰ backscatter in **dB** (incidence-corrected SAR cross-section). Matches forward-model radar channel. |
| `BIBQD18N341_D087_T016S03_V03.IMG` | 17 KB | T16 | **C** | Complete **low-resolution** BIDR backscatter grid (96×128 px browse-scale). Ideal for **quick sparsity / σ⁰ template tests** in Phase F. |
| `BIBQD18N341_D087_T016S03_V03.ZIP` | 3 KB | T16 | **C** | Compressed archive of the above — keep with `.LBL`/`.IMG`. |

**Footprint (from label):** lat ~12–24°N, lon ~332–350°W. Mid-latitude early SAR — good for generic template testing, not polar lakes.

**Recommended action:** Copy to `M5_Inference/data/templates/cassini_radar/bidr/` and add a row to `manifest.csv` (`use_case: radar_backscatter_prior`).

---

### Cassini RADAR — Titan BIDR (geometry / sparsity)

| File | Size | Flyby | Role | Why suitable |
|------|------|-------|------|--------------|
| `BIEQI69S314_D220_T071S01_V03.IMG` | 351 MB | **T71** (2010-07-07) | **C** (partial) | Full-resolution **incidence-angle backplane** (29,952×3,072 float32). **Not σ⁰** — use for **coverage mask, incidence geometry, sparsity footprint** over south polar / lake-region swath. |
| `BIEQI69S314_D220_T071S01_V03.ZIP` | 79 MB | T71 | **C** (partial) | Archive of incidence product. |

**Footprint:** lat ~−76° to −23°, lon ~25–204°W. Polar/lake-relevant geography — valuable for **lake-focused sparsity experiments** once mask is derived.

**Recommended action:** Register in manifest as `use_case: incidence_geometry` or `sparsity_mask`; download matching **backscatter** BIDR from same pass for σ⁰ calibration. Migrate under `M5_Inference/Inference_Data/raw/` or `data/templates/cassini_radar/bidr/`.

---

### Surface topography template

| File | Size | Region | Role | Why suitable |
|------|------|--------|------|--------------|
| `DEM_T25_T28_Sotra_Facula_09JULY10_isis3.cub` | 726 KB | Sotra Facula (T25–T28) | **C** / surface boundary | ISIS cube — SAR-derived **surface topography** for morphology / boundary conditions when generating synthetic environments. |
| `DEM_T25_T28_Sotra_Facula_09JULY10_isis3.cub.gz` | 213 KB | same | **C** | Compressed copy — redundant if `.cub` kept. |

**Recommended action:** Move to `M5_Inference/data/templates/` or `data/references/`; cite in environment generator provenance.

---

## ⚠️ Partially suitable — use with caveats

| Item | Size | Issue | Experiment use |
|------|------|-------|----------------|
| `CORADR_0077/` (volume tree) | ~32 MB | Titan **distant radiometry only** (SBDR). **No BIDR/SAR** on this volume (Mar 14, 2006). | Passive radiometry channel only; useful for extended forward model, **not** primary SAR sparsity template. |
| `CORADR_0077/DATA/SBDR/SBDR_01_D077_V01.TAB` | 12 MB | Titan SBDR bursts | Role **C** passive / radiometer calibration — secondary to LBDR/BIDR for Phase 1. |
| `CORADR_0077.tar.gz` | 8.6 MB | Duplicate of expanded volume | Keep one copy; prefer extracted tree or drop archive after verify. |
| `BIEQI69S314…` (see above) | 351 MB | Wrong BIDR **band** for σ⁰ prior | Suitable for geometry/sparsity only until backscatter sibling is downloaded. |
| `BIBQD…` (see above) | 17 KB | **Browse-resolution** only | Suitable for pipeline **smoke tests**, not publication-quality regional templates. |

---

## ❌ Not suitable for the Titan experiment

These should **not** be loaded as Titan observation priors or ground truth.

| File | Size | Target / content | Why excluded |
|------|------|------------------|--------------|
| `LBDR_02_003_V01.TAB` | 77 MB | **EARTH** (1999-08-18 flyby) | `TARGET_NAME = EARTH` — Cassini calibration pass over South Pacific / South America. Wrong planet for Titan forward-model calibration. |
| `LBDR_02_003_V01.ZIP` | 2.5 MB | Earth LBDR archive | Same as above. |

**Note:** The **correct** Titan LBDR for the staged pipeline is **`LBDR_02_D294_V02`** (~1.9 GB) under [`M5_Inference/Inference_Data/raw/CORADR_0294/LBDR/`](../M5_Inference/Inference_Data/raw/CORADR_0294/LBDR/) — not in this orphan folder.

---

## 📚 Reference & literature (not pipeline inputs)

Support **Role B** (priors), **Role D** (methods), or mission context — cite in docs; do not pass to `forward_model()` as observations.

| File | Size | Topic | Experiment relevance |
|------|------|-------|---------------------|
| `[03]Hayes_2016.md` | 96 KB | Titan lakes & seas (Hayes 2016) | **High** — science anchor for Layers 1–2, material bounds, observation noise framing ([`INFERENCE_ALGORITHM_CORE_ALIGNMENT.md`](../M5_Inference/INFERENCE_ALGORITHM_CORE_ALIGNMENT.md)). |
| `Scholar References.md` | 68 KB | Compiled notes (Hothorn, Hayes, Krejcar, etc.) | **Medium** — design priors; deduplicated canonical Hayes block should live in [`M5_Inference/Inference_Data/`](../M5_Inference/) or Research Papers. |
| `[01]Computational_Inference.md` | 40 KB | Hothorn et al. — ensemble / computational inference | **Medium (Role D)** — centralized inference baseline framing, not Titan data. |
| `[01]noaa_27165_DS1.md` | 80 KB | NOAA / BAMS operational satellite note | **Low** — Earth weather/ops context; not aligned with Titan subsurface experiment. |
| `[02AI_in_remote_sensing_and_satellite_image_processin.md` | 62 KB | 2026 AI + remote sensing review | **Low** — general ML/RS survey; optional background only. |
| `25-Cassini_Titan_Imaging_Strategy_180112-1.docx` | 1 MB | Cassini Titan imaging strategy (internal/JPL-style) | **Low–medium** — mission planning reference for flyby selection; not ingestible data. |

---

## 🗂️ PDS catalogs & volume documentation (spec only)

| File / path | Role | Notes |
|-------------|------|-------|
| `BIDRDS.CAT` | **Ref** | PDS catalog for BIDR data set `CO-SSA-RADAR-5-BIDR-V1.0` — σ⁰ accuracy ±3/±2 dB, product definitions. |
| `cartods.cat` | **Ref** | Cartographic / map projection catalog. |
| `CORADR_0077/DOCUMENT/*` (BIDRSIS, BODPSIS, VOLSIS) | **Ref** | Product SIS — required reading for ISIS extraction and column definitions. |
| `CORADR_0077/CATALOG/*`, `CALIB/*`, `INDEX/*` | **Ref** | Volume metadata, beam patterns, cumulative index. |
| `README.md` | **Ref** | Points to migrated LBDR in `M5_Inference/Inference_Data/`. |

---

## Cross-check: canonical vs orphan data

| Data product | This folder (`Agentic Lab/Inference_Data`) | Canonical (`M5_Inference/Inference_Data`) |
|--------------|--------------------------------------------|-------------------------------------------|
| Titan LBDR (T120 / S101 pass) | ❌ Not present | ✅ `LBDR_02_D294_V02.TAB` + manifest |
| Titan BIDR T71 incidence | ✅ `BIEQI69S314…IMG` | ❌ Not registered |
| Titan BIDR T16 backscatter (browse) | ✅ `BIBQD…` | ❌ Not registered |
| Earth LBDR calibration | ⚠️ `LBDR_02_003_V01` (exclude) | ❌ |
| Derived `bursts_inference.csv` | ❌ | ⚠️ Header only — not extracted |
| `manifest.csv` (templates) | ❌ | Empty header in `M5_Inference/data/templates/cassini_radar/` |

---

## Recommended priority actions

1. **Migrate ✅ items** into `M5_Inference/` layout (`raw/`, `data/templates/cassini_radar/bidr/`, update `manifest.csv`).
2. **Delete or archive ❌** `LBDR_02_003_V01.*` (Earth) from Titan staging to avoid accidental use.
3. **Download T71 backscatter BIDR** (σ⁰ sibling of `BIEQI69S314…`) for lake-region radar prior.
4. **Extract** canonical `LBDR_02_D294_V02` → `bursts_inference.csv` (ISIS Tier B — see [`../M5_Inference/PLANETARY_TOOLS.md`](../M5_Inference/PLANETARY_TOOLS.md)).
5. **Relocate literature** to `Research Papers/` or a single `references/` folder — keep one canonical `[03]Hayes_2016.md`.
6. **Consolidate** `CORADR_0077.tar.gz` vs expanded tree (keep one).

---

## Quick inspect commands

From `M5_Inference/` with Tier A tools installed:

```bash
source .venv-planetary/bin/activate
python scripts/peek_pds.py ../Inference_Data/BIEQI69S314_D220_T071S01_V03.IMG
python scripts/peek_pds.py ../Inference_Data/BIBQD18N341_D087_T016S03_V03.IMG --label ../Inference_Data/BIBQD18N341_D087_T016S03_V03.LBL
python scripts/peek_pds.py ../Inference_Data/LBDR_02_003_V01.TAB   # confirms TARGET_NAME=EARTH
```

---

## Suitability legend (used above)

| Symbol | Meaning |
|--------|---------|
| ✅ | Ready for experiment pipeline (Role C or strong template) after manifest registration |
| ⚠️ | Useful but incomplete, wrong band, or secondary priority |
| ❌ | Wrong target, wrong role, or misleading if used as Titan input |
| 📚 | Citation / design reference only |
| 🗂️ | PDS specification & volume docs |

---

*Generated for ExploreTitan M5 Phase F data coordination. Update this file when products are migrated to `M5_Inference/Inference_Data/`.*
