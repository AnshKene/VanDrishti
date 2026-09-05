import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    # Using TestClient as a context manager triggers startup/shutdown events
    with TestClient(app) as c:
        yield c

def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_dashboard_overview(client):
    response = client.get("/api/dashboard/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_projects" in data
    assert "total_hotspots" in data
    assert data["total_projects"] == 3
    assert data["total_hotspots"] == 157

def test_projects_listing(client):
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

def test_project_detail(client):
    response = client.get("/api/projects/MH-001")
    assert response.status_code == 200
    assert response.json()["project_id"] == "MH-001"

def test_invalid_project(client):
    response = client.get("/api/projects/NONEXISTENT")
    assert response.status_code == 404

def test_hotspots_listing_and_pagination(client):
    response = client.get("/api/hotspots?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["total"] == 157

def test_hotspots_filtering(client):
    response = client.get("/api/hotspots?priority=HIGH")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 8
    for item in data["items"]:
        assert item["priority_level"] == "HIGH PRIORITY"

def test_hotspot_detail(client):
    r = client.get("/api/hotspots?page_size=1")
    hid = r.json()["items"][0]["hotspot_id"]
    
    response = client.get(f"/api/hotspots/{hid}")
    assert response.status_code == 200
    assert response.json()["hotspot_id"] == hid

def test_invalid_hotspot(client):
    response = client.get("/api/hotspots/NONEXISTENT")
    assert response.status_code == 404

def test_evidence(client):
    r = client.get("/api/hotspots?page_size=1")
    hid = r.json()["items"][0]["hotspot_id"]
    
    response = client.get(f"/api/hotspots/{hid}/evidence")
    assert response.status_code == 200
    assert response.json()["hotspot_id"] == hid
    assert "ndvi_change" in response.json()

def test_provenance(client):
    r = client.get("/api/hotspots?page_size=1")
    hid = r.json()["items"][0]["hotspot_id"]
    
    response = client.get(f"/api/hotspots/{hid}/provenance")
    assert response.status_code == 200
    assert response.json()["hotspot_id"] == hid
    assert response.json()["model_name"] == "Delta Temporal CNN"

def test_maps_hotspots(client):
    response = client.get("/api/maps/hotspots")
    assert response.status_code == 200
    assert "type" in response.json()
    assert response.json()["type"] == "FeatureCollection"

def test_maps_projects(client):
    response = client.get("/api/maps/projects")
    assert response.status_code == 200
    assert "type" in response.json()
    assert response.json()["type"] == "FeatureCollection"

def test_satellite_years(client):
    response = client.get("/api/satellite/years")
    assert response.status_code == 200
    data = response.json()
    assert "available_years" in data
    assert 2021 in data["available_years"]
    assert 2025 in data["available_years"]
    assert 2026 in data["reference_years"]

def test_satellite_metadata_all_projects_and_years(client):
    for pid in ["MH-001", "MH-002", "MH-003"]:
        for yr in [2021, 2022, 2023, 2024, 2025, 2026]:
            response = client.get(f"/api/satellite/{pid}/{yr}/metadata")
            assert response.status_code == 200
            data = response.json()
            assert data["project_id"] == pid
            assert data["year"] == yr
            assert len(data["bounds"]) == 4
            assert len(data["coordinates"]) == 4
            assert data["image_url"] == f"/api/satellite/{pid}/{yr}/image.png"
            assert data["is_reference_year"] == (yr == 2026)

def test_satellite_image_stream(client):
    for pid in ["MH-001", "MH-002", "MH-003"]:
        response = client.get(f"/api/satellite/{pid}/2023/image.png")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert len(response.content) > 1000 # Real PNG data

def test_satellite_invalid_queries(client):
    r1 = client.get("/api/satellite/NONEXISTENT/2021/metadata")
    assert r1.status_code == 404
    
    r2 = client.get("/api/satellite/MH-001/1990/image.png")
    assert r2.status_code == 404
    
    r3 = client.get("/api/satellite/NONEXISTENT/2021/tiles/12/100/100.png")
    assert r3.status_code == 404

def test_satellite_tiles_xyz(client):
    # Test valid intersecting tile for MH-001 (z=12, x=2946, y=1801)
    response = client.get("/api/satellite/MH-001/2025/tiles/12/2946/1801.png")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 1000

    # Test outside tile (returns transparent 256x256 PNG)
    resp_outside = client.get("/api/satellite/MH-001/2025/tiles/12/0/0.png")
    assert resp_outside.status_code == 200
    assert resp_outside.headers["content-type"] == "image/png"

def test_satellite_regional_endpoints(client):
    # Metadata for MH-001 in 2025 (pilot regional raster)
    r_meta = client.get("/api/satellite/regional/MH-001/2025/metadata")
    assert r_meta.status_code == 200
    data = r_meta.json()
    assert data["project_id"] == "MH-001"
    assert data["year"] == 2025
    assert data["is_regional"] is True
    assert data["width"] == 1200
    assert data["height"] == 1100
    assert data["bounds"] == [78.75, 21.0, 79.1, 21.3]

    # Tile retrieval for regional tile (z=13, x=5892, y=3602)
    r_tile = client.get("/api/satellite/regional/MH-001/2025/tiles/13/5892/3602.png")
    assert r_tile.status_code == 200
    assert r_tile.headers["content-type"] == "image/png"
    assert len(r_tile.content) > 1000



