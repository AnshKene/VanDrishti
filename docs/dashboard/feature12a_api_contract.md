# Feature 12-A: API Contract

The API layer acts as a strict read-only interface projecting the frozen CSV/GeoJSON artifacts from Feature 11. 

## Endpoints

### 1. Projects
**`GET /api/projects`**
Returns the aggregate summary of all processed projects.
- **Response**: `List[PROJECT]`

**`GET /api/projects/:projectId`**
Returns specific project metrics.
- **Response**: `PROJECT`

### 2. Investigator Queue (Hotspots)
**`GET /api/hotspots`**
Returns the prioritized list of candidate hotspots. Supports querying.
- **Query Parameters**:
  - `project`: String (Filter by project_id)
  - `priority`: String (Filter by HIGH, MEDIUM, LOW, UNSUPPORTED)
  - `evidence`: String (Filter by STRONG, MODERATE, WEAK)
  - `sort_by`: String (e.g., `priority_score`, `max_cnn_score`)
  - `order`: String (`asc` or `desc`)
- **Response**: `List[HOTSPOT]`

**`GET /api/hotspots/:hotspotId`**
Returns full details for a single hotspot.
- **Response**: `HOTSPOT`

### 3. Hotspot Details & Traceability
**`GET /api/hotspots/:hotspotId/evidence`**
Returns the specific independent satellite proxy metrics used to score the hotspot.
- **Response**: `EVIDENCE`

**`GET /api/hotspots/:hotspotId/provenance`**
Returns the strict ML provenance chain, including frozen checksums and model checkpoints, validating the origin of the data.
- **Response**: `PROVENANCE`

### 4. Geospatial Data
**`GET /api/maps/projects`**
Returns boundaries of all processed projects.
- **Response**: `GeoJSON FeatureCollection` (Polygons)

**`GET /api/maps/hotspots`**
Returns hotspot locations and their priority attributes for mapping libraries.
- **Query Parameters**: `project`, `priority`
- **Response**: `GeoJSON FeatureCollection` (Points or Polygons)

### 5. Statistics
**`GET /api/statistics/overview`**
Returns top-level KPIs for the `/dashboard` landing page (total hotspots, breakdown by priority, breakdown by project).
- **Response**: JSON Object
