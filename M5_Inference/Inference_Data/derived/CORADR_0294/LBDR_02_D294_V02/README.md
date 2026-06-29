# derived/CORADR_0294/LBDR_02_D294_V02/

Inference-ready extracts from **LBDR_02_D294_V02** (Titan S101 pass).

| File | Status | Description |
|------|--------|-------------|
| `product_summary.json` | Ready | Run metadata + column mapping |
| `bursts_inference.csv` | Header only | Populate via LBDR extraction |
| `geometry.csv` | Header only | Subspacecraft track for agent graph |
| `sparsity_mask_2d.npy` | Pending | Grid coverage mask |
| `sparsity_mask_2d.json` | Pending | Mask grid definition |

**Extraction:** ISIS `sbdr2isis` / `sbdr2grid` on LBDR table, or custom parser per `SBDR.FMT`.  
See [`../../../SCHEMA.md`](../../../SCHEMA.md).
