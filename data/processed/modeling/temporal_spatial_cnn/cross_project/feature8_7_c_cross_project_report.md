# Feature 8.7-C -- Leave-One-Project-Out Temporal Delta CNN Generalization Experiment

## Final Scientific Decision: **B) TEMPORAL CROSS-PROJECT GENERALIZATION EXISTS BUT IS MIXED**
## Status: **FEATURE 8.7-C -- PASS (EXPERIMENTS COMPLETED)**

---

## 1. Experimental Setup

| Experiment | Training Projects | Held-Out Project | Train N | Val N | Test N | Positives | Prevalence |
|---|---|---|---|---|---|---|---|
| A | MH-002 + MH-003 | MH-001 | 6829 | 1499 | 2424 | 262 | 10.8% |
| B | MH-001 + MH-003 | MH-002 | 2917 | 286 | 7549 | 904 | 12.0% |
| C | MH-001 + MH-002 | MH-003 | 8023 | 1950 | 779 | 159 | 20.4% |

---

## 2. Main Results: Temporal Delta CNN vs XGBoost vs Spatial CNN

| Exp | Held-Out | CNN PR-AUC | XGBoost PR-AUC | F8.6 Spatial PR-AUC | CNN-XGB | CNN-Spatial |
|---|---|---|---|---|---|---|
| A | MH-001 | **0.2619** | 0.0910 | 0.2121 | +0.1709 | +0.0498 |
| B | MH-002 | **0.2654** | 0.1408 | 0.3381 | +0.1246 | -0.0727 |
| C | MH-003 | **0.4070** | 0.1145 | 0.1470 | +0.2925 | +0.2600 |

| Exp | Held-Out | CNN F1 | XGBoost F1 | CNN Precision | CNN Recall | CNN Balanced Acc |
|---|---|---|---|---|---|---|
| A | MH-001 | 0.1889 | 0.1635 | 0.3469 | 0.1298 | 0.5501 |
| B | MH-002 | 0.3572 | 0.2293 | 0.3246 | 0.3971 | 0.6424 |
| C | MH-003 | 0.4315 | 0.2006 | 0.2751 | 1.0000 | 0.6621 |

---

## 3. Answers to Required Scientific Questions

1. **Does Delta Temporal CNN generalize to MH-001?** CNN PR-AUC=0.2619 vs XGBoost=0.0910. Yes -- beats XGBoost.
2. **Does Delta Temporal CNN generalize to MH-002?** CNN PR-AUC=0.2654 vs XGBoost=0.1408. Yes -- beats XGBoost.
3. **Does Delta Temporal CNN generalize to MH-003?** CNN PR-AUC=0.4070 vs XGBoost=0.1145. Yes -- beats XGBoost.
4. **Outperforms XGBoost on all?** 3 of 3 experiments. YES.
5. **Temporal CNN vs F8.6 Spatial CNN?** 2 of 3 experiments temporal wins.
6. **Consistent advantage?** Consistent.
7. **Hardest project to generalize to?** MH-001 (lowest CNN PR-AUC).
8. **FP or FN dominated?** Refer to confusion matrices in cross_project_temporal_confusion_matrices.csv.
9. **Distribution shift?** Refer to cross_project_temporal_distribution_shift.csv. MH-003 is smallest project (N=779).
10. **Temporal representation transferable?** B) TEMPORAL CROSS-PROJECT GENERALIZATION EXISTS BUT IS MIXED.
11. **Project-specific overfitting?** Performance variation across projects suggests some project specificity -- see project metrics.
12. **More complexity justified?** Possibly -- temporal delta shows promise.

---

## 4. Comparison with Feature 8.6 (Spatial CNN LOPO)

| Held-Out Project | F8.7-C Delta Temporal PR-AUC | F8.6 Spatial CNN PR-AUC | Delta Improvement |
|---|---|---|---|
| MH-001 | 0.2619 | 0.2121 | +0.0498 |
| MH-002 | 0.2654 | 0.3381 | -0.0727 |
| MH-003 | 0.4070 | 0.1470 | +0.2600 |

---

## 5. Important Methodological Notes

- **CONDITIONAL COMPARISON with Feature 8.6**: Feature 8.6 used ALL samples per held-out project (multi-year patches); Feature 8.7-C uses only samples with complete 5-year sequences. Populations differ.
- **MH-003 limitation**: Only 159 positive samples in MH-003. PR-AUC estimates are highly variable.
- **Train-only normalization**: Confirmed. Delta normalization stats computed from training-project samples only.
- **No threshold leakage**: Threshold selected from internal validation (training-project blocks only).

---

## 6. Scientific Disclaimer

The model predicts spatial-temporal multispectral patterns associated with rule-derived historical disturbance-candidate labels. It does NOT establish illegal activity, environmental non-compliance, unauthorized land use, causality, intent, or confirmed land-use change. Predictions must be treated as screening signals requiring independent regulatory or ground verification.
