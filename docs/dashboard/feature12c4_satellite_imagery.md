# Feature 12-C.4: Real Year-Wise Satellite Imagery Map Layer (Tiled Raster Architecture)

**Feature Status**: **PASS**  
**Implementation Scope**: Real-Time Web Mercator XYZ Tiled Raster Projection (`rasterio.warp.reproject` to EPSG:3857) & MapLibre Vector/Raster Layer Integration  
**Date**: August 2026  

---

## 1. Discovered Source Satellite Rasters & Metadata

All satellite rasters in `data/processed/satellite/` were inventoried directly from disk:
- **Total Satellite GeoTIFF Files**: 18 multiband files (3 projects $\times$ 6 observation years: 2021, 2022, 2023, 2024, 2025, and 2026 reference year).
- **Sensor**: Sentinel-2 Surface Reflectance (Harmonized, Copernicus).
- **Composite Method**: Seasonal Median Composite (Dry Season: Jan–May & Nov–Dec), with Scene Classification Layer (SCL) cloud/shadow masking.
- **Band Descriptions / Mapping**:
  - Band 1: `B2` (Blue, 490 nm)
  - Band 2: `B3` (Green, 560 nm)
  - Band 3: `B4` (Red, 665 nm)
  - Band 4: `B8` (Near-Infrared, 842 nm)
  - Band 5: `B11` (Short-Wave Infrared 1, 1610 nm)
  - Band 6: `B12` (Short-Wave Infrared 2, 2190 nm)

---

## 2. Forensic Raster Metrics & Project Alignment

| Project ID | Project Name | Observation Years | Source Dimensions ($W \times H$) | Native Resolution | CRS | Geographic Bounds [minX, minY, maxX, maxY] | Boundary Coverage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MH-001** | Gondkhari Underground Coal Mine | 2021–2026 | $104 \times 183$ px | $\approx 29.8\text{ m}$ ($0.00026949^\circ$) | `EPSG:4326` | `[78.912596, 21.132687, 78.940623, 21.182005]` | **100% OVERLAP (PASS)** |
| **MH-002** | Gadchiroli Iron Ore Mine | 2021–2026 | $184 \times 157$ px | $\approx 29.8\text{ m}$ ($0.00026949^\circ$) | `EPSG:4326` | `[80.332832, 19.583094, 80.382419, 19.625404]` | **100% OVERLAP (PASS)** |
| **MH-003** | Bhivpuri Pumped Storage Project | 2021–2026 | $233 \times 154$ px | $\approx 29.8\text{ m}$ ($0.00026949^\circ$) | `EPSG:4326` | `[73.442395, 18.908279, 73.505187, 18.949781]` | **100% OVERLAP (PASS)** |

---

## 3. Tiled Raster Architecture (Web Mercator XYZ)

- **Tile Endpoint**: `GET /api/satellite/{project_id}/{year}/tiles/{z}/{x}/{y}.png`
- **Dynamic Reprojection**: On request, reprojects source GeoTIFF bands (B4 Red, B3 Green, B2 Blue) from `EPSG:4326` into `EPSG:3857` (Web Mercator) for the exact $(z, x, y)$ tile bounding box using bilinear resampling.
- **Contrast Stretch**: Linear scaling from $[0, 2800]$ surface reflectance units to $[0, 255]$ 8-bit RGBA.
- **Nodata Handling**: Outside the project raster boundary, pixels have alpha 0 (transparent PNG), preventing any rectangular white border artifacts.
- **MapLibre Integration**: Uses standard MapLibre `raster` tile source (`tileSize: 256`, `minzoom: 8`, `maxzoom: 19`) allowing continuous pan, zoom, and multi-layer vector overlays.

---

## 4. Verification Summary

1. **Automated Unit Tests**: `python -m pytest dashboard/backend` -> **18/18 PASS** (including tile generator and boundary verification).
2. **Frontend Type Check & Build**: `tsc -b && vite build` -> **0 TypeScript errors, build PASS**.
3. **Artifact Integrity**: `python scratch/verify_checksums.py` -> **100% MATCH (0 mutations to frozen artifacts)**.
4. **Live Tile Verification**: `python scratch/test_all_tiles.py` -> **18/18 project/year combinations return authentic distinct PNG tiles (PASS)**.
5. **Scientific Disclaimer**: Permanent footer on all map views explicitly stating Sentinel-2 visual observations are proxy context and CNN detections are candidate ranking signals.

