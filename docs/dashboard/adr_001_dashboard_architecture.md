# ADR 001: Dashboard Architecture

## Status
Accepted

## Context
The project has transitioned from an ML experimentation pipeline (Features 1-11) to an operational decision-support phase (Feature 12). We need to build an investigator dashboard to view the generated ML hotspots and independent satellite evidence.

## Decisions & Rationale

1. **Why dashboard is read-only**
   The ML outputs must remain immutable for scientific validity and auditability. The dashboard exists to visualize the output of a controlled data pipeline, not to alter it. Allowing users to adjust ML thresholds in the UI would break the frozen validation environment established in Feature 8.8.
   
2. **Why ML artifacts remain source-of-truth**
   Moving data out of CSV/GeoJSON into a traditional writable RDBMS introduces a risk of data drift. By maintaining the ML artifacts as the sole source of truth, the backend ensures it always displays the exact output of the scientific pipeline.

3. **Why an API layer exists**
   Instead of the frontend fetching raw heavy CSVs and parsing them in the browser, an API layer (FastAPI) abstracts data aggregation, pagination, and sorting. This keeps the client lightweight and improves performance.

4. **Why provenance is mandatory**
   Investigators must trust the system. Because satellite AI predictions can be flawed or suffer from calibration shift (as diagnosed in Feature 10.1), the system must explicitly expose the chain of evidence connecting a final hotspot to its source patches, NDVI changes, and CNN model versions.

5. **Why no model inference occurs inside the dashboard**
   Running deep learning models inside an operational dashboard requires significant compute (GPUs, heavy memory footprint) and complicates deployment. Decoupling the inference pipeline (batch processing) from the visualization pipeline allows the dashboard to run on cheap, standard web infrastructure.

6. **Why no legal/compliance conclusions are displayed**
   Satellite imagery and temporal CNNs identify structural spectral change, which correlates with historical disturbance labels. They cannot determine *intent*, *permitting status*, or *legal compliance*. Explicitly banning terms like "illegal activity" prevents investigators from misinterpreting proxy signals as definitive legal facts. 

7. **Why evidence remains proxy evidence**
   NDVI and Dynamic World are automated satellite derivatives. They are independent of the CNN but still subject to remote-sensing limitations (cloud cover, phenology). Therefore, they "support" the CNN candidate but do not "prove" real-world ground truth.

## Consequences
- Dashboard deployment will be highly stable and cheap (read-only FastAPI + React).
- Updating the dashboard with new data requires re-running the ML pipeline (Features 9-11) and pushing new artifacts to the server. Real-time inference is intentionally sacrificed for strict scientific integrity.
