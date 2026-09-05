# Feature 8.7.1 — Temporal CNN Result Integrity, Paired Comparison & Statistical Generalization Audit

## Final Scientific Decision: **A) TEMPORAL DELTA ADVANTAGE STATISTICALLY SUPPORTED**
## Audit Status: **FEATURE 8.7.1 — PASS (AUDIT VALIDATED)**

---

## 1. Upstream Checksum Verification
**PASS** — All upstream Feature 8.7-A, 8.7-B, 8.6, 8.5, 8.4.1, 8.3, and 8.2.2 artifacts verified intact.

---

## 2. Exact Common Test Population Verification
- **Test set size**: 1226 samples
- **Duplicate IDs**: 0
- **Coordinate NaN**: 0
- **Target mismatches**: 0
- **Positive count**: 188 (15.3% prevalence)

[OK] **100% exact alignment confirmed** across all three models.

---

## 3. Metric Reconstruction (Independent)

| Metric | Raw Temporal CNN | Delta Temporal CNN | 2025 Spatial Control |
|---|---|---|---|
| **PR-AUC** | 0.1453 | **0.3791** | 0.2429 |
| **ROC-AUC** | 0.4890 | **0.7258** | 0.6174 |
| **F1** | 0.0892 | **0.3232** | 0.2728 |
| **Precision** | 0.1111 | 0.2052 | 0.1589 |
| **Recall** | 0.0745 | **0.7606** | 0.9628 |
| **Balanced Accuracy** | 0.4833 | **0.6135** | 0.5199 |
| **TN / FP / FN / TP** | 926/112/174/14 | 484/554/45/143 | 80/958/7/181 |
| **Threshold** | 0.35 | 0.1 | 0.05 |

Metrics reconstruct identically to Feature 8.7-B reported values. [OK]

---

## 4. Threshold Audit
All thresholds selected using **validation data only**. [OK] All match.

---

## 5. Primary Paired Comparison (Identical N=1226 population)

| Metric | Delta − Control |
|---|---|
| **PR-AUC difference** | **+0.1362** |
| **F1 difference** | +0.0504 |
| **Balanced Accuracy difference** | **+0.0935** |
| **Precision difference** | +0.0463 |
| **Recall difference** | -0.2021 |

---

## 6. Spatial-Group-Aware Bootstrap (N=1,000 resamples)

| Metric | Mean Difference | 95% CI | Excludes Zero |
|---|---|---|---|
| **PR-AUC (Δ − Control)** | **0.1255** | **[0.0185, 0.2798]** | **YES [OK]** |
| F1 (Δ − Control) | 0.0586 | [-0.0065, 0.1773] | NO |
| Balanced Acc (Δ − Control) | 0.0994 | [-0.0064, 0.2324] | NO |

**The 95% CI for PR-AUC difference [0.0185, 0.2798] excludes zero.**

---

## 7. Population Shift Analysis
- Feature 8.3 test: N=8,121 — Prevalence=15.6%
- Feature 8.7 test: N=1226 — Prevalence=15.3%
- **5-year completeness filter did NOT materially shift positive prevalence** (≈15.3% vs 15.6%). The smaller N is caused by the stricter multi-year data requirement, not population cherry-picking.

---

## 8. Project-Wise Results

| Project | N | Positives | Model | PR-AUC | F1 |
|---|---|---|---|---|---|
| MH-001 | 547 | 128 | Raw Temporal | 0.2300 | 0.1275 |
| MH-001 | 547 | 128 | **Delta Temporal** | **0.5106** | **0.4961** |
| MH-001 | 547 | 128 | Spatial Control | 0.3699 | 0.3797 |
| MH-002 | 594 | 60 | Raw Temporal | 0.0779 | 0.0194 |
| MH-002 | 594 | 60 | **Delta Temporal** | **0.1154** | **0.1891** |
| MH-002 | 594 | 60 | Spatial Control | 0.0803 | 0.1885 |
| MH-003 | 85 | 0 | All models | N/A | 0.0000 |

---

## 9. Spatial-Block Analysis
- **Blocks with positives evaluated**: 8
- **Delta wins**: **7 / 8** blocks (88%)
- **Control wins**: 1 blocks
- **Ties**: 0 blocks
- **Zero-positive blocks (skipped)**: 4

The Delta advantage is **broad-based**, winning in the majority of spatial blocks.

---

## 10. Feature 8.3 Comparison (CONDITIONAL)
| | Feature 8.3 Spatial CNN | Feature 8.7-B Delta CNN |
|---|---|---|
| PR-AUC | 0.1977 | **0.3791** |
| Test N | 8,121 | 1,226 |

**CONDITIONAL COMPARISON**: Test populations differ. Direct numeric comparison is not valid without identical sample populations.

---

## 11. Cross-Project Generalization Claim
Feature 8.7-B does **NOT** establish temporal cross-project generalization. Feature 8.6 established this for the spatial CNN only.
-> **Recommended next step: Feature 8.7-C — Leave-One-Project-Out Temporal CNN Generalization**

---

## 12. Final Integrity Checklist
All 22 audit checks: **PASS**

---

## 13. Scientific Disclaimer
The model predicts spatial-spectral patterns associated with historical Feature 7.2 disturbance-candidate labels. It does **NOT** establish illegal activity, environmental non-compliance, causality, intent, or confirmed land-use change.
