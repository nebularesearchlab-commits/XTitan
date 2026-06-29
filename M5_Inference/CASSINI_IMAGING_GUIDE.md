# Cassini RADAR Imaging — Acquisition Guide for ExploreTitan

How to locate, filter, and download Titan RADAR products from NASA PDS for use as **observation priors** and **sparsity masks** in the M5_Inference pipeline. Ground truth remains synthetic; Cassini data constrains realism only.

**Parent doc:** [`../DATA_SOURCES.md`](../DATA_SOURCES.md)  
**Local destination:** `M5_Inference/data/templates/cassini_radar/`  
**Modification context:** [`MODIFICATION_DESIGN.md`](MODIFICATION_DESIGN.md) Phase F

---

## 1. What you need from Cassini (ExploreTitan roles)

| Need | Cassini product | ExploreTitan use |
|------|-----------------|------------------|
| **SAR backscatter images** | BIDR (Basic Image Data Record) | Surface template; radar forward-model calibration |
| **Topography** | ABDR / SAR-topo / Cornell DTM | Surface boundary for subsurface grid |
| **Coverage sparsity** | BIDR observation footprint | Mask: which grid cells have real observations |
| **Polar lakes region** | T63–T71, T110 flybys | Lake-focused experiment template |
| **Radiometry** | SBDR / LBDR | Passive brightness temperature channel (optional) |

**Do not need for Phase 1:** Full archive download (TB-scale). Start with 5–20 BIDR swaths.

---

## 2. Primary search portals (ranked)

### Tier A — Start here

| Portal | URL | Best for |
|--------|-----|----------|
| **PDS Imaging Atlas (your query)** | [Titan RADAR — thumbnails available](https://pds-imaging.jpl.nasa.gov/search/?fq=ATLAS_MISSION_NAME%3Acassini&fq=ATLAS_INSTRUMENT_NAME%3Aradar&fq=-ATLAS_THUMBNAIL_URL%3Abrwsnotavail.jpg&fq=ATLAS_SPACECRAFT_NAME%3A%22cassini%20orbiter%22&fq=TARGET%3Atitan&q=*%3A*) | Browse SAR swaths with preview images |
| **PDS Imaging Atlas (broad RADAR)** | [All Cassini RADAR](https://pds-imaging.jpl.nasa.gov/search/?fq=ATLAS_MISSION_NAME:cassini&fq=ATLAS_INSTRUMENT_NAME:radar&q=*:*) | All modes including altimetry bursts |
| **Cassini mission portal** | [PDS Imaging Node — Cassini](https://pds-imaging.jpl.nasa.gov/portal/cassini_mission.html) | Product descriptions, BIDR SIS, volume index |
| **Cornell RADAR DMP** | [Digital Map Products](https://data.astro.cornell.edu/RADAR/) | **Pre-mosaicked global gridded maps** (~9% coverage) — fastest for sparsity templates |
| **Titan Trek** | [trek.nasa.gov/titan](https://trek.nasa.gov/titan/) | Map-based search; geographic context for flybys |

### Tier B — Bulk / programmatic

| Portal | URL | Best for |
|--------|-----|----------|
| **RADAR online volumes** | [pds-imaging.jpl.nasa.gov/volumes/radar.html](https://pds-imaging.jpl.nasa.gov/volumes/radar.html) | Flyby-organized ZIP volumes (BIDR, ABDR, SBDR, LBDR) |
| **Cornell eCommons DTM** | [SAR-derived topography](https://ecommons.cornell.edu/items/88de3ac0-b77b-46fa-bb30-ba02f17cf12c) | Global interpolated topography (ISIS cubes) |
| **PDS Atmospheres Cassini hub** | [act-find.html](https://pds-atmospheres.nmsu.edu/data_and_services/atmospheres_data/Cassini/act-find.html) | Cross-links to Atlas, OPUS, Titan Trek |

### Tier C — Documentation (calibrate simulators)

| Resource | URL |
|----------|-----|
| RADAR User's Guide (2nd ed.) | [RADARUsersGuide2ndEdV2.pdf](https://pds-imaging.jpl.nasa.gov/documentation/RADARUsersGuide2ndEdV2.pdf) |
| Image Atlas user guide | [Cassini_Users_Guide_ImageAtlas.pdf](https://pds-imaging.jpl.nasa.gov/documentation/Cassini_Users_Guide_ImageAtlas_9.12.pdf) |
| BIDR product SIS | Linked from [Cassini RADAR portal](https://pds-imaging.jpl.nasa.gov/portal/cassini_mission.html) |
| RADAR instrument page | [inst-radar.html](https://pds-atmospheres.nmsu.edu/data_and_services/atmospheres_data/Cassini/inst-radar.html) |

---

## 3. Your Atlas URL — filter breakdown

Base query (thumbnail-filtered Titan SAR):

```
https://pds-imaging.jpl.nasa.gov/search/
  ?fq=ATLAS_MISSION_NAME:cassini
  &fq=ATLAS_INSTRUMENT_NAME:radar
  &fq=-ATLAS_THUMBNAIL_URL:brwsnotavail.jpg
  &fq=ATLAS_SPACECRAFT_NAME:"cassini orbiter"
  &fq=TARGET:titan
  &q=*:*
```

| Filter | Meaning | Suggestion |
|--------|---------|------------|
| `ATLAS_MISSION_NAME:cassini` | Cassini-Huygens mission only | Keep |
| `ATLAS_INSTRUMENT_NAME:radar` | RADAR instrument (SAR, altimetry, radiometry) | Keep; narrow in UI if needed |
| `-ATLAS_THUMBNAIL_URL:brwsnotavail.jpg` | Exclude products without browse thumbnail | **Good for visual search**; may hide valid but unbrowseable products |
| `ATLAS_SPACECRAFT_NAME:"cassini orbiter"` | Orbiter data (not Huygens probe) | Keep |
| `TARGET:titan` | Titan flybys only | Keep |
| `q=*:*` | Match all remaining records | Keep |

**Note:** Atlas may display *"currently undergoing an update; some data may be temporarily unavailable."* If search fails, use Cornell DMP or volume index (Section 5).

---

## 4. Recommended Atlas workflow (step-by-step)

### Step 1 — Open pre-filtered Titan RADAR search

Use your URL or the [broad RADAR Titan search](https://pds-imaging.jpl.nasa.gov/search/?fq=ATLAS_MISSION_NAME:cassini&fq=ATLAS_INSTRUMENT_NAME:radar&fq=TARGET:titan&q=*:*).

### Step 2 — Narrow by product type (UI dropdowns)

In the left panel, set:

| Parameter | Recommended value | Why |
|-----------|-------------------|-----|
| **Target** | Titan | Already filtered |
| **Product Type** | Basic Image (BIDR) / SAR-related | SAR swaths for backscatter templates |
| **Spacecraft altitude** | 900–1600 km (SAR range) | Per RADAR User's Guide SAR mode |
| **Time range** | 2004-10 to 2017-09 | Cassini at Saturn |

For **polar lakes**, add lat constraint:

| Parameter | Value |
|-----------|-------|
| **Sub-spacecraft latitude** | 65° to 90° N (or S) |

### Step 3 — Use Get Count before full search

Click **Get Count** (Atlas UI) to preview result size. Target **10–50 products** for a first template set, not thousands.

### Step 4 — Browse thumbnails

- Select products with clear lake/shoreline or dune features for morphology diversity.
- Record **Product ID** and **Start Time** for provenance in `data/templates/cassini_radar/manifest.csv`.

### Step 5 — Download

| Method | When to use |
|--------|-------------|
| **Bulk File Download → Create WGET File** | 5–50 products (recommended) |
| **Reports → Download CSV** | Metadata manifest only (geometry, times, IDs) |
| **Individual product link** | Single swath inspection |

WGET instructions: Atlas help → [Bulk File Download](https://pds-imaging.jpl.nasa.gov/atlas/intro.html) (macOS: `source atlas_wget_script*` in Downloads).

### Step 6 — Store locally

```
M5_Inference/data/templates/cassini_radar/
├── manifest.csv              # Product ID, flyby, time, lat, lon, local path
├── bidr/                     # Raw PDS BIDR products
├── thumbnails/               # Optional browse copies
└── sparsity_masks/           # Derived 0/1 grids for forward_model
```

---

## 5. Alternative when Atlas is slow or empty

### Option A — Cornell Digital Map Products (fastest global context)

1. Go to [data.astro.cornell.edu/RADAR/](https://data.astro.cornell.edu/RADAR/)
2. Download gridded backscatter / topo map products (PDS3 indices included)
3. Use map index to build **global sparsity mask** (~9% observed area)

**Best for:** Phase F sparsity mask without per-flyby hunting.

### Option B — Volume index by flyby

1. [RADAR volumes page](https://pds-imaging.jpl.nasa.gov/volumes/radar.html)
2. Find Titan flyby label (e.g. `T77`, `T110`)
3. Download volume ZIP containing BIDR + calibration

**Notable flybys for ExploreTitan:**

| Flyby | Date (approx) | Region / note |
|-------|---------------|---------------|
| T16–T28 | 2005–2006 | Early SAR; varied terrain |
| T63–T71 | 2009–2010 | North polar lakes |
| T110 | 2015-03 | High-latitude (75°N); gravity + lakes |
| T120 | 2016-06 | Final SAR swaths |

### Option C — Titan Trek (geographic)

1. [trek.nasa.gov/titan](https://trek.nasa.gov/titan/)
2. Navigate to Ontario Lacus, Kraken Mare, or dune fields
3. Click data overlay → links to underlying PDS products

---

## 6. Product type reference (what to download)

| Product | Extension / label | Contains | ExploreTitan channel |
|---------|-------------------|----------|----------------------|
| **BIDR** | `.IMG` + `.LBL` | Calibrated SAR backscatter grid | `radar_backscatter` prior |
| **ABDR** | Burst altimetry | Surface height profile | Topography boundary |
| **ASUM** | CSV summary | Altimetry summary | Quick topo lookup |
| **SBDR / LBDR** | Burst ordered | Radiometry / scatterometry | Optional passive channel |
| **DMP** | Cornell gridded maps | Global mosaic tiles | Sparsity + regional template |

**Phase 1 priority:** BIDR + Cornell DMP index.  
**Phase 2:** ABDR for lake bathymetry context; PGDA gravity separately in `data/references/`.

---

## 7. Pre-built search URLs (copy-paste)

### Titan SAR with browse thumbnails (your query)

https://pds-imaging.jpl.nasa.gov/search/?fq=ATLAS_MISSION_NAME%3Acassini&fq=ATLAS_INSTRUMENT_NAME%3Aradar&fq=-ATLAS_THUMBNAIL_URL%3Abrwsnotavail.jpg&fq=ATLAS_SPACECRAFT_NAME%3A%22cassini%20orbiter%22&fq=TARGET%3Atitan&q=*%3A*

### Titan RADAR — all products (no thumbnail filter)

https://pds-imaging.jpl.nasa.gov/search/?fq=ATLAS_MISSION_NAME:cassini&fq=ATLAS_INSTRUMENT_NAME:radar&fq=TARGET:titan&q=*:*

### Titan RADAR — north polar region (atlas text search supplement)

Add in search box or Geometry tab:

```
SUB_SPACECRAFT_LATITUDE:[65 TO 90]
```

Or use Titan Trek north pole view, then cross-reference Product IDs in Atlas.

### Cassini RADAR portal (documentation + volume links)

https://pds-imaging.jpl.nasa.gov/portal/cassini_mission.html

---

## 8. manifest.csv schema (track what you download)

Create `data/templates/cassini_radar/manifest.csv`:

| Column | Example | Purpose |
|--------|---------|---------|
| `product_id` | `CO-SSA-RADAR-5-BIDR-V1.0/...` | PDS identifier |
| `flyby` | `T110` | Mission event |
| `start_time_utc` | `2015-03-11T...` | Temporal provenance |
| `sub_spacecraft_lat` | `75.2` | Region tag |
| `sub_spacecraft_lon` | `120.5` | Region tag |
| `product_type` | `BIDR` | Processing pipeline |
| `local_file` | `bidr/T110_xxx.IMG` | Path in repo |
| `use_case` | `lake_sparsity_mask` | How used in simulation |

---

## 9. Processing tools (after download)

**Full install guide:** [`PLANETARY_TOOLS.md`](PLANETARY_TOOLS.md) — tiered setup (Python quick-read + optional ISIS3).

| Tier | Tool | Install | Use |
|------|------|---------|-----|
| **A** | Python + `src/pds_io.py` | `pip install -r requirements-planetary.txt` | Label parse, BIDR → NumPy, `scripts/peek_pds.py` |
| **B** | **ISIS3** | `environment-planetary.yml` / `scripts/install_planetary_tools.sh --full` | `bidr2isis`, `sbdr2grid`, LBDR burst extraction |
| **B** | **GDAL** | conda-forge (in env file) | GeoTIFF export after ISIS |
| **C** | **QGIS** | [qgis.org](https://qgis.org) | Map overlay (optional GUI) |

Quick inspect after download:

```bash
python scripts/peek_pds.py path/to/product.IMG --plot --sample 512
```

For ExploreTitan Phase F: convert selected BIDR swath to a simple **2D numpy mask** → `sparsity_masks/t110_lakes.npy`.

---

## 10. Suggested first download set (minimal)

1. **Cornell DMP** backscatter index — global sparsity template  
2. **3 BIDR swaths** from Atlas (your URL): one lake, one dune, one bright plains  
3. **manifest.csv** with Product IDs and geometry  
4. Optional: **PGDA Titan gravity SHA** → `data/references/pgda_titan_gravity.sha`

Total size: typically **< 500 MB** if you avoid bulk volume ZIPs.

---

## 11. Integration with forward model (MODIFICATION_DESIGN Phase F)

```python
def load_sparsity_mask(template_path: str, grid_shape: tuple) -> np.ndarray:
    """
    Load Cassini-derived coverage mask.
    1 = cell has real observation coverage; 0 = unobserved (infer only).
    """
```

Apply in `forward_model()`:

```python
if sparsity_mask is not None:
    obs[node] = None if sparsity_mask[node] == 0 else simulated_value
```

This implements Phase 2 from `DATA_SOURCES.md`: *same synthetic truth, Cassini-like sparsity*.

---

## 12. Troubleshooting

| Issue | Action |
|-------|--------|
| Atlas shows no results | Remove thumbnail filter; try volume index |
| Atlas update message | Use Cornell DMP or `volumes/radar.html` |
| Thumbnail but download fails | Use WGET script, not browser bulk download |
| Wrong product type | Filter Product Type = BIDR in Atlas left panel |
| Coordinates confusing | Prefer Titan Trek for lat/lon, then Product ID in Atlas |
| File format unfamiliar | Read `.LBL` label file; use ISIS3 or FIJI |

**Help:** PDS Imaging Node — webmaster link on Atlas page; [PDS support](https://pds.jpl.nasa.gov/).

---

*Guide for ExploreTitan template acquisition — not an operational mission data pipeline.*
