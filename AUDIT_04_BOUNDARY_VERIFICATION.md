# AUDIT 04: Project Boundary Verification

**Audit Date**: August 2026  
**Auditor**: Forensic Truth Audit Subsystem  
**Scope**: Geometric, geodesic, and regulatory verification of project boundaries for MH-001, MH-002, and MH-003.

---

## 1. Project Boundary Summary Table

| Project ID | Project Name | Raw KML Source File | GeoJSON Boundary Path | Approved Clearance Ha | Computed Geodesic Area (ha) | Centroid (Lat, Lon) | Validity & Topology | Used in Frontend? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MH-001** | Gondkhari Underground Coal Mine | `data/raw/Gondkhari/kml/970858_FC_KML_1672903420512_Lease limit.kml` | `data/processed/project_boundaries/gondkhari_boundary.geojson` | 862.00 ha (Mine Lease) / 87.35 ha (Forest) | **862.26 ha** | (21.156692, 78.926002) | **VALID** (Polygon) | **YES** |
| **MH-002** | Gadchiroli Iron Ore Mine | `data/raw/Gadchiroli/kml/30227102_FC_KML_1702025392040_FC_937.077_Area_1.kml` | `data/processed/project_boundaries/gadchiroli_boundary.geojson` | 937.077 ha (Forest) / 990.26 ha (CA Land) | **938.81 ha** | (19.601717, 80.353511) | **VALID** (MultiPolygon) | **YES** |
| **MH-003** | Bhivpuri Pumped Storage Project | `data/raw/Bhivpuri PSP/kml/6958645_FC_KML_1696507173302_Bhivpuri Off Stream Open Loop Pumped Storage Project (1800 MW).kml` | `data/processed/project_boundaries/bhivpuri_boundary.geojson` | 20.15 ha (Forest) / 117.02 ha (Full Complex) | **117.02 ha** | (18.934965, 73.462291) | **VALID** (MultiPolygon) | **YES** |

---

## 2. Forensic Boundary Checks

1. **Source Document Reconciliation**:
   - For **MH-001 (Gondkhari)**: The Stage-II Forest Clearance order (`CADASTRAL MAP 862ha-r.pdf`) specifies an 862 ha total mine lease. Geodesic area calculation on `gondkhari_boundary.geojson` in EPSG:32644 yields **862.26 ha** (99.97% alignment).
   - For **MH-002 (Gadchiroli)**: The Stage-II clearance documents specify 937.077 ha proposed forest land for diversion. Geodesic area calculation on `gadchiroli_boundary.geojson` yields **938.81 ha** (99.8% alignment).
   - For **MH-003 (Bhivpuri PSP)**: The Stage-II clearance order specifies 20.15 ha forest land diversion within the 117.02 ha total project footprint. Geodesic area calculation yields **117.02 ha** (100% alignment).
2. **Coordinate & Geolocation Verification**:
   - Geometries were checked against real physical locations in Maharashtra:
     - MH-001: Nagpur district, Maharashtra (21.15°N, 78.93°E) — matches Gondkhari coal block geography.
     - MH-002: Gadchiroli district, Maharashtra (19.60°N, 80.35°E) — matches Surjagarh/Gadchiroli iron ore forest terrain.
     - MH-003: Pune/Raigad districts, Western Ghats (18.93°N, 73.46°E) — matches Bhivpuri/Shirota pumped storage geography.
3. **Frontend / Backend Boundary Consumption**:
   - `dashboard/backend/app/data.py` reads all 3 GeoJSON files directly from `data/processed/project_boundaries/*.geojson` and serves them via `/api/maps/projects`.
   - `dashboard/frontend/src/components/MapView.tsx` renders them dynamically as vector boundary polygons.
   - **Zero hardcoded boundary coordinates** exist in frontend or backend application code.
