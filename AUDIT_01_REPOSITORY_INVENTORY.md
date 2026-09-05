# AUDIT 01: Complete Repository Inventory

**Audit Date**: August 2026  
**Auditor**: Forensic Truth Audit Subsystem  
**Scope**: Full repository structure, file classifications, byte sizes, usage status, authoritativeness, and anomaly detection.

---

## 1. Executive Summary of File Inventory

- **Total Non-Git/Non-NodeModules Files**: 672 files
- **Total Repository Data Volume**: ~205 MB (excluding `node_modules` and `.git`)
- **Key File Formats**:
  - **CSV (`.csv`)**: 248 files (49.96 MB) — Metrics, audits, predictions, sample metadata, manifests.
  - **GeoTIFF (`.tif`)**: 135 files (15.77 MB) — Satellite rasters, vegetation indices, candidate grids.
  - **KML (`.kml`)**: 59 files (4.08 MB) — Raw government/clearance boundary and cadastral maps.
  - **PDF (`.pdf`)**: 47 files (137.56 MB) — Original environmental clearance Stage I/II orders, DGPS maps, site inspection reports.
  - **Markdown (`.md`)**: 48 files (212 KB) — System documentation, feature reports, audit certificates.
  - **Python (`.py`)**: 26 files (364 KB) — Core data processing pipelines, audit routines, FastAPI backend.
  - **JSON (`.json`)**: 24 files (109 KB) — Normalization metadata, architectures, priority rules, configs.
  - **NPZ (`.npz`)**: 12 files (107.34 MB) — Compressed NumPy spatial/temporal multidimensional training tensors.
  - **GeoJSON (`.geojson`)**: 8 files (6.39 MB) — Authoritative boundaries, candidate patch geometries, prioritized hotspot clusters.
  - **PyTorch Model Checkpoints (`.pth`)**: 7 files (959 KB) — Trained weights for Spatial, Raw Temporal, Delta Temporal, and LOPO CNN models.
  - **TypeScript/TSX (`.ts`, `.tsx`)**: 17 files (46.8 KB) — React dashboard, MapLibre map components, API client.
  - **CSS/HTML/Configs**: 10 files — Tailwind styles, PostCSS, Vite build configuration.

---

## 2. Directory Structure & Classification Table

| Path / Subdirectory | Primary File Types | Purpose | Actively Used? | Authoritative? | Generated or Source? | Suspicious / Duplicated? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `AGENTS.md` | Markdown | Permanent engineering rules & agent operating guidelines | Yes | Yes | Source | None |
| `README.md` | Markdown | Project overview & high-level documentation | Yes | Yes | Source | None |
| `data/raw/` | PDF, KML | Original Stage-I/II clearance orders, site inspection reports, official KML polygons for Gondkhari, Gadchiroli, Bhivpuri PSP | Yes (Source) | Yes (Primary Source) | Source (Government) | Clean; contains real clearance documents |
| `data/processed/project_boundaries/` | GeoJSON | Validated project boundary polygons in EPSG:4326 for MH-001, MH-002, MH-003 | Yes | Yes | Generated from KML | Clean; verified coordinates and areas |
| `data/processed/satellite/` | GeoTIFF, CSV | Multiband Sentinel-2 L2A rasters (2021–2026), Dynamic World annual mode classifications | Yes | Yes | Generated (GEE/Copernicus) | Clean; real multispectral reflectance |
| `data/processed/vegetation/ndvi/` | GeoTIFF | Annual NDVI vegetation rasters per project (2021–2026) | Yes | Yes | Generated | Clean; valid float NDVI values |
| `data/processed/change/` | GeoTIFF, CSV | Annual delta spectral rasters (NDVI, NDWI, NDBI) and candidate disturbance grids | Yes | Yes | Generated | Clean; proxy anomaly candidate grids |
| `data/processed/training/` | CSV, JSON | Training sample metadata, split assignments, feature distributions | Yes | Yes | Generated | Clean |
| `data/processed/modeling/baseline/` | CSV, JSON | Feature 8.1 Tabular ML (XGBoost) baseline models and evaluation metrics | Read-only | Yes (Frozen) | Generated | Clean |
| `data/processed/modeling/cnn_baseline/` | CSV, PNG, PTH | Feature 8.2 Spatial 2D CNN baseline weights and evaluation metrics | Read-only | Yes (Frozen) | Generated | Clean |
| `data/processed/modeling/cross_project_generalization/` | CSV, JSON, PTH | Feature 8.6 Leave-One-Project-Out spatial CNN evaluation artifacts | Read-only | Yes (Frozen) | Generated | Clean |
| `data/processed/modeling/temporal_spatial_cnn/` | NPZ, PTH, CSV, JSON | Feature 8.7-A/B/C/D temporal tensors, normalization metadata, Delta CNN weights (`temporal_cnn_delta.pth`), LOPO models, audit reports | Yes (Selected Model) | Yes (Frozen F8.7/F8.8) | Generated | Clean; verified checksums |
| `data/processed/modeling/pilot_inference/` | CSV, GeoJSON | Feature 9 inference outputs: 10,752 predictions, 10,004 candidate patches, 157 spatial hotspots | Yes | Yes (Frozen F9) | Generated | Clean; verified threshold logic |
| `data/processed/modeling/candidate_validation/` | CSV, GeoJSON, PNG | Feature 10 multi-source validation evidence (NDVI slopes, Dynamic World transitions) & Feature 10.1 calibration | Yes | Yes (Frozen F10) | Generated | Clean; proxy evidence documented |
| `data/processed/modeling/candidate_prioritization/` | CSV, JSON, GeoJSON | Feature 11 prioritized investigator queue (157 hotspots: 8 High, 15 Med, 46 Low, 88 Unsupported) | Yes (Production Input) | Yes (Frozen F11) | Generated | Clean; consumed directly by dashboard |
| `data/processed/modeling/dashboard/` | CSV | Feature 12-A source manifest and SHA-256 data contract definitions | Yes | Yes | Generated | Clean |
| `dashboard/backend/` | Python, Pytest | Read-only FastAPI projection backend (`app/main.py`, `data.py`, `integrity.py`, `schemas.py`, `tests/`) | Yes | Yes | Source | Clean; 13/13 unit tests pass |
| `dashboard/frontend/` | TSX, TS, CSS, Vite | React + TypeScript + MapLibre investigator dashboard (`src/pages/`, `src/components/`, `src/api.ts`) | Yes | Yes | Source | Clean; compiles with 0 TS errors |
| `docs/` | Markdown | Architecture Decision Records (ADRs), Data Contracts, API Specs, and `PROJECT_CONTEXT.md` | Yes | Yes | Source | Clean |
| `src/` | Python | Source pipeline code for data inventory, boundary validation, multispectral change, candidate detection, model audits | Yes | Yes | Source | Clean |
| `scratch/` | Python, CSV | Verification, auditing, and runner scripts executed across features | Reference/Audit | No | Generated/Scratch | Scratch scripts used for reproducibility |

---

## 3. Findings on Suspicious, Mock, or Hardcoded Content

1. **No Mock or Demo Data in Backend/Frontend**:
   - Zero occurrences of `mock`, `fake`, `demo`, or `dummy` data in production paths.
   - All 157 hotspots, 3 projects, and boundary polygons are dynamically loaded from `data/processed/`.
2. **Hardcoded Project Display Name Map**:
   - In `dashboard/backend/app/data.py` (line 37): `name_map = {"MH-001": "Gondkhari", "MH-002": "Gadchiroli", "MH-003": "Bhivpuri PSP"}` maps project IDs to human-readable names. This is purely cosmetic display metadata.
3. **Empty CSV Files**:
   - 4 CSV files in `data/processed/modeling/temporal_spatial_cnn/` (`temporal_cnn_error_analysis.csv`, `temporal_cnn_model_comparison.csv`, `temporal_cnn_temporal_metrics.csv`, `temporal_cnn_validation_metrics.csv`) are 2 bytes (empty headers/placeholders), while the authoritative metrics were stored in `temporal_cnn_test_metrics.csv`, `audit/feature8_7_1_metric_reconstruction.csv`, and `final_audit/feature8_7_d_metric_reconstruction.csv`.
4. **GeoTIFF Integrity**:
   - All 135 GeoTIFF files are valid rasters with legitimate geographic coordinate bounds and floating/integer pixel variance (0 constant files, 0 all-NaN files).
