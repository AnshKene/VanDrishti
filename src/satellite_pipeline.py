"""
PARIVESH Real Google Earth Engine Satellite Data Pipeline (Feature 4 - Final Integrity Corrected)

Extracts Sentinel-2 Surface Reflectance Harmonized (COPERNICUS/S2_SR_HARMONIZED)
and Dynamic World (GOOGLE/DYNAMICWORLD/V1) observations for the three validated
project boundaries across 2021-2026.

Integrates:
- Scene-level pre-filtering (CLOUDY_PIXEL_PERCENTAGE < 20%)
- Pixel-level cloud/shadow masking via SCL (Scene Classification Layer) band
- 6 Base Spectral Bands: B2, B3, B4, B8, B11, B12 (NDVI deferred to Feature 5)
- Dynamic World V1 reference baseline mode classification labels
- Precise temporal provenance and 2026 future period tracking in satellite_metadata.csv
"""

import csv
import json
import sys
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import ee

# Earth Engine Project Configuration
GEE_PROJECT_ID = "aqueous-aileron-505816-s1"

# Project Mappings to boundary files
PROJECT_MAPPING: Dict[str, Dict[str, str]] = {
    "MH-001": {
        "project_name": "Gondkhari",
        "boundary_file": "data/processed/project_boundaries/gondkhari_boundary.geojson",
        "folder_name": "MH-001",
    },
    "MH-002": {
        "project_name": "Gadchiroli",
        "boundary_file": "data/processed/project_boundaries/gadchiroli_boundary.geojson",
        "folder_name": "MH-002",
    },
    "MH-003": {
        "project_name": "Bhivpuri PSP",
        "boundary_file": "data/processed/project_boundaries/bhivpuri_boundary.geojson",
        "folder_name": "MH-003",
    },
}

# Monitoring Period Settings
YEARS = [2021, 2022, 2023, 2024, 2025, 2026]
MAX_CLOUD_PERCENT = 20
S2_BANDS = ["B2", "B3", "B4", "B8", "B11", "B12"]


def initialize_earth_engine() -> bool:
    """Initializes Google Earth Engine with designated project ID."""
    try:
        ee.Initialize(project=GEE_PROJECT_ID)
        print(f"Google Earth Engine initialization: SUCCESS (Project: {GEE_PROJECT_ID})", flush=True)
        return True
    except Exception as err:
        print(f"Google Earth Engine initialization: FAILED ({err})", file=sys.stderr, flush=True)
        return False


def load_geojson_geometry(boundary_path: Path) -> Tuple[Optional[ee.Geometry], str]:
    """Loads GeoJSON boundary file and returns GEE Geometry object."""
    if not boundary_path.exists():
        return None, f"Boundary file '{boundary_path}' not found."

    try:
        with open(boundary_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        geom_dict = data["features"][0]["geometry"]
        ee_geom = ee.Geometry(geom_dict)
        return ee_geom, "Valid"
    except Exception as err:
        return None, f"Error parsing GeoJSON '{boundary_path.name}': {err}"


def mask_s2_clouds_scl(image: ee.Image) -> ee.Image:
    """
    Applies pixel-level cloud and shadow masking on Sentinel-2 SR Harmonized imagery using the SCL band.
    SCL Band Classes masked out:
      3 = Cloud Shadows
      8 = Cloud Medium Probability
      9 = Cloud High Probability
      10 = Thin Cirrus
      11 = Snow / Ice
    """
    scl = image.select("SCL")
    valid_mask = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
    return image.updateMask(valid_mask)


def download_single_raster(url: str, output_path: Path, retries: int = 3) -> bool:
    """Downloads GeoTIFF raster content from Earth Engine URL with retry logic."""
    import time
    for attempt in range(1, retries + 1):
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                content = resp.read()

            if url.endswith(".zip") or content.startswith(b"PK"):
                with zipfile.ZipFile(BytesIO(content)) as z:
                    for fname in z.namelist():
                        if fname.endswith(".tif") or fname.endswith(".tiff"):
                            output_path.write_bytes(z.read(fname))
                            return True
            else:
                output_path.write_bytes(content)
                return True
        except Exception as err:
            if attempt < retries:
                time.sleep(2 * attempt)
            else:
                print(f"Warning: Failed to download GeoTIFF '{output_path.name}' after {retries} attempts: {err}", file=sys.stderr, flush=True)
                return False

    return False


def process_project_year(pid: str, pname: str, folder_name: str, b_file: Path, yr: int) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Processes a single project year and returns metadata records for Sentinel-2 and Dynamic World."""
    base_out_dir = Path("data/processed/satellite")
    proj_dir = base_out_dir / folder_name
    proj_dir.mkdir(parents=True, exist_ok=True)

    ee_geom, geom_status = load_geojson_geometry(b_file)
    requested_start = f"{yr}-01-01"
    requested_end = f"{yr}-12-31"
    monitoring_win = "Jan-May & Nov-Dec (Dry Season)"

    is_current_year = (yr == 2026)
    proc_status = "partial_current_year" if is_current_year else "completed"
    missing_period = "2026-11-01 to 2026-12-31 (future_monitoring_period)" if is_current_year else "None"

    if ee_geom is None:
        fail_rec = {
            "project_id": pid,
            "project_name": pname,
            "year": str(yr),
            "dataset": "N/A",
            "requested_start_date": requested_start,
            "requested_end_date": requested_end,
            "monitoring_window": monitoring_win,
            "actual_available_start_date": "N/A",
            "actual_available_end_date": "N/A",
            "selected_observation_start_date": "N/A",
            "selected_observation_end_date": "N/A",
            "images_available": "0",
            "images_after_cloud_filter": "0",
            "images_used": "0",
            "cloud_threshold": "N/A",
            "composite_method": "N/A",
            "bands": "N/A",
            "boundary_file": b_file.as_posix(),
            "processing_status": "failed_boundary_missing",
            "missing_period": missing_period,
        }
        return fail_rec, fail_rec

    # Dry season filter: Jan-May & Nov-Dec (excludes June-October monsoon cloud obscuration)
    dry_season_filter = ee.Filter.Or(
        ee.Filter.calendarRange(1, 5, "month"),
        ee.Filter.calendarRange(11, 12, "month")
    )

    # Query Sentinel-2 Collection
    s2_raw = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(ee_geom)
        .filterDate(requested_start, requested_end)
        .filter(dry_season_filter)
    )
    s2_filtered = s2_raw.filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", MAX_CLOUD_PERCENT))

    # Query Dynamic World Collection
    dw_raw = (
        ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
        .filterBounds(ee_geom)
        .filterDate(requested_start, requested_end)
        .filter(dry_season_filter)
    )

    # Retrieve collection statistics & timestamps
    eval_dict = ee.Dictionary({
        "s2_avail": s2_raw.size(),
        "s2_filtered": s2_filtered.size(),
        "dw_avail": dw_raw.size(),
        "s2_timestamps": s2_raw.aggregate_array("system:time_start"),
        "s2_filt_timestamps": s2_filtered.aggregate_array("system:time_start"),
    }).getInfo()

    s2_avail = eval_dict["s2_avail"]
    s2_filt = eval_dict["s2_filtered"]
    dw_avail = eval_dict["dw_avail"]

    # Calculate actual available start and end observation dates from Earth Engine
    if s2_avail > 0:
        raw_ts = sorted(eval_dict["s2_timestamps"])
        act_avail_start = ee.Date(raw_ts[0]).format("YYYY-MM-dd").getInfo()
        act_avail_end = ee.Date(raw_ts[-1]).format("YYYY-MM-dd").getInfo()
    else:
        act_avail_start, act_avail_end = "N/A", "N/A"

    if s2_filt > 0:
        filt_ts = sorted(eval_dict["s2_filt_timestamps"])
        sel_obs_start = ee.Date(filt_ts[0]).format("YYYY-MM-dd").getInfo()
        sel_obs_end = ee.Date(filt_ts[-1]).format("YYYY-MM-dd").getInfo()
    else:
        sel_obs_start, sel_obs_end = act_avail_start, act_avail_end

    # 1. Sentinel-2 Composite (6 Base Spectral Bands: B2, B3, B4, B8, B11, B12 with SCL Pixel-Level Cloud/Shadow Masking)
    s2_status = proc_status
    s2_out_file = proj_dir / f"sentinel2_{yr}.tif"

    if s2_filt > 0:
        # Apply scene-level filter + SCL pixel-level cloud/shadow mask
        s2_masked_coll = s2_filtered.map(mask_s2_clouds_scl)
        s2_comp = s2_masked_coll.select(S2_BANDS).median().clip(ee_geom)

        s2_url = s2_comp.getDownloadURL({
            "name": f"sentinel2_{pid}_{yr}",
            "scale": 30,
            "crs": "EPSG:4326",
            "filePerBand": False,
        })
        if not download_single_raster(s2_url, s2_out_file):
            s2_status = "export_failed"
    else:
        s2_status = "insufficient_observations"

    s2_record = {
        "project_id": pid,
        "project_name": pname,
        "year": str(yr),
        "dataset": "Sentinel-2 SR Harmonized",
        "requested_start_date": requested_start,
        "requested_end_date": requested_end,
        "monitoring_window": monitoring_win,
        "actual_available_start_date": act_avail_start,
        "actual_available_end_date": act_avail_end,
        "selected_observation_start_date": sel_obs_start,
        "selected_observation_end_date": sel_obs_end,
        "images_available": str(s2_avail),
        "images_after_cloud_filter": str(s2_filt),
        "images_used": str(s2_filt),
        "cloud_threshold": f"{MAX_CLOUD_PERCENT}% scene-filter + SCL pixel-mask",
        "composite_method": "Seasonal Median Composite (SCL Cloud/Shadow Masked)",
        "bands": "B2,B3,B4,B8,B11,B12",
        "boundary_file": b_file.as_posix(),
        "processing_status": s2_status,
        "missing_period": missing_period,
    }

    # 2. Dynamic World Composite (Reference Baseline Mode Label)
    dw_status = proc_status
    dw_out_file = proj_dir / f"dynamicworld_{yr}.tif"

    if dw_avail > 0:
        dw_label = dw_raw.select("label").reduce(ee.Reducer.mode()).rename("label").clip(ee_geom)

        dw_url = dw_label.getDownloadURL({
            "name": f"dynamicworld_{pid}_{yr}",
            "scale": 30,
            "crs": "EPSG:4326",
            "filePerBand": False,
        })
        if not download_single_raster(dw_url, dw_out_file):
            dw_status = "export_failed"
    else:
        dw_status = "insufficient_observations"

    dw_record = {
        "project_id": pid,
        "project_name": pname,
        "year": str(yr),
        "dataset": "Dynamic World V1 (reference_baseline)",
        "requested_start_date": requested_start,
        "requested_end_date": requested_end,
        "monitoring_window": monitoring_win,
        "actual_available_start_date": act_avail_start,
        "actual_available_end_date": act_avail_end,
        "selected_observation_start_date": sel_obs_start,
        "selected_observation_end_date": sel_obs_end,
        "images_available": str(dw_avail),
        "images_after_cloud_filter": str(dw_avail),
        "images_used": str(dw_avail),
        "cloud_threshold": "N/A",
        "composite_method": "Seasonal Mode Composite",
        "bands": "label",
        "boundary_file": b_file.as_posix(),
        "processing_status": dw_status,
        "missing_period": missing_period,
    }

    print(f"  [{pid} {pname} {yr}] S2: {s2_filt}/{s2_avail} scenes ({sel_obs_start} to {sel_obs_end}, {s2_status}) | DW: {dw_avail} scenes ({dw_status})", flush=True)
    return s2_record, dw_record


def process_satellite_data() -> List[Dict[str, str]]:
    """Executes Sentinel-2 and Dynamic World processing for all projects across 2021-2026."""
    metadata_records: List[Dict[str, str]] = []

    tasks = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        for pid, proj_info in PROJECT_MAPPING.items():
            pname = proj_info["project_name"]
            b_file = Path(proj_info["boundary_file"])
            folder_name = proj_info["folder_name"]

            print(f"Submitting tasks for Project {pid}: {pname} (2021-2026)...", flush=True)
            for yr in YEARS:
                t = executor.submit(process_project_year, pid, pname, folder_name, b_file, yr)
                tasks.append(t)

        for future in as_completed(tasks):
            try:
                s2_rec, dw_rec = future.result()
                metadata_records.append(s2_rec)
                metadata_records.append(dw_rec)
            except Exception as err:
                print(f"Error in satellite processing task: {err}", file=sys.stderr, flush=True)

    # Sort records deterministically by project_id, dataset, year
    metadata_records.sort(key=lambda r: (r["project_id"], r["dataset"], r["year"]))
    return metadata_records


def write_satellite_metadata_csv(records: List[Dict[str, str]], output_csv: Path) -> None:
    """Writes satellite metadata records to CSV file."""
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "project_id",
        "project_name",
        "year",
        "dataset",
        "requested_start_date",
        "requested_end_date",
        "monitoring_window",
        "actual_available_start_date",
        "actual_available_end_date",
        "selected_observation_start_date",
        "selected_observation_end_date",
        "images_available",
        "images_after_cloud_filter",
        "images_used",
        "cloud_threshold",
        "composite_method",
        "bands",
        "boundary_file",
        "processing_status",
        "missing_period",
    ]

    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    if not initialize_earth_engine():
        sys.exit(1)

    print("Starting Final Audited PARIVESH Satellite Pipeline (Sentinel-2 & Dynamic World)...", flush=True)
    records = process_satellite_data()
    output_csv = Path("data/processed/satellite/satellite_metadata.csv")
    write_satellite_metadata_csv(records, output_csv)

    print("\nPARIVESH Satellite Pipeline Processing Complete", flush=True)
    print("===============================================", flush=True)
    print(f"Total processed composite raster products logged: {len(records)}", flush=True)
    print(f"Metadata log written to: {output_csv.as_posix()}", flush=True)


if __name__ == "__main__":
    main()
