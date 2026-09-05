# Feature 12-A: Map Specification

The map is the primary geographic interface for the dashboard. It must render GeoJSON boundaries reliably without freezing or degrading UI performance.

## Map Library
- **Recommended**: MapLibre GL JS / react-map-gl
- **Rationale**: Excellent handling of vector tiles and heavy GeoJSON payloads, open-source, and extremely fast.

## Required Layers

### 1. Project Boundaries
- **Source**: `data/processed/project_boundaries/*.geojson`
- **Styling**: Thick, dashed outline with a transparent fill. Does not obscure underlying satellite/map tiles.

### 2. Hotspot Polygons (or Points)
- **Source**: `maps/feature11_prioritized_hotspots.geojson`
- **Styling by Priority**:
  - `HIGH PRIORITY`: Red / High Opacity fill
  - `MEDIUM PRIORITY`: Orange / Medium Opacity fill
  - `LOW PRIORITY`: Yellow / Low Opacity fill
  - `UNSUPPORTED`: Gray / Transparent fill
- **Interactions**: 
  - Hover: Tooltip showing Hotspot ID and evidence summary.
  - Click: Navigate to `/hotspots/:hotspotId`.

### 3. Basemap
- **Type**: Satellite or clean topological base map (e.g., Mapbox Satellite or OpenStreetMap Carto).
- **Rationale**: Investigators need geographic context to evaluate spatial anomalies.

## Data Loading
- Coordinates must NOT be hardcoded.
- The React frontend fetches GeoJSON dynamically via the `/api/maps/hotspots` endpoint and injects it into a MapLibre `Source` component.
