# Planetary Tools — ExploreTitan / M5_Inference

Organized install guide for reading Cassini RADAR PDS products and supporting the inference experiment pipeline.

**Quick start (label + array preview, no ISIS):**

```bash
cd M5_Inference
python3 -m venv .venv-planetary
source .venv-planetary/bin/activate
pip install -r requirements-planetary.txt
python scripts/peek_pds.py ../Inference_Data/BIEQI69S314_D220_T071S01_V03.IMG --plot
```

**Full RADAR processing (BIDR → cube, LBDR → burst grids):**

```bash
cd M5_Inference
bash scripts/install_planetary_tools.sh --full
conda activate exploretitan-planetary
```

---

## 1. What you are reading

Cassini `.IMG` files in this project are **PDS3** planetary products — not TIFF, PNG, or ENVI rasters. Labels may be **embedded** in record 1 of the file or shipped as a separate `.LBL`.

| Local example | PDS type | Experiment role |
|---------------|----------|-----------------|
| `BIEQI69S314_D220_T071S01_V03.IMG` | BIDR backplane | Role C — sparsity / geometry prior |
| `LBDR_02_D294_V02.TAB` | LBDR burst table | Role C — σ⁰ noise calibration |
| `environment_001.csv` | Synthetic | Role A — ground truth (no PDS tools needed) |
| `titan_materials.csv` | Physics bounds | Role B — forward model (no PDS tools needed) |

See [`Inference_Data/SCHEMA.md`](Inference_Data/SCHEMA.md) and [`CASSINI_IMAGING_GUIDE.md`](CASSINI_IMAGING_GUIDE.md) for acquisition workflows.

---

## 2. Tool tiers

### Tier A — Quick read (required for daily work)

Install in ~1 minute. Enough to inspect labels, load BIDR arrays into NumPy, and preview in the notebook.

| Tool | Install | Use in ExploreTitan |
|------|---------|---------------------|
| **Python 3.9+** | system / venv | Notebook + `src/pds_io.py` |
| **NumPy, Matplotlib, Pandas** | `requirements-planetary.txt` | Arrays, plots, derived CSVs |
| **pvl** | `requirements-planetary.txt` | Parse PDS3 `.LBL` text |
| **PyYAML** | `requirements-planetary.txt` | `inference_data_manifest.yaml` |
| **`src/pds_io.py`** | in repo | `read_pds3_image()`, `summarize_product()` |
| **`scripts/peek_pds.py`** | in repo | CLI quick inspect + optional plot |

```bash
pip install -r requirements-planetary.txt
python scripts/peek_pds.py path/to/product.IMG
python scripts/peek_pds.py Inference_Data/raw/.../LBDR_02_D294_V02.TAB --label-only
```

### Tier B — RADAR processing (download when extracting LBDR / georeferencing BIDR)

USGS ISIS3 is the reference toolchain for Cassini RADAR. Use when Tier A is not enough (full burst extraction, map projection, cube export).

| Tool | Install | Use in ExploreTitan |
|------|---------|---------------------|
| **ISIS3** | `environment-planetary.yml` or `install_planetary_tools.sh --full` | `bidr2isis`, `sbdr2isis`, `sbdr2grid`, `qview` |
| **GDAL** | conda-forge (included in env file) | `gdalinfo`, GeoTIFF export after ISIS |
| **QGIS** | [qgis.org](https://qgis.org) (optional GUI) | Visual map overlay on Titan |

```bash
conda activate exploretitan-planetary
bidr2isis from=product.IMG to=product.cub
qview product.cub
sbdr2grid from=LBDR_02_D294_V02.TAB to=bursts.cub
```

Document ISIS version in derived CSV provenance (`extraction_tool` column in `SCHEMA.md`).

### Tier C — Acquisition & browse (no install, browser)

| Tool | URL | Use |
|------|-----|-----|
| **PDS Imaging Atlas** | [Atlas Titan RADAR search](https://pds-imaging.jpl.nasa.gov/search/?fq=ATLAS_MISSION_NAME:cassini&fq=ATLAS_INSTRUMENT_NAME:radar&fq=TARGET:titan&q=*:*) | Find + WGET download BIDR/LBDR |
| **RADAR volume index** | [volumes/radar.html](https://pds-imaging.jpl.nasa.gov/volumes/radar.html) | Flyby ZIP volumes (CORADR_XXXX) |
| **Cornell RADAR DMP** | [data.astro.cornell.edu/RADAR/](https://data.astro.cornell.edu/RADAR/) | Global sparsity template (~9% coverage) |
| **Titan Trek** | [trek.nasa.gov/titan](https://trek.nasa.gov/titan/) | Lat/lon → product ID lookup |
| **PDS prod label query** | [planetarydata.jpl.nasa.gov/img/pds/prod](https://planetarydata.jpl.nasa.gov/img/pds/prod) | Fetch `.LBL` text by path |

### Tier D — Optional / not recommended for Phase 1

| Tool | Notes |
|------|-------|
| **FIJI / ImageJ** | OK for ad-hoc preview after export to TIFF; poor native PDS3 support |
| **ENVI** | Commercial; only if you already own a license |
| **PDS4View** | PDS4-focused; Cassini RADAR is PDS3 |

---

## 3. File type → tool matrix

| Extension | Content | Tier A (Python) | Tier B (ISIS) | Derived output |
|-----------|---------|-----------------|---------------|----------------|
| `.IMG` (BIDR) | Gridded float32 SAR / backplane | `read_pds3_image()` | `bidr2isis` → `.cub` | `sparsity_mask_2d.npy` |
| `.LBL` | Detached PDS3 label | `pvl` / `summarize_product()` | input to ISIS | metadata JSON |
| `.TAB` (LBDR) | Binary burst table | label peek only | `sbdr2isis`, `sbdr2grid` | `bursts_inference.csv` |
| `.CAT` | PDS catalog | text editor | — | spec reference |
| `.npy` | Derived mask | NumPy | — | `forward_model` input |

---

## 4. Install paths (macOS)

### A only — Python quick-read

```bash
cd M5_Inference
python3 -m venv .venv-planetary
source .venv-planetary/bin/activate
pip install -r requirements-planetary.txt
python scripts/peek_pds.py --help
```

### A + B — Conda environment with ISIS3

Requires [Miniforge](https://github.com/conda-forge/miniforge) or Anaconda.

```bash
cd M5_Inference
bash scripts/install_planetary_tools.sh --full
conda activate exploretitan-planetary
python scripts/peek_pds.py ../Inference_Data/BIEQI69S314_D220_T071S01_V03.IMG
isisinfo -version
```

Manual equivalent:

```bash
conda env create -f environment-planetary.yml
conda activate exploretitan-planetary
pip install -r requirements-planetary.txt
```

### Optional — QGIS (GUI maps)

```bash
brew install --cask qgis
# Use after exporting ISIS cube → GeoTIFF with gdal_translate
```

---

## 5. Experiment workflow map

```
PDS download (Tier C browser)
        │
        ▼
raw/  .IMG / .TAB / .LBL          ← Tier A: peek_pds.py / pds_io.summarize_product
        │
        ├─ BIDR ──► Tier A: numpy array + mask
        │           Tier B: bidr2isis → sparsity_mask_2d.npy
        │
        └─ LBDR ──► Tier B: sbdr2grid → bursts_inference.csv
                    Tier A: label + row count sanity check
        │
        ▼
derived/  CSV / NPY               ← forward_model + inversion (notebook / src/)
        │
        ▼
results/  metrics JSON            ← evaluate_phase1
```

---

## 6. BIDR product naming (which band did you download?)

Cassini BIDR filenames encode the backplane type. Example: `BIEQI69S314_D220_T071S01_V03`

| Prefix pattern | Typical content |
|----------------|-----------------|
| `BIEQ…` / `BIQ…` | σ⁰ backscatter (what you usually want for radar prior) |
| `BIEQI…` (with incidence note in label) | Incidence angle backplane |
| `BIM…` | Beam mask |
| `BIN…` | Normalized backscatter variant |

Always read the `NOTE` and `OBJECT = IMAGE` fields in the label (`peek_pds.py --label-only`).

---

## 7. Troubleshooting

| Symptom | Fix |
|---------|-----|
| Preview / Photos cannot open `.IMG` | Expected — use `peek_pds.py` or ISIS |
| `pdsimage2.wr.usgs.gov` 404 | Mirror moved; use Atlas or volume ZIP from [radar.html](https://pds-imaging.jpl.nasa.gov/volumes/radar.html) |
| Out of memory loading full BIDR | Use `peek_pds.py --sample 512` or read a crop in notebook |
| LBDR `.TAB` is ~2 GB | Do not load whole file in pandas; use ISIS `sbdr2grid` or stream parser |
| ISIS conda solve fails | Install Miniforge; run `install_planetary_tools.sh --full` again |
| Wrong dtype / garbage image | Check `SAMPLE_TYPE` in label (`PC_REAL` → big-endian float32) |

---

## 8. Related docs

| Doc | Topic |
|-----|-------|
| [`CASSINI_IMAGING_GUIDE.md`](CASSINI_IMAGING_GUIDE.md) | Where to download products |
| [`Inference_Data/SCHEMA.md`](Inference_Data/SCHEMA.md) | Derived file contracts |
| [`src/pds_io.py`](src/pds_io.py) | Python quick-read API |
| [`src/README.md`](src/README.md) | Module roadmap (Phase F) |

---

*Tier A supports Phase 1 notebook work immediately. Add Tier B when extracting LBDR bursts or georeferencing BIDR masks for Phase F.*
