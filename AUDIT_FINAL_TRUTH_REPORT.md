# ENVIRONMENTAL MONITORING — TRUTH AUDIT

**Audit Date**: August 2026  
**Auditor**: Forensic Truth Audit Subsystem  
**Scope**: Codebase, data pipelines, model weights, satellite rasters, boundary geometries, backend API, and frontend user interface.

---

## Overall Verdict

**B. MOSTLY IMPLEMENTED BUT IMPORTANT GAPS EXIST**

> **Verdict Justification**: The engineering implementation, data pipelines, PyTorch 3D CNN architectures, FastAPI backend, and React/MapLibre frontend are **genuinely implemented, mathematically reproducible, and leakage-safe**. All 135 GeoTIFFs, 10,752 temporal tensors, and 157 prioritized hotspots contain real, non-fabricated data. However, **important scientific gaps and limitations exist**: the training labels and candidate definitions are 100% rule-derived spectral anomaly heuristics rather than ground-truth field surveys, Feature 10 satellite validation is partially circular, and the satellite imagery map mode (Feature 12-C.4) is not yet integrated into the frontend.

---

## What Is Definitely Real

1. **Project Boundaries & Government Clearances**:
   - Original Stage-I and Stage-II forest clearance orders, DGPS maps, and boundary KMLs in `data/raw/` are authentic government files.
   - Processed GeoJSON boundaries for MH-001 (862.26 ha), MH-002 (938.81 ha), and MH-003 (117.02 ha) match the official clearance hectare limits.
2. **Sentinel-2 & Dynamic World Satellite Data**:
   - All 18 multiband GeoTIFFs (6 bands, 10m resolution, 2021–2026) and 18 Dynamic World rasters contain genuine Copernicus surface reflectance and classified land cover.
   - Zero constant, placeholder, or synthetic mock arrays exist in the 135 GeoTIFF files.
3. **Temporal Dataset & Tensors**:
   - 10,752 complete 5-year temporal sequences in `temporal_patches_{train,val,test}.npz` and `temporal_delta_{train,val,test}.npz` are real extracted arrays.
   - Spatial and temporal train/test splits are strictly disjoint ($Train \cap Test = \emptyset$).
4. **PyTorch Model Weights**:
   - Trained 3D CNN model checkpoints (`temporal_cnn_delta.pth`, LOPO checkpoints) exist.
   - Independent forward pass recomputation on the test split ($N=1,226$) produced **PR-AUC = 0.379072, F1 = 0.323164, Accuracy = 0.511419**, matching reported metrics to 6 decimal places.
5. **Prioritized Hotspot Catalog**:
   - 157 spatial hotspots clustered via DBSCAN from 10,004 candidate patches.
   - Stratified priority breakdown: 8 High, 15 Medium, 46 Low, 88 Unsupported across Gondkhari (73), Gadchiroli (28), and Bhivpuri (56).

---

## What Is Definitely Implemented

1. **Data Preprocessing & Feature Engineering**: Full Python pipeline in `src/` computing NDWI, NDBI, NDVI deltas, and multi-spectral anomaly grids.
2. **PyTorch 3D CNN Model Suite**: Delta Temporal CNN, Raw Temporal CNN, and Spatial Control models with training, validation, and LOPO cross-validation routines.
3. **Pilot Inference & DBSCAN Clustering**: Batch inference on 10,752 sequences generating candidate GeoJSON points and clusters.
4. **Read-Only FastAPI Projection Backend**: `dashboard/backend/` passes all 13 automated unit tests and serves typed REST endpoints with SHA-256 integrity verification.
5. **React + MapLibre Dashboard**: `dashboard/frontend/` builds cleanly (`tsc` 0 errors, Vite bundle PASS) and renders real project polygons and hotspot markers on OpenStreetMap.

---

## What Is Only Partially Implemented

1. **Satellite Raster Display**: GeoTIFF rasters exist on disk in `data/processed/satellite/`, but there is currently no tile server or raster rendering pipeline connected to the browser.
2. **Independent Validation**: Feature 10 provides multi-source proxy indicators (NDVI slope and Dynamic World transitions), but these are supporting proxy signals rather than independent ground-truth verification.

---

## What Is Not Implemented

1. **Feature 12-C.4 (Real Satellite Imagery Map Layer)**:
   - The frontend currently renders only Carto Light (OSM raster tiles).
   - The `[ Map ] [ Satellite ]` toggle switch and satellite tile source are not yet implemented.
2. **Live Backend Inference**:
   - The dashboard does not run real-time ML inference on arbitrary uploaded rasters; it projects frozen Feature 11 pilot inference outputs.

---

## What Is Hard-Coded

1. **Project Name Lookup in Backend**:
   - `dashboard/backend/app/data.py` (L37): `name_map = {"MH-001": "Gondkhari", "MH-002": "Gadchiroli", "MH-003": "Bhivpuri PSP"}` maps IDs to names because the summary CSV lacked a project name column.
2. **Initial Map Camera Center**:
   - `dashboard/frontend/src/components/MapView.tsx` (L79): `center: [73.5, 19.5]` sets the initial view box before dynamic bounds fitting.
3. **No Hardcoded Scientific Data**:
   - Hotspot counts, priority levels, coordinates, and evidence metrics are **dynamically aggregated from authoritative CSV/GeoJSON files**.

---

## What Is Derived From Proxy Labels

- **All Training Targets ($y$)**:
  - The binary labels $y \in \{0, 1\}$ are derived from heuristic threshold rules (e.g., $\Delta \text{NDVI} \le p_{05}$ and $\Delta \text{NDBI} \ge p_{95}$).
  - The CNN model is an automated statistical surrogate for multi-spectral change heuristics, **not** a confirmed deforestation detector trained on ground-truth field data.

---

## What Cannot Currently Be Verified

1. **Real-World Environmental Accuracy**:
   - Without ground-truth physical field audits or drone surveys conducted across the 157 hotspot locations in Maharashtra, the actual real-world true-positive rate cannot be objectively verified.
2. **Temporal Behavior in 2026**:
   - 2026 satellite imagery exists in partial form but has not undergone full non-monsoon annual temporal delta modeling.

---

## Scientific Weaknesses

1. **Surrogate Proxy Ground Truth**: Training models on heuristic percentile cutoffs risks reinforcing spectral artifacts (e.g., agricultural harvesting or seasonal moisture variations).
2. **Partial Circularity in Validation**: Using NDVI changes to validate candidates originally flagged by NDVI/NDBI anomaly thresholds.
3. **Uncalibrated Probabilities**: Median prediction probability is 0.1746 with a high concentration of samples above threshold 0.10; scores must be treated as relative ranking indicators rather than true probabilities.
4. **Geographic Scope**: Models were trained and evaluated on only 3 projects in Maharashtra.

---

## Engineering Bugs & Cleanliness Findings

1. **Empty Metrics CSVs**: 4 placeholder CSV files in `data/processed/modeling/temporal_spatial_cnn/` (`temporal_cnn_error_analysis.csv`, etc.) have 2-byte sizes (empty headers), though authoritative metrics exist in sibling files.
2. **Report Documentation Discrepancy**: A minor wording discrepancy exists in `feature10_1_calibration_report.md` regarding probability concentration phrasing vs actual numeric percentiles in the CSV.

---

## Dashboard & Map Problems

- **No Satellite Layer Switcher**: The map only displays OSM street/light tiles. Investigators cannot visually cross-reference hotspot points against true satellite imagery in the UI.

---

## Reproducibility Evaluation

- **Code & Test Reproducibility**: **HIGH (PASS)**.
  - Python scripts and tests execute with standard dependencies (`torch`, `fastapi`, `geopandas`, `rasterio`).
  - Frontend builds cleanly with zero TypeScript errors via `npm run build`.
  - Checksum manifests match across all frozen directories.

---

## Ranked Issues & Remediation Priorities

| Priority | Area | Issue Description | Recommended Remediation |
| :--- | :--- | :--- | :--- |
| **CRITICAL** | Scientific Claims | Potential for misunderstanding surrogate proxy labels as legal violations. | Maintain permanent disclaimers in UI and documentation stating system provides candidate ranking signals, not compliance determinations. |
| **HIGH** | Frontend / Map | Feature 12-C.4 Satellite Basemap Layer is not implemented. | Implement satellite basemap toggle (`[ Map ] [ Satellite ]`) in `MapView.tsx` using a legitimate XYZ satellite tile provider. |
| **MEDIUM** | Model Calibration | Raw sigmoid output is uncalibrated across pilot population. | Continue using relative ranking percentiles rather than interpreting raw floats as true physical probabilities. |
| **LOW** | Code Cleanliness | 4 empty CSV placeholders in `temporal_spatial_cnn/`. | Keep frozen for checksum stability, but document in repository notes. |
