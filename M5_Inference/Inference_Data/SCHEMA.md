# Inference_Data — File Format Specification

Formats for storing Cassini RADAR products and derived inference inputs for the M5_Inference / ExploreTitan pipeline.

---

## 1. Design principles

| Principle | Rule |
|-----------|------|
| **Raw is immutable** | PDS `.LBL` / `.ZIP` / `.TAB` unchanged under `raw/` |
| **Derived is small** | Commit only CSV/JSON/NPY summaries, not 32,768-sample echo arrays |
| **Provenance** | Every derived file links to `product_id`, `pds_label_path`, extraction tool + version |
| **Inference contract** | Derived columns map to `forward_model` channels in `MODIFICATION_DESIGN.md` |

---

## 2. Raw layer — PDS product storage

### Path convention

```
raw/{PDS_VOLUME}/{PRODUCT_TYPE}/{PRODUCT_ID}.{ext}
```

**Example (LBDR_02_D294_V02):**

```
raw/CORADR_0294/LBDR/LBDR_02_D294_V02.LBL
raw/CORADR_0294/LBDR/LBDR_02_D294_V02.ZIP    # optional; ~1.9 GB uncompressed TAB inside
raw/CORADR_0294/LBDR/product_metadata.json    # copy of label + local paths
```

### `product_metadata.json` (required per raw product)

JSON mirror of the PDS3 label with local ingestion fields.

```json
{
  "pds_version_id": "PDS3",
  "data_set_id": "CO-V/E/J/S-RADAR-3-LBDR-V1.0",
  "data_set_name": "CASSINI RADAR LONG BURST DATA RECORD",
  "product_id": "LBDR_02_D294_V02",
  "product_version_id": "02",
  "instrument_host_name": "CASSINI ORBITER",
  "instrument_name": "CASSINI RADAR",
  "target_name": "TITAN",
  "mission_name": "CASSINI-HUYGENS",
  "start_time": "2017-254T20:36:14.565",
  "stop_time": "2017-254T22:06:14.445",
  "closest_approach_time": "2017-254T19:04:49.942",
  "trigger_time": "2017-254T15:21:00.556",
  "epoch_time": "2017-254T15:16:03.000",
  "spacecraft_clock_start_count": 1883857560,
  "spacecraft_clock_stop_count": 1883862960,
  "product_creation_time": "2018-060T20:29:01.000",
  "description": "CASSINI RADAR LONG BURST DATA RECORD FOR THE TITAN S101 PASS ...",
  "pds_volume": "CORADR_0294",
  "pds_relative_path": "/data/cassini/cassini_orbiter/CORADR_0294/DATA/LBDR/LBDR_02_D294_V02.LBL",
  "pds_prod_url": "https://planetarydata.jpl.nasa.gov/img/pds/prod?q=OFSN+%3D+/data/cassini/cassini_orbiter//CORADR_0294/DATA/LBDR/LBDR_02_D294_V02.LBL+AND+RT+%3D+PDS_LABEL",
  "volume_url": "https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0294/",
  "binary_table": {
    "file_name": "LBDR_02_D294_V02.TAB",
    "record_bytes": 132344,
    "file_records": 14515,
    "label_records": 1,
    "table_rows": 14514,
    "table_columns": 236,
    "row_bytes": 132344,
    "structure_format": "SBDR.FMT",
    "required_storage_bytes": 1920973160,
    "compressed_file": "LBDR_02_D294_V02.ZIP"
  },
  "echo_data_column": {
    "name": "ECHO_DATA",
    "data_type": "PC_REAL",
    "items": 32768,
    "item_bytes": 4,
    "start_byte": 1273,
    "note": "Full echo stored in raw TAB only; derived layer stores statistics"
  },
  "local_ingestion": {
    "ingested_at": null,
    "ingested_by": null,
    "raw_files_present": [],
    "status": "catalogued"
  }
}
```

**Label source:** [PDS prod — LBDR_02_D294_V02](https://planetarydata.jpl.nasa.gov/img/pds/prod?q=OFSN+%3D+/data/cassini/cassini_orbiter//CORADR_0294/DATA/LBDR/LBDR_02_D294_V02.LBL+AND+RT+%3D+PDS_LABEL)

---

## 3. Catalog — `catalog/products.csv`

Master index of all products ingested into Inference_Data.

| Column | Type | Description |
|--------|------|-------------|
| `product_id` | string | PDS PRODUCT_ID |
| `pds_volume` | string | e.g. CORADR_0294 |
| `product_type` | enum | LBDR, SBDR, BIDR, ABDR, ASUM |
| `target_name` | string | TITAN |
| `pass_id` | string | e.g. S101, T110 |
| `start_time_utc` | ISO8601 | START_TIME |
| `stop_time_utc` | ISO8601 | STOP_TIME |
| `burst_count` | int | Table rows (if applicable) |
| `raw_status` | enum | catalogued, label_only, downloaded, extracted |
| `derived_path` | string | Relative path under `derived/` |
| `pds_prod_url` | URL | PDS label query link |
| `use_case` | string | forward_calib, sparsity_mask, geometry_prior |
| `notes` | string | Free text |

---

## 4. Derived layer — inference-ready formats

Path:

```
derived/{pds_volume}/{product_id}/
```

### 4.1 `product_summary.json`

Run-level metadata for the inference pipeline.

```json
{
  "product_id": "LBDR_02_D294_V02",
  "pds_volume": "CORADR_0294",
  "target_name": "TITAN",
  "pass_id": "S101",
  "burst_count": 14514,
  "radar_modes_present": ["scatterometry", "altimetry", "SAR_low", "SAR_high", "radiometer"],
  "time_range": {
    "start": "2017-254T20:36:14.565",
    "stop": "2017-254T22:06:14.445",
    "closest_approach": "2017-254T19:04:49.942"
  },
  "derived_files": {
    "bursts_inference": "bursts_inference.csv",
    "geometry": "geometry.csv",
    "sparsity_mask_2d": "sparsity_mask_2d.npy"
  },
  "extraction": {
    "tool": "sbdr2isis | custom_lbdr_extract",
    "tool_version": null,
    "extracted_at": null,
    "source_raw": "../raw/CORADR_0294/LBDR/LBDR_02_D294_V02.LBL"
  },
  "inference_mapping": {
    "radar_backscatter_column": "sigma0_corrected",
    "incidence_column": "act_incidence_angle_deg",
    "position_columns": ["sub_spacecraft_latitude_deg", "sub_spacecraft_longitude_deg"],
    "time_column": "utc_time",
    "burst_key": "burst_id"
  }
}
```

### 4.2 `bursts_inference.csv` (primary derived table)

One row per RADAR burst. Columns extracted from SBDR segment of LBDR (see [BODP SIS](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0284/DOCUMENT/BODPSIS.PDF), ISIS [sbdr2grid](https://isis.astrogeology.usgs.gov/Isis2/html/sbdr2grid.html)).

| Column | Type | Units | ExploreTitan use |
|--------|------|-------|------------------|
| `burst_id` | int | — | Unique burst key (match across SBDR/LBDR/BIDR) |
| `utc_time` | string | ISO8601 | Temporal ordering |
| `radar_mode` | int | 0–15 | 0=scatter, 1=alt, 2=SAR low, 3=SAR high, 4=radiometer |
| `beam_number` | int | — | Antenna beam |
| `sub_spacecraft_latitude_deg` | float | deg | Agent / grid placement |
| `sub_spacecraft_longitude_deg` | float | deg | Positive east |
| `spacecraft_altitude_km` | float | km | Resolution / geometry prior |
| `act_incidence_angle_deg` | float | deg | Forward-model geometry |
| `act_azimuth_angle_deg` | float | deg | Anisotropic backscatter |
| `pass_incidence_angle_deg` | float | deg | Pass-frame geometry |
| `sigma0_corrected` | float | — | **Primary radar_backscatter proxy** (NRCS σ⁰) |
| `sigma0_uncorrected` | float | — | Sensitivity check |
| `antenna_temp_k` | float | K | Radiometry channel (optional) |
| `quality_flag` | int | — | Exclude bad bursts from inference |
| `echo_peak_dn` | float | DN | Echo statistic (not full array) |
| `echo_mean_dn` | float | DN | Echo statistic |
| `echo_std_dn` | float | DN | Echo statistic |
| `echo_samples` | int | — | Always 32768 for LBDR when present |

**Header row (empty template committed to repo):**

See `derived/CORADR_0294/LBDR_02_D294_V02/bursts_inference.csv`.

### 4.3 `geometry.csv` (optional split)

Subset of `bursts_inference.csv` for M5 agent graph construction:

| Column | Type |
|--------|------|
| `burst_id` | int |
| `utc_time` | string |
| `sub_spacecraft_latitude_deg` | float |
| `sub_spacecraft_longitude_deg` | float |
| `spacecraft_altitude_km` | float |
| `act_incidence_angle_deg` | float |

### 4.4 `sparsity_mask_2d.npy` (optional)

NumPy array shape `(n_lat, n_lon)` or project-specific grid matching `TitanGrid`:

| Value | Meaning |
|-------|---------|
| `1` | Cell observed (burst footprint coverage) |
| `0` | Unobserved — inference from neighbors only |

Metadata sidecar: `sparsity_mask_2d.json`

```json
{
  "shape": [180, 360],
  "lat_min": -90,
  "lat_max": 90,
  "lon_min": 0,
  "lon_max": 360,
  "projection": "equirectangular",
  "source_product_id": "LBDR_02_D294_V02"
}
```

---

## 5. Manifest — `manifests/inference_data_manifest.yaml`

Links Inference_Data to simulation runs.

```yaml
version: "1.0"
project: ExploreTitan
default_product: LBDR_02_D294_V02

products:
  - product_id: LBDR_02_D294_V02
    catalog_row: 1
    raw: raw/CORADR_0294/LBDR/
    derived: derived/CORADR_0294/LBDR_02_D294_V02/
    primary_table: bursts_inference.csv

simulation_bindings:
  forward_model_calibration:
    source: derived/CORADR_0294/LBDR_02_D294_V02/bursts_inference.csv
    columns:
      backscatter: sigma0_corrected
      incidence: act_incidence_angle_deg
  sparsity_mask:
    source: derived/CORADR_0294/LBDR_02_D294_V02/sparsity_mask_2d.npy
```

---

## 6. Product-type extensions

| PDS type | Raw path | Primary derived file | Notes |
|----------|----------|----------------------|-------|
| **LBDR** | `raw/.../LBDR/` | `bursts_inference.csv` | SBDR fields + echo stats |
| **SBDR** | `raw/.../SBDR/` | `bursts_inference.csv` | No raw echo column |
| **BIDR** | `raw/.../BIDR/` | `sar_grid.csv` | Gridded σ⁰ / backscatter image |
| **ABDR** | `raw/.../ABDR/` | `altimetry_profile.csv` | Surface height vs track |
| **ASUM** | `raw/.../ASUM/` | `altimetry_summary.csv` | CSV summary per pass |

---

## 7. Loader contract (notebook / `src/io_loaders.py`)

```python
def load_inference_bursts(
    derived_dir: str = "Inference_Data/derived/CORADR_0294/LBDR_02_D294_V02",
) -> pd.DataFrame:
    """Load bursts_inference.csv; validate required columns."""

def load_product_metadata(
    raw_dir: str = "Inference_Data/raw/CORADR_0294/LBDR",
) -> dict:
    """Load product_metadata.json."""
```

Required columns for pipeline: `burst_id`, `sigma0_corrected`, `sub_spacecraft_latitude_deg`, `sub_spacecraft_longitude_deg`, `act_incidence_angle_deg`.

---

## 8. References

- [PDS label — LBDR_02_D294_V02](https://planetarydata.jpl.nasa.gov/img/pds/prod?q=OFSN+%3D+/data/cassini/cassini_orbiter//CORADR_0294/DATA/LBDR/LBDR_02_D294_V02.LBL+AND+RT+%3D+PDS_LABEL)
- [CORADR_0294 volume](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0294/)
- [BODP SIS (SBDR/LBDR)](https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/CORADR_0284/DOCUMENT/BODPSIS.PDF)
- [RADAR instrument — LBDR description](https://pds-atmospheres.nmsu.edu/data_and_services/atmospheres_data/Cassini/inst-radar.html)
