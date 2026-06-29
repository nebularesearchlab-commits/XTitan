# Inference_Data

Canonical store for **Cassini RADAR (and future) observation products** converted into **ExploreTitan inference-ready formats**.

Raw PDS archives stay in `raw/`; lightweight derived tables used by the notebook and `forward_model` live in `derived/`.

**Schema reference:** [`SCHEMA.md`](SCHEMA.md)  
**Imaging acquisition:** [`../CASSINI_IMAGING_GUIDE.md`](../CASSINI_IMAGING_GUIDE.md)  
**Reading PDS files:** [`../PLANETARY_TOOLS.md`](../PLANETARY_TOOLS.md)  
**Pipeline spec:** [`../MODIFICATION_DESIGN.md`](../MODIFICATION_DESIGN.md)

---

## Layout

```
Inference_Data/
├── README.md                 ← this file
├── SCHEMA.md                 ← column definitions and JSON contracts
├── catalog/
│   └── products.csv          ← master index of all ingested products
├── manifests/
│   └── inference_data_manifest.yaml
├── raw/                      ← original PDS (large — gitignored)
│   └── CORADR_0294/
│       └── LBDR/
│           ├── LBDR_02_D294_V02.LBL
│           ├── LBDR_02_D294_V02.ZIP   (optional local copy)
│           └── product_metadata.json
└── derived/                  ← inference pipeline inputs (commit small CSV/JSON)
    └── CORADR_0294/
        └── LBDR_02_D294_V02/
            ├── product_summary.json
            ├── bursts_inference.csv
            ├── geometry.csv              (optional split)
            └── sparsity_mask_2d.npy      (optional grid mask)
```

---

## First catalogued product

| Field | Value |
|-------|-------|
| **Product ID** | `LBDR_02_D294_V02` |
| **PDS volume** | `CORADR_0294` |
| **Target** | Titan |
| **Pass** | S101 (T101) |
| **Type** | LBDR — Long Burst Data Record (SBDR + raw echo) |
| **Label** | [PDS prod query](https://planetarydata.jpl.nasa.gov/img/pds/prod?q=OFSN+%3D+/data/cassini/cassini_orbiter//CORADR_0294/DATA/LBDR/LBDR_02_D294_V02.LBL+AND+RT+%3D+PDS_LABEL) |
| **Bursts** | 14,514 rows (transmitter on) |
| **Uncompressed size** | ~1.92 GB (`.TAB` binary table) |

---

## Workflow

1. **Ingest** — Download `.LBL` (+ `.ZIP` if needed) into `raw/{volume}/{product_type}/`
2. **Catalog** — Append row to `catalog/products.csv`; copy label fields to `product_metadata.json`
3. **Extract** — Run extraction (ISIS `sbdr2isis` / custom parser) → `derived/.../bursts_inference.csv`
4. **Consume** — `io_loaders.load_inference_bursts()` in notebook Phase F → forward-model calibration / sparsity masks

Do **not** commit multi-GB `.TAB` / `.ZIP` files. Commit `derived/` summaries and metadata only.
