# AUDIT 05: Training Labels, Ground Truth & Scientific Validity

**Audit Date**: August 2026  
**Auditor**: Forensic Truth Audit Subsystem  
**Scope**: In-depth inspection of label generation, ground-truth provenance, leakage risks, and circular validation.

---

## 1. How Were Training Labels Generated?

Code inspection of `src/candidate_detection.py`, `src/disturbance_baseline.py`, and `src/lulc_dataset.py` reveals the exact mechanism:

1. **Source Data for Labels**:
   - Sentinel-2 multi-spectral bands across 4 historical annual intervals (2021→2022, 2022→2023, 2023→2024, 2024→2025).
   - Derived spectral indices: NDVI (vegetation), NDBI (built-up/bare soil), NDWI (water/moisture).
2. **Deterministic Percentile Heuristic**:
   - For each project, pooled historical delta distributions were calculated.
   - **Anomaly Thresholds**:
     - $\Delta \text{NDVI} \le p_{05}$ (extreme vegetation loss)
     - $\Delta \text{NDBI} \ge p_{95}$ (extreme bare/built-up increase)
     - $\Delta \text{NDWI} \le p_{05}$ or $\ge p_{95}$ (extreme moisture anomaly)
3. **Category Assignment**:
   - **Category 3**: Persistent Multi-Year Candidate ($\ge 2$ multi-spectral transitions).
   - **Category 2**: Single-Transition Multi-Spectral Candidate ($= 1$ multi-spectral transition).
   - **Category 1**: Single Spectral Anomaly Signal.
   - **Category 0**: Normal / No Anomaly.
4. **Binary Target Formulation**:
   $$y = \begin{cases} 1 & \text{if } \text{Category} \in \{2, 3\} \\ 0 & \text{if } \text{Category} \in \{0, 1\} \end{cases}$$

---

## 2. Critical Scientific Findings

### A. Surrogate Proxy Nature (Brutal Honesty)
- **No Human Ground-Truth Annotations**: Training labels were **NOT** derived from physical on-site field surveys, forest department ground logs, or regulatory non-compliance citations.
- **Surrogate Classifier**: The ML models (Tabular XGBoost, Spatial CNN, Delta Temporal CNN) are **surrogate statistical classifiers trained to emulate a deterministic multi-spectral change rule**.
- **What the Model Actually Learns**: The Delta Temporal CNN learns the spatiotemporal reflectance patterns that predict whether a patch satisfies the heuristic percentile cutoff rules.

### B. Circular Validation Risk in Feature 10
- In Feature 10 ("Independent Candidate Validation"), candidate hotspots are evaluated against:
  1. Mean NDVI slope trajectory ($\Delta \text{NDVI}$).
  2. Dynamic World categorical transitions (vegetation $\rightarrow$ bare/built).
- **Assessment**: Because the candidate patches and training targets were originally defined using spectral index thresholds (including NDVI), downstream validation using NDVI is **partially circular proxy corroboration**, NOT an independent external ground-truth validation.
- While Dynamic World incorporates a separate global Google/WRI model, it is also optical satellite-derived proxy data.

### C. Scientific Claim Boundaries
- The CNN outputs represent a **candidate screening and spatial-temporal ranking signal**.
- **It is scientifically invalid to claim environmental violations, unauthorized mining, illegal deforestation, or compliance breach based on these predictions alone.**

---

## 3. Leakage and Contamination Audit

- **Spatial Coordinate Leakage**: Latitude, longitude, and explicit project IDs were excluded from input feature tensors ($X$).
- **Temporal Contamination**: 2026 data was strictly excluded from training and validation.
- **Normalization Leakage**: Means and standard deviations were computed exclusively on `temporal_delta_train.npz` ($N=8,534$) and applied outward to validation and test tensors.
- **Data Leakage Verdict**: **PASS** (Engineering leakage is cleanly avoided; the primary limitation is domain-level proxy label formulation).
