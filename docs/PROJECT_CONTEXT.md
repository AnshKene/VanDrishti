# Environmental Monitoring — Authoritative Project Context & Memory

> **IMPORTANT**: This document is the persistent, authoritative project memory for the Environmental Monitoring system.
> Future AI sessions, agents, and contributors must consult this document and [`AGENTS.md`](file:///c:/Users/anshk/Desktop/Environmental-Monitoring/AGENTS.md) before performing any work.
> If the current repository state conflicts with assumptions or chat history, authoritative files and verified artifacts in the repository take precedence.

---

## 1. Project Identity & Objective

- **System Name**: Environmental Monitoring — AI-Assisted Environmental Project Monitoring and Decision-Support System.
- **Core Objective**: Monitor environmentally approved project areas using satellite-derived spatial and temporal information to identify locations that warrant further investigation by human environmental analysts.
- **Scope & Claim Boundaries**:
  - The system does **NOT** automatically determine illegal activity, unauthorized land use, causality, intent, or environmental non-compliance.
  - CNN outputs serve as candidate detection and relative ranking signals.
  - Spectral vegetation indices (e.g., NDVI) and land cover transition datasets (e.g., Dynamic World) provide supporting proxy evidence, **not** ground truth.
  - The dashboard operates as a read-only decision-support interface.

---

## 2. Completed Pipeline & Feature History

### Features 1–3: Data Ingestion & Boundary Preparation
- Acquired and prepared geographic project boundaries (GeoJSON / shapefiles) and baseline satellite data.
- Established consistent coordinate reference systems (CRS) and spatial bounding boxes.

### Feature 6: Training Dataset Preparation
- Preprocessed multispectral satellite rasters and generated standardized patches.
- Formatted spatial and temporal training tensors with associated split metadata.

### Feature 7: Change Detection & Candidate Generation
- Developed spatial anomaly screening and candidate proposal pipeline across monitored projects.

### Feature 8: Machine Learning & CNN Experimentation Suite
- **Classical & Spatial CNN**: Evaluated classical ML (XGBoost controls) against spatial 2D CNNs.
- **Robustness & Benchmarking**: Conducted controlled benchmark audits across diverse spatial patches.
- **Feature 8.6 (Leave-One-Project-Out Spatial CNN)**:
  - Validated spatial CNN generalization by holding out each project in turn.
  - Spatial CNN outperformed XGBoost baseline across all three held-out project sites.
- **Feature 8.6.1 (Population Discrepancy Audit)**:
  - Audited evaluation populations across cross-validation runs.
  - Confirmed **no data leakage**; discrepancies explained as evaluation-design differences.
- **Feature 8.7-A (Temporal Dataset Engineering)**:
  - Engineered 10,752 complete 5-year temporal sequences spanning 2021–2025.
  - Tensor shapes: Full temporal `(5, 15, 15, 6)`, Temporal Delta `(4, 15, 15, 6)`.
  - Excluded 2026 due to partial year coverage.
  - Enforced strict train-only normalization.
  - Audited test population: 579 incomplete temporal centers excluded from relevant evaluation test sets.
- **Feature 8.7-B (Temporal Architecture Evaluation & Selection)**:
  - Evaluated Raw Temporal CNN, Delta Temporal CNN, and Spatial-only control.
  - **Selected Model**: **Delta Temporal CNN** (strongest temporal representation).
  - Key Metrics:
    - Delta Temporal CNN PR-AUC: `0.3791`
    - Spatial-only Control PR-AUC: `0.2429`
    - Bootstrap PR-AUC Difference 95% CI: `[0.0185, 0.2798]` (statistically supported temporal delta advantage).
- **Feature 8.7.1 (Temporal Integrity Audit)**:
  - Temporal integrity and statistical audit completed: **PASS**.
- **Feature 8.7.2 (Population Reconciliation)**:
  - Reconciled frozen temporal test population to exact **1,226** sequences (**PASS**).
  - Note: 1,602 was an initial pre-execution design estimate, not a frozen dataset artifact.
- **Feature 8.7-C (Leave-One-Project-Out Temporal CNN)**:
  - Evaluated Delta Temporal CNN across held-out projects.
  - Delta CNN beat XGBoost on all 3 held-out projects.
  - Delta CNN beat Spatial CNN on 2 out of 3 projects (confirming temporal advantage is strong, though not universally superior in all spatial configurations).
- **Feature 8.7-D (Temporal Chain Leakage Audit)**:
  - Complete chain integrity audit completed: **PASS**.
  - Verified no train/test contamination, no normalization leakage, and no threshold leakage.
- **Feature 8.8 (Final Model Selection & Research Readiness)**:
  - Formally selected **Delta Temporal CNN** (from Feature 8.7-B).
  - Model status: **READY FOR LIMITED RESEARCH / PILOT INFERENCE**.

---

### Feature 9: Pilot Inference Pipeline
- Executed pilot inference using the selected Delta Temporal CNN.
- **Target Population**: 10,752 complete 5-year temporal sequences.
- **Operational Threshold**: `0.10`.
- **Outputs**:
  - 10,004 candidate patches.
  - 157 clustered spatial hotspots.
  - Prediction arrays and GeoJSON spatial feature collections generated and stored.

---

### Feature 10: Candidate Validation & Hotspot Quality Assessment
- Independent multi-source validation conducted on the 157 candidate hotspots:
  - **157 Total Hotspots**: 69 independently supported, 88 weak/unsupported, 0 insufficient data.
- **Evidence Streams**: Multi-temporal NDVI trajectories and Dynamic World land cover categorical transitions.
- **Interpretation Rule**: Proxy evidence provides supporting context for review, not definitive ground truth.

---

### Feature 10.1: Calibration & Threshold Diagnostic
- Diagnostic evaluation revealed substantial output distribution shifting on the pilot population:
  - **Median predicted probability**: `0.8521`.
  - **Operational Rule**: Treat CNN outputs as a ranking/confidence signal, not a calibrated real-world probability.
  - **Official Operational Threshold**: Maintained at **`0.10`**. Do not adjust the operational threshold based solely on downstream diagnostic fit.

---

### Feature 11: Candidate Prioritization & Investigator Queue
- Authoritative priority stratification of the 157 hotspots:
  - **HIGH Priority**: 8 hotspots
  - **MEDIUM Priority**: 15 hotspots
  - **LOW Priority**: 46 hotspots
  - **UNSUPPORTED**: 88 hotspots
  - **Total**: 157 hotspots (69 Supported, 88 Unsupported)
- **Authoritative Project Distribution**:
  - **MH-001 (Gondkhari)**: 73 hotspots
  - **MH-002 (Gadchiroli)**: 28 hotspots
  - **MH-003 (Bhivpuri PSP)**: 56 hotspots
  - *(Warning: Do not alter these authoritative totals with deprecated or partial counts such as 18/70/69).*

---

### Features 12-A to 12-C.2: Dashboard Architecture & Implementation
- **Feature 12-A (System Architecture)**:
  ```
  [ Immutable ML & Spatial Layer ] (Features 8–11 Artifacts)
                 ↓
  [ Read-Only FastAPI Projection Backend ] (dashboard/backend/)
                 ↓
  [ React + TypeScript + MapLibre Frontend ] (dashboard/frontend/)
  ```
  - Direct read-only filesystem projection; no database required.
- **Feature 12-B (FastAPI Backend)**:
  - Implemented in `dashboard/backend/`.
  - Endpoints: `/api/health`, `/api/dashboard/overview`, `/api/projects`, `/api/projects/{id}`, `/api/hotspots`, `/api/hotspots/{id}`, `/api/hotspots/{id}/evidence`, `/api/hotspots/{id}/provenance`, `/api/maps/hotspots`, `/api/maps/projects`.
  - Automated tests: 13/13 **PASS**. Read-only invariants enforced.
- **Feature 12-C (React + MapLibre Frontend)**:
  - Implemented in `dashboard/frontend/` with routing for Overview (`/dashboard`), Project Directory (`/projects`), Project Detail (`/projects/:id`), Hotspot Queue (`/hotspots`), and Hotspot Detail (`/hotspots/:id`).
  - No client-side ML inference; purely renders backend projections.
- **Feature 12-C.1 (Build & Tooling Stabilization)**:
  - Resolved Vite/Rolldown bundler incompatibilities by standardizing on Vite `5.4.10`.
  - TypeScript build, production bundle (`npm run build`), and browser runtime: **PASS**.
- **Feature 12-C.2 (Map Projection & CRS Alignment)**:
  - Fixed blank map display root cause: corrected CRS handling, boundary geometry parsing, and MapLibre source configuration.
  - Real OpenStreetMap (OSM) basemap rendering verified.
  - Project boundary polygons and hotspot point/polygon layers render with correct geographical coordinates.
  ### Feature 12-C.4: Real Year-Wise Satellite Imagery Map Layer
- **Status**: **PASS (Completed)**
- **Implementation**:
  - Direct read-only FastAPI projection of authentic Sentinel-2 L2A seasonal composite GeoTIFFs (`data/processed/satellite/`) for years 2021, 2022, 2023, 2024, 2025, and 2026 (reference year).
  - True-color band mapping: Red (B4), Green (B3), Blue (B2) with nodata alpha masking and linear reflectance scaling.
  - Endpoints: `GET /api/satellite/years`, `GET /api/satellite/{project_id}/{year}/metadata`, `GET /api/satellite/{project_id}/{year}/image.png`.
  - Frontend: MapLibre `image` source integration with `[ Map (OSM) ] [ Satellite ] [ Hybrid ]` mode toggles and observation year buttons `[2021] [2022] [2023] [2024] [2025] [2026 (Ref)]`.
  - Hotspot overlays, priority color-coding, and popups fully preserved.
  - Tests: 17/17 pytest PASS, 0 TypeScript errors, Vite build PASS, SHA-256 integrity verified.

---

## 3. Current Dashboard State & Capabilities

The dashboard application is fully functional and running against authoritative backend data:
- **Overview Dashboard**: Metrics overview, hotspot distribution by priority and project, recent alerts.
- **Project Directory & Detail**: Real project boundaries, project-level hotspot counts, metadata, and year-wise satellite imagery.
- **Investigator Queue & Hotspot Detail**: Filterable by priority, project, and validation status; shows multi-temporal NDVI/Dynamic World evidence, model provenance, and spatial context on MapLibre.
- **Maps**: Real OSM tiles, real year-wise Sentinel-2 satellite imagery, hybrid overlay mode, verified project boundaries, and real hotspot coordinates.

---

## 4. Current Status

Feature 12-C.4 is complete. All planned dashboard core features are implemented and verified.


---

## 5. Satellite & Geospatial Data Findings

### Local Satellite GeoTIFF Repository
- Initial inspection identified real local GeoTIFF files with:
  - 6 multispectral bands
  - CRS: `EPSG:4326`
  - Valid geographic bounds and calibrated reflectance values
- **Prerequisite for Sentinel-2 Raster Integration**:
  Before implementing an interactive raster viewer for local Sentinel-2 scenes:
  1. Inventory all local GeoTIFF rasters in `data/`.
  2. Map file paths to project IDs (`MH-001`, `MH-002`, `MH-003`).
  3. Catalog covered acquisition years (2021–2025).
  4. Verify band configurations, scaling, and CRS consistency.
  5. Check spatial coverage against project boundary polygons.
  6. Design an efficient, read-only projection mechanism (e.g., dynamic tile server or thumbnail generation) without mutating source rasters.
  7. **Never fabricate missing bands, timestamps, or imagery years.**

### Google Earth Imagery Guidelines
- Google Earth Historical Imagery can serve as an external visual cross-check during manual investigator reviews.
- **Prohibited Uses**:
  - Must **NOT** be incorporated into CNN training datasets.
  - Must **NOT** be labeled as Sentinel-2 evidence or ground truth.
  - Do not scrape or construct automated pipelines relying on undocumented Google Earth endpoints.

---

## 6. Scientific Status & Known Limitations

- **Current Status**: **Research Prototype / Validated Pilot Decision-Support System**.
- **Validated Strengths**:
  - Internal experimental consistency and reproducible data preparation.
  - Leakage-safe model evaluation (leave-one-project-out cross-validation).
  - Demonstrable cross-project anomaly ranking ability.
  - Statistically validated temporal delta advantage over purely spatial representations.
  - Multi-source independent proxy evidence correlation.
- **Limitations & Remaining Gaps**:
  - Evaluated on only 3 project areas in Maharashtra (limited geographic diversity).
  - Labels derived from proxy change heuristics, not systematic ground-truth field surveys.
  - 579 incomplete temporal centers excluded from temporal evaluation.
  - Model output probabilities are uncalibrated (median `0.8521`); must be used as relative ranking scores.
  - No formal full-year 2026 operational evaluation.

---

## 7. Immutability & Safe Change Protocol

1. **Frozen Artifacts**: Features 8–11 are frozen. Any modification to `data/`, model checkpoints, or frozen candidate outputs requires explicit authorization.
2. **Pre-Change Verification**: Check whether proposed changes touch frozen datasets.
3. **Isolated Projection**: Keep backend and frontend decoupled from ML training code.
4. **Checksum & Test Validation**: Run test suites (`pytest`, `npm test`, `npm run build`) before declaring changes complete.

---

## 8. Protocol for Future AI Sessions

When continuing work in this repository:
1. Review [`AGENTS.md`](file:///c:/Users/anshk/Desktop/Environmental-Monitoring/AGENTS.md) for immutable rules and engineering constraints.
2. Read this document ([`docs/PROJECT_CONTEXT.md`](file:///c:/Users/anshk/Desktop/Environmental-Monitoring/docs/PROJECT_CONTEXT.md)) to understand the exact pipeline state.
3. Verify the git working directory and file status.
4. Pick up directly at **FEATURE 12-C.4** (or subsequent documented next task).
5. Upon feature completion, append the newly completed feature details to Section 2 and advance Section 4.
