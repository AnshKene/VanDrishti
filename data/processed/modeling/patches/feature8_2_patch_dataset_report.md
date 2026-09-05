# Feature 8.2 — Spatial 15×15 Multi-Spectral Patch Dataset Preparation Report

### Final Status Decision: **FAIL — PATCH SPATIAL LEAKAGE DETECTED**

* **Audit Timestamp**: 2026-08-24T00:12:00+05:30
* **Feature**: Feature 8.2 — Spatial 15×15 Multi-Spectral Patch Dataset Preparation
* **Upstream Manifest Checksum Status**: **PASS (100% Uncorrupted & Immutable)**
* **CNN Model Training Status**: **NOT TRAINED (0 Models Trained)**

---

### 1. Patch Dataset Summary

* **Total Requested Center Pixels**: **`79,406`**
* **Successfully Extracted Patches ($15 \times 15 \times 6$)**: **`75,600`**
* **Rejected Samples (Border Pixels $< 7$ px from Raster Edge)**: **`3806`**
* **Patch Input Tensor Shape**: **`(15, 15, 6)`** (`float32`)
* **Spectral Bands Included**: `B2`, `B3`, `B4`, `B8`, `B11`, `B12` (Raw Reflectances Only)
* **Target Definition**: `Target = 1` (Category 2/3 candidates), `Target = 0` (Category 0/1 non-disturbance)

---

### 2. Spatial Patch Footprint Leakage Audit ($450\text{m} \times 450\text{m}$ Bounding Box Geometry)

| Project ID | Split Pair | Overlapping Footprint Pairs | Min Center Distance (m) | Min Edge Distance (m) | Leakage Status |
|---|---|---|---|---|---|
| `MH-001` | `train_vs_val` | **15306** | 391.91 m | 0.00 m | **FAIL_PATCH_OVERLAP_DETECTED** |
| `MH-001` | `train_vs_test` | **0** | N/A m | N/A m | **PASS_ZERO_OVERLAP** |
| `MH-001` | `val_vs_test` | **4855** | 391.94 m | 0.00 m | **FAIL_PATCH_OVERLAP_DETECTED** |
| `MH-002` | `train_vs_val` | **0** | N/A m | N/A m | **PASS_ZERO_OVERLAP** |
| `MH-002` | `train_vs_test` | **0** | N/A m | N/A m | **PASS_ZERO_OVERLAP** |
| `MH-002` | `val_vs_test` | **0** | N/A m | N/A m | **PASS_ZERO_OVERLAP** |
| `MH-003` | `train_vs_val` | **0** | N/A m | N/A m | **PASS_ZERO_OVERLAP** |
| `MH-003` | `train_vs_test` | **0** | N/A m | N/A m | **PASS_ZERO_OVERLAP** |
| `MH-003` | `val_vs_test` | **0** | N/A m | N/A m | **PASS_ZERO_OVERLAP** |

> **CRITICAL SPATIAL FOOTPRINT FINDING**:
> In project `MH-001 Gondkhari`, the 30m spatial block grid produced a minimum center-to-center distance of **`391.9m`** between train and validation center points. Because a $15 \times 15$ pixel patch has a $450\text{m} \times 450\text{m}$ footprint ($225\text{m}$ radius), two centers `391.9m` apart have overlapping outer footprint edges ($391.9\text{m} < 450.0\text{m}$). This generated **`20161`** overlapping bounding box footprint pairs between `train` and `val` in Gondkhari.

---

### 3. Class Distribution by Split & Project (`patch_class_distribution.csv`)

| Spatial Split | Project ID | Total Patches | Target 0 (Non-Disturbance) | Target 1 (Disturbance Candidate) | Imbalance Ratio |
|---|---|---|---|---|---|
| `train` | `MH-001` | **22,578** | 19,962 | 2,616 | 7.6:1 |
| `train` | `MH-002` | **34,439** | 30,234 | 4,205 | 7.2:1 |
| `train` | `MH-003` | **4,510** | 3,409 | 1,101 | 3.1:1 |
| `val` | `MH-001` | **5,381** | 4,949 | 432 | 11.5:1 |
| `val` | `MH-002` | **3,820** | 3,405 | 415 | 8.2:1 |
| `val` | `MH-003` | **53** | 53 | 0 | N/A |
| `test` | `MH-001` | **1,062** | 986 | 76 | 13.0:1 |
| `test` | `MH-002` | **3,192** | 2,878 | 314 | 9.2:1 |
| `test` | `MH-003` | **565** | 565 | 0 | N/A |

---

### 4. Comprehensive Dataset Audit Checklist Summary (17 / 17 Evaluated)

| Audit Check | Target Criterion | Measured Finding | Status |
|---|---|---|---|
| Patch Tensor Shape | (15, 15, 6) | (15, 15, 6) | **PASS** |
| Bands Included | B2, B3, B4, B8, B11, B12 Only | 6 Bands Only | **PASS** |
| Target Leakage into Tensor | Zero Target Features in Tensor | Raw Reflectances Only | **PASS** |
| Historical Year Scope | 2021-2025 Baseline Only | 2021-2025 Only (2026=0) | **PASS** |
| Monsoon Exclusion | June-October Excluded | June-October Excluded (0) | **PASS** |
| Patch Footprint Spatial Overlap | 0 Footprint Overlaps | 20161 Bounding Box Overlaps | **FAIL_PATCH_OVERLAP_DETECTED** |
| Temporal Split Consistency | 0 Coordinate Inconsistencies | 0 Inconsistencies | **PASS** |
| Normalization Preprocessing | Train Split Only | Train Split Only | **PASS** |
| CNN Training Count | 0 Models Trained | 0 Models Trained | **PASS** |

---

### 5. Final Status Decision

**Final Feature 8.2 Status**: **`FAIL — PATCH SPATIAL LEAKAGE DETECTED`**
