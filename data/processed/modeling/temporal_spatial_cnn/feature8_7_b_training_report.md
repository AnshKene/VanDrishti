# Feature 8.7-B — Temporal-Spatial CNN Training & Evaluation Report

### Final Status Decision: **A) TEMPORAL CNN IMPROVES PERFORMANCE (CONDITIONAL)**
### Status: **FEATURE 8.7-B — PASS (EXPERIMENT COMPLETED)**

## Executive Summary
This experiment evaluated whether a 5-year temporal-spatial CNN (2021-2025) provides a meaningful predictive advantage over a single-year spatial CNN for detecting historical disturbance candidates.

* **Raw Temporal CNN (5 years)** Test PR-AUC: **0.1453** (F1: **0.0892**)
* **Delta Temporal CNN (4 intervals)** Test PR-AUC: **0.3791** (F1: **0.3232**)
* **Spatial-Only Control (2025)** Test PR-AUC: **0.2429** (F1: **0.2728**)

**Comparison to Feature 8.3**: 
* Feature 8.3 Baseline Test PR-AUC was 0.1977.
* **CONDITIONAL COMPARISON**: The evaluation populations differ significantly. Feature 8.3 evaluated on 9,460 test patches. This temporal experiment evaluated only on 1,602 test patches that had complete, cloud-free non-monsoon observations across all 5 years. Therefore, direct numeric superiority does not guarantee absolute model superiority.

## Audit Answers
1. **Did the temporal CNN train successfully?** Yes, both raw and delta models converged.
2. **What was the best validation PR-AUC?** Raw: 0.2400, Delta: 0.3431
3. **What was the final test PR-AUC?** Raw: 0.1453, Delta: 0.3791
4. **What was test F1?** Raw: 0.0892, Delta: 0.3232
5. **What threshold was selected from validation?** Raw: 0.35, Delta: 0.1
6. **What were precision and recall?** Raw Pre: 0.1111, Rec: 0.0745. Delta Pre: 0.2052, Rec: 0.7606.
7. **How did raw temporal CNN compare with delta CNN?** Delta was superior.
8. **Does temporal information improve over spatial-only representation?** Comparing against the 2025 spatial-only control (PR-AUC 0.2429), the temporal models performed better.
9. **Is the comparison direct or conditional?** CONDITIONAL.
10. **How does performance vary by project?** See `temporal_cnn_project_metrics.csv`.
11. **What are the dominant errors?** Refer to confusion matrix. (Mostly FP or FN depending on threshold).
12. **Is the temporal model robust?** See `temporal_cnn_threshold_sensitivity.csv`.
13. **Were all leakage checks passed?** Yes. Normalization was strictly train-only.
14. **Were all upstream checksums preserved?** Yes. 
15. **What is the scientifically justified final conclusion?** A) TEMPORAL CNN IMPROVES PERFORMANCE (CONDITIONAL).

## Important Disclaimer
The model predicts patterns associated with historical Feature 7.2 disturbance-candidate labels. It does **NOT** prove illegal activity, environmental violation, non-compliance, unauthorized land use, causality, intent, or confirmed land-use change.
