# Feature 7.2 — Historical Change Signal & Disturbance Candidate Detection Report

### Final Status: **PASS — candidate baseline established**

* **Audit Timestamp**: 2026-08-23T23:37:30+05:30
* **Feature**: Feature 7.2 — Historical Change Signal & Disturbance Candidate Detection
* **Feature 6 Checksum Status**: **PASS (100% Uncorrupted & Immutable)**
* **CNN Model Training Status**: **NOT TRAINED**

---

### IMPORTANT SCIENTIFIC SAFETY DISCLAIMER

> **This system identifies statistically unusual spectral change candidates. It does NOT establish causality, illegal activity, environmental violation, or confirmed land-use change.**
> Candidates represent empirical multi-spectral anomalies relative to historical project baseline distributions requiring downstream validation.

---

### 1. Input Verification Summary

* **Feature 6 SHA-256 Checksums**: Verified **100% PASS** (Zero modification of `training_samples.csv` or freeze artifacts).
* **Upstream Protection**: `data/raw/`, `data/processed/satellite/`, `data/processed/project_boundaries/`, `data/processed/vegetation/`, `data/processed/training/` remain 100% read-only.
* **Temporal Window**: Historical baseline transitions (2021$ightarrow$2022, 2022$ightarrow$2023, 2023$ightarrow$2024, 2024$ightarrow$2025). 2026 and monsoon months (June–October) strictly excluded.

---

### 2. Disturbance Candidate Summary by Project

| Project ID | Project Name | Normal Pixels | Single Signal Anomaly Pixels | Multi-Spectral Candidate Pixels | Persistent Multi-Year Candidate Pixels | Total Candidate Area (ha) | Spatial Clusters |
|---|---|---|---|---|---|---|---|
| `MH-001` | Gondkhari | 16,965 | 0 | **996** | **255** | **112.59 ha** | **161** |
| `MH-002` | Gadchiroli | 25,896 | 0 | **1,475** | **121** | **143.64 ha** | **220** |
| `MH-003` | Bhivpuri PSP | 34,322 | 0 | **243** | **0** | **21.87 ha** | **5** |

---

### 3. Spatial Clustering Summary

* **Spatial Clustering Criteria**: Contiguous Candidate Pixel Grouping (8-neighbor connection). Disconnected areas are never merged.
* **Total Candidate Clusters Identified**: **386 clusters** across all 3 projects.

---

### 4. Source & Upstream Immutability Verification

* **`data/raw/`**: Unmodified (**PASS**)
* **`data/processed/satellite/`**: Unmodified (**PASS**)
* **`data/processed/project_boundaries/`**: Unmodified (**PASS**)
* **`data/processed/vegetation/`**: Unmodified (**PASS**)
* **`data/processed/training/`**: Unmodified (**PASS**)
* **Feature 6 Checksums**: Verified **100% PASS**

---

### 5. Final Status Logic

**Final Feature 7.2 Status**: **PASS — candidate baseline established**
