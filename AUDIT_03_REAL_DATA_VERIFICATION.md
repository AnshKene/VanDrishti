# AUDIT 03: Real Satellite Data Verification

**Audit Date**: August 2026  
**Auditor**: Forensic Truth Audit Subsystem  
**Scope**: Inspection of all 135 GeoTIFF satellite files in the repository.

---

## 1. Overview of Satellite Rasters

Across the repository, exactly **135 GeoTIFF files** (15.77 MB) were inventoried and inspected using `rasterio` and `numpy`:
- **Multiband Sentinel-2 L2A Rasters**: 18 files (6 bands each: Blue, Green, Red, NIR, SWIR-1, SWIR-2; 2021–2026 across MH-001, MH-002, MH-003).
- **Dynamic World Annual Mode Rasters**: 18 files (1 band categorical: 2021–2026 across MH-001, MH-002, MH-003).
- **NDVI Rasters**: 18 files (1 band floating point: 2021–2026 across MH-001, MH-002, MH-003).
- **Spectral Delta & Index Rasters (NDVI, NDWI, NDBI)**: 66 files.
- **Candidate Grids**: 15 files.

---

## 2. Forensic Statistical Inspection of Multiband Sentinel-2 Rasters

Every multiband Sentinel-2 GeoTIFF was opened and analyzed for authenticity (checking for constant arrays, synthetic uniform distributions, invalid coordinates, or corrupted nodata values):

| Project | Year | Bands | Width × Height | CRS | Bounds [minx, miny, maxx, maxy] | Data Range (Min - Max) | Mean Value | Std Dev | Is Real? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MH-001** | 2021 | 6 | 453 × 581 | EPSG:32644 | [282860, 2337600, 287390, 2343410] | 0.0 – 3078.5 | 694.3 | 362.1 | **REAL** |
| **MH-001** | 2022 | 6 | 453 × 581 | EPSG:32644 | [282860, 2337600, 287390, 2343410] | 0.0 – 3375.3 | 682.1 | 358.4 | **REAL** |
| **MH-001** | 2023 | 6 | 453 × 581 | EPSG:32644 | [282860, 2337600, 287390, 2343410] | 0.0 – 3251.2 | 701.4 | 371.8 | **REAL** |
| **MH-001** | 2024 | 6 | 453 × 581 | EPSG:32644 | [282860, 2337600, 287390, 2343410] | 0.0 – 3304.3 | 710.2 | 366.5 | **REAL** |
| **MH-001** | 2025 | 6 | 453 × 581 | EPSG:32644 | [282860, 2337600, 287390, 2343410] | 0.0 – 3764.3 | 725.8 | 380.2 | **REAL** |
| **MH-001** | 2026 | 6 | 453 × 581 | EPSG:32644 | [282860, 2337600, 287390, 2343410] | 0.0 – 3962.0 | 734.1 | 385.6 | **REAL** |
| **MH-002** | 2021 | 6 | 557 × 504 | EPSG:32644 | [429870, 2165070, 435440, 2170110] | 0.0 – 1287.0 | 482.3 | 215.7 | **REAL** |
| **MH-002** | 2022 | 6 | 557 × 504 | EPSG:32644 | [429870, 2165070, 435440, 2170110] | 0.0 – 1359.0 | 490.1 | 219.4 | **REAL** |
| **MH-002** | 2023 | 6 | 557 × 504 | EPSG:32644 | [429870, 2165070, 435440, 2170110] | 0.0 – 1427.0 | 487.6 | 218.1 | **REAL** |
| **MH-002** | 2024 | 6 | 557 × 504 | EPSG:32644 | [429870, 2165070, 435440, 2170110] | 0.0 – 2642.0 | 512.4 | 242.0 | **REAL** |
| **MH-002** | 2025 | 6 | 557 × 504 | EPSG:32644 | [429870, 2165070, 435440, 2170110] | 0.0 – 2348.5 | 508.9 | 238.6 | **REAL** |
| **MH-002** | 2026 | 6 | 557 × 504 | EPSG:32644 | [429870, 2165070, 435440, 2170110] | 0.0 – 2115.0 | 499.2 | 231.5 | **REAL** |
| **MH-003** | 2021 | 6 | 694 × 491 | EPSG:32643 | [335830, 2090880, 342770, 2095790] | 0.0 – 1931.5 | 554.8 | 291.3 | **REAL** |
| **MH-003** | 2022 | 6 | 694 × 491 | EPSG:32643 | [335830, 2090880, 342770, 2095790] | 0.0 – 2035.5 | 561.2 | 295.0 | **REAL** |
| **MH-003** | 2023 | 6 | 694 × 491 | EPSG:32643 | [335830, 2090880, 342770, 2095790] | 0.0 – 1977.5 | 558.1 | 292.8 | **REAL** |
| **MH-003** | 2024 | 6 | 694 × 491 | EPSG:32643 | [335830, 2090880, 342770, 2095790] | 0.0 – 2184.0 | 572.6 | 304.1 | **REAL** |
| **MH-003** | 2025 | 6 | 694 × 491 | EPSG:32643 | [335830, 2090880, 342770, 2095790] | 0.0 – 2324.5 | 580.4 | 311.7 | **REAL** |
| **MH-003** | 2026 | 6 | 694 × 491 | EPSG:32643 | [335830, 2090880, 342770, 2095790] | 0.0 – 2558.0 | 589.1 | 318.4 | **REAL** |

---

## 3. Forensic Test Results

1. **Synthetic / Mock Data Check**:  
   - **0 out of 135 files** contain constant, uniform, or synthetic mock values.
   - Values represent true surface reflectance scaled by $10^4$ (typical Copernicus Sentinel-2 L2A surface reflectance ranges from 0 to 4000).
2. **Coordinate Alignment Check**:  
   - Geographic bounding boxes align exactly with the project UTM projections (Zone 44N for Gondkhari and Gadchiroli, Zone 43N for Bhivpuri).
   - Pixel spatial resolution is exactly **10 meters** ($10.0 \times 10.0$ m ground sampling distance).
3. **Temporal Coverage**:  
   - 2021–2025 non-monsoon composites are complete across all 3 projects.
   - 2026 data is present but was excluded from Feature 8.7 training/evaluation due to partial annual coverage.
4. **Current Dashboard Integration Status**:  
   - **Important Finding**: While real Sentinel-2 GeoTIFF files exist in `data/processed/satellite/`, they are **NOT yet directly served as raster imagery layers in the web dashboard**. The dashboard currently displays the OSM/Carto basemap with overlaid vector boundaries and hotspot markers. Feature 12-C.4 is specifically scoped to implement satellite basemap visualization.
