# Titan Mind Map Standalone Site Blueprint

## Project Title

**Titan Data Atlas: Standalone Interactive Mind Map Site (Cassini Titan Scope)**

---

## 1) Build Intent

Build a standalone website that visualizes the Titan-relevant Cassini data ecosystem as an interactive, navigable mind map.  
The site should be static-deployable (no required backend), Replit-friendly, and maintainable as a reproducible data product.

This blueprint is designed so implementation can begin immediately in Replit with minimal architecture rework.

---

## 2) Definition of "Full" (Titan-Only)

"Full" means Titan-complete within the identified Titan branches and linked assets, not full-mission Cassini across all targets.

### In Scope (Primary)

1. `sci-titan.html` content hierarchy (overview + Titan science sections).
2. `sci-titan-flybys.html` complete flyby table graph.
3. Titan flyby artifact trees:
   - `Cassini/Cassini/Cassini Titan Master Time lines 5-28-19/`
   - `Cassini/Cassini/TOST_Products_per_Flyby/HandoffPackages/`
   - `Cassini/Cassini/TOST_Products_per_Flyby/SPASS/`
   - `Cassini/Cassini/TOST_Products_per_Flyby/CIMSTimelineWithGaps/`
   - `Cassini/Cassini/TOST_Products_per_Flyby/OutreachGraphics/`
4. Titan Tour Atlas branches:
   - `pub/Cassini/tour_atlas/titan/TITAN_XMB/`
   - `pub/Cassini/tour_atlas/titan/tables/`
5. Titan references reachable from Titan pages (docs, summary sheets, flyby trackers).

### In Scope (Secondary)

1. Titan-relevant instrument landing pages (`inst-radar-sar`, `inst-radar`, `inst-cirs`, etc.) as context nodes.
2. Huygens landing page link integration where Titan page references it.
3. External tool nodes as references (OPUS, Image Atlas, Titan Trek), marked as external.

### Out of Scope (v1)

1. Non-Titan planetary targets (rings-only, icy moon-only branches unrelated to Titan flyby chain).
2. Mirroring binary assets locally unless explicitly needed.
3. Full text extraction from every PDF for v1 (metadata + title parsing is enough).

---

## 3) Product Goals

1. **Cognitive navigation:** a user can traverse Titan mission knowledge by phase, flyby, instrument, and asset type.
2. **Research utility:** each node resolves to source metadata and direct URL.
3. **Scalability:** graph supports thousands of assets without unusable visual clutter.
4. **Reproducibility:** data generation is scriptable and deterministic.
5. **Portable deployment:** static hosting on Replit Deploy, Cloudflare Pages, Netlify, or GitHub Pages.

---

## 4) Non-Functional Requirements

1. **Performance:** initial page interactive under 3 seconds on typical broadband after first build.
2. **Progressive rendering:** avoid plotting all file-level nodes at startup.
3. **Accessibility:** keyboard search and readable contrast baseline.
4. **Resilience:** crawler handles broken links/timeouts and records failures without stopping.
5. **Traceability:** every node has `source_url` and `discovered_from`.

---

## 5) High-Level System Architecture

### Layer A — Data Acquisition

Crawler + parser scripts fetch Titan entry pages and index directories, normalize URLs, and extract node/edge candidates.

### Layer B — Data Normalization

Deduplicate entities, classify node types, infer flyby IDs, mission phases, and instrument tags.

### Layer C — Graph Build

Generate `graph.json` (or sharded graph chunks) plus `search-index.json`.

### Layer D — Static Site

Frontend app loads graph data and provides:
- mind map canvas
- expandable branches
- filters
- details panel
- source linking

### Layer E — Optional Update Workflow

Manual "refresh data" button in Replit runs scripts and updates graph artifacts.

---

## 6) Recommended Tech Stack (Replit-Friendly)

## Frontend

- `React + TypeScript + Vite`
- `Cytoscape.js` (or `react-force-graph` if preferred)
- `Zustand` or built-in React state for graph/filter state
- `MiniSearch` or `Fuse.js` for client-side search

## Data Pipeline

- `Python 3.11+`
- `httpx` or `requests`
- `beautifulsoup4` + `lxml`
- `pydantic` for schema validation
- `orjson` for fast JSON writes

## Tooling

- `npm` for frontend
- `pip`/`uv` for Python scripts
- `Makefile` or `taskfile` for one-command runs

---

## 7) Information Architecture (IA)

Top-level nav:

1. **Mind Map** (primary interactive graph)
2. **Flyby Explorer** (table/list view with filters)
3. **Collections** (directory-centric lens)
4. **Methods** (how data was crawled/normalized)
5. **About & Sources** (citations, constraints, policy notes)

Core mental models supported:

1. by mission phase (Prime, XM, XXM, nT / finale)
2. by flyby ID (`T0`, `TA`, `TB`, ..., `T126`, etc.)
3. by artifact type (handoff, SPASS, CIMS timeline, outreach media, geometry plots, tables)
4. by instrument/data family

---

## 8) Graph Model Specification

Use a property graph with typed nodes and typed edges.

### Node Types

1. `root` — Titan Atlas root node.
2. `section` — page sections (`surface`, `atmosphere`, etc.).
3. `page` — HTML pages.
4. `collection` — directory/index collections.
5. `flyby` — canonical flyby entity.
6. `artifact` — concrete file resource (pdf/jpg/tab/txt/mov).
7. `instrument` — instrument context nodes.
8. `external_tool` — OPUS/Image Atlas/Titan Trek.
9. `reference` — reports/summary docs.

### Edge Types

1. `contains`
2. `references`
3. `has_flyby`
4. `has_artifact`
5. `belongs_to_phase`
6. `related_instrument`
7. `same_flyby_variant`
8. `external_link`

### Required Node Fields

```json
{
  "id": "string-unique",
  "type": "flyby|artifact|collection|...",
  "label": "human readable",
  "source_url": "https://...",
  "discovered_from": "https://...",
  "tags": ["Titan", "Prime", "SPASS"],
  "meta": {}
}
```

### Required Edge Fields

```json
{
  "id": "edge-unique",
  "source": "node-id-a",
  "target": "node-id-b",
  "type": "has_artifact",
  "meta": {}
}
```

---

## 9) Canonical Naming Rules

1. Normalize host aliases: treat `atmos.nmsu.edu` and `pds-atmospheres.nmsu.edu` as related but preserve original source URL.
2. URL canonicalization:
   - lowercase host
   - remove fragment for entity identity
   - strip tracking/query params unless semantically necessary
3. File identity:
   - canonical by full path URL
   - preserve original filename in metadata
4. Flyby identity:
   - parse patterns like `T0`, `TA`, `TB`, `T126`, `nTxxx` from link text and filenames
   - merge known aliases under one canonical flyby node

---

## 10) Titan Data Acquisition Blueprint

### Step 1 — Seed Set

Start from:

1. `.../Cassini/sci-titan.html`
2. `.../Cassini/sci-titan-flybys.html`
3. `.../Cassini/sci-titan-ref.html`
4. `.../Cassini/act-find.html` (for common tools)
5. `.../Huygens/Huygens.html` (contextual)

### Step 2 — Controlled Expansion

Traverse links only if they match Titan inclusion rules:

1. URL path in known Titan directories
2. or link text/path indicates Titan flyby asset
3. or explicitly whitelisted contextual pages

### Step 3 — Directory Index Parsing

For Apache-style index pages:

1. parse every listed file/child link
2. classify by extension
3. connect child resources to parent collection

### Step 4 — Flyby Entity Resolution

From `sci-titan-flybys.html`:

1. create one `flyby` node per unique flyby ID
2. attach date, mission phase (if inferable), and linked artifact bundle

### Step 5 — Output Artifacts

Generate:

1. `data/graph/graph.json`
2. `data/graph/nodes.ndjson` (optional debugging)
3. `data/graph/edges.ndjson` (optional debugging)
4. `data/search/search-index.json`
5. `data/reports/crawl-report.json`

---

## 11) Recommended Repository Layout

```text
titan-data-atlas/
  README.md
  package.json
  pyproject.toml
  .gitignore
  apps/
    web/
      index.html
      src/
        main.tsx
        app/
          App.tsx
          routes.tsx
        components/
          MindMapCanvas.tsx
          FilterPanel.tsx
          DetailsPanel.tsx
          FlybyTable.tsx
        lib/
          graph-loader.ts
          layout.ts
          search.ts
        styles/
          globals.css
  data/
    graph/
      graph.json
      crawl-report.json
    search/
      search-index.json
  scripts/
    crawl/
      crawl_titan.py
      parse_indices.py
      normalize_entities.py
      build_graph.py
      build_search_index.py
    qa/
      validate_graph.py
      check_broken_links.py
  docs/
    METHODS.md
    DATA_POLICY.md
```

---

## 12) Frontend Feature Blueprint

## 12.1 Mind Map Canvas

1. Default view: root -> sections -> major collections.
2. Click-expand for deep branches (flyby -> artifacts).
3. Node color by type.
4. Edge style by relationship.
5. Pan/zoom with reset button.

## 12.2 Filter Panel

1. Mission phase
2. Flyby ID
3. Node type
4. File extension
5. Instrument

## 12.3 Details Panel

1. Node label/type
2. Description (if available)
3. Source URL (open in new tab)
4. Parent/child links
5. Related nodes

## 12.4 Search

1. Full-text search over labels, tags, filenames.
2. Jump-to-node result behavior.
3. Recent search chips.

## 12.5 Flyby Explorer (Table View)

1. One row per flyby.
2. Columns for date, phase, artifact counts.
3. Expand row to show linked files/categories.

---

## 13) Visual and Interaction Design Guidance

1. Use dark neutral background for graph legibility.
2. Maintain consistent color legend:
   - flyby = amber
   - collection = blue
   - artifact = gray
   - reference = purple
   - external = green
3. Keep labels concise and truncate long file names in-node.
4. Show full path only in details panel.
5. Add "Open source" action for each node.

---

## 14) Performance Strategy

1. Do not render all artifact nodes at load.
2. Use hierarchical loading:
   - load root graph first
   - fetch branch chunk on expansion
3. Memoize layout output for unchanged subgraphs.
4. Debounce search input.
5. Optionally precompute layout coordinates for stable initial view.

---

## 15) Data Quality and QA Plan

## Structural QA

1. no duplicate node IDs
2. no edges with missing endpoints
3. all nodes have source URLs
4. every artifact has a parent collection or flyby

## Semantic QA

1. flyby ID extraction correctness checks
2. phase assignment sanity checks
3. extension/type classification checks

## Link QA

1. record status of outbound URLs
2. flag dead links in report
3. do not remove failed nodes automatically (mark as unavailable)

---

## 16) Compliance, Attribution, and Ethics

1. Include attribution to PDS Atmospheres Node and related public sources.
2. Preserve source URLs rather than claiming local authorship.
3. Respect `robots.txt` and responsible crawl pacing.
4. Do not mirror large binary assets unless policy and storage allow it.

---

## 17) Replit Build Plan (Milestones)

## Milestone 1 — Project Skeleton (Day 1)

1. Initialize repo structure.
2. Scaffold Vite React app.
3. Add Python script folder and dependencies.
4. Add placeholder graph and UI shell.

## Milestone 2 — Titan Crawler MVP (Day 1-2)

1. Implement seed crawl.
2. Parse `sci-titan` + `sci-titan-flybys`.
3. Parse major directory indexes.
4. Emit raw node/edge candidates.

## Milestone 3 — Graph Normalization (Day 2-3)

1. Canonicalize URLs.
2. Resolve flyby entities and aliases.
3. Classify node/edge types.
4. Emit validated `graph.json`.

## Milestone 4 — Interactive Mind Map (Day 3-4)

1. Render graph root and major branches.
2. Add details panel and source links.
3. Add branch expansion behavior.

## Milestone 5 — Search + Filters (Day 4-5)

1. Build client search index.
2. Add multi-filter controls.
3. Add flyby-focused quick filters.

## Milestone 6 — QA + Deployment (Day 5)

1. Run structural/semantic/link checks.
2. Write methods and limitations page.
3. Deploy static build from Replit.

---

## 18) Replit Runtime and Command Blueprint

Use two workflows: data refresh and web app.

### Data Refresh Commands

```bash
python scripts/crawl/crawl_titan.py
python scripts/crawl/normalize_entities.py
python scripts/crawl/build_graph.py
python scripts/crawl/build_search_index.py
python scripts/qa/validate_graph.py
```

### Web Commands

```bash
npm install
npm run dev
npm run build
npm run preview
```

### Optional One-Command Tasks

```bash
make data
make web
make qa
```

---

## 19) Suggested Data Contracts

## `crawl-report.json`

Tracks:
1. crawl start/end time
2. seed URLs
3. pages visited
4. assets discovered by type
5. failures/timeouts

## `graph.json`

Tracks:
1. schema version
2. node array
3. edge array
4. generation timestamp

## `search-index.json`

Tracks:
1. tokenized search documents
2. node ID references
3. optional ranking metadata

---

## 20) Failure Handling Strategy

1. If fetch fails: log and continue.
2. If parse fails for one page: keep partial extraction.
3. If normalization conflict: preserve both records and flag for review.
4. If graph validation fails: block release build.

---

## 21) MVP Acceptance Criteria

A build qualifies as MVP when all are true:

1. Titan root map loads with expandable hierarchy.
2. At least the major Titan collections are represented with counts.
3. Flyby nodes resolve and open linked artifacts.
4. Search finds flyby IDs and key references.
5. Source links are visible and clickable from details panel.
6. Static build deploys and runs without backend services.

---

## 22) Post-MVP Extensions

1. Add PDF title/abstract extraction for richer node summaries.
2. Add timeline visualization synchronized with graph selection.
3. Add "compare flybys" mode by artifact class.
4. Add citation export (BibTeX/JSON).
5. Add snapshot/version history of graph updates.

---

## 23) Implementation Notes for the Builder

1. Start with graph correctness, then polish visuals.
2. Keep crawler idempotent and cache-friendly.
3. Avoid tight coupling between parser and UI.
4. Use schema versioning from day one.
5. Preserve enough metadata for future scientific reuse.

---

## 24) Ready-to-Build Checklist

- [ ] Replit project initialized with frontend + Python scripts
- [ ] Titan seed URLs configured
- [ ] URL canonicalization rules implemented
- [ ] Flyby ID parser implemented and tested
- [ ] `graph.json` generation working
- [ ] Mind map renders root + first-level Titan branches
- [ ] Branch expansion and details panel working
- [ ] Search and filters operational
- [ ] QA scripts passing
- [ ] Static deploy live

---

## 25) Final Delivery Statement

This blueprint is intentionally implementation-oriented.  
If followed as written, it will produce a deployable standalone Titan mind map site with a reproducible data pipeline suitable for iterative scientific expansion.

