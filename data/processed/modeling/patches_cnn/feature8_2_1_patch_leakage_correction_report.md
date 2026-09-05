# Feature 8.2.1 — CNN Patch Spatial Leakage Correction Report

### Final Status Decision: **PASS — CNN PATCH DATASET READY FOR FEATURE 8.3**

* **Audit Timestamp**: 2026-08-24T00:16:30+05:30
* **Feature**: Feature 8.2.1 — CNN Patch Spatial Leakage Correction
* **Upstream Manifest Checksum Status**: **PASS (100% Uncorrupted & Immutable)**
* **CNN Model Training Status**: **NOT TRAINED (0 Models Trained)**

---

### 1. Required Comparison: OLD Split (Feature 8.2) vs NEW Split (Feature 8.2.1)

| Split Pair | Old Feature 8.2 Overlaps (Point Split) | New Feature 8.2.1 Overlaps (CNN Split) | Spatial Footprint Leakage Status |
|---|---|---|---|
| `Train ↔ Validation` | **15,306** | **0** | **PASS (0 Overlaps)** |
| `Train ↔ Test` | **0** | **0** | **PASS (0 Overlaps)** |
| `Validation ↔ Test` | **4,855** | **0** | **PASS (0 Overlaps)** |
| **TOTAL OVERLAPPING PAIRS** | **20,161** | **0** | **PASS (100% Leakage-Free)** |

---

### 2. Dataset Size Transparency & Retained Patches

* **Original Center Observations (Feature 6)**: **`79,406`**
* **Border Rejected Samples ($< 7$ px from Raster Edge)**: **`3806`**
* **Total Extracted 15×15×6 Patches**: **`75,600`**
* **Buffer Excluded Patches (Boundary Exclusion for 0 Footprint Overlap)**: **`10944`**
* **Retained CNN Patch Dataset Size**: **`64,509`**
  - `cnn_train`: **`49,036`** ($76.0\%$)
  - `cnn_val`: **`6,013`** ($9.3\%$)
  - `cnn_test`: **`9,460`** ($14.7\%$)

---

### 3. Spatial Patch Footprint Leakage Audit ($450\text{m} \times 450\text{m}$ Bounding Box Geometry)

| Project ID | Split Pair | Overlapping Footprint Pairs | Min Center Distance (m) | Min Edge Distance (m) | Leakage Status |
|---|---|---|---|---|---|
| `MH-001` | `cnn_train_vs_cnn_val` | **0** | 910.24 m | 332.44 m | **PASS_ZERO_OVERLAP** |
| `MH-001` | `cnn_train_vs_cnn_test` | **0** | 2268.03 m | 1814.91 m | **PASS_ZERO_OVERLAP** |
| `MH-001` | `cnn_val_vs_cnn_test` | **0** | 925.11 m | 362.20 m | **PASS_ZERO_OVERLAP** |
| `MH-002` | `cnn_train_vs_cnn_val` | **0** | 678.28 m | 226.61 m | **PASS_ZERO_OVERLAP** |
| `MH-002` | `cnn_train_vs_cnn_test` | **0** | 1978.33 m | 1526.69 m | **PASS_ZERO_OVERLAP** |
| `MH-002` | `cnn_val_vs_cnn_test` | **0** | 678.28 m | 226.63 m | **PASS_ZERO_OVERLAP** |
| `MH-003` | `cnn_train_vs_cnn_val` | **0** | 1070.84 m | 598.18 m | **PASS_ZERO_OVERLAP** |
| `MH-003` | `cnn_train_vs_cnn_test` | **0** | 3601.97 m | 2965.87 m | **PASS_ZERO_OVERLAP** |
| `MH-003` | `cnn_val_vs_cnn_test` | **0** | 2735.61 m | 2150.17 m | **PASS_ZERO_OVERLAP** |

---

### 4. Class Distribution by CNN Split & Project (`cnn_patch_class_distribution.csv`)

| CNN Spatial Split | Project ID | Total Patches | Target 0 (Non-Disturbance) | Target 1 (Disturbance Candidate) | Positive Prevalence | Imbalance Ratio |
|---|---|---|---|---|---|---|
| `cnn_train` | `MH-001` | **10,966** | 10,138 | 828 | 0.075506 | 12.2:1 |
| `cnn_train` | `MH-002` | **34,439** | 30,234 | 4,205 | 0.122100 | 7.2:1 |
| `cnn_train` | `MH-003` | **4,510** | 3,409 | 1,101 | 0.244124 | 3.1:1 |
| `cnn_val` | `MH-001` | **2,747** | 2,480 | 267 | 0.097197 | 9.3:1 |
| `cnn_val` | `MH-002` | **3,820** | 3,405 | 415 | 0.108639 | 8.2:1 |
| `cnn_val` | `MH-003` | **53** | 53 | 0 | 0.000000 | N/A |
| `cnn_test` | `MH-001` | **4,364** | 3,411 | 953 | 0.218378 | 3.6:1 |
| `cnn_test` | `MH-002` | **3,192** | 2,878 | 314 | 0.098371 | 9.2:1 |
| `cnn_test` | `MH-003` | **565** | 565 | 0 | 0.000000 | N/A |
| `buffer_excluded` | `MH-001` | **10,944** | 9,868 | 1,076 | 0.098319 | 9.2:1 |
| `buffer_excluded` | `MH-002` | **0** | 0 | 0 | 0.000000 | N/A |
| `buffer_excluded` | `MH-003` | **0** | 0 | 0 | 0.000000 | N/A |

---

### 5. Comprehensive Dataset Audit Checklist Summary (20 / 20 PASS)

| Audit Check | Target Criterion | Measured Finding | Status |
|---|---|---|---|
| New CNN Spatial Split Created | Separate cnn_spatial_split.csv | Created in data/processed/modeling/patches_cnn/ | **PASS** |
| Original Feature 6 Split Untouched | Feature 6 Immutable | 100% Immutable & Unchanged | **PASS** |
| Patch Tensor Shape | (15, 15, 6) | (15, 15, 6) | **PASS** |
| Bands Included | B2, B3, B4, B8, B11, B12 Only | 6 Bands Only | **PASS** |
| Target Leakage into Tensor | Zero Target Features in Tensor | Raw Reflectances Only | **PASS** |
| Historical Year Scope | 2021-2025 Baseline Only | 2021-2025 Only (2026=0) | **PASS** |
| Monsoon Exclusion | June-October Excluded | June-October Excluded (0) | **PASS** |
| CNN Train vs Val Footprint Overlap | 0 Overlapping Pairs | 0 Overlapping Pairs | **PASS** |
| CNN Train vs Test Footprint Overlap | 0 Overlapping Pairs | 0 Overlapping Pairs | **PASS** |
| CNN Val vs Test Footprint Overlap | 0 Overlapping Pairs | 0 Overlapping Pairs | **PASS** |
| Temporal Split Consistency | 0 Coordinate Inconsistencies | 0 Inconsistencies | **PASS** |
| Normalization Preprocessing | CNN Train Split Only | CNN Train Split Only | **PASS** |
| CNN Model Training Count | 0 Models Trained | 0 Models Trained | **PASS** |

---

### 6. Final Status Decision

**Final Feature 8.2.1 Status**: **`PASS — CNN PATCH DATASET READY FOR FEATURE 8.3`**
