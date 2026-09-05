# Feature 8.0 — Disturbance Modeling Design & Feasibility Audit Report

### Final Feasibility Decision: **READY FOR BASELINE MODEL**

* **Audit Timestamp**: 2026-08-23T23:55:30+05:30
* **Feature**: Feature 8.0 — Disturbance Modeling Design & Feasibility Audit
* **Upstream Manifest Checksums**:
  - Feature 6 Checksum: **PASS (100% Uncorrupted)**
  - Feature 7.2 Checksum: **PASS (100% Uncorrupted)**
  - Feature 7.3 Checksum: **PASS (100% Uncorrupted)**
* **CNN / ML Model Training Status**: **NOT TRAINED (0 Models Trained)**

---

### 1. Key Audit Findings & Recommendations

1. **Target Definition Recommendation**:
   * **Option A (Binary Disturbance Candidate)** is recommended:
     - `0` = Non-Disturbance (Normal / Single-Signal Anomalies)
     - `1` = Disturbance Candidate (Multi-Spectral / Persistent Candidates)
   * Minority class proportion: **`~4.0%`** across projects (MH-001: 13.06%, MH-002: 15.32%, MH-003: 18.82%).

2. **Label Source & Target Leakage Control**:
   * Labels originate from Feature 7.2 rule-derived multi-spectral candidate categories.
   * To prevent target leakage and circularity, model inputs should use raw Sentinel-2 6-band reflectances ($B2, B3, B4, B8, B11, B12$) and continuous spectral indices, while excluding Feature 7.2/7.3 output scores from feature inputs.

3. **Spatial & Temporal Leakage Control**:
   * **Patch Size Safety**: **15x15 Patch Size (450m x 450m)** is **`PASS`** (Patch radius $210	ext{m} < 	ext{Min split distance } 391.9	ext{m}$). 33x33 is **`FAIL`** ($480	ext{m} > 391.9	ext{m}$).
   * **Temporal Coordinate Repeat Safety**: Spatial coordinate grouping (`GroupKFold` by coordinate ID) must be enforced to prevent multi-temporal repeat leakage across 2021–2025 ($4.53	imes$ repeat factor).

4. **Project Generalization Strategy**:
   * **Project-Aware Baseline Model** is recommended over unweighted global LOPO due to landscape domain shifts (`MH-002 Gadchiroli` dense forest reserve vs `MH-001 Gondkhari` coal mine pit edge).

5. **Recommended Modeling Hierarchy**:
   * **Stage 1 (Immediate Next Step)**: Tabular Baseline Model (Random Forest / XGBoost / Logistic Regression) using point/patch multi-spectral features.
   * **Stage 2 (Future Step)**: 2D CNN (ResNet-18) on $15 	imes 15$ multi-spectral patch stacks after baseline evaluation.

6. **Recommended Evaluation Metrics for Class Imbalance**:
   * **Primary Metrics**: Precision-Recall AUC (PR-AUC), F1-Score, Macro F1, Balanced Accuracy.
   * **Secondary Metrics**: Precision, Recall, Confusion Matrix. (Plain Accuracy is strictly forbidden).

---

### 2. Output Audit Artifacts Generated

The following audit artifacts were created under [`data/processed/modeling/`](file:///c:/Users/anshk/Desktop/Environmental-Monitoring/data/processed/modeling/):
1. `data/processed/modeling/feature8_target_options.csv`
2. `data/processed/modeling/feature8_label_audit.csv`
3. `data/processed/modeling/feature8_class_distribution.csv`
4. `data/processed/modeling/feature8_leakage_audit.csv`
5. `data/processed/modeling/feature8_project_generalization.csv`
6. `data/processed/modeling/feature8_feature_availability.csv`
7. `data/processed/modeling/feature8_patch_feasibility.csv`
8. `data/processed/modeling/feature8_model_strategy.csv`
9. [`data/processed/modeling/feature8_modeling_design_report.md`](file:///c:/Users/anshk/Desktop/Environmental-Monitoring/data/processed/modeling/feature8_modeling_design_report.md)

---

### 3. Final Feasibility Decision

**Final Decision**: **`READY FOR BASELINE MODEL`**
