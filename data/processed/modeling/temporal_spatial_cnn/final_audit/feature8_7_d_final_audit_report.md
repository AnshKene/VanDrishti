# Feature 8.7-D -- Final Temporal CNN Cross-Experiment Integrity & Population Audit

## Final Scientific Decision: **B) FEATURE 8.7 CHAIN VALID WITH QUALIFICATIONS**
## Audit Status: **FEATURE 8.7-D -- PASS (AUDIT VALIDATED)**

---

## 1. Pre-/Post-Audit Checksums
All upstream Feature 8.7-A/B/C, 8.7.1, 8.7.2, and 8.6 artifact checksums verified **PASS** before and after the audit.

---

## 2. Feature 8.7-A Dataset Reconciliation

| Item | Value | Status |
|---|---|---|
| Total temporal samples | 10752 | PASS |
| Train / Val / Test | 8534 / 992 / 1226 | PASS |
| Train+Val+Test = Total | 10752 = 10752 | PASS |
| Duplicate IDs | 0 | PASS |
| Multi-split IDs | 0 | PASS |
| NPZ y vs metadata targets | All match | PASS |
| Complete 5-yr centers | 1226 | PASS |
| Incomplete centers excluded | 579 | PASS |

---

## 3. Feature 8.7-B Metric Reconstruction

| Model | Reconstructed PR-AUC | Reported | Match |
|---|---|---|---|
| Raw Temporal CNN | 0.1453 | 0.1453 | PASS |
| Delta Temporal CNN | 0.3791 | 0.3791 | PASS |
| Spatial-Only Control | 0.2429 | 0.2429 | PASS |

---

## 4. Feature 8.7.1 / 8.7.2 Population Verification

- Test N from frozen NPZ = **1226** (expected 1,226): **PASS**
- No artifact stores N=1,602 as actual frozen data: **PASS** (1,602 was spec text only)
- 579 incomplete centers correctly excluded: **PASS**
- Delta AP - Control AP = **0.1362** (expected ~0.1362): **PASS**
- Reported bootstrap CI [0.0185, 0.2798]: **CONFIRMED VALID**

---

## 5. Feature 8.7-C Leave-One-Project-Out Population Summary

| Exp | Hold-Out | Train N | Val N | Test N | Pos | Prev | Blocks | CNN PR-AUC | XGB PR-AUC | Spatial PR-AUC |
|---|---|---|---|---|---|---|---|---|---|---|
| A | MH-001 | 6829 | 1499 | 2424 | 262 | 10.8% | 11 | **0.2619** | 0.091 | 0.2121 |
| B | MH-002 | 2917 | 286 | 7549 | 904 | 12.0% | 12 | **0.2654** | 0.1408 | 0.3381 |
| C | MH-003 | 8023 | 1950 | 779 | 159 | 20.4% | 12 | **0.407** | 0.1145 | 0.147 |

---

## 6. Sample Contamination Audit (train, val, held-out test)

All experiments verified: **train intersection test = 0, val intersection test = 0, project exclusivity = 0**. No sample contamination detected.

---

## 7. Normalization Leakage Audit

For all 3 experiments, normalization statistics were computed from training-project samples only.
Held-out project contribution = **0** in all experiments.

---

## 8. Threshold Selection Audit

All thresholds selected from internal validation set (training-project blocks only).
Test samples used for threshold selection = **0** in all experiments.

---

## 9. Metric Reconstruction (Feature 8.7-C)

| Experiment | Held-Out | CNN PR-AUC (Reconstructed) | Reported | Diff | Beats XGB | Beats Spatial |
|---|---|---|---|---|---|---|
| A | MH-001 | 0.2619 | 0.2619 | 5.55e-17 | YES | YES |
| B | MH-002 | 0.2654 | 0.2654 | 5.55e-17 | YES | NO |
| C | MH-003 | 0.4070 | 0.4070 | 0.00e+00 | YES | YES |

---

## 10. XGBoost Verification (from Feature 8.6 authoritative CSV)

- MH-001 XGBoost PR-AUC = **0.0910** (CNN 0.2619 > 0.0910: CONFIRMED)
- MH-002 XGBoost PR-AUC = **0.1408** (CNN 0.2654 > 0.1408: CONFIRMED)
- MH-003 XGBoost PR-AUC = **0.1145** (CNN 0.4070 > 0.1145: CONFIRMED)
- **CNN beats XGBoost: 3/3 experiments** -- CONFIRMED

---

## 11. Spatial CNN Comparison (Feature 8.6 vs Feature 8.7-C)

**Classification: CONDITIONAL**

Feature 8.6 and Feature 8.7-C use different evaluation populations:
- F8.6 evaluated on all center-year patches (N up to 41,451 per project, all years individually)
- F8.7-C evaluated only on centers with complete 5-year sequences (N up to 7,549 per project)

| Held-Out | Temporal CNN PR-AUC | Spatial CNN PR-AUC | Winner |
|---|---|---|---|
| MH-001 | 0.2619 | 0.2121 | Temporal |
| MH-002 | 0.2654 | 0.3381 | Spatial |
| MH-003 | 0.4070 | 0.1470 | Temporal |

Temporal beats Spatial: **2/3** experiments. This comparison is conditional on population differences.

---

## 12. Validated Scientific Claims

**ALLOWED (verified):**
- "Temporal Delta CNN generalizes to all three unseen environmental projects."
- "Temporal Delta CNN outperforms XGBoost on all three held-out projects (3/3)."
- "Temporal Delta CNN advantage over the Feature 8.6 spatial CNN is mixed (2/3)."
- "The cross-project temporal advantage is real but project-specific."

**NOT ALLOWED:**
- "Temporal CNN universally outperforms spatial CNN." (MH-002 counterexample)
- "Temporal CNN proves environmental non-compliance." (No model can establish this)
- "Temporal CNN is globally superior to XGBoost." (LOPO experiment only)

---

## 13. Final Chain Status

| Feature | Status | Notes |
|---|---|---|
| Feature 8.7-A | PASS | N=10,752 retained, 579 incomplete excluded |
| Feature 8.7-B | PASS | All metrics reconstruct within tolerance |
| Feature 8.7.1 | PASS | Bootstrap CI [0.0185,0.2798] excludes zero |
| Feature 8.7.2 | PASS | 1,602 confirmed as spec text, not frozen data |
| Feature 8.7-C | PASS | 3/3 LOPO experiments, no leakage, no overlap |
| Feature 8.6 (baseline) | PASS | XGBoost values verified from authoritative CSV |

**Reason:** All metrics reconstruct, all populations verified, no leakage detected. F8.6 vs F8.7-C comparison is CONDITIONAL due to different evaluation populations.

---

## 14. Scientific Disclaimer

The model predicts spatial-temporal multispectral patterns associated with rule-derived historical disturbance-candidate labels. It does NOT establish illegal activity, environmental non-compliance, unauthorized land use, causality, intent, or confirmed land-use change. All predictions must be treated as screening signals requiring independent regulatory or ground verification.
