# AUDIT 08: Dashboard Frontend & Map Verification

**Audit Date**: August 2026  
**Auditor**: Forensic Truth Audit Subsystem  
**Scope**: React + TypeScript + MapLibre frontend application in `dashboard/frontend/`.

---

## 1. Frontend Build & Static Analysis

- **Location**: `dashboard/frontend/`
- **Framework**: React 18 + TypeScript + Vite 5.4.21 + MapLibre GL JS + TailwindCSS
- **Build Verification**:
  - `tsc -b`: **0 TypeScript compilation errors**
  - `vite build`: **PASS** (produced optimized production bundle in 10.46s: `dist/assets/index-*.js`, `dist/assets/index-*.css`)
- **Lint Verification**: **PASS**

---

## 2. Forensic Code Inspection for Hardcoded / Fake Data

- **Literal & Mock Search**:
  - Searched all `.ts`, `.tsx`, and `.js` files for `mock`, `fake`, `demo`, `sample`, `dummy`, `hardcoded`, `placeholder`.
  - **Results**: **0 mock or fake datasets found**.
- **Map Coordinate Inspection**:
  - Searched for coordinate float literals.
  - The only literal found is `center: [73.5, 19.5]` in `MapView.tsx`, which serves purely as the initial default camera position centered on Maharashtra before dynamic bounds fitting occurs.
  - All rendered boundary polygons and hotspot circles are sourced directly from backend API endpoints (`/api/maps/projects` and `/api/maps/hotspots`).

---

## 3. Map Layers & Rendering Audit

| Map Component / Layer | Source Endpoint | Technology | Rendered Elements | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Basemap** | Carto Light (`cartocdn.com`) | MapLibre Raster Tiles | OpenStreetMap base geographical layer | **WORKING & VERIFIED** |
| **Project Boundaries** | `/api/maps/projects` | MapLibre GeoJSON Layer | Real polygon boundaries for Gondkhari, Gadchiroli, Bhivpuri PSP | **WORKING & VERIFIED** |
| **Hotspot Markers** | `/api/maps/hotspots` | MapLibre Circle Layer | 157 hotspots dynamically styled by priority color | **WORKING & VERIFIED** |
| **Satellite Imagery Layer** | *None* | *Not yet implemented* | Real Sentinel-2 / provider satellite tile switcher | **NOT IMPLEMENTED (Feature 12-C.4)** |

**Important Map Finding**: The current map is a functional vector/OSM basemap renderer. Satellite imagery mode is **NOT yet implemented** in the frontend.
