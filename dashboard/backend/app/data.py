import json
import pandas as pd
from pathlib import Path
import math

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
F11_DIR = REPO_ROOT / "data/processed/modeling/candidate_prioritization"
F10_DIR = REPO_ROOT / "data/processed/modeling/candidate_validation"
BOUNDARIES_DIR = REPO_ROOT / "data/processed/project_boundaries"

# In-memory data store
_hotspots_df = None
_projects_df = None
_hotspots_geojson = None
_projects_geojson = None
_patches_df = None

def load_data():
    global _hotspots_df, _projects_df, _hotspots_geojson, _projects_geojson, _patches_df
    
    # Load Hotspots
    hp_path = F11_DIR / "feature11_hotspot_priority.csv"
    if hp_path.exists():
        _hotspots_df = pd.read_csv(hp_path)
        # NaN to None for JSON compliance
        _hotspots_df = _hotspots_df.replace({float('nan'): None})
    else:
        raise FileNotFoundError(f"Missing {hp_path}")
        
    # Load Projects
    pj_path = F11_DIR / "feature11_project_summary.csv"
    if pj_path.exists():
        _projects_df = pd.read_csv(pj_path)
        
        # Add project name mapping manually or from metadata if available. 
        # Hardcoding mapping derived from metadata inspection.
        name_map = {"MH-001": "Gondkhari", "MH-002": "Gadchiroli", "MH-003": "Bhivpuri PSP"}
        _projects_df["project_name"] = _projects_df["project_id"].map(name_map)
    else:
        raise FileNotFoundError(f"Missing {pj_path}")

    # Load Patches for provenance
    pt_path = F10_DIR / "hotspot_evidence/validated_candidate_patches.csv"
    if pt_path.exists():
        _patches_df = pd.read_csv(pt_path)

    # Load Hotspots GeoJSON
    hg_path = F11_DIR / "maps/feature11_prioritized_hotspots.geojson"
    if hg_path.exists():
        with open(hg_path, "r") as f:
            _hotspots_geojson = json.load(f)
            
    # Load Project Boundaries GeoJSON
    _projects_geojson = {"type": "FeatureCollection", "features": []}
    if BOUNDARIES_DIR.exists():
        for gj_file in BOUNDARIES_DIR.glob("*.geojson"):
            with open(gj_file, "r") as f:
                feature = json.load(f)
                # Ensure it's a feature or collection
                if feature.get("type") == "FeatureCollection":
                    _projects_geojson["features"].extend(feature["features"])
                elif feature.get("type") == "Feature":
                    _projects_geojson["features"].append(feature)

def get_overview_stats():
    total_projects = len(_projects_df)
    total_hotspots = len(_hotspots_df)
    high = len(_hotspots_df[_hotspots_df["priority_level"] == "HIGH PRIORITY"])
    medium = len(_hotspots_df[_hotspots_df["priority_level"] == "MEDIUM PRIORITY"])
    low = len(_hotspots_df[_hotspots_df["priority_level"] == "LOW PRIORITY"])
    unsup = len(_hotspots_df[_hotspots_df["priority_level"] == "UNSUPPORTED / MONITOR"])
    
    proj_dist = []
    for _, row in _projects_df.iterrows():
        proj_dist.append({
            "project_id": row["project_id"],
            "hotspot_count": row["hotspot_count"],
            "high_priority": row["high_priority"]
        })
        
    return {
        "total_projects": total_projects,
        "total_hotspots": total_hotspots,
        "high_priority": high,
        "medium_priority": medium,
        "low_priority": low,
        "unsupported": unsup,
        "supported_hotspots": high + medium + low,
        "project_distribution": proj_dist
    }

def get_projects():
    projects = []
    for _, row in _projects_df.iterrows():
        projects.append({
            "project_id": row["project_id"],
            "project_name": row.get("project_name", ""),
            "total_hotspots": row["hotspot_count"],
            "high_priority_count": row["high_priority"],
            "medium_priority_count": row["medium_priority"],
            "low_priority_count": row["low_priority"],
            "unsupported_count": row["unsupported"],
            "last_updated": "2026-08-24T00:00:00Z"
        })
    return projects

def get_project(project_id: str):
    df = _projects_df[_projects_df["project_id"] == project_id]
    if df.empty:
        return None
    row = df.iloc[0]
    return {
        "project_id": row["project_id"],
        "project_name": row.get("project_name", ""),
        "total_hotspots": row["hotspot_count"],
        "high_priority_count": row["high_priority"],
        "medium_priority_count": row["medium_priority"],
        "low_priority_count": row["low_priority"],
        "unsupported_count": row["unsupported"],
        "last_updated": "2026-08-24T00:00:00Z"
    }

def get_hotspots(project=None, priority=None, evidence=None, search=None, page=1, page_size=25):
    df = _hotspots_df.copy()
    
    if project:
        df = df[df["project_id"] == project]
    if priority:
        # e.g., "HIGH" maps to "HIGH PRIORITY"
        if not priority.endswith("PRIORITY") and priority != "UNSUPPORTED":
            priority_val = f"{priority} PRIORITY" if priority != "UNSUPPORTED" else "UNSUPPORTED / MONITOR"
        else:
            priority_val = priority
        df = df[df["priority_level"] == priority_val]
    if evidence:
        if not evidence.endswith("SUPPORT"):
            evidence_val = f"{evidence}_SUPPORT"
        else:
            evidence_val = evidence
        df = df[df["feature10_evidence_class"] == evidence_val]
    if search:
        df = df[df["hotspot_id"].str.contains(search, case=False)]
        
    total = len(df)
    total_pages = max(1, math.ceil(total / page_size))
    
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_df = df.iloc[start_idx:end_idx]
    
    items = page_df.to_dict("records")
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages
    }

def get_hotspot(hotspot_id: str):
    df = _hotspots_df[_hotspots_df["hotspot_id"] == hotspot_id]
    if df.empty:
        return None
    return df.iloc[0].to_dict()

def get_evidence(hotspot_id: str):
    df = _hotspots_df[_hotspots_df["hotspot_id"] == hotspot_id]
    if df.empty:
        return None
    row = df.iloc[0]
    return {
        "hotspot_id": row["hotspot_id"],
        "ndvi_change": row["ndvi_change"],
        "ndvi_evidence": int(row["ndvi_evidence"]),
        "dynamic_world_evidence": int(row["dynamic_world_evidence"]),
        "temporal_evidence": row["temporal_evidence"],
        "spatial_evidence": int(row["spatial_evidence"]),
        "evidence_class": row["feature10_evidence_class"],
        "evidence_summary": row["evidence_summary"]
    }

def get_provenance(hotspot_id: str):
    df = _hotspots_df[_hotspots_df["hotspot_id"] == hotspot_id]
    if df.empty:
        return None
    row = df.iloc[0]
    
    # Extract patches from F10 dataset if available
    patch_ids = []
    if _patches_df is not None:
        p_df = _patches_df[_patches_df["hotspot_id"] == hotspot_id]
        patch_ids = p_df["temporal_sample_id"].tolist()
        
    return {
        "hotspot_id": row["hotspot_id"],
        "source_feature": "Feature 11",
        "source_file": "feature11_hotspot_priority.csv",
        "source_patch_ids": patch_ids,
        "model_name": "Delta Temporal CNN",
        "model_feature": "Feature 8.7-B",
        "model_version": "Frozen Checkpoint",
        "threshold": 0.10,
        "input_years": [2021, 2022, 2023, 2024, 2025],
        "data_checksum": "Matches feature11_checksums_sha256.csv",
        "generated_at": "2026-08-24T00:00:00Z"
    }

def get_hotspots_geojson():
    return _hotspots_geojson

def get_projects_geojson():
    return _projects_geojson

def get_satellite_years():
    return {
        "available_years": [2021, 2022, 2023, 2024, 2025, 2026],
        "operational_years": [2021, 2022, 2023, 2024, 2025],
        "reference_years": [2026]
    }

def get_satellite_metadata(project_id: str, year: int):
    sat_dir = REPO_ROOT / "data/processed/satellite" / project_id
    tif_path = sat_dir / f"sentinel2_{year}.tif"
    if not tif_path.exists():
        return None
    
    import rasterio
    from rasterio.warp import transform_bounds
    
    with rasterio.open(tif_path) as src:
        bounds = src.bounds
        crs = str(src.crs)
        w, h = src.width, src.height
        
        if src.crs.to_string() != "EPSG:4326":
            wgs84 = transform_bounds(src.crs, "EPSG:4326", bounds.left, bounds.bottom, bounds.right, bounds.top)
        else:
            wgs84 = (bounds.left, bounds.bottom, bounds.right, bounds.top)
        
        min_lon, min_lat, max_lon, max_lat = [float(round(x, 6)) for x in wgs84]
        
        # MapLibre image coordinates format: [top-left, top-right, bottom-right, bottom-left]
        coordinates = [
            [min_lon, max_lat],
            [max_lon, max_lat],
            [max_lon, min_lat],
            [min_lon, min_lat]
        ]
        
        return {
            "project_id": project_id,
            "year": year,
            "sensor": "Sentinel-2 L2A (Harmonized)",
            "composite_type": "Seasonal Median Composite (Dry Season, SCL Cloud/Shadow Masked)",
            "crs": crs,
            "width": w,
            "height": h,
            "bounds": [min_lon, min_lat, max_lon, max_lat],
            "coordinates": coordinates,
            "image_url": f"/api/satellite/{project_id}/{year}/image.png",
            "tile_url_template": f"/api/satellite/{project_id}/{year}/tiles/{{z}}/{{x}}/{{y}}.png",
            "resolution_description": "Sentinel-2 L2A • True Color (B4/B3/B2) • ~30 m grid",
            "band_names": ["B4 (Red)", "B3 (Green)", "B2 (Blue)"],
            "stretch_range": [0.0, 2800.0],
            "is_reference_year": (year == 2026)
        }

def get_satellite_png(project_id: str, year: int) -> Optional[bytes]:
    sat_dir = REPO_ROOT / "data/processed/satellite" / project_id
    tif_path = sat_dir / f"sentinel2_{year}.tif"
    if not tif_path.exists():
        return None
    
    import rasterio
    import numpy as np
    from PIL import Image
    import io
    
    with rasterio.open(tif_path) as src:
        # Bands: 1=B2 (Blue), 2=B3 (Green), 3=B4 (Red)
        r = src.read(3).astype(np.float32)
        g = src.read(2).astype(np.float32)
        b = src.read(1).astype(np.float32)
        
        # Valid mask: non-zero in all RGB channels
        valid_mask = (r > 0) | (g > 0) | (b > 0)
        alpha = np.where(valid_mask, 255, 0).astype(np.uint8)
        
        # Linear stretch: 0 to 2800 surface reflectance units mapped to 0 to 255
        r_scaled = np.clip(r / 2800.0 * 255.0, 0, 255).astype(np.uint8)
        g_scaled = np.clip(g / 2800.0 * 255.0, 0, 255).astype(np.uint8)
        b_scaled = np.clip(b / 2800.0 * 255.0, 0, 255).astype(np.uint8)
        
        rgba = np.stack([r_scaled, g_scaled, b_scaled, alpha], axis=-1)
        img = Image.fromarray(rgba, mode="RGBA")
        
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        return buf.getvalue()

WEB_MERCATOR_HALF = 20037508.342789244

def _tile_to_mercator_bounds(z: int, x: int, y: int):
    tile_count = 2 ** z
    tile_size = (WEB_MERCATOR_HALF * 2.0) / tile_count
    minx = -WEB_MERCATOR_HALF + x * tile_size
    maxx = minx + tile_size
    maxy = WEB_MERCATOR_HALF - y * tile_size
    miny = maxy - tile_size
    return minx, miny, maxx, maxy

# In-memory tile cache to ensure instantaneous rendering on repeat requests
_tile_cache = {}

def get_satellite_tile(project_id: str, year: int, z: int, x: int, y: int, tile_size: int = 256) -> Optional[bytes]:
    cache_key = (project_id, year, z, x, y)
    if cache_key in _tile_cache:
        return _tile_cache[cache_key]
        
    sat_dir = REPO_ROOT / "data/processed/satellite" / project_id
    tif_path = sat_dir / f"sentinel2_{year}.tif"
    if not tif_path.exists():
        return None
        
    import rasterio
    from rasterio.warp import reproject, Resampling, transform_bounds
    from rasterio.crs import CRS
    import numpy as np
    from PIL import Image
    import io
    
    dst_crs = CRS.from_epsg(3857)
    minx, miny, maxx, maxy = _tile_to_mercator_bounds(z, x, y)
    
    with rasterio.open(tif_path) as src:
        src_crs = src.crs
        src_bounds_3857 = transform_bounds(src_crs, dst_crs, src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top)
        
        # Check intersection with raster coverage
        if (maxx < src_bounds_3857[0] or minx > src_bounds_3857[2] or
            maxy < src_bounds_3857[1] or miny > src_bounds_3857[3]):
            # Outside raster bounds -> empty transparent PNG
            img = Image.new("RGBA", (tile_size, tile_size), (0, 0, 0, 0))
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            png_bytes = buf.getvalue()
            if len(_tile_cache) < 2048:
                _tile_cache[cache_key] = png_bytes
            return png_bytes
        
        # Destination transform for tile
        dst_transform = rasterio.transform.from_bounds(minx, miny, maxx, maxy, tile_size, tile_size)
        
        # Read B4 (Red, band 3), B3 (Green, band 2), B2 (Blue, band 1)
        b_red = src.read(3).astype(np.float32)
        b_green = src.read(2).astype(np.float32)
        b_blue = src.read(1).astype(np.float32)
        
        dst_red = np.zeros((tile_size, tile_size), dtype=np.float32)
        dst_green = np.zeros((tile_size, tile_size), dtype=np.float32)
        dst_blue = np.zeros((tile_size, tile_size), dtype=np.float32)
        
        reproject(
            source=b_red,
            destination=dst_red,
            src_transform=src.transform,
            src_crs=src_crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear
        )
        reproject(
            source=b_green,
            destination=dst_green,
            src_transform=src.transform,
            src_crs=src_crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear
        )
        reproject(
            source=b_blue,
            destination=dst_blue,
            src_transform=src.transform,
            src_crs=src_crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear
        )
        
        valid_mask = (dst_red > 0) | (dst_green > 0) | (dst_blue > 0)
        r_u8 = np.clip(dst_red / 2800.0 * 255.0, 0, 255).astype(np.uint8)
        g_u8 = np.clip(dst_green / 2800.0 * 255.0, 0, 255).astype(np.uint8)
        b_u8 = np.clip(dst_blue / 2800.0 * 255.0, 0, 255).astype(np.uint8)
        alpha = np.where(valid_mask, 255, 0).astype(np.uint8)
        
        rgba = np.stack([r_u8, g_u8, b_u8, alpha], axis=-1)
        img = Image.fromarray(rgba, mode="RGBA")
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        png_bytes = buf.getvalue()
        
        if len(_tile_cache) < 2048:
            _tile_cache[cache_key] = png_bytes
        return png_bytes

def get_satellite_regional_metadata(project_id: str, year: int):
    sat_dir = REPO_ROOT / "data/processed/satellite_regional" / project_id
    tif_path = sat_dir / f"sentinel2_{year}.tif"
    if not tif_path.exists():
        # Fallback to local project-crop if regional not yet acquired
        return get_satellite_metadata(project_id, year)
    
    import rasterio
    from rasterio.warp import transform_bounds
    
    with rasterio.open(tif_path) as src:
        bounds = src.bounds
        crs = str(src.crs)
        w, h = src.width, src.height
        
        if src.crs.to_string() != "EPSG:4326":
            wgs84 = transform_bounds(src.crs, "EPSG:4326", bounds.left, bounds.bottom, bounds.right, bounds.top)
        else:
            wgs84 = (bounds.left, bounds.bottom, bounds.right, bounds.top)
        
        min_lon, min_lat, max_lon, max_lat = [float(round(x, 6)) for x in wgs84]
        
        dx = src.transform.a
        dy = -src.transform.e
        center_lat = (min_lat + max_lat) / 2.0
        import math
        res_m = dx * 111320.0 * math.cos(math.radians(center_lat))
        
        coordinates = [
            [min_lon, max_lat],
            [max_lon, max_lat],
            [max_lon, min_lat],
            [min_lon, min_lat]
        ]
        
        return {
            "project_id": project_id,
            "year": year,
            "sensor": "Sentinel-2 L2A (Harmonized)",
            "composite_type": "Regional Dry-Season Median Composite (SCL Masked)",
            "crs": crs,
            "width": w,
            "height": h,
            "bounds": [min_lon, min_lat, max_lon, max_lat],
            "coordinates": coordinates,
            "image_url": f"/api/satellite/regional/{project_id}/{year}/image.png",
            "tile_url_template": f"/api/satellite/regional/{project_id}/{year}/tiles/{{z}}/{{x}}/{{y}}.png",
            "resolution_description": f"Sentinel-2 L2A • True Color • ~{res_m:.1f} m grid (Regional Basemap)",
            "band_names": ["B4 (Red)", "B3 (Green)", "B2 (Blue)"],
            "stretch_range": [0.0, 2800.0],
            "is_reference_year": (year == 2026),
            "is_regional": True
        }

def get_satellite_regional_tile(project_id: str, year: int, z: int, x: int, y: int, tile_size: int = 256) -> Optional[bytes]:
    cache_key = ("regional", project_id, year, z, x, y)
    if cache_key in _tile_cache:
        return _tile_cache[cache_key]
        
    sat_dir = REPO_ROOT / "data/processed/satellite_regional" / project_id
    tif_path = sat_dir / f"sentinel2_{year}.tif"
    if not tif_path.exists():
        # Fallback to local crop
        return get_satellite_tile(project_id, year, z, x, y, tile_size)
        
    import rasterio
    from rasterio.warp import reproject, Resampling, transform_bounds
    from rasterio.crs import CRS
    import numpy as np
    from PIL import Image
    import io
    
    dst_crs = CRS.from_epsg(3857)
    minx, miny, maxx, maxy = _tile_to_mercator_bounds(z, x, y)
    
    with rasterio.open(tif_path) as src:
        src_crs = src.crs
        src_bounds_3857 = transform_bounds(src_crs, dst_crs, src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top)
        
        # Check intersection with regional raster coverage
        if (maxx < src_bounds_3857[0] or minx > src_bounds_3857[2] or
            maxy < src_bounds_3857[1] or miny > src_bounds_3857[3]):
            # Outside raster bounds -> empty transparent PNG
            img = Image.new("RGBA", (tile_size, tile_size), (0, 0, 0, 0))
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            png_bytes = buf.getvalue()
            if len(_tile_cache) < 2048:
                _tile_cache[cache_key] = png_bytes
            return png_bytes
        
        dst_transform = rasterio.transform.from_bounds(minx, miny, maxx, maxy, tile_size, tile_size)
        
        # Regional GeoTIFF has 3 bands: Band 1=B4 (Red), Band 2=B3 (Green), Band 3=B2 (Blue)
        b_red = src.read(1).astype(np.float32)
        b_green = src.read(2).astype(np.float32)
        b_blue = src.read(3).astype(np.float32)
        
        dst_red = np.zeros((tile_size, tile_size), dtype=np.float32)
        dst_green = np.zeros((tile_size, tile_size), dtype=np.float32)
        dst_blue = np.zeros((tile_size, tile_size), dtype=np.float32)
        
        reproject(
            source=b_red,
            destination=dst_red,
            src_transform=src.transform,
            src_crs=src_crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear
        )
        reproject(
            source=b_green,
            destination=dst_green,
            src_transform=src.transform,
            src_crs=src_crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear
        )
        reproject(
            source=b_blue,
            destination=dst_blue,
            src_transform=src.transform,
            src_crs=src_crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear
        )
        
        valid_mask = (dst_red > 0) | (dst_green > 0) | (dst_blue > 0)
        r_u8 = np.clip(dst_red / 2800.0 * 255.0, 0, 255).astype(np.uint8)
        g_u8 = np.clip(dst_green / 2800.0 * 255.0, 0, 255).astype(np.uint8)
        b_u8 = np.clip(dst_blue / 2800.0 * 255.0, 0, 255).astype(np.uint8)
        alpha = np.where(valid_mask, 255, 0).astype(np.uint8)
        
        rgba = np.stack([r_u8, g_u8, b_u8, alpha], axis=-1)
        img = Image.fromarray(rgba, mode="RGBA")
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        png_bytes = buf.getvalue()
        
        if len(_tile_cache) < 2048:
            _tile_cache[cache_key] = png_bytes
        return png_bytes


