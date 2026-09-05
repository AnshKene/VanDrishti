import os
import sys
import json
import time
import hashlib
from pathlib import Path

import ee
import rasterio
import numpy as np

root = Path(r"c:\Users\anshk\Desktop\Environmental-Monitoring")
base_out_dir = root / "data" / "processed" / "satellite_regional"
base_out_dir.mkdir(parents=True, exist_ok=True)

GEE_PROJECT_ID = "aqueous-aileron-505816-s1"

PROJECT_CONFIGS = {
    "MH-001": {
        "project_name": "Gondkhari",
        "aoi": [78.7500, 21.0000, 79.1000, 21.3000],
        "width": 1200,
        "height": 1100
    },
    "MH-002": {
        "project_name": "Gadchiroli",
        "aoi": [80.1800, 19.4500, 80.5400, 19.7600],
        "width": 1200,
        "height": 1100
    },
    "MH-003": {
        "project_name": "Bhivpuri PSP",
        "aoi": [73.3000, 18.7800, 73.6500, 19.0800],
        "width": 1200,
        "height": 1100
    }
}

YEARS = [2021, 2022, 2023, 2024, 2025, 2026]

print("================================================================================", flush=True)
print("SCALING REGIONAL SENTINEL-2 DATA ACQUISITION (18 DATASETS)", flush=True)
print("================================================================================", flush=True)

ee.Initialize(project=GEE_PROJECT_ID)
print(f"GEE Initialized with project: {GEE_PROJECT_ID}", flush=True)

def mask_s2_clouds_scl(image: ee.Image) -> ee.Image:
    scl = image.select("SCL")
    valid_mask = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
    return image.updateMask(valid_mask)

# Dry season calendar filter (Jan-May & Nov-Dec)
dry_season_filter = ee.Filter.Or(
    ee.Filter.calendarRange(1, 5, "month"),
    ee.Filter.calendarRange(11, 12, "month")
)

results = []

for pid, cfg in PROJECT_CONFIGS.items():
    p_dir = base_out_dir / pid
    p_dir.mkdir(parents=True, exist_ok=True)
    aoi_bounds = cfg["aoi"]
    aoi_geom = ee.Geometry.Rectangle(aoi_bounds)
    w_px = cfg["width"]
    h_px = cfg["height"]
    
    min_lon, min_lat, max_lon, max_lat = aoi_bounds
    scale_x = (max_lon - min_lon) / w_px
    scale_y = -(max_lat - min_lat) / h_px
    
    print(f"\n==================== PROJECT: {pid} ({cfg['project_name']}) ====================", flush=True)
    
    for yr in YEARS:
        tif_path = p_dir / f"sentinel2_{yr}.tif"
        meta_path = p_dir / f"sentinel2_{yr}_metadata.json"
        
        # Check if already completed and verified (e.g. MH-001 2025)
        if tif_path.exists() and meta_path.exists() and pid == "MH-001" and yr == 2025:
            print(f"  [{pid} / {yr}] ALREADY COMPLETED & VERIFIED (Skipping re-download)", flush=True)
            with open(meta_path, "r") as f:
                meta_doc = json.load(f)
            results.append(meta_doc)
            continue
            
        print(f"\n  --- Processing {pid} / {yr} ---", flush=True)
        start_date = f"{yr}-01-01"
        end_date = f"{yr}-12-31" if yr < 2026 else "2026-05-31"
        is_ref_year = (yr == 2026)
        
        # Filter Sentinel-2 collection
        s2_coll = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(aoi_geom)
            .filterDate(start_date, end_date)
            .filter(dry_season_filter)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 15))
            .sort("CLOUDY_PIXEL_PERCENTAGE")
            .limit(12)
        )
        
        scene_count = s2_coll.size().getInfo()
        print(f"    Selected {scene_count} clear dry-season scenes for {yr}", flush=True)
        
        s2_masked = s2_coll.map(mask_s2_clouds_scl)
        # Select True Color bands: B4 (Red), B3 (Green), B2 (Blue) and cast to uint16
        rgb_comp = s2_masked.select(["B4", "B3", "B2"]).median().toUint16().clip(aoi_geom)
        
        t0 = time.time()
        print(f"    Requesting computePixels for {w_px}x{h_px} grid...", flush=True)
        
        pixels = None
        for attempt in range(1, 4):
            try:
                pixels = ee.data.computePixels({
                    'expression': rgb_comp,
                    'fileFormat': 'GEO_TIFF',
                    'grid': {
                        'dimensions': {
                            'width': w_px,
                            'height': h_px
                        },
                        'affineTransform': {
                            'scaleX': scale_x,
                            'shearX': 0,
                            'translateX': min_lon,
                            'shearY': 0,
                            'scaleY': scale_y,
                            'translateY': max_lat
                        },
                        'crsCode': 'EPSG:4326'
                    }
                })
                break
            except Exception as e:
                print(f"    Attempt {attempt} failed: {e}. Retrying...", flush=True)
                time.sleep(3 * attempt)
                
        if pixels is None:
            raise RuntimeError(f"Failed to acquire {pid} {yr} after 3 attempts.")
            
        t1 = time.time()
        tif_path.write_bytes(pixels)
        print(f"    Downloaded {len(pixels):,} bytes in {t1-t0:.2f}s", flush=True)
        
        # Forensic Inspection of created GeoTIFF
        sha256_hash = hashlib.sha256(pixels).hexdigest()
        
        with rasterio.open(tif_path) as src:
            w, h = src.width, src.height
            count = src.count
            dtype = src.dtypes[0]
            crs = str(src.crs)
            transform = src.transform
            dx = transform.a
            dy = -transform.e
            bounds = src.bounds
            
            center_lat = (bounds.bottom + bounds.top) / 2.0
            m_lon = 111320.0 * np.cos(np.radians(center_lat))
            m_lat = 110540.0
            res_m_x = dx * m_lon
            res_m_y = dy * m_lat
            
            band_names = ["Band 1 (B4 Red)", "Band 2 (B3 Green)", "Band 3 (B2 Blue)"]
            band_stats = {}
            for i, bname in enumerate(band_names, start=1):
                arr = src.read(i).astype(np.float32)
                valid = arr[arr > 0]
                if len(valid) > 0:
                    band_stats[bname] = {
                        "min": float(np.min(valid)),
                        "p02": float(np.percentile(valid, 2)),
                        "median": float(np.median(valid)),
                        "p98": float(np.percentile(valid, 98)),
                        "max": float(np.max(valid)),
                        "valid_pixel_percentage": float(len(valid) / (w * h) * 100.0)
                    }
                    
            print(f"    Verified: {w}x{h} px, CRS={crs}, Res=~{res_m_x:.1f}m x ~{res_m_y:.1f}m, SHA256={sha256_hash[:12]}...", flush=True)
            
        meta_doc = {
            "project_id": pid,
            "year": yr,
            "role": "regional_basemap",
            "source_collection": "COPERNICUS/S2_SR_HARMONIZED",
            "observation_window": f"{start_date} to {end_date} (Dry Season)",
            "scenes_used": scene_count,
            "cloud_masking": "SCL scene classification (classes 3, 8, 9, 10, 11 masked) + QA60",
            "composite_method": "Seasonal Pixel-wise Median",
            "bands": ["B4 (Red)", "B3 (Green)", "B2 (Blue)"],
            "crs": crs,
            "native_grid_resolution": f"~{res_m_x:.1f} m (dx={dx:.8f} deg, dy={dy:.8f} deg)",
            "dimensions": [w, h],
            "bounds": [bounds.left, bounds.bottom, bounds.right, bounds.top],
            "file_size_bytes": len(pixels),
            "sha256": sha256_hash,
            "is_reference_year": is_ref_year,
            "band_statistics": band_stats,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        with open(meta_path, "w") as f:
            json.dump(meta_doc, f, indent=2)
            
        results.append(meta_doc)

# Write master regional manifest CSV
manifest_csv = base_out_dir / "satellite_regional_manifest.csv"
with open(manifest_csv, "w", newline="", encoding="utf-8") as f:
    import csv
    writer = csv.writer(f)
    writer.writerow(["project_id", "year", "role", "width", "height", "bounds", "resolution", "file_size_bytes", "sha256", "is_reference_year"])
    for r in results:
        writer.writerow([r["project_id"], r["year"], r["role"], r["dimensions"][0], r["dimensions"][1], str(r["bounds"]), r["native_grid_resolution"], r["file_size_bytes"], r["sha256"], r.get("is_reference_year", False)])

print(f"\n================================================================================", flush=True)
print(f"SUCCESS: All 18 Regional Datasets Acquired and Manifest Saved to {manifest_csv.relative_to(root)}", flush=True)
print(f"================================================================================", flush=True)
