# Feature 7.2 — Final Read-Only Dataset Freeze Report

### Final Status: **FROZEN / PASS**

* **Audit Timestamp**: 2026-08-23T23:43:00+05:30
* **Feature**: Feature 7.2 — Historical Change Signal & Disturbance Candidate Detection
* **Feature 6 Checksum Status**: **PASS (100% Uncorrupted & Immutable)**
* **CNN Training Status**: **NOT TRAINED**

---

### 1. Verification Checklist Summary

| Check ID | Verification Parameter | Expected Value | Measured Value | Result |
|---|---|---|---|---|
| **1** | Feature 7.2 CSV Outputs | 5 Files Exist | All 5 CSVs Exist & Readable | **PASS** |
| **2** | Candidate GeoTIFF Rasters | 15 Rasters Exist | All 15 GeoTIFF Rasters Exist | **PASS** |
| **3** | Category Sum Equality | $\text{Cat 0} + \text{Cat 1} + \text{Cat 2} + \text{Cat 3} = \text{Total}$ | Verified Equal for all Projects | **PASS** |
| **4** | Historical Temporal Scope | $2021–2025$ Baseline Only | $2021–2025$ Only ($2026$ = 0) | **PASS** |
| **5** | Spatial Polygon Masking | Polygon-Masked inside Boundary | Verified inside Validated GeoJSON | **PASS** |
| **6** | UTM Metric Area Calculation | $0.09\text{ ha/pixel}$ | Verified Area Calculation | **PASS** |
| **7** | Persistence Verification | Multi-Spectral $\ge 2$ Transitions | Verified persistence tracking | **PASS** |
| **8** | Threshold Provenance | Empirical Baseline Percentiles | $p_{05}$ NDVI, $p_{95}$ NDBI/NDWI | **PASS** |
| **9** | Data Quality & Integrity | 0 Inf / 0 Corrupted | 0 Inf / 0 Corrupted | **PASS** |
| **10** | Upstream Immutability | Feature 6 SHA-256 Manifest | Verified **100% PASS** | **PASS** |

---

### 2. Final Project Category Breakdown (`disturbance_candidates.csv`)

| Project ID | Project Name | Total Valid Pixels | Normal (Cat 0) | Single-Signal (Cat 1) | Multi-Spectral Candidate (Cat 2) | Persistent Candidate (Cat 3) | Candidate Area (ha) | Spatial Clusters |
|---|---|---|---|---|---|---|---|---|
| `MH-001` | Gondkhari | 9,581 | 5,790 | 2,540 | **996** | **255** | **112.59 ha** | **161** |
| `MH-002` | Gadchiroli | 10,417 | 5,896 | 2,925 | **1,475** | **121** | **143.64 ha** | **220** |
| `MH-003` | Bhivpuri PSP | 1,291 | 676 | 372 | **243** | **0** | **21.87 ha** | **5** |

---

### 3. SHA-256 Checksum Manifest (`feature7_2_checksums_sha256.csv`)

| Filename | Size (Bytes) | SHA-256 Checksum |
|---|---|---|
| `disturbance_candidates.csv` | `361` | `343d06992d7018c14b6c9cb3b4f711921477188e373e72a8f9a54bf3e04c202e` |
| `disturbance_candidate_clusters.csv` | `39,061` | `ca5068e9017c35b42bf5778060e1c9c22229ff88f8260899865e4fd09bede2b4` |
| `historical_change_distribution.csv` | `5,076` | `d93616e83206a810a2614532eb31a43974a9c35bf5b263b567e65a4335ddfd52` |
| `change_threshold_sensitivity.csv` | `1,350` | `79ff10f0abda5e86f9003dd3c4ddd67a60df9b45a662e4b10a085f94f34f072c` |
| `change_pixel_signals.csv` | `298,109` | `62a24c97ff355dfdd3b213aa00fad6ae5c7604a895b3df4915d64003551171fb` |
| `candidate_2021_2022.tif` | `18,606` | `92483c78151a25b97feebb58605d4315b38a9e4f9f5a14bb01b92ba57c844887` |
| `candidate_2022_2023.tif` | `18,606` | `28b18eea1376b15bde98b274356c56ad44277d5170877fbe309345e49a40de81` |
| `candidate_2023_2024.tif` | `18,606` | `a06813d2549c53d7a5d0bd60e764cd2ebf372617a09055191bcc7878abf0e7a2` |
| `candidate_2024_2025.tif` | `18,606` | `85fb039aeff42871f42f2575e25115cd481b219c48b4625566531efdcb6da6b7` |
| `persistent_candidate.tif` | `18,606` | `7e82b8eda00fa4454671e086721b81077fe760dd27c0505cfb57202123e76fd0` |
| `candidate_2021_2022.tif` | `27,888` | `b73933ee483d7bc6c45a1a593185e1b2688a678d408b01864f2cf23039c92aca` |
| `candidate_2022_2023.tif` | `27,888` | `194669346dcdbea1f8aaec105d09177d929c85d60fa9ef33952724d238062f6e` |
| `candidate_2023_2024.tif` | `27,888` | `60e1e8f413a96c7dab743fd9d16c3211dec86478894a84d899221e58f4de28a1` |
| `candidate_2024_2025.tif` | `27,888` | `68fd0bebfb9d93a946e9f0fb7ad7c9eb0be1983acb5d251838228c7e0315f2f9` |
| `persistent_candidate.tif` | `27,888` | `0b408eacf7d4963e40142d592e9432dd7995d013add9063b453e1f8a32dcba7d` |
| `candidate_2021_2022.tif` | `34,967` | `f4a06c9b963b52bbf338160a990a5b19599870d5934f5ec5548f0e0cb4198851` |
| `candidate_2022_2023.tif` | `34,967` | `1469c37796cc9829e1b07694fae5c948098e166f3308cb7c5cf54218b63805f6` |
| `candidate_2023_2024.tif` | `34,967` | `44403b2def43341e0199cbf34cfe6bbe5a480421076cb39aae7123f298309cf2` |
| `candidate_2024_2025.tif` | `34,967` | `37da08e182988a30edf474d77a58b3d63b6c6f5902e6930bdf9a936488b50f1f` |
| `persistent_candidate.tif` | `34,967` | `b8fb11ed147a2e25f0f8842ae043f93c630334a2632b7b53b89317c974a94461` |
