"""
PARIVESH Real Monsoon Satellite Data Audit (Feature 4 - June-October Audit)

Audits Sentinel-2 Surface Reflectance Harmonized (COPERNICUS/S2_SR_HARMONIZED)
availability and valid pixel boundary coverage for June, July, August, September,
and October across historical years 2021-2025 and available 2026 months.

Generates data/processed/satellite/monsoon_audit.csv with actual empirical
GEE statistics for each Project x Year x Month.
"""

import csv
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    },
    "MH-002": {
        "project_name": "Gadchiroli",
        "boundary_file": "data/processed/project_boundaries/gadchiroli_boundary.geojson",
    },
    "MH-003": {
        "project_name": "Bhivpuri PSP",
        "boundary_file": "data/processed/project_boundaries/bhivpuri_boundary.geojson",
    },
}

YEARS = [2021, 2022, 2023, 2024, 2025, 2026]
MONSOON_MONTHS = [
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
]
MAX_CLOUD_PERCENT = 20


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


def audit_project_month(pid: str, pname: str, b_file: Path, yr: int, month_num: int, month_name: str) -> Dict[str, str]:
    """Audits a single Project x Year x Month combination using GEE queries."""
    # Current audit execution date: August 23, 2026
    # Future months in 2026 (September, October) must be marked future_period
    if yr == 2026 and month_num in [9, 10]:
        return {
            "project_id": pid,
            "project_name": pname,
            "year": str(yr),
            "month": f"{month_num:02d}",
            "month_name": month_name,
            "scenes_available": "0",
            "scenes_cloud_filtered": "0",
            "usable_scenes": "0",
            "valid_pixel_coverage_percent": "0.0",
            "usability_status": "future_period",
        }

    ee_geom, geom_status = load_geojson_geometry(b_file)
    if ee_geom is None:
        return {
            "project_id": pid,
            "project_name": pname,
            "year": str(yr),
            "month": f"{month_num:02d}",
            "month_name": month_name,
            "scenes_available": "0",
            "scenes_cloud_filtered": "0",
            "usable_scenes": "0",
            "valid_pixel_coverage_percent": "0.0",
            "usability_status": "failed_boundary_missing",
        }

    start_date = f"{yr}-{month_num:02d}-01"
    if month_num == 12:
        end_date = f"{yr+1}-01-01"
    else:
        end_date = f"{yr}-{month_num+1:02d}-01"

    # Total boundary pixels at 30m resolution
    total_pix_img = ee.Image.constant(1).clip(ee_geom)
    total_pix_count = (
        total_pix_img.reduceRegion(reducer=ee.Reducer.count(), geometry=ee_geom, scale=30, maxPixels=1e9)
        .get("constant")
        .getInfo()
    )

    if total_pix_count is None or total_pix_count == 0:
        total_pix_count = 1  # Guard against divide by zero

    # 1. Total available Sentinel-2 scenes
    s2_raw = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(ee_geom)
        .filterDate(start_date, end_date)
    )

    # 2. Scene-level cloud filtered scenes (<20% cloud cover)
    s2_filtered = s2_raw.filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", MAX_CLOUD_PERCENT))

    raw_avail = s2_raw.size().getInfo()
    filt_avail = s2_filtered.size().getInfo()

    valid_coverage_pct = 0.0
    usable_scenes_count = 0

    if filt_avail > 0:
        # Apply pixel-level SCL cloud/shadow mask
        s2_masked = s2_filtered.map(mask_s2_clouds_scl)
        comp = s2_masked.select("B2").median().clip(ee_geom)

        # Count valid non-masked pixels inside boundary
        valid_sum_dict = comp.mask().reduceRegion(
            reducer=ee.Reducer.sum(), geometry=ee_geom, scale=30, maxPixels=1e9
        ).getInfo()

        valid_pix_sum = valid_sum_dict.get("B2", 0.0) if valid_sum_dict else 0.0
        if valid_pix_sum is None:
            valid_pix_sum = 0.0

        valid_coverage_pct = min(100.0, (valid_pix_sum / float(total_pix_count)) * 100.0)
        usable_scenes_count = filt_avail

    # Usability Classification Rule
    if filt_avail == 0 or valid_coverage_pct == 0.0:
        usability_status = "no_data"
    elif valid_coverage_pct >= 80.0:
        usability_status = "usable"
    elif valid_coverage_pct >= 50.0:
        usability_status = "limited"
    else:
        usability_status = "insufficient"

    print(
        f"  [{pid} {pname} {yr}-{month_num:02d} ({month_name})] Avail: {raw_avail:2d} | Filt(<20%): {filt_avail:2d} | Coverage: {valid_coverage_pct:5.1f}% ({usability_status})",
        flush=True,
    )

    return {
        "project_id": pid,
        "project_name": pname,
        "year": str(yr),
        "month": f"{month_num:02d}",
        "month_name": month_name,
        "scenes_available": str(raw_avail),
        "scenes_cloud_filtered": str(filt_avail),
        "usable_scenes": str(usable_scenes_count),
        "valid_pixel_coverage_percent": f"{valid_coverage_pct:.1f}",
        "usability_status": usability_status,
    }


def run_monsoon_audit() -> List[Dict[str, str]]:
    """Runs the June-October monsoon data audit across all projects and years."""
    records: List[Dict[str, str]] = []
    tasks = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        for pid, proj_info in PROJECT_MAPPING.items():
            pname = proj_info["project_name"]
            b_file = Path(proj_info["boundary_file"])

            print(f"Submitting monsoon audit tasks for Project {pid}: {pname}...", flush=True)
            for yr in YEARS:
                for month_num, month_name in MONSOON_MONTHS:
                    t = executor.submit(audit_project_month, pid, pname, b_file, yr, month_num, month_name)
                    tasks.append(t)

        for future in as_completed(tasks):
            try:
                rec = future.result()
                records.append(rec)
            except Exception as err:
                print(f"Error in monsoon audit task: {err}", file=sys.stderr, flush=True)

    # Sort records deterministically by project_id, year, month
    records.sort(key=lambda r: (r["project_id"], r["year"], r["month"]))
    return records


def write_monsoon_audit_csv(records: List[Dict[str, str]], output_csv: Path) -> None:
    """Writes monsoon audit records to CSV."""
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "project_id",
        "project_name",
        "year",
        "month",
        "month_name",
        "scenes_available",
        "scenes_cloud_filtered",
        "usable_scenes",
        "valid_pixel_coverage_percent",
        "usability_status",
    ]

    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    if not initialize_earth_engine():
        sys.exit(1)

    print("Starting PARIVESH Real Monsoon Data Audit (June-October)...", flush=True)
    records = run_monsoon_audit()
    output_csv = Path("data/processed/satellite/monsoon_audit.csv")
    write_monsoon_audit_csv(records, output_csv)

    print("\nPARIVESH Monsoon Data Audit Complete", flush=True)
    print("====================================", flush=True)
    print(f"Total audit records logged: {len(records)}", flush=True)
    print(f"Audit log written to: {output_csv.as_posix()}", flush=True)


if __name__ == "__main__":
    main()
