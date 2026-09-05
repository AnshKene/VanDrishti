# Feature 12-C.4: Regional Sentinel-2 Satellite Basemap Acquisition & Architecture Plan

**Document Version**: 1.0 (Planning & Architecture Only — No Code/Data Modifications)  
**Target Feature**: Feature 12-C.4 Correction (Continuous Year-Wise Satellite Basemap)  
**Date**: August 2026  
**Status**: DESIGN & PROPOSAL (Pending User Approval)

---

## 1. Current Limitation & Diagnostic Summary

A rigorous forensic audit established that:
1. **Authenticity**: The 18 local multiband GeoTIFFs (`data/processed/satellite/`) are authentic Sentinel-2 Surface Reflectance seasonal dry-season median composites across 2021–2026.
2. **Spatial Restriction**: The rasters are tightly cropped bounding boxes around individual mine/project boundaries:
   - **MH-001 (Gondkhari)**: $2.91\text{ km} \times 5.45\text{ km}$ ($104 \times 183\text{ px}$ at $\approx 29.8\text{ m/px}$)
   - **MH-002 (Gadchiroli)**: $5.20\text{ km} \times 4.68\text{ km}$ ($184 \times 157\text{ px}$ at $\approx 29.8\text{ m/px}$)
   - **MH-003 (Bhivpuri PSP)**: $6.61\text{ km} \times 4.59\text{ km}$ ($233 \times 154\text{ px}$ at $\approx 29.8\text{ m/px}$)
3. **Root Cause of Visible Boundary**: The current dashboard map viewport spans $\approx 15\text{–}30\text{ km}$ across at standard zoom levels (12–14). Because the source files contain zero satellite pixels outside the $3\text{–}6\text{ km}$ project perimeter, Web Mercator XYZ tiles render transparent everywhere outside the project bounding box. This creates an unavoidable rectangular patch when overlaid on OSM.
4. **Architectural Truth**: Tiled rendering (XYZ) is only a delivery protocol; it cannot create satellite observation data that was never collected. A continuous satellite basemap requires acquiring wider regional Sentinel-2 observations.

---

## 2. Required Satellite Coverage & Viewport Analysis

### Viewport Geometry Analysis
- **Standard Dashboard Project Viewport**:
  - Container width: $\sim 900\text{–}1500\text{ px}$, height: $\sim 400\text{–}800\text{ px}$.
  - Default initial zoom: level 12–13.
  - Geographic footprint at zoom 12: $\approx 18\text{ km (longitude)} \times 12\text{ km (latitude)}$.
  - Normal investigator pan radius: $\pm 10\text{ km}$ around project perimeter to observe surrounding drainage basins, haul roads, village settlements, and forest buffers.

---

## 3. Recommended Regional Areas of Interest (AOIs)

The three monitored projects are geographically distant across Maharashtra:
- **MH-001 $\leftrightarrow$ MH-002**: $\sim 230\text{ km}$ separation (Nagpur District vs. Gadchiroli District).
- **MH-001 $\leftrightarrow$ MH-003**: $\sim 670\text{ km}$ separation (Vidarbha vs. Konkan/Western Ghats).

A single statewide raster is computationally inefficient. Instead, **three dedicated regional AOIs** centered on each project provide optimal coverage with minimal data overhead.

### AOI Geometry Specifications (EPSG:4326)

| Project | Center Coordinate | Project Span | Buffer Applied | Regional AOI Bounding Box [minLon, minLat, maxLon, maxLat] | AOI Physical Dimensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MH-001** (Gondkhari Coal Mine) | $78.9265^\circ\text{E}, 21.1573^\circ\text{N}$ | $2.9 \times 5.4\text{ km}$ | $\approx 15\text{ km}$ | `[78.7500, 21.0000, 79.1000, 21.3000]` ($\approx 36.3\text{ km W} \times 33.2\text{ km H}$) | $\sim 1,205\text{ km}^2$ |
| **MH-002** (Gadchiroli Iron Ore) | $80.3576^\circ\text{E}, 19.6042^\circ\text{N}$ | $5.2 \times 4.7\text{ km}$ | $\approx 15\text{ km}$ | `[80.1800, 19.4500, 80.5400, 19.7600]` ($\approx 37.8\text{ km W} \times 34.3\text{ km H}$) | $\sim 1,296\text{ km}^2$ |
| **MH-003** (Bhivpuri PSP) | $73.4738^\circ\text{E}, 18.9290^\circ\text{N}$ | $6.6 \times 4.6\text{ km}$ | $\approx 15\text{ km}$ | `[73.3000, 18.7800, 73.6500, 19.0800]` ($\approx 36.9\text{ km W} \times 33.2\text{ km H}$) | $\sim 1,225\text{ km}^2$ |

*Rationale*: A $\sim 35\text{ km} \times 35\text{ km}$ extent provides complete coverage for zooms 12–18 during normal panning, without wasting bandwidth on empty regional expanses.

---

## 4. Year-Wise Acquisition Plan (2021–2026)

To maintain temporal integrity and ensure the year selector reflects real historical observations:

| Year | Role | Observation Window | Cloud Masking Protocol |
| :--- | :--- | :--- | :--- |
| **2021** | Operational Year | Jan 1 – May 31 & Nov 1 – Dec 31, 2021 | SCL Scene Classification (classes 3, 8, 9, 10 masked) + QA60 |
| **2022** | Operational Year | Jan 1 – May 31 & Nov 1 – Dec 31, 2022 | SCL Scene Classification (classes 3, 8, 9, 10 masked) + QA60 |
| **2023** | Operational Year | Jan 1 – May 31 & Nov 1 – Dec 31, 2023 | SCL Scene Classification (classes 3, 8, 9, 10 masked) + QA60 |
| **2024** | Operational Year | Jan 1 – May 31 & Nov 1 – Dec 31, 2024 | SCL Scene Classification (classes 3, 8, 9, 10 masked) + QA60 |
| **2025** | Operational Year | Jan 1 – May 31 & Nov 1 – Dec 31, 2025 | SCL Scene Classification (classes 3, 8, 9, 10 masked) + QA60 |
| **2026** | **Reference Period (Ref)** | Jan 1 – May 31, 2026 | SCL Scene Classification (classes 3, 8, 9, 10 masked) + QA60 |

*Strict Rule*: Every year must be processed independently. No temporal interpolation or cross-year sharing.

---

## 5. Sentinel-2 Processing Methodology

To maintain 100% scientific consistency with the existing Features 8–11 processing pipeline:
- **Source Collection**: `COPERNICUS/S2_SR_HARMONIZED` (Level-2A Bottom of Atmosphere Surface Reflectance).
- **Composite Statistic**: Pixel-wise **median** across cloud-free observations in the dry-season window.
- **Bands Included**:
  - `B4` (Red, 665 nm) — Native 10m
  - `B3` (Green, 560 nm) — Native 10m
  - `B2` (Blue, 490 nm) — Native 10m
  - *(Optional)* `B8` (NIR, 842 nm) for false-color vegetation inspection
- **Output Resolution**: Native **10 m grid** ($0.00008983^\circ$) or **20 m grid** ($0.00017966^\circ$).
- **CRS**: `EPSG:4326` (WGS 84).
- **Format**: Cloud-Optimized GeoTIFF (COG) with Deflate compression and internal overviews (pyramids).

---

## 6. Storage & Performance Estimates

### Data Sizing

| Resolution Mode | Dimensions per Regional AOI | File Size per GeoTIFF (Compressed COG) | Total 18 Files (3 Projects $\times$ 6 Years) | Tile Serving Latency |
| :--- | :--- | :--- | :--- | :--- |
| **Native 10 m** | $\approx 3,700 \times 3,700\text{ px}$ | $\sim 28\text{ MB}$ | **$\sim 504\text{ MB}$** | $\approx 10\text{–}15\text{ ms}$ / tile |
| **Optimized 20 m** | $\approx 1,850 \times 1,850\text{ px}$ | $\sim 8\text{ MB}$ | **$\sim 144\text{ MB}$** | $\approx 4\text{–}8\text{ ms}$ / tile |

### Dynamic vs. Pre-Generated Tile Serving Decision
- **Recommendation: Dynamic XYZ Tile Generation with In-Memory LRU Cache**.
- *Justification*:
  1. Total storage is small ($\le 500\text{ MB}$), easily fitting in standard local storage.
  2. Dynamic generation avoids pre-rendering and storing $>50,000$ individual PNG tile files on disk.
  3. Python `rasterio.warp.reproject` on a COG with internal pyramids generates a $256 \times 256$ Web Mercator tile in $<10\text{ ms}$.
  4. In-memory caching guarantees $0\text{ ms}$ latency on viewport revisits.

---

## 7. Preservation of Dual Data Roles (Strict Separation)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   SEPARATION OF SATELLITE DATA ROLES                             │
├────────────────────────────────────────┬─────────────────────────────────────────┤
│ ROLE A: Regional Basemap Layer         │ ROLE B: Project Analytical Rasters      │
│ Directory: data/processed/satellite_   │ Directory: data/processed/satellite/    │
│            regional/                   │ (FROZEN & IMMUTABLE)                    │
│ Extent: ~35 km × 35 km regional AOI    │ Extent: Exact project bounding box      │
│ Purpose: Continuous visual map context │ Purpose: Authoritative model input,     │
│          and natural pan/zoom          │          NDVI change, Dynamic World     │
│          basemap navigation            │          metrics, Feature 8-11 evidence │
└────────────────────────────────────────┴─────────────────────────────────────────┘
```

*Strict Guarantee*: Role A regional data will NEVER overwrite, modify, or replace Role B authoritative ML artifacts.

---

## 8. Target Google Earth-Style Visual Architecture

```
                  MapLibre Viewport
┌───────────────────────────────────────────────────┐
│ [ Map (OSM) ]  [ SATELLITE (Active) ]  [ Hybrid ] │
│ Year: [2021] [2022] [2023] [2024] [2025] [2026 Ref]│
├───────────────────────────────────────────────────┤
│                                                   │
│   Regional Sentinel-2 Web Mercator XYZ Basemap    │
│   (Continuous ~35 km true-color imagery layer)    │
│                                                   │
│          ┌───────────────────────────┐            │
│          │  Authoritative Project    │            │
│          │  Boundary (Dashed Line)   │            │
│          │                           │            │
│          │   ● High Priority Hotspot │            │
│          │   ● Medium Priority       │            │
│          │                           │            │
│          └───────────────────────────┘            │
│                                                   │
│   Seamless natural panning across landscape...    │
│                                                   │
└───────────────────────────────────────────────────┘
```

---

## 9. Backend & Frontend Architecture

### Backend (`dashboard/backend/`)
- Directory: `data/processed/satellite_regional/{project_id}/sentinel2_{year}.tif`.
- Endpoints:
  - `GET /api/satellite/regional/{project_id}/{year}/tiles/{z}/{x}/{y}.png`: Streams Web Mercator XYZ tiles from regional GeoTIFFs.
  - `GET /api/satellite/regional/{project_id}/{year}/metadata`: Returns regional bounds, resolution, and observation period.
- Checksums: Register all new regional rasters in `satellite_regional_checksums_sha256.csv`.

### Frontend (`dashboard/frontend/src/components/MapView.tsx`)
- Satellite / Hybrid mode uses `api.getSatelliteRegionalTileUrl(projectId, year)`.
- Base Carto tiles hidden in Satellite mode, allowing pure continuous regional satellite observation.
- Dashed project boundaries and interactive Feature 11 hotspot circles overlay cleanly at exact geographic coordinates.
- Resolution HUD updated to: `Sentinel-2 L2A (Harmonized) • True Color • 10m/20m Regional Basemap`.

---

## 10. Data Lineage & Provenance Tracking

Every regional GeoTIFF will maintain complete GEE acquisition metadata embedded in TIFF tags:
- `PROVENANCE_SOURCE`: `COPERNICUS/S2_SR_HARMONIZED`
- `PROVENANCE_DATE_RANGE`: Dry season observation window
- `PROVENANCE_CLOUD_FILTER`: `CLOUDY_PIXEL_PERCENTAGE < 20`, SCL cloud/shadow masked
- `PROVENANCE_COMPOSITE`: Seasonal median
- `PROVENANCE_CRS`: `EPSG:4326`
- `PROVENANCE_HASH_SHA256`: SHA-256 checksum

---

## 11. Immutability & Safety Protocol

1. **New Directory Only**: Regional satellite files are placed strictly in `data/processed/satellite_regional/`.
2. **Zero Modification to Features 8–11**: Model weights, evaluation CSVs, candidate patches, and existing `data/processed/satellite/` files remain 100% frozen.
3. **Integrity Check**: Startup `verify_all_checksums()` in `integrity.py` verifies both existing artifacts and new regional manifest.

---

## 12. Verification Strategy

When data acquisition and implementation proceed:
1. **Geometric Alignment**: Compare regional raster coordinates against authoritative project boundary GeoJSON to ensure sub-pixel alignment ($<1\text{ m}$ deviation).
2. **Temporal Differentiation**: Test tile hash uniqueness across all 6 years (2021–2026) for each project.
3. **Viewport Continuity**: Browser testing verifying that panning $\pm 10\text{ km}$ from the project boundary displays continuous satellite imagery with no rectangular borders.
4. **Interactive Fidelity**: Confirm clicking hotspots opens popups and routes to `/hotspots/:id`.
5. **Automated Test Suite**: Pytest coverage for all regional tile endpoints + Vite frontend build verification.

---

## 13. Risks, Trade-offs & Limitations

1. **GEE Export Quota / Time**: Exporting 18 regional GeoTIFFs ($35\text{ km} \times 35\text{ km}$) requires executing an authenticated Google Earth Engine export task or downloading pre-staged Sentinel-2 scenes.
2. **Resolution Fidelity**: True color 10m imagery reveals roads, clearings, and water bodies cleanly, but zooming to building level (zoom 18+) will show pixelation corresponding to 10m physical resolution. No artificial hallucination will be applied.
3. **2026 Status**: 2026 imagery remains strictly a reference visualization period and will not be introduced into ML logic.

---

## 14. Exact Implementation Steps for Future Execution

Once this acquisition plan is approved:
1. **Step 1**: Execute GEE extraction script (`scripts/data_acquisition/export_regional_sentinel2.py`) for the 3 defined AOIs across 2021–2026.
2. **Step 2**: Place the 18 COG files into `data/processed/satellite_regional/{MH-001,MH-002,MH-003}/sentinel2_{year}.tif`.
3. **Step 3**: Generate SHA-256 checksum manifest `data/processed/satellite_regional/checksums_sha256.csv`.
4. **Step 4**: Update `dashboard/backend/app/data.py` and `dashboard/backend/app/main.py` with regional tile routes.
5. **Step 5**: Update `dashboard/frontend/src/components/MapView.tsx` to point to regional tiles in Satellite and Hybrid modes.
6. **Step 6**: Run automated tests, verify browser pan/zoom continuity across all 3 projects and 6 years, and update documentation.

---

### Conclusion & Stop Statement
This plan details the minimum, scientifically rigorous satellite acquisition required to achieve a Google-Earth-like continuous satellite map experience without compromising project immutability or fabricating data. 

In strict adherence to planning mode rules, **no application code or datasets were modified during this step**. Execution is stopped here pending review and authorization of the data acquisition plan.
