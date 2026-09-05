# Feature 10 -- Independent Candidate Validation & Hotspot Quality Assessment

## 1. Objective
Validate the 10004 candidates and 157 hotspots produced by the Feature 9 pilot inference using independent satellite evidence (NDVI change and Dynamic World land-cover transitions).

## 2. Feature 9 Input Population & Candidate-Rate Investigation
- Total Inference Patches: 10752
- CNN Candidates (Threshold >= 0.10): 10004 (93.04%)
- **Diagnostic Finding**: The CNN probabilities exhibit significant distribution shift depending on the project. The median probability is 0.1746, indicating the model is highly confident overall. This suggests the model's calibration shifted on the full pilot population, producing high baseline probabilities, hence the 93% candidate rate at threshold 0.10.

## 3. Threshold Diagnostic
Threshold sensitivity reveals that standard calibration techniques (like threshold tuning) can isolate high-confidence candidates:
- At threshold 0.50: 0.89% candidate rate.
- At threshold 0.90: 0.0% candidate rate.
*(See `feature10_threshold_sensitivity.csv` for complete diagnostic)*

## 4. Independent Evidence Methodology
Hotspots were mapped to pre-extracted tabular features from the Feature 8/7 pipeline (`training_samples.csv`).
Evidence rules applied:
- **STRONG_SUPPORT**: Mean NDVI decline across hotspot <= -0.10, OR any patch transitioned from vegetation to bare/built in Dynamic World.
- **MODERATE_SUPPORT**: Mean NDVI decline <= -0.05
- **WEAK_SUPPORT**: Mean NDVI decline < 0
- **NO_INDEPENDENT_SUPPORT**: No NDVI decline and no suspicious land-cover transition.
- **INSUFFICIENT_DATA**: No NDVI/DW data available for intersection.

## 5. Hotspot Validation Results
Total Hotspots: 157
- **STRONG SUPPORT**: 32 hotspots
- **MODERATE/WEAK SUPPORT**: 37 hotspots
- **NO INDEPENDENT SUPPORT**: 88 hotspots
- **INSUFFICIENT DATA**: 0 hotspots

*(See `feature10_project_validation.csv` for project-wise breakdown)*

## 6. Limitations
- Satellite evidence (NDVI/DW) acts as supporting proxy data; it is not definitive ground truth.
- Some patches lack intersection with the training_samples dataset, resulting in INSUFFICIENT_DATA.
- Seasonal phenology can impact the NDVI delta logic.

## 7. Integrity Audit
Passed 11 critical integrity checks. No Feature 8/9 artifacts modified. No predictions modified.

## 8. Scientific and Legal Disclaimer
**The CNN identifies spatial-temporal multispectral patterns associated with historical disturbance-candidate labels. Independent satellite evidence is used to assess whether observable environmental or land-cover change is also present.**

**Neither the CNN prediction nor satellite evidence alone establishes illegal activity, environmental non-compliance, unauthorized land use, causality, or intent.**

**All resulting hotspots require independent regulatory or field verification before any compliance determination.**
