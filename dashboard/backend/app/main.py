from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Any
from . import schemas
from . import data
from . import integrity

app = FastAPI(
    title="Environmental Monitoring Dashboard API",
    description="Read-only projection of immutable ML artifacts.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    try:
        integrity.verify_all_checksums()
        data.load_data()
    except Exception as e:
        import sys
        print(f"CRITICAL STARTUP FAILURE: {e}", file=sys.stderr)
        sys.exit(1)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Immutable backend online."}

@app.get("/api/dashboard/overview", response_model=schemas.OverviewStats)
def get_overview():
    return data.get_overview_stats()

@app.get("/api/projects", response_model=List[schemas.Project])
def list_projects():
    return data.get_projects()

@app.get("/api/projects/{project_id}", response_model=schemas.Project)
def get_project(project_id: str):
    p = data.get_project(project_id)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return p

@app.get("/api/hotspots", response_model=schemas.PaginatedHotspots)
def list_hotspots(
    project: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    evidence: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100)
):
    return data.get_hotspots(project, priority, evidence, search, page, page_size)

@app.get("/api/hotspots/{hotspot_id}", response_model=schemas.Hotspot)
def get_hotspot(hotspot_id: str):
    hs = data.get_hotspot(hotspot_id)
    if not hs:
        raise HTTPException(status_code=404, detail="Hotspot not found")
    return hs

@app.get("/api/hotspots/{hotspot_id}/evidence", response_model=schemas.Evidence)
def get_evidence(hotspot_id: str):
    ev = data.get_evidence(hotspot_id)
    if not ev:
        raise HTTPException(status_code=404, detail="Hotspot evidence not found")
    return ev

@app.get("/api/hotspots/{hotspot_id}/provenance", response_model=schemas.Provenance)
def get_provenance(hotspot_id: str):
    prov = data.get_provenance(hotspot_id)
    if not prov:
        raise HTTPException(status_code=404, detail="Hotspot provenance not found")
    return prov

@app.get("/api/maps/hotspots")
def get_maps_hotspots():
    gj = data.get_hotspots_geojson()
    if gj is None:
        raise HTTPException(status_code=503, detail="GeoJSON not available")
    return gj

@app.get("/api/maps/projects")
def get_maps_projects():
    gj = data.get_projects_geojson()
    if gj is None or len(gj.get("features", [])) == 0:
        raise HTTPException(status_code=503, detail="Authoritative project boundaries not found")
    return gj

@app.get("/api/satellite/years", response_model=schemas.SatelliteYearsResponse)
def get_satellite_years():
    return data.get_satellite_years()

@app.get("/api/satellite/{project_id}/{year}/metadata", response_model=schemas.SatelliteMetadata)
def get_satellite_metadata(project_id: str, year: int):
    meta = data.get_satellite_metadata(project_id, year)
    if not meta:
        raise HTTPException(status_code=404, detail=f"Satellite raster not found for {project_id} in {year}")
    return meta

@app.get("/api/satellite/{project_id}/{year}/image.png")
def get_satellite_image(project_id: str, year: int):
    png_bytes = data.get_satellite_png(project_id, year)
    if not png_bytes:
        raise HTTPException(status_code=404, detail=f"Satellite raster image not found for {project_id} in {year}")
    return Response(content=png_bytes, media_type="image/png")

@app.get("/api/satellite/{project_id}/{year}/tiles/{z}/{x}/{y}.png")
def get_satellite_tile(project_id: str, year: int, z: int, x: int, y: int):
    png_bytes = data.get_satellite_tile(project_id, year, z, x, y)
    if not png_bytes:
        raise HTTPException(status_code=404, detail=f"Satellite raster not found for {project_id} in {year}")
    return Response(content=png_bytes, media_type="image/png")

@app.get("/api/satellite/regional/{project_id}/{year}/metadata", response_model=schemas.SatelliteMetadata)
def get_satellite_regional_metadata(project_id: str, year: int):
    meta = data.get_satellite_regional_metadata(project_id, year)
    if not meta:
        raise HTTPException(status_code=404, detail=f"Regional satellite raster not found for {project_id} in {year}")
    return meta

@app.get("/api/satellite/regional/{project_id}/{year}/tiles/{z}/{x}/{y}.png")
def get_satellite_regional_tile(project_id: str, year: int, z: int, x: int, y: int):
    png_bytes = data.get_satellite_regional_tile(project_id, year, z, x, y)
    if not png_bytes:
        raise HTTPException(status_code=404, detail=f"Regional satellite tile not found for {project_id} in {year}")
    return Response(content=png_bytes, media_type="image/png")



