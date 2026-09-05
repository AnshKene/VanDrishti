# Feature 9 -- Delta Temporal CNN Pilot Inference & Spatial Hotspot Generation

## 1. Objective
Build a reproducible pilot inference pipeline using the frozen Delta Temporal CNN (Feature 8.7-B) to identify spatial-temporal disturbance candidates.

## 2. Model & Checkpoint
- **Model Used**: Delta Temporal CNN (CompactTemporalCNN, time_steps=4, in_channels=6)
- **Model Checkpoint**: `data/processed/modeling/temporal_spatial_cnn/model/temporal_cnn_delta.pth`

## 3. Input Representation & Temporal Construction
- **Input Representation**: 4x15x15x6 inter-annual spectral delta patches (Sentinel-2, non-monsoon).
- **Temporal Construction**: `delta_t = reflectance_(t+1) - reflectance_t` computed exactly as in Feature 8.7-B.
- **Preprocessing**: Frozen means and standard deviations loaded from Feature 8.7-B metadata.

## 4. Inference Configuration
- **Threshold Source**: Validation-derived operating threshold from Feature 8.7-B (`temporal_cnn_test_metrics.csv`).
- **Operating Threshold**: 0.1
- **Number of Inference Samples**: 10752 (Complete 5-year sequences only)

## 5. Project-Wise Results
| Project | Inference Patches | Candidates | % Candidate | Max Prob | Hotspots |
|---|---|---|---|---|---|
| MH-001 | 2424 | 2345 | 96.74% | 0.4636 | 73 |
| MH-002 | 7549 | 7216 | 95.59% | 0.625 | 28 |
| MH-003 | 779 | 443 | 56.87% | 0.2165 | 56 |

## 6. Hotspot Statistics
- Total spatial hotspots generated: **157**
- Grouping algorithm: DBSCAN (eps=1.5 patches, chebyshev distance, identifying 8-connected patch groups)
- Properties extracted: Patch count, Mean Probability, Max Probability, Priority Score, Centroid

## 7. Integrity Checks
All checks passed:
- No spatial leakage, 2026 data, or monsoon data present.
- Preprocessing matches frozen pipeline exactly.
- Probabilities rigorously bounded `[0,1]`.
- No upstream frozen artifacts modified.

## 8. Limitations
- Inference is limited to the 10752 samples with complete 2021-2025 non-monsoon sequences. 579 centers with incomplete sequences are implicitly excluded.
- Candidate priority scores provide internal relative ranking only.

## 9. Scientific and Legal Disclaimer
**IMPORTANT: This pilot inference identifies spatial-temporal multispectral patterns associated with historical disturbance-candidate labels. The resulting candidates require independent verification and must not be interpreted as confirmed environmental non-compliance, unauthorized land use, or confirmed illegal activity.**

## 10. Execution Status
- **Exact Execution Command**: `python scratch/run_feature9_pilot_inference.py`
- **Final Status**: **PASS (PILOT INFERENCE COMPLETED)**
