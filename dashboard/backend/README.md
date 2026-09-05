# Environmental Monitoring Dashboard Backend (Feature 12-B)

This is a **strictly read-only projection** backend built with FastAPI. It serves frozen ML artifacts from Feature 9-11 pipelines to the frontend dashboard.

## Setup & Installation

1. Navigate to this directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the backend using Uvicorn (make sure your working directory is `dashboard/backend` or you adjust the module path):

```bash
cd dashboard/backend
uvicorn app.main:app --reload
```

## Integrity Guarantees
- **Read-Only**: There is no database or write capability.
- **Startup Verification**: The application parses the `feature11_checksums_sha256.csv` and `feature12a_source_manifest.csv` on boot. If any CSV or GeoJSON file has been tampered with, the backend will refuse to start.

## API Documentation
Once running, interactive API documentation is automatically available at:
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
