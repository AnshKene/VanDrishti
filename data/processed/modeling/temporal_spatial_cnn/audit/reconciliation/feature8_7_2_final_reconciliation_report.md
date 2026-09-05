# Feature 8.7.2 -- Temporal CNN Test Population Reconciliation & Audit Correction

## Final Scientific Decision: **A) FEATURE 8.7.1 VALID — ORIGINAL POPULATION CONFIRMED**
## Audit Status: **FEATURE 8.7.2 -- PASS (RECONCILIATION COMPLETE)**

---

## 1. Root Cause of the Apparent "1,602 vs 1,226" Discrepancy

The '1,602' figure cited in the Feature 8.7-B USER REQUEST specification was a **pre-execution estimate**, not a verified count from a frozen artifact.

**Evidence trail:**

| Source | N |
|---|---|
| Feature 8.7-B USER REQUEST spec (input text) | 1,602 |
| Frozen `temporal_patches_test.npz` | **1,226** |
| `temporal_patch_metadata.csv` (cnn_test rows) | **1,226** |
| `temporal_patch_class_distribution.csv` (cnn_test) | **1,226** |
| `temporal_cnn_test_metrics.csv` (N column, all models) | **1,226** |
| Feature 8.7.1 audited N | **1,226** |

**Conclusion:** There is no true 376-sample missing population. The '1,602' number never represented a frozen artifact. Feature 8.7.1 correctly audited N = **1,226** -- the only population that ever existed.

---

## 2. Where Does "1,602" Come From?

The Feature 8.7-B task specification stated:

> cnn_train = 8,131 / cnn_val = 1,019 / cnn_test = **1,602** / Total = 10,752

These were pre-execution estimates. The actual Feature 8.7-A execution produced a different internal split:

> cnn_train = 8,534 / cnn_val = 992 / cnn_test = **1,226** / Total = 10,752

The total (10,752) matches exactly, confirming no samples were lost. Only the within-split allocation differed from the spec estimate. The 8.7-B training code used the actual NPZ files, not the spec numbers.

---

## 3. What Were the 579 Centers Excluded From Feature 8.2 Test?

The Feature 8.2 cnn_test split contained **1,805 unique center coordinates**.
Feature 8.7 required complete 5-year non-monsoon sequences, which only **1,226** centers possessed.

| Years Available | Center Count |
|---|---|
| 1 | 18 |
| 2 | 56 |
| 3 | 159 |
| 4 | 346 |
| 5 | **1,226** (retained) |
| **Total** | **1,805** |

The **579 excluded centers** (1,805 - 1,226) lacked at least one complete annual Sentinel-2 observation across the 2021-2025 non-monsoon window. This is a methodologically valid exclusion documented in Feature 8.7-A.

---

## 4. Project Distribution

| Project | F8.2 Test Centers | F8.7 Temporal Test | Removed |
|---|---|---|---|
| MH-001 | 1017 | 547 | 470 |
| MH-002 | 663 | 594 | 69 |
| MH-003 | 125 | 85 | 40 |

---

## 5. Metric Reconstruction on N=1,226 (the Correct Population)

| Metric | Raw Temporal | Delta Temporal | Spatial Control |
|---|---|---|---|
| **PR-AUC** | 0.1453 | **0.3791** | 0.2429 |
| **F1** | 0.0892 | **0.3232** | 0.2728 |
| **Balanced Acc** | 0.4833 | **0.6135** | 0.5199 |
| **TN/FP/FN/TP** | 926/112/174/14 | 484/554/45/143 | 80/958/7/181 |

Metrics match Feature 8.7.1 and Feature 8.7-B exactly.

---

## 6. Bootstrap Recheck on N=1,226

| Metric | Mean | 95% CI | Excludes Zero |
|---|---|---|---|
| **Delta PR-AUC - Control PR-AUC** | **0.1255** | **[0.0185, 0.2798]** | **YES** |
| Delta F1 - Control F1 | 0.0586 | [-0.0065, 0.1773] | NO |
| Delta BalAcc - Control BalAcc | 0.0994 | [-0.0064, 0.2324] | NO |

The 95% CI for PR-AUC difference **excludes zero**.
The Feature 8.7.1 statistical conclusion **REMAINS VALID AND UNCHANGED**.

---

## 7. Summary Answer to Required Questions

| Question | Answer |
|---|---|
| Original Feature 8.7-B N | 1,226 (spec said 1,602 but spec was a pre-execution estimate) |
| Feature 8.7.1 N | 1,226 |
| Difference | 0 (no real discrepancy in frozen data) |
| Exact reason for "1,602 vs 1,226" | The '1,602' was the spec input number; the actual NPZ always contained 1,226 |
| Correct population | **N = 1,226** |
| Corrected Delta PR-AUC | **0.3791** (unchanged) |
| Corrected Control PR-AUC | **0.2429** (unchanged) |
| Corrected AP difference | **+0.1362** |
| Corrected 95% CI | **[0.0185, 0.2798]** |
| Final scientific decision | **A) FEATURE 8.7.1 VALID — ORIGINAL POPULATION CONFIRMED** |

---

## 8. Scientific Disclaimer

The model predicts patterns associated with historical Feature 7.2 disturbance candidates.
It does NOT establish illegal activity, environmental non-compliance, causality, intent,
or confirmed land-use change.
