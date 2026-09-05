# AUDIT 02: End-to-End Data Lineage & Pipeline Traceability

**Audit Date**: August 2026  
**Auditor**: Forensic Truth Audit Subsystem  
**Scope**: Complete traceability from raw government clearance documents to dashboard map visualization.

---

## 1. Concrete Pipeline Flow Diagram

```
[ RAW CLEARANCE KML / PDF ]
  │
  ├──> src/data_inventory.py, src/metadata_audit.py
  │      └──> data/processed/project_metadata.csv
  │
  └──> src/boundary_validation.py
         └──> data/processed/project_boundaries/*.geojson (MH-001, MH-002, MH-003)
                │
[ SATELLITE INGESTION (Sentinel-2 L2A & Dynamic World) ]
  │
  ├──> src/satellite_pipeline.py
  │      └──> data/processed/satellite/{MH-001,MH-002,MH-003}/*.tif (2021-2026, 6 bands)
  │
  ├──> src/ndvi_analysis.py, src/monsoon_audit.py
  │      └──> data/processed/vegetation/ndvi/{MH-001,MH-002,MH-003}/*.tif
  │
  └──> src/multispectral_change.py
         └──> data/processed/change/temporal/{MH-001,MH-002,MH-003}/delta_*_{ndvi,ndwi,ndbi}.tif
                │
[ CANDIDATE GENERATION & HEURISTIC LABELS ]
  │
  └──> src/candidate_detection.py
         ├──> data/processed/change/candidates/{MH-001,MH-002,MH-003}/persistent_candidate.tif
         └──> data/processed/training/training_samples.csv (10,752 spatial-temporal points)
                │
[ DATASET ENGINEERING (Feature 8.7-A) ]
  │
  └──> scratch/run_feature8_7_c_cross_project.py & audit scripts
         ├──> data/processed/modeling/temporal_spatial_cnn/temporal_patches_{train,val,test}.npz
         ├──> data/processed/modeling/temporal_spatial_cnn/temporal_delta_{train,val,test}.npz
         └──> data/processed/modeling/temporal_spatial_cnn/temporal_normalization_metadata.json
                │
[ MODEL TRAINING & AUDIT (Feature 8.7-B, 8.7-D, 8.8) ]
  │
  └──> 3D CNN (CompactTemporalCNN) trained on train_delta (N=8,534)
         ├──> Model Checkpoint: data/processed/modeling/temporal_spatial_cnn/model/temporal_cnn_delta.pth
         └──> Test Metrics: data/processed/modeling/temporal_spatial_cnn/temporal_cnn_test_metrics.csv
                │
[ PILOT INFERENCE (Feature 9) ]
  │
  └──> scratch/run_feature9_pilot_inference.py (Inference on all 10,752 sequences @ threshold 0.10)
         ├──> data/processed/modeling/pilot_inference/predictions/pilot_predictions.csv (10,752 rows)
         ├──> data/processed/modeling/pilot_inference/predictions/candidate_patches_10004.csv (10,004 patches)
         ├──> DBSCAN Spatial Clustering -> pilot_hotspots.csv (157 hotspots)
         └──> data/processed/modeling/pilot_inference/maps/hotspots.geojson (157 points)
                │
[ CANDIDATE VALIDATION & CALIBRATION (Feature 10 & 10.1) ]
  │
  └──> scratch/run_feature10_validation.py, run_feature10_1_calibration.py
         ├──> data/processed/modeling/candidate_validation/hotspot_evidence/validated_hotspots.csv (157 rows)
         └──> data/processed/modeling/candidate_validation/calibration/feature10_1_probability_distribution.csv
                │
[ EVIDENCE-BASED PRIORITIZATION (Feature 11) ]
  │
  └──> scratch/run_feature11_prioritization.py (Applies scoring formula & rules)
         ├──> data/processed/modeling/candidate_prioritization/feature11_hotspot_priority.csv (157 hotspots)
         ├──> data/processed/modeling/candidate_prioritization/feature11_project_summary.csv (3 projects)
         └──> data/processed/modeling/candidate_prioritization/maps/feature11_prioritized_hotspots.geojson
                │
[ READ-ONLY PROJECTION BACKEND (Feature 12-B) ]
  │
  └──> dashboard/backend/app/main.py, data.py, integrity.py
         ├──> Verifies SHA-256 Checksums on startup
         ├──> Serves /api/dashboard/overview, /api/projects, /api/hotspots, /api/maps/*
         └──> Returns real GeoJSON and priority metrics
                │
[ REACT + MAPLIBRE FRONTEND (Feature 12-C) ]
  │
  └──> dashboard/frontend/src/pages/Overview.tsx, Hotspots.tsx, HotspotDetail.tsx, MapView.tsx
         ├──> Fetches API endpoints
         └──> Renders OSM Map, Project Boundaries, Hotspot Markers with real coordinates
```

---

## 2. Step-by-Step Transition Audit

| Step | Input Artifact(s) | Responsible Code / Module | Output Artifact(s) | Verification / Reproducibility Status |
| :--- | :--- | :--- | :--- | :--- |
| **1. Boundary Acquisition** | `data/raw/*/{documents,kml}/*.kml` | `src/data_inventory.py`, `src/boundary_validation.py` | `data/processed/project_boundaries/{gondkhari,gadchiroli,bhivpuri}_boundary.geojson` | **Verified**: Areas match Stage-I/II clearance hectares. Geometries valid. |
| **2. Satellite Ingestion** | Sentinel-2 L2A API / Dynamic World GEE | `src/satellite_pipeline.py` | `data/processed/satellite/{MH-001,002,003}/*.tif` (6 bands, 2021-2026) | **Verified**: 18 multiband rasters exist with valid reflectance (0-4000). |
| **3. Spectral Deltas & Anomaly Rasters** | Satellite GeoTIFFs (2021-2025) | `src/multispectral_change.py`, `src/candidate_detection.py` | `data/processed/change/temporal/*`, `persistent_candidate.tif` | **Verified**: Percentile thresholds (p05 NDVI, p95 NDBI) computed deterministically. |
| **4. Heuristic Label Formulation** | `persistent_candidate.tif` + `training_samples.csv` | `src/disturbance_baseline.py` | Category 2/3 multi-spectral persistent anomalies mapped to $y=1$, else $y=0$ | **Verified**: Labels are 100% rule-derived spectral anomaly heuristics. |
| **5. Temporal Tensors** | Sample coordinates + multiband GeoTIFFs | `scratch/run_feature8_7_c_cross_project.py`, `src/lulc_dataset.py` | `temporal_patches_{train,val,test}.npz`, `temporal_delta_{train,val,test}.npz` | **Verified**: Exact shapes: Train (8534,4,15,15,6), Val (992,4,15,15,6), Test (1226,4,15,15,6). |
| **6. Model Training & Evaluation** | `temporal_delta_train.npz`, `temporal_delta_test.npz` | PyTorch 3D CNN training (`CompactTemporalCNN`) | `temporal_cnn_delta.pth`, `temporal_cnn_test_metrics.csv` | **Verified**: Independently loaded weights; recomputed PR-AUC=0.379072 (exact match). |
| **7. Pilot Inference** | `temporal_cnn_delta.pth` + all 10,752 temporal sequences | `scratch/run_feature9_pilot_inference.py` | `pilot_predictions.csv` (10,752 rows), `candidate_patches_10004.csv` (10,004 rows), `pilot_hotspots.csv` (157 rows) | **Verified**: Threshold 0.10 produces 10,004 patches and 157 DBSCAN clusters. |
| **8. Candidate Validation** | `pilot_hotspots.csv` + NDVI & Dynamic World rasters | `scratch/run_feature10_validation.py` | `validated_hotspots.csv` (157 rows: 69 supported, 88 unsupported) | **Verified**: Rules: Strong (32), Moderate (13), Weak (24), No Support (88). |
| **9. Prioritization Queue** | `validated_hotspots.csv` + priority scoring formula | `scratch/run_feature11_prioritization.py` | `feature11_hotspot_priority.csv`, `feature11_prioritized_hotspots.geojson` | **Verified**: 8 High, 15 Med, 46 Low, 88 Unsupported across MH-001 (73), MH-002 (28), MH-003 (56). |
| **10. Backend Serving** | Feature 11 CSV/GeoJSON + Boundary GeoJSON | `dashboard/backend/app/main.py`, `data.py` | REST API `/api/*` | **Verified**: 13/13 tests pass; reads directly from Feature 11 artifacts. |
| **11. Frontend Rendering** | Backend REST API | `dashboard/frontend/src/*` | Web UI with interactive MapLibre map | **Verified**: Typescript clean, bundle built, real coordinates plotted on OSM map. |

---

## 3. Downstream Consumption & Disconnection Audit

- **Are Feature 11 outputs consumed by the dashboard?**  
  **YES**. `dashboard/backend/app/data.py` reads `data/processed/modeling/candidate_prioritization/feature11_hotspot_priority.csv` and `feature11_prioritized_hotspots.geojson`.
- **Are raw GeoTIFF files currently rendered in the frontend?**  
  **NO**. As designed, satellite rasters exist in `data/processed/satellite/` but are not yet served as map tiles to the browser (Feature 12-C.4 is the planned task).
- **Are intermediate Feature 8 model weights connected to real-time inference in the dashboard?**  
  **NO (By Design)**. The dashboard operates as a read-only projection of precomputed Feature 9/10/11 artifacts; it does not execute live PyTorch forward passes during HTTP requests.
