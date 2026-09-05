# Feature 12-A: UI Information Architecture

The frontend application provides an intuitive mapping and investigation interface to evaluate the prioritized queues generated in Feature 11.

## Site Map

- **`/dashboard`**: Global Overview
- **`/projects`**: Project Directory
  - **`/projects/:projectId`**: Project-Specific Map & Overview
- **`/hotspots`**: Master Investigator Queue
  - **`/hotspots/:hotspotId`**: Hotspot Detail & Evidence Trace

---

## Page Layouts

### 1. `/dashboard` (Global Overview)
- **Header**: System Title ("Environmental Monitoring Decision-Support").
- **KPI Cards**: Total Projects, Total Hotspots, Independent Evidence Support Rate.
- **Priority Breakdown Chart**: Donut chart of HIGH, MEDIUM, LOW, and UNSUPPORTED hotspots.
- **Project Heatmap**: Lightweight map or table showing hotspot density per project.
- **Recent Data Info**: Date of last model inference and data pipeline run.

### 2. `/projects` & `/projects/:projectId`
- **List View**: Sortable grid of all monitored projects (MH-001, MH-002, etc.).
- **Detail View**: 
  - Large interactive map focused on the project boundary.
  - Sidebar showing project summary statistics (hotspots by priority).
  - Quick-links to filter the Investigator Queue to this specific project.

### 3. `/hotspots` (Investigator Queue)
- **Layout**: Split screen. Left: Map displaying hotspots. Right: Data Table.
- **Search & Filter Panel**: Filter by Project, Priority Level, and Evidence Class.
- **Data Table**: Columns for Hotspot ID, Priority Level, Priority Score, CNN Score, NDVI Change, and Action.
- **Interaction**: Clicking a row centers the map on the hotspot and expands it, or navigates to the Detail page.

### 4. `/hotspots/:hotspotId` (Hotspot Detail)
- **Map Focus**: Fully zoomed-in map of the specific candidate boundary. Toggleable layers for underlying satellite basemaps (if available).
- **Header**: Hotspot ID & Priority Badge (color-coded).
- **Recommendation Alert**: Prominent display of the recommended action (e.g., "Prioritize independent field verification").
- **Evidence Panel**:
  - **CNN Signal**: Max score, percentiles, spatial patch count.
  - **NDVI Evidence**: Measured decline.
  - **Dynamic World Evidence**: Detected transitions (e.g., vegetation to bare).
- **Provenance Panel**: Strict lineage showing exact source datasets, checksums, and model checkpoints ensuring data integrity.
