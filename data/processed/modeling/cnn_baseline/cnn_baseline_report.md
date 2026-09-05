# Feature 8.3 — CNN Baseline Model Training, Evaluation & Leakage-Safe Experiment Report

### Final Status Decision: **FEATURE 8.3 — CNN BASELINE TRAINED & EVALUATED**
### Scientific Model Decision Outcome: **A) CNN IMPROVES GENERALIZATION**

* **Audit Timestamp**: 2026-08-24T00:27:00+05:30
* **Feature Audited**: Feature 8.3 — CNN Baseline Model Training, Evaluation & Leakage-Safe Experiment
* **Upstream Manifest Checksum Status**: **PASS (100% Uncorrupted & Immutable)**
* **Frozen Feature 8.2.2 Checksum Status**: **PASS (100% Uncorrupted & Immutable)**
* **CNN Models Trained**: **1 (Compact 2D Multispectral CNN Baseline)**

---

### 1. Primary Empirical Model Performance Comparison

| Model Architecture | Input Features | Val PR-AUC (AP) | Test PR-AUC (AP) | Val F1 | Test F1 | Test Balanced Acc | Decision |
|---|---|---|---|---|---|---|---|
| `Naive Majority Baseline` | None | **0.090948** | **0.064870** | 0.0000 | 0.0000 | 0.5000 | Baseline |
| `Logistic Regression` | Point Spectral (Set C) | **0.112031** | **0.065825** | 0.1445 | 0.1221 | 0.5191 | Tabular Best Val |
| `XGBoost Baseline` | Point Spectral (Set C) | **0.103384** | **0.073024** | 0.1548 | 0.1009 | 0.5092 | Tabular Best Test |
| `Compact 2D CNN (Feature 8.3)` | 15×15×6 Spatial Tensor | **0.241588** | **0.197685** | **0.1551** | **0.2834** | **0.5467** | **A) CNN IMPROVES GENERALIZATION** |


---

### 2. Scientific & Legal Safety Disclaimer

> **IMPORTANT SCIENTIFIC LIMITATION**:
> This 2D Multispectral CNN model learns spatial patterns associated with rule-derived historical disturbance-candidate labels (Feature 7.2 Category 2/3). It does **NOT** establish:
> - illegal activity or legal violations
> - environmental non-compliance
> - causality or intent
> - confirmed land-use change
> 
> High predicted disturbance-candidate probabilities indicate statistically unusual spatial multi-spectral reflectance signals requiring independent ground or regulatory verification.

---

### 3. Project-Wise Test Performance (`cnn_project_metrics.csv`)

| Project ID | Project Name | Test Samples | Positives | Prevalence | PR-AUC | F1-Score | Precision | Recall | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `MH-001` | Gondkhari | 4364 | 953 | 0.218378 | **0.3285** | **0.3951** | 0.2670 | 0.7597 | Calculated |
| `MH-002` | Gadchiroli | 3192 | 314 | 0.098371 | **0.0895** | **0.1737** | 0.0979 | 0.7707 | Calculated |
| `MH-003` | Bhivpuri PSP | 565 | 0 | 0.000000 | **PR-AUC is undefined/not estimable for this project because there are zero positive ground-truth samples.** | **0.0000** | 0.0000 | 0.0000 | Zero Positive Test Samples |

---

### 4. Comprehensive Experiment Checklist (24 / 24 PASS)

| Check ID | Criterion | Measured Finding | Status |
|---|---|---|---|
| **1** | Frozen Dataset Checksum Verification | 100% SHA-256 Match | **PASS** |
| **2** | Train Patches Used | 49,915 Patches | **PASS** |
| **3** | Validation Patches Used | 6,620 Patches | **PASS** |
| **4** | Test Patches Used | 8,121 Patches | **PASS** |
| **5** | Tensor Shape | `(15, 15, 6)` | **PASS** |
| **6** | Correct 6 Sentinel-2 Bands | B2, B3, B4, B8, B11, B12 | **PASS** |
| **7** | Reflectance Scaling Verified | Scaled Reflectance Verified | **PASS** |
| **8** | No Double Normalization | Single Standardized Pipeline | **PASS** |
| **9** | Normalization from Train Only | Fitted Strictly on `cnn_train` | **PASS** |
| **10** | Class Weighting from Train Only | `pos_weight` $= 7.1374$ | **PASS** |
| **11** | No Oversampling / SMOTE | Strict Immutability | **PASS** |
| **12** | No Synthetic Samples | 0 Synthetic Samples | **PASS** |
| **13** | No Target Leakage into Tensor | Raw Reflectances Only | **PASS** |
| **14** | Zero Spatial Footprint Leakage | 0 Overlapping Footprint Pairs | **PASS** |
| **15** | Zero Temporal Coordinate Leakage | 0 Temporal Split Inconsistencies | **PASS** |
| **16** | Threshold Selection on Val Only | Selected Threshold $= 0.10$ | **PASS** |
| **17** | Test Evaluated Exactly Once | Evaluated Once with Frozen Threshold | **PASS** |
| **18** | Project-Wise Metrics Generated | Exported to CSV | **PASS** |
| **19** | Temporal Metrics Generated | Exported to CSV | **PASS** |
| **20** | Confusion Matrices Generated | Exported to CSV & PNG | **PASS** |
| **21** | Training History Exported | CSV & PNG Plots Generated | **PASS** |
| **22** | Model Saved Reproducibly | Saved `cnn_baseline.pth` & Architecture JSON | **PASS** |
| **23** | Upstream Checksums Unchanged | 100% SHA-256 Match | **PASS** |
| **24** | Final Report Exported | Exported `cnn_baseline_report.md` | **PASS** |

---

### 5. Final Status Decision

**Final Status**: **`FEATURE 8.3 — CNN BASELINE TRAINED & EVALUATED`**
