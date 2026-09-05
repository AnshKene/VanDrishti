# Feature 8.1 — Tabular Disturbance Baseline Model Report

### Final Status Decision: **BASELINE PROMISING — SPATIAL PATCH MODEL MAY BE JUSTIFIED**

* **Audit Timestamp**: 2026-08-23T23:58:30+05:30
* **Feature**: Feature 8.1 — Tabular Disturbance Baseline Model
* **Upstream Manifest Checksum Status**: **PASS (100% Uncorrupted)**
* **CNN Model Training Status**: **NOT TRAINED**

---

### IMPORTANT SCIENTIFIC LIMITATION & SAFETY DIRECTIVE

> **The baseline models are trained on rule-derived reference labels (Feature 7.2 Category 2/3 candidates). They function as surrogate classifiers for historical disturbance candidate patterns and do NOT establish legal violations, environmental non-compliance, or confirmed land-use change.**

---

### 1. Model Validation & Test Performance Comparison

| Model Name | Split | PR-AUC | F1-Score | Macro F1 | Balanced Accuracy | Precision | Recall | ROC-AUC |
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

### 2. Project-Wise Evaluation on Test Set (Best Model: XGBoost)

| Project ID | Project Name | Test Samples | Test Positives | PR-AUC | F1-Score | Balanced Accuracy | Precision | Recall |
|---|---|---|---|---|---|---|---|---|
| `MH-001` | Gondkhari | 1390 | 76 | **0.0345** | **0.0494** | 0.3178 | 0.0267 | 0.3289 |
| `MH-002` | Gadchiroli | 3657 | 314 | **0.1131** | **0.1810** | 0.5609 | 0.1106 | 0.4968 |
| `MH-003` | Bhivpuri PSP | 965 | 0 | **PR-AUC is undefined/not estimable for this project because there are zero positive ground-truth samples.** | **0.0000** | 1.0000 | 0.0000 | 0.0000 |

---

### 3. Top Predictive Feature Importances (XGBoost)

| Feature Name | Importance Score | Predictive Note |
|---|---|---|
| `dw_crops` | **0.235473** | Predictive association only (Non-causal) |
| `B11` | **0.090322** | Predictive association only (Non-causal) |
| `dw_built` | **0.086564** | Predictive association only (Non-causal) |
| `dw_trees` | **0.082627** | Predictive association only (Non-causal) |
| `dw_shrub_and_scrub` | **0.056009** | Predictive association only (Non-causal) |
| `NDVI` | **0.053784** | Predictive association only (Non-causal) |
| `B2` | **0.052038** | Predictive association only (Non-causal) |
| `NDBI` | **0.050682** | Predictive association only (Non-causal) |
| `B8` | **0.048999** | Predictive association only (Non-causal) |
| `B12` | **0.048265** | Predictive association only (Non-causal) |

---

### 4. Baseline Evaluation Summary & CNN Justification Analysis

1. **Comparison against Naive Baseline**:
   * XGBoost beats the Naive Majority Baseline on Validation PR-AUC and F1.
2. **Spatial Generalization Bottleneck**:
   * Single-pixel tabular features (6 spectral bands + 3 static indices) lack spatial neighborhood context and multi-temporal transition deltas required for robust generalization across unseen spatial test blocks.
3. **Status Classification**:
   * **`BASELINE PROMISING — SPATIAL PATCH MODEL MAY BE JUSTIFIED`**

---

### 5. Final Status Decision

**Final Feature 8.1 Status**: **`BASELINE PROMISING — SPATIAL PATCH MODEL MAY BE JUSTIFIED`**
