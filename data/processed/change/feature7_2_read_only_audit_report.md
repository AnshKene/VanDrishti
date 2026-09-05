# Feature 7.2 — Read-Only Audit & Bug Investigation Report

### Audit Status: **FAIL (Requires Targeted Summary Mapping Correction)**

* **Audit Timestamp**: 2026-08-23T23:39:45+05:30
* **Feature Audited**: Feature 7.2 — Historical Change Signal & Disturbance Candidate Detection
* **Upstream Protection**: **100% Read-Only & Immutability Verified**
* **CNN Model Training Status**: **NOT TRAINED**

---

### 1. Investigation of Single-Signal Anomaly Count = 0

* **Observed Symptom**: `disturbance_candidates.csv` reported `single_signal_anomaly_pixels = 0` across all three projects (`MH-001 Gondkhari`, `MH-002 Gadchiroli`, `MH-003 Bhivpuri PSP`).
* **Root Cause Discovered**:
  In `src/candidate_detection.py`, transition-level anomaly detection correctly identified single-signal anomaly pixels (`signal_count == 1`). For example, in `MH-001 Gondkhari` during the $2021ightarrow2022$ transition, **808 single-signal anomaly pixels** were detected.
  However, when aggregating into the project-wide multi-year summary grid `final_candidate_grid`:
  - `anomaly_count_grid` was only incremented for multi-spectral candidates (`candidate_grid >= 2`).
  - Single-signal anomaly pixels (`candidate_grid == 1`) were omitted from `anomaly_count_grid` tracking and were never assigned to `final_candidate_grid`.
  - As a result, `final_candidate_grid` only contained category values `0` (normal), `2` (single-transition multi-spectral candidate), and `3` (persistent multi-year candidate). Calling `(final_candidate_grid == 1).sum()` yielded **`0`** for all projects.

---

### 2. Comprehensive Checklist Audit (PASS / FAIL)

| Audit ID | Audit Parameter | Required Criterion | Empirical Finding | Status |
|---|---|---|---|---|
| **1** | **p05 / p95 Thresholds** | Empirical lower/upper tail percentiles | Lower 5th percentile ($p_{05}$) for $\Delta\text{NDVI}$ & $\Delta\text{NDWI}$, upper 95th percentile ($p_{95}$) for $\Delta\text{NDBI}$ evaluated across historical transitions. | **PASS** |
| **2** | **Single-Signal Detection** | Include single-signal anomaly pixels in summary | Transition-level detection works correctly, but multi-year summary grid omitted category 1, reporting 0 count. | **FAIL** |
| **3** | **Multi-Spectral $\ge 2$-Signal Logic** | Category 2 requires $\ge 2$ independent signals | Category 2 correctly requires $\ge 2$ independent spectral signals (`veg_signal + built_signal + water_signal >= 2`). | **PASS** |
| **4** | **$\ge 2$-Transition Persistence** | Category 3 requires $\ge 2$ historical transitions | Category 3 correctly requires multi-spectral candidates to occur across $\ge 2$ historical transitions (`anomaly_count_grid >= 2`). | **PASS** |
| **5** | **Polygon Masking** | Candidate pixels strictly inside GeoJSON polygon | Candidate pixels reprojected and polygon-masked to validated GeoJSON project boundaries. | **PASS** |
| **6** | **UTM Area Calculations** | Projected metric area calculation | Metric area calculated on projected UTM 30m grid ($0.09\text{ ha/pixel}$). | **PASS** |
| **7** | **Cluster Connectivity** | 8-neighbor spatial connected components | 8-neighbor spatial connected components grouping applied cleanly. Disconnected areas never merged. | **PASS** |
| **8** | **Temporal Scope** | Historical 2021–2025 only | Historical baseline transitions only ($2021\rightarrow2022, 2022\rightarrow2023, 2023\rightarrow2024, 2024\rightarrow2025$). $2026$ and monsoon months ($June–October$) strictly excluded. | **PASS** |
| **9** | **Immutability Check** | Feature 6 SHA-256 manifest & read-only data | Feature 6 SHA-256 checksum manifest verified **PASS**. Upstream directories (`data/raw/`, `data/processed/satellite/`, `data/processed/project_boundaries/`, `data/processed/vegetation/`, `data/processed/training/`) remain 100% untouched. | **PASS** |
| **10** | **NaN / Inf Safety** | Zero NaN/Inf leakage into statistics | `inf_count = 0` and `nan_count` cleanly masked. Zero NaN/Inf values leak into statistics. | **PASS** |

---

### 3. Recommendation for Subsequent Correction Task

1. Fix the multi-year grid aggregation logic in `src/candidate_detection.py` so that single-signal anomaly pixels (`candidate_grid == 1`) are tracked into `final_candidate_grid` as category `1`.
2. Re-run `src/candidate_detection.py` to regenerate Feature 7.2 output CSVs, candidate GeoTIFF rasters, and `feature7_2_candidate_detection_report.md`.
