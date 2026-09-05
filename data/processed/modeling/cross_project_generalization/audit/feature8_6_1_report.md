# Feature 8.6.1 — Cross-Project Population Reconciliation & Generalization Audit

### Final Decision Outcome: **B) POPULATION DIFFERENCE EXPLAINED BUT COMPARISON REQUIRES EXPLICIT QUALIFICATION**
### Status: **FEATURE 8.6.1 — PASS (AUDIT VALIDATED)**

## Executive Summary
The apparent population discrepancy for MH-003 between Feature 8.3 (N = 565) and Feature 8.6 Experiment C (N = 5,128) is methodologically valid and expected.

* **Feature 8.3 (CNN Baseline)** used a global spatial block split across all projects. Its test set only contained patches assigned to the `cnn_test` split (N = 565 for MH-003).
* **Feature 8.6 (Leave-One-Project-Out)** tests the model's ability to generalize to an entirely unseen project. Because the *entire* MH-003 project is excluded from training, it is methodologically correct to evaluate the model on *all* footprint-safe patches in MH-003 (`cnn_train` + `cnn_val` + `cnn_test` = 5,128), rather than restricting evaluation to the small global test subset.

## Answers to Required Audit Questions

1. **Why does MH-003 have 565 samples in Feature 8.3?**
   It restricted evaluation strictly to the `cnn_test` split of the frozen dataset.
2. **Why does MH-003 have 5,128 samples in Feature 8.6?**
   It evaluated on the combination of `cnn_train`, `cnn_val`, and `cnn_test` splits for the held-out project, maximizing the evaluation set size without leakage.
3. **Where exactly does the population diverge?**
   The populations diverge at the spatial split selection stage. Feature 8.6 includes `cnn_train` and `cnn_val` patches for the held-out project.
4. **Why are there 570 positives in Feature 8.6 but zero in Feature 8.3?**
   The positive samples for MH-003 in the frozen split happened to be allocated to `cnn_train` and `cnn_val` spatial blocks. Feature 8.6 includes these blocks in its held-out evaluation.
5. **Is the target definition identical?**
   Yes. Both use Feature 7.2 Category 2/3.
6. **Is the spatial split identical?**
   No, by design. Feature 8.6 aggregates all valid spatial blocks for the held-out project.
7. **Is the footprint buffer identical?**
   Yes. Buffer-excluded patches were correctly excluded in both.
8. **Is the temporal filtering identical?**
   Yes. 2026 and monsoon months are excluded.
9. **Did Feature 8.6 use any Feature 8.3 test samples?**
   Yes, for the held-out project, but they were strictly held out from training.
10. **Did Feature 8.6 use any Feature 8.3 training/validation samples?**
    Yes, for the held-out project, it used them for *testing*.
11. **Did Feature 8.6 use buffer-excluded samples?**
    No.
12. **Was there any target leakage?**
    No.
13. **Was there any spatial leakage?**
    No. The train/test project sets are mutually exclusive.
14. **Was there any temporal leakage?**
    No.
15. **Is Feature 8.6 scientifically valid?**
    Yes.
16. **Does Feature 8.6 need to be rerun?**
    No.
17. **Is Feature 8.7 safe to begin?**
    Yes.

## Verification
All checksums passed. No existing artifacts were modified.
