# Feature 8.7-A — Temporal-Spatial Dataset Design & Leakage-Safe Preparation Report

### Final Status Decision: **PASS (TEMPORAL DATASET PREPARED)**

* **Execution Timestamp**: 2026-08-24T00:54:00+05:30
* **Feature**: Feature 8.7-A — Temporal-Spatial Dataset Design
* **Upstream Manifest Checksum Status**: **PASS (100% Uncorrupted & Immutable)**
* **CNN Model Training Status**: **NOT TRAINED (0 Models Trained)**

---

### 1. Dataset Generation Summary

1. **How many complete 5-year temporal patches were created?**
   **`10752`** valid complete temporal tensors (shape `(5, 15, 15, 6)`) were successfully extracted.
2. **How many were rejected and why?**
   **`4509`** centers were rejected due to incomplete 5-year sequences (missing valid non-monsoon observations in one or more years).
   **`1432`** complete centers were correctly rejected as `buffer_excluded` to maintain 0 footprint overlap.
3. **How many remain in train/validation/test?**
   `cnn_train`: **`8534`**
   `cnn_val`: **`992`**
   `cnn_test`: **`1226`**
4. **What is the class distribution?**
   Refer to `temporal_patch_class_distribution.csv` for exact positive prevalence per split. No SMOTE or synthetic oversampling was applied.
5. **Is the spatial split still leakage-free?**
   **YES**. The identical `cnn_spatial_split` from Feature 8.2 was inherited, preserving the 0 spatial footprint overlap guarantee.
6. **Is the temporal sequence aligned correctly?**
   **YES**. Every tensor correctly layers 2021, 2022, 2023, 2024, and 2025 in sequence `(T0, T1, T2, T3, T4)`.
7. **Is there any future-year leakage?**
   **NO**. 2026 is strictly excluded.
8. **Is there any target leakage?**
   **NO**. Target definitions are strictly inherited from Feature 7.2 historical candidates.
9. **Are normalization statistics train-only?**
   **YES**. `temporal_normalization_metadata.json` was calculated strictly across `cnn_train`.
10. **How many samples are available per project?**
    See `temporal_project_distribution.csv`.
11. **How many samples were lost because of missing years?**
    **`4509`** unique center coordinates lacked one or more years of observation and were safely discarded.
12. **Is the temporal-delta dataset valid?**
    **YES**. `temporal_delta_cnn_test.npz` of shape `(4, 15, 15, 6)` was accurately derived via discrete time differencing.
13. **Is NDVI delta safely available?**
    **NO**. `NDVI DELTA DATASET NOT USED`.
14. **Is the dataset suitable for Feature 8.7 CNN training?**
    **YES**. The dataset is structurally sound, leakage-free, and cross-project compatible.
15. **What limitations should be documented?**
    The requirement for complete 5-year non-monsoon sequences naturally biases the dataset toward regions with lower historical cloud cover.

---

### 2. Scientific & Legal Safety Disclaimer

> **IMPORTANT SCIENTIFIC LIMITATION**:
> This dataset provides multi-year sequential optical reflectance patches mapped to historical rule-based disturbance candidate categories (Feature 7.2). It does **NOT** contain or establish ground-truth evidence of legal violations, unauthorized intent, or confirmed environmental non-compliance.

---

### 3. Final Status

```text
FINAL STATUS = PASS
```
