# Feature 12-A: Implementation Plan

The dashboard will be implemented in two distinct future features to maintain safety and modularity.

## Feature 12-B: Read-Only API Backend
1. **Initialize Backend**: Set up a Python FastAPI project in `src/api/` or `backend/`.
2. **Data Ingestion**: Write a data-loading service that parses `feature11_hotspot_priority.csv`, `feature11_project_summary.csv`, and `validated_candidate_patches.csv` into memory (Pandas) or a local SQLite/DuckDB file on startup.
3. **Checksum Verification**: Implement the startup checksum test ensuring the underlying Feature 8-11 pipeline files have not been tampered with.
4. **Endpoint Creation**: Implement all GET endpoints defined in `feature12a_api_contract.md`.
5. **Testing**: Write pytest test cases to ensure no endpoints mutate data and that spatial/priority filters return the correct intersections.

## Feature 12-C: React Frontend
1. **Initialize Frontend**: Set up a React app (Vite or Next.js) in `frontend/`.
2. **Component Library**: Configure TailwindCSS or MUI.
3. **Map Integration**: Install and configure `react-map-gl` and MapLibre GL JS.
4. **State & Fetching**: Implement React Query or SWR to fetch data from the FastAPI backend.
5. **Pages**: Implement the UI Information Architecture (`/dashboard`, `/projects`, `/hotspots`).
6. **Investigator Queue**: Build the sortable/filterable table interacting with the API layer.
7. **Refinement**: Polish visual design, ensuring clear, scientific, and non-accusatory terminology ("Disturbance Candidate", "Proxy Evidence").
