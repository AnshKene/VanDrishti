# Feature 8.4.1 — Controlled Benchmark Threshold, Prediction & Metric Integrity Audit Report

### Final Decision Outcome: **A) METRICS VALID — CNN ADVANTAGE REMAINS**
### Status: **FEATURE 8.4.1 — PASS (AUDIT VALIDATED)**

* **Audit Timestamp**: 2026-08-24T00:37:30+05:30
* **Feature**: Feature 8.4.1 — Controlled Benchmark Threshold, Prediction & Metric Integrity Audit
* **Upstream & Pre-Feature Manifest Status**: **PASS (100% Uncorrupted & Immutable)**
* **Identical Common Evaluation Population**: **`8,121`** footprint-safe spatial test patches ($100\%$ match)
* **Model Retraining Count**: **`0` (Strict Read-Only Audit)**

---

### 1. Answers to Required Audit Questions

1. **Were all models evaluated on exactly the same 8,121 samples?**
   - **YES (PASS)**. All 5 models (Naive Majority, Logistic Regression, Random Forest, XGBoost, CNN) were evaluated on the **exact same 8,121 spatial test samples** (`common_population.csv`). Verified zero missing IDs, zero duplicate IDs, zero coordinate mismatches, and zero target mismatches.

2. **Were predictions correctly aligned with targets?**
   - **YES (PASS)**. Predictions were joined by unique `sample_id` and verified row-by-row against target ground-truth. `100%` exact alignment verified.

3. **Were thresholds selected only from validation data?**
   - **YES (PASS)**. The CNN threshold ($0.10$) was selected on `cnn_val` ($N=6,620$). The tabular model threshold ($0.20$) was selected on `tabular_val` ($N=7,439$). Zero test samples were used for threshold selection.

4. **Are PR-AUC calculations correct?**
   - **YES (PASS)**. Calculated using `average_precision_score(y_true, y_score)`. Reconstructed values match Feature 8.4 saved values within **$< 10^-8$ absolute error**.

5. **Are F1 calculations correct?**
   - **YES (PASS)**. Calculated using `f1_score(y_true, y_pred)`. Reconstructed values match Feature 8.4 saved values within **$< 10^-8$ absolute error**.

6. **Why is XGBoost F1 = 0.0047 at threshold = 0.20 on the common test set?**
   - **EMPIRICAL EXPLANATION**: The XGBoost model was trained on class-imbalanced tabular data (pos_weight = 56.47). On the footprint-safe common test set, XGBoost predicts probabilities concentrated at very low values (median probability = 0.0024, 75th percentile < 0.05). At the fixed 0.20 threshold, XGBoost predicts only 8 positive samples out of 8,121 (TP=3, FP=5, FN=1264, TN=6849), yielding high precision (0.3750) but near-zero recall (0.0024) and F1 = 0.0047. When evaluated at lower operating thresholds (e.g., 0.05), XGBoost F1 increases to 0.1550.

7. **Does the CNN advantage survive a strict metric audit?**
   - **YES (PASS)**. On PR-AUC (Average Precision, which is threshold-independent), CNN achieves **`0.197685`** vs XGBoost **`0.156534`** (+26.3% relative improvement). On F1-score, CNN achieves **`0.2834`** vs XGBoost **`0.0047`** at fixed operating thresholds, and +0.2788 mean paired bootstrap difference (95% CI [+0.1653, +0.4042], CI > 0).

8. **Is further retraining necessary?**
   - **NO**. The controlled benchmark metrics are 100% valid, leakage-free, and reproducible.

---

### 2. Metric Reconstruction Table (Tolerance $< 10^-8$)

| Model Architecture | Recalculated PR-AUC | Saved PR-AUC | PR-AUC Diff | Recalculated F1 | Saved F1 | F1 Diff | Status |
|---|---|---|---|---|---|---|---|
| `Naive Majority Baseline` | **0.156015** | 0.156015 | 0.00000000 | **0.0000** | 0.0000 | 0.00000000 | **EXACT_MATCH_PASS** |
| `Logistic Regression` | **0.156314** | 0.156314 | 0.00000000 | **0.0047** | 0.0047 | 0.00000000 | **EXACT_MATCH_PASS** |
| `Random Forest (Set C)` | **0.164128** | 0.164128 | 0.00000000 | **0.0047** | 0.0047 | 0.00000000 | **EXACT_MATCH_PASS** |
| `XGBoost Baseline (Set C)` | **0.156534** | 0.156534 | 0.00000000 | **0.0047** | 0.0047 | 0.00000000 | **EXACT_MATCH_PASS** |
| `Compact 2D CNN (Feature 8.3)` | **0.197685** | 0.197685 | 0.00000000 | **0.2834** | 0.2834 | 0.00000000 | **EXACT_MATCH_PASS** |

---

### 3. Threshold Sensitivity Analysis (Diagnostic Only)

| Diagnostic Threshold | XGBoost Precision | XGBoost Recall | XGBoost F1 | CNN Precision | CNN Recall | CNN F1 |
|---|---|---|---|---|---|---|
| `0.05` | 0.1420 | 0.1705 | **0.1550** | 0.1740 | 0.7624 | **0.2834** |
| `0.10` | 0.2857 | 0.0095 | **0.0183** | 0.1740 | 0.7624 | **0.2834** |
| `0.15` | 0.3333 | 0.0039 | **0.0078** | 0.2670 | 0.3951 | **0.3186** |
| `0.20` | 0.3750 | 0.0024 | **0.0047** | 0.3541 | 0.1855 | **0.2435** |
| `0.25` | 0.3750 | 0.0024 | **0.0047** | 0.4507 | 0.1034 | **0.1682** |
| `0.30` | 0.3333 | 0.0016 | **0.0031** | 0.5484 | 0.0537 | **0.0978** |

---

### 4. Scientific & Legal Safety Disclaimer

> **IMPORTANT SCIENTIFIC LIMITATION**:
> The 2D Multispectral CNN model predicts spatial multi-spectral reflectance signals associated with rule-derived historical disturbance-candidate labels (Feature 7.2 Category 2/3). It does **NOT** establish:
> - illegal activity or legal violations
> - environmental non-compliance
> - causality, intent, or unauthorized land use
> - confirmed land-use change

---

### 5. Final Status Decision

```text
FINAL DECISION OUTCOME: A) METRICS VALID — CNN ADVANTAGE REMAINS

FINAL FEATURE STATUS: FEATURE 8.4.1 — PASS (AUDIT VALIDATED)
```
