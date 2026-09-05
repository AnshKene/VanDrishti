# Feature 8.1.1 — Baseline Evaluation Correction & Leakage Audit Report

### Final Status Decision: **BASELINE PROMISING — SPATIAL PATCH MODEL MAY BE JUSTIFIED**

* **Audit Timestamp**: 2026-08-24T00:00:15+05:30
* **Feature Audited**: Feature 8.1 — Tabular Disturbance Baseline Model
* **Upstream Manifest Checksum Status**: **PASS (100% Uncorrupted)**
* **XGBoost scale_pos_weight (Train Set Only)**: **`6.766376`**
* **CNN Model Training Status**: **NOT TRAINED**

---

### 1. Root Cause of PR-AUC Implementation Bug & Resolution

* **Root Cause**: In Feature 8.1, PR-AUC was calculated using `sklearn.metrics.auc(r, p)` where `p, r` came from `precision_recall_curve`. When evaluating a constant majority predictor (predicting constant probability 0.0), `precision_recall_curve` inserted artificial boundary points (1, 0) and (0, 1), generating a false trapezoidal area artifact of **`0.5455`**.
* **Resolution**: Replaced `auc(r, p)` with **`sklearn.metrics.average_precision_score(y_true, y_score)`**.
* **Automated Regression Assertion**:
  - `Validation Positive Prevalence`: $852 / 9368 = \mathbf{0.090948}$ -> `Majority AP`: $\mathbf{0.090948}$ (**PASS - Error < 1e-6**).
  - `Test Positive Prevalence`: $390 / 6012 = \mathbf{0.064870}$ -> `Majority AP`: $\mathbf{0.064870}$ (**PASS - Error < 1e-6**).

---

### 2. Feature Matrix Leakage Correction (`feature8_1_feature_leakage_audit.csv`)

* **Spatial Location Features Removed**: `latitude`, `longitude`, and `project_id` were strictly removed from predictive model input matrix X.
* **Target Circularity Audit**: Verified zero target-derived features entered X.
* **Allowed Features in X**:
  - Sentinel-2 Bands (B2, B3, B4, B8, B11, B12)
  - Derived Spectral Indices (NDVI, NDWI, NDBI)
  - Dynamic World Reference Features (`dynamic_world_class` One-Hot, `dynamic_world_confidence`).

---

### 3. Corrected Model Performance Comparison (`feature8_1_model_comparison_corrected.csv`)

| Model Name | Split | PR-AUC (AP) | F1-Score | Macro F1 | Balanced Accuracy | Precision | Recall | ROC-AUC |
|---|---|---|---|---|---|---|---|---|
| `Naive Majority Baseline` | `validation` | **0.0909** | **0.0000** | 0.4762 | 0.5000 | 0.0000 | 0.0000 | 0.5000 |
| `Naive Majority Baseline` | `test` | **0.0649** | **0.0000** | 0.4832 | 0.5000 | 0.0000 | 0.0000 | 0.5000 |
| `Logistic Regression` | `validation` | **0.1120** | **0.1445** | 0.4467 | 0.4987 | 0.0903 | 0.3603 | 0.5064 |
| `Logistic Regression` | `test` | **0.0658** | **0.1221** | 0.4174 | 0.5191 | 0.0703 | 0.4641 | 0.5485 |
| `Random Forest` | `validation` | **0.1090** | **0.0109** | 0.4799 | 0.4993 | 0.0746 | 0.0059 | 0.5515 |
| `Random Forest` | `test` | **0.0631** | **0.0000** | 0.4813 | 0.4962 | 0.0000 | 0.0000 | 0.5007 |
| `XGBoost` | `validation` | **0.1034** | **0.1548** | 0.5159 | 0.5292 | 0.1206 | 0.2160 | 0.5129 |
| `XGBoost` | `test` | **0.0730** | **0.1009** | 0.4965 | 0.5092 | 0.0724 | 0.1667 | 0.5673 |

---

### 4. Corrected Project-Wise Test Set Evaluation (`feature8_1_project_metrics_corrected.csv`)

| Project ID | Project Name | Test Samples | Positives | Prevalence | PR-AUC | F1-Score | Precision | Recall | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `MH-001` | Gondkhari | 1390 | 76 | 0.054676 | **0.0345** | **0.0494** | 0.0267 | 0.3289 | Calculated |
| `MH-002` | Gadchiroli | 3657 | 314 | 0.085863 | **0.1131** | **0.1810** | 0.1106 | 0.4968 | Calculated |
| `MH-003` | Bhivpuri PSP | 965 | 0 | 0.000000 | **PR-AUC is undefined/not estimable for this project because there are zero positive ground-truth samples.** | **0.0000** | 0.0000 | 0.0000 | Zero Positive Test Samples |

---

### 5. Final Status Decision

* **Comparison against Corrected Majority Baseline**:
  - Validation Majority Baseline PR-AUC: **`0.090948`**
  - Validation Logistic Regression PR-AUC: **`0.112031`** (+0.021083 over majority baseline)
  - Validation Random Forest PR-AUC: **`0.108969`** (+0.018021 over majority baseline)
  - Validation XGBoost PR-AUC: **`0.103384`** (+0.012436 over majority baseline)
* **Conclusion**: All three tabular baseline models beat the corrected Naive Majority Baseline on validation PR-AUC.

**Final Feature 8.1.1 Status**: **`BASELINE PROMISING — SPATIAL PATCH MODEL MAY BE JUSTIFIED`**
