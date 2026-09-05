# Feature 8.8 -- Final Model Selection & Evidence Consolidation

## Selected Model: **Delta Temporal CNN (Feature 8.7-B)**
## Deployment Readiness: **B) READY FOR LIMITED RESEARCH/PILOT INFERENCE**
## Status: **FEATURE 8.8 -- PASS (COMPLETE)**

---

## 1. Upstream Checksum Summary
13 of 13 manifests verified PASS.
All checksums intact.

---

## 2. Master Model Comparison

| Model | Feature | PR-AUC | F1 | Bal.Acc | Comparability |
|---|---|---|---|---|---|
| Logistic Regression | 8.1 | 0.1563 | 0.0047 | 0.5008 | DIRECT (N=8,121) |
| Random Forest | 8.1 | 0.1641 | 0.0047 | 0.5008 | DIRECT (N=8,121) |
| XGBoost (Tabular) | 8.1 | 0.1565 | 0.0047 | 0.5008 | DIRECT (N=8,121) |
| Compact Spatial CNN | 8.3 | 0.1977 | 0.2834 | 0.5467 | DIRECT (N=8,121) |
| Raw Temporal CNN | 8.7-B | 0.1453 | 0.0892 | 0.4833 | CONDITIONAL (N=1,226) |
| Spatial-Only Control | 8.7-B | 0.2429 | 0.2728 | 0.5199 | CONDITIONAL (N=1,226) |
| **Delta Temporal CNN** | **8.7-B** | **0.3791** | **0.3232** | **0.6135** | CONDITIONAL (N=1,226) |

> **Note**: DIRECT comparisons share the F8.4 common population (N=8,121).
> CONDITIONAL comparisons use F8.7 temporal population (N=1,226, complete 5-yr sequences only).
> Numeric PR-AUC values CANNOT be directly compared across DIRECT and CONDITIONAL rows.

---

## 3. Direct vs Conditional Comparisons

### DIRECT (valid numeric comparison)
- **Spatial CNN > XGBoost > RF > LR** on F8.4 common population (N=8,121) [validated F8.4.1]
- **Delta CNN > Spatial Control** on F8.7 temporal test (N=1,226) [bootstrap CI [0.0185,0.2798], excludes zero, validated F8.7.1]

### CONDITIONAL (different populations -- interpret with caution)
- **Delta CNN vs Spatial CNN across LOPO projects**: Temporal beats Spatial on 2/3 projects. F8.6 and F8.7-C use different sample sets (5-yr filter). Not a global superiority claim.
- **Delta CNN (N=1,226) vs Spatial CNN (N=8,121)**: PR-AUC 0.3791 vs 0.1977 -- CANNOT be compared directly.

---

## 4. Cross-Project Evidence (Feature 8.7-C LOPO)

| Held-Out | Delta CNN PR-AUC | XGBoost PR-AUC | Spatial CNN PR-AUC | Delta>XGB | Delta>Spatial |
|---|---|---|---|---|---|
| MH-001 | 0.2619 | 0.0910 | 0.2121 | YES | YES |
| MH-002 | 0.2654 | 0.1408 | 0.3381 | YES | **NO** |
| MH-003 | 0.4070 | 0.1145 | 0.1470 | YES | YES |

**Delta CNN beats XGBoost: 3/3** (CONFIRMED)
**Delta CNN beats Spatial CNN: 2/3** (CONDITIONAL comparison -- populations differ)

---

## 5. Temporal Evidence Summary (Feature 8.7.1)

- Standard temporal test population: N=1,226 (complete 5-yr non-monsoon sequences)
- Delta CNN PR-AUC: **0.3791** vs Spatial Control: **0.2429**
- Difference: **+0.1362**
- Bootstrap 95% CI: **[0.0185, 0.2798]** -- **EXCLUDES ZERO**
- Bootstrap resamples: 1,000 (spatial-group-aware)
- Spatial block wins: **7/8**
- **Conclusion**: Temporal delta (inter-annual spectral change) provides statistically supported discriminative signal on the F8.7 population. This evidence does NOT automatically apply to the F8.3 or F8.4 populations.

---

## 6. Evidence Matrix Summary

| Model | Predictive | Spatial Gen | Temporal Gen | Cross-Project | Statistical | Leakage-Safe |
|---|---|---|---|---|---|---|
| LR | WEAK | NE | NE | NE | WEAK | STRONG |
| RF | WEAK | NE | NE | NE | WEAK | STRONG |
| XGBoost | WEAK | MODERATE | NE | WEAK | MODERATE | STRONG |
| Spatial CNN | MODERATE | MODERATE | NE | MODERATE | MODERATE | STRONG |
| Raw Temporal | WEAK | WEAK | WEAK | NE | WEAK | STRONG |
| Spatial Control | MODERATE | NE | NE | NE | MODERATE | STRONG |
| **Delta Temporal** | MODERATE | MODERATE | **STRONG** | MODERATE | **STRONG** | STRONG |

---

## 7. Key Limitations

1. **MH-002**: Temporal CNN underperforms Spatial CNN (conditional comparison)
2. **Only 3 projects**: LOPO generalization is limited -- no formal cross-project significance test is valid with N=3
3. **5-year coverage requirement**: 579 centers (32% of F8.3 test) cannot be evaluated by temporal model
4. **Rule-derived labels**: Model replicates algorithmic label patterns, not confirmed ground-truth
5. **No field validation**: All performance estimates against proxy labels only
6. **Limited geographic scope**: 3 projects in same region -- environmental diversity unknown
7. **FP-dominated on MH-003**: 419 FP vs 159 TP -- screening mode, not precise detection

---

## 8. Final Recommendation

**SELECT MODEL:** Delta Temporal CNN (Feature 8.7-B)

**PRIMARY REASON:** Strongest validated cross-project generalization. Beats XGBoost on all 3 unseen projects. Temporal delta signal statistically supported by bootstrap CI excluding zero.

**STRONGEST EVIDENCE:** F8.7.1 bootstrap CI [0.0185, 0.2798] excludes zero. F8.7-C LOPO beats XGBoost 3/3.

**MAIN LIMITATION:** Requires complete 5-year non-monsoon Sentinel-2 coverage. Only 3 projects evaluated. MH-002 temporal result below Spatial CNN (conditional comparison).

**DEPLOYMENT STATUS:** B) READY FOR LIMITED RESEARCH/PILOT INFERENCE -- not for operational enforcement. Predictions require independent field/regulatory verification.

**SECONDARY RECOMMENDATION:** For areas lacking 5-year coverage, use Compact Spatial CNN (F8.3) which has the strongest evidence on the common population.

**NEXT SCIENTIFIC STEP:** Field validation on high-confidence Delta CNN predictions across all 3 projects. Expand to additional geographic regions before any operational use.

---

## 9. Scientific Disclaimer

The model predicts spatial-temporal multispectral patterns associated with rule-derived historical disturbance-candidate labels. It does NOT establish illegal activity, environmental non-compliance, unauthorized land use, causality, intent, or confirmed land-use change. All predictions must be treated as screening signals requiring independent regulatory or ground verification.
