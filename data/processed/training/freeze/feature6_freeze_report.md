# Feature 6 — Final Dataset Freeze Report

### Status: **FROZEN / PASS**

* **Audit Timestamp**: 2026-08-23T23:28:45+05:30
* **Feature**: Feature 6 — Real LULC Reference Dataset Preparation
* **CNN Training Status**: **NOT TRAINED**

---

### 1. Verification Checklist Summary

| Check ID | Verification Parameter | Expected Value | Measured Value | Result |
|---|---|---|---|---|
| **1** | Dataset Row Count | `79,406` | `79,406` | **PASS** |
| **2** | Unique Spatial Locations | `17,540` | `17,540` | **PASS** |
| **3** | Dynamic World Min Confidence | `>= 0.60` | `0.60` (Count < 0.60: `0`) | **PASS** |
| **4** | Historical Years Included | `2021–2025` | `[2021, 2022, 2023, 2024, 2025]` | **PASS** |
| **5** | Excluded Future Period | No `2026` | 2026 Count: `0` | **PASS** |
| **6** | Seasonal Filtering | `Jan–May & Nov–Dec` | `Jan–May & Nov–Dec` | **PASS** |
| **7** | Spatial Split Consistency | `0` Inconsistent Coords | `0` Inconsistent Coords | **PASS** |
| **8** | Buffer Samples in CSV | `0` Buffer Samples | `0` Buffer Samples | **PASS** |
| **9** | $15 \times 15$ Patch Safety | $\ge 210\text{m}$ Min Dist | `MH-001`: 391.9m, `MH-002`: 678.3m, `MH-003`: 1070.8m | **PASS** |
| **10** | Duplicate Audit | `0` Duplicates | Spatio-Temporal: `0`, Sample_ID: `0` | **PASS** |

---

### 2. Class Distribution (Frozen Snapshot)

* **Vegetation (Class 0)**: `76,888` samples
* **Built-up (Class 2)**: `2,309` samples
* **Bare Land (Class 1)**: `209` samples
* **Total Observations**: `79,406` samples

---

### 3. SHA-256 Checksum Manifest (`feature6_checksums_sha256.csv`)

| Filename | Size (Bytes) | SHA-256 Checksum |
|---|---|---|
| `training_samples.csv` | `14,434,643` | `812d09f720ef0c03070d4d25a42c9f41e2a0a965dda02e745415e740a87e8db1` |
| `class_availability_audit.csv` | `6,147` | `973dadcee8408467e851cfe463a868f478ce5a1f2b66cd6b6ed378819aa1469e` |
| `bare_land_pipeline_trace.csv` | `62,797` | `3fc136c6c7b12bb59503339b536456fa598c9fc4f8948d2648df68f256f18224` |
| `spatial_temporal_validation.csv` | `382` | `c1e205b7eb421be856fb1a51e8b3ce2da6a57967663c897725e6e218d48987ab` |
| `spatial_split_audit.csv` | `4,179` | `c46f86193a4fc7ab751b7020d025db47e7472511d05788d39bcf79b59701c3c8` |
| `class_distribution_audit.csv` | `4,398` | `77e52f1a456cd3b51093b59f72b21e88f521bfe6627aff02f79990e4c05a5873` |
