# templates/

Real-data-derived templates that constrain simulation realism (not ground truth).

## cassini_radar/

Cassini RADAR products for sparsity masks and surface morphology priors.

**Acquisition:** [`../../CASSINI_IMAGING_GUIDE.md`](../../CASSINI_IMAGING_GUIDE.md)

```
cassini_radar/
├── manifest.csv           # Product IDs, flyby, geometry, local paths
├── bidr/                  # PDS BIDR products (.IMG + .LBL)
├── thumbnails/            # Optional browse images
└── sparsity_masks/        # Derived .npy or .csv observation masks
```

**Primary Atlas search (Titan SAR, thumbnails):**  
https://pds-imaging.jpl.nasa.gov/search/?fq=ATLAS_MISSION_NAME%3Acassini&fq=ATLAS_INSTRUMENT_NAME%3Aradar&fq=-ATLAS_THUMBNAIL_URL%3Abrwsnotavail.jpg&fq=ATLAS_SPACECRAFT_NAME%3A%22cassini%20orbiter%22&fq=TARGET%3Atitan&q=*%3A*

**Fast alternative:** [Cornell RADAR DMP](https://data.astro.cornell.edu/RADAR/)

## lake_region_topo/ (optional)

Cornell SAR-derived DTM subset for polar lake experiments.

**Source:** [Cornell eCommons DTM](https://ecommons.cornell.edu/items/88de3ac0-b77b-46fa-bb30-ba02f17cf12c)
