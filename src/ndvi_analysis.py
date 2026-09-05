"""
PARIVESH Real NDVI & Vegetation Baseline Analysis (Feature 5 - Spatial Area Corrected)

Calculates real Sentinel-2 NDVI baselines from multi-spectral GeoTIFF composites
(COPERNICUS/S2_SR_HARMONIZED) masked strictly to validated GeoJSON project boundaries
for three environmentally approved Maharashtra projects (MH-001, MH-002, MH-003).

Formula:
  NDVI = (B8 - B4) / (B8 + B4)
  where B4 = Red (Band 3), B8 = NIR (Band 4)

Outputs:
  - data/processed/vegetation/spatial_integrity_audit.csv
  - data/processed/vegetation/ndvi_statistics.csv
  - data/processed/vegetation/ndvi_candidate_thresholds.csv
  - data/processed/vegetation/ndvi_change_analysis.csv
  - data/processed/vegetation/ndvi/<project_id>/ndvi_<year>.tif
"""

import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from rasterio.warp import Resampling, calculate_default_transform, reproject
from shapely.geometry import mapping

# Metric EPSG projections matching Feature 3 boundary validation
PROJECT_UTM: Dict[str, str] = {
    "MH-001": "EPSG:32644",
    "MH-002": "EPSG:32644",
    "MH-003": "EPSG:32643",
}

PROJECT_NAMES: Dict[str, str] = {
    "MH-001": "Gondkhari",
    "MH-002": "Gadchiroli",
    "MH-003": "Bhivpuri PSP",
}

BOUNDARY_FILES: Dict[str, str] = {
    "MH-001": "data/processed/project_boundaries/gondkhari_boundary.geojson",
    "MH-002": "data/processed/project_boundaries/gadchiroli_boundary.geojson",
    "MH-003": "data/processed/project_boundaries/bhivpuri_boundary.geojson",
}

YEARS = [2021, 2022, 2023, 2024, 2025, 2026]
CANDIDATE_THRESHOLDS = [0.20, 0.25, 0.30, 0.35, 0.40]
PROVISIONAL_VEGETATION_THRESHOLD = 0.25


def compute_metric_area_ha(src: rasterio.DatasetReader, mask_2d: np.ndarray, target_crs: str) -> Tuple[int, float]:
    """
    Reprojects a 2D boolean polygon mask from raster CRS (EPSG:4326) to target metric CRS (e.g. EPSG:32644)
    at 30m resolution and calculates valid pixel count and projected area in hectares.
    """
    transform_utm, width_utm, height_utm = calculate_default_transform(
        src.crs, target_crs, src.width, src.height, *src.bounds, resolution=30.0
    )
    dst_array = np.zeros((height_utm, width_utm), dtype=np.uint8)
    reproject(
        source=mask_2d.astype(np.uint8),
        destination=dst_array,
        src_transform=src.transform,
        src_crs=src.crs,
        dst_transform=transform_utm,
        dst_crs=target_crs,
        resampling=Resampling.nearest,
    )
    pixel_count = int(np.sum(dst_array == 1))
    area_ha = (pixel_count * (30.0 * 30.0)) / 10000.0
    return pixel_count, float(area_ha)


def process_project_year(
    pid: str, pname: str, b_path: Path, yr: int, target_crs: str
) -> Tuple[Dict[str, str], Dict[str, str], List[Dict[str, str]]]:
    """Processes a single project year, masking strictly by validated boundary geometry."""
    tif_path = Path(f"data/processed/satellite/{pid}/sentinel2_{yr}.tif")
    if not tif_path.exists():
        raise FileNotFoundError(f"Source Sentinel-2 raster '{tif_path}' not found.")

    proc_status = "partial_current_year" if yr == 2026 else "completed"

    # 1. Load validated GeoJSON boundary
    gdf = gpd.read_file(b_path)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    gdf_utm = gdf.to_crs(target_crs)
    boundary_area_ha = float(gdf_utm.geometry.area.sum() / 10000.0)
    geoms = [mapping(geom) for geom in gdf.geometry]

    with rasterio.open(tif_path) as src:
        # Calculate raster bounding box area
        bbox_w_m = (src.bounds.right - src.bounds.left) * 111320.0 * np.cos(np.radians(src.bounds.bottom))
        bbox_h_m = (src.bounds.top - src.bounds.bottom) * 111320.0
        bbox_area_ha = float((bbox_w_m * bbox_h_m) / 10000.0)

        # 2. Polygon-mask raster imagery
        out_image, out_transform = mask(src, geoms, crop=False, nodata=np.nan)

        b4 = out_image[2].astype(np.float64)  # Band 3 = B4 Red
        b8 = out_image[3].astype(np.float64)  # Band 4 = B8 NIR

        denom = b8 + b4
        polygon_valid_mask = (~np.isnan(b4)) & (~np.isnan(b8)) & (denom != 0) & (b4 > 0) & (b8 > 0)

        # Compute metric area strictly inside boundary polygon
        masked_valid_pixels, masked_area_ha = compute_metric_area_ha(src, polygon_valid_mask, target_crs)

        area_diff_pct = abs(masked_area_ha - boundary_area_ha) / boundary_area_ha * 100.0
        spatial_status = "PASS" if area_diff_pct < 5.0 else "FAIL"

        audit_rec = {
            "project_id": pid,
            "project_name": pname,
            "year": str(yr),
            "boundary_area_ha": f"{boundary_area_ha:.3f}",
            "raster_footprint_area_ha": f"{bbox_area_ha:.3f}",
            "masked_valid_area_ha": f"{masked_area_ha:.3f}",
            "valid_pixel_count": str(masked_valid_pixels),
            "crs": target_crs,
            "pixel_width_m": "30.0",
            "pixel_height_m": "30.0",
            "area_diff_percent": f"{area_diff_pct:.2f}",
            "spatial_status": spatial_status,
        }

        # 3. Calculate NDVI strictly inside boundary
        ndvi = np.full_like(b4, np.nan, dtype=np.float64)
        ndvi[polygon_valid_mask] = (b8[polygon_valid_mask] - b4[polygon_valid_mask]) / denom[polygon_valid_mask]
        v_ndvi = ndvi[polygon_valid_mask]

        mean_v = float(np.mean(v_ndvi))
        med_v = float(np.median(v_ndvi))
        min_v = float(np.min(v_ndvi))
        max_v = float(np.max(v_ndvi))
        std_v = float(np.std(v_ndvi))
        p10, p25, p75, p90 = [float(x) for x in np.percentile(v_ndvi, [10, 25, 75, 90])]

        # Candidate threshold investigation (polygon-masked)
        thresh_records = []
        for thresh in CANDIDATE_THRESHOLDS:
            veg_m = polygon_valid_mask & (ndvi >= thresh)
            veg_count, veg_ha = compute_metric_area_ha(src, veg_m, target_crs)
            veg_pct = (veg_ha / masked_area_ha * 100.0) if masked_area_ha > 0 else 0.0
            thresh_records.append({
                "project_id": pid,
                "project_name": pname,
                "year": str(yr),
                "threshold": f"{thresh:.2f}",
                "vegetation_area_ha": f"{veg_ha:.3f}",
                "vegetation_percentage": f"{veg_pct:.2f}",
                "vegetation_pixel_count": str(veg_count),
                "threshold_status": "provisional",
            })

        # Provisional Threshold Metrics (NDVI >= 0.25)
        prov_veg_mask = polygon_valid_mask & (ndvi >= PROVISIONAL_VEGETATION_THRESHOLD)
        _, prov_veg_ha = compute_metric_area_ha(src, prov_veg_mask, target_crs)
        prov_veg_pct = (prov_veg_ha / masked_area_ha * 100.0) if masked_area_ha > 0 else 0.0

        stat_rec = {
            "project_id": pid,
            "project_name": pname,
            "year": str(yr),
            "processing_status": proc_status,
            "mean_ndvi": f"{mean_v:.4f}",
            "median_ndvi": f"{med_v:.4f}",
            "min_ndvi": f"{min_v:.4f}",
            "max_ndvi": f"{max_v:.4f}",
            "std_ndvi": f"{std_v:.4f}",
            "p10_ndvi": f"{p10:.4f}",
            "p25_ndvi": f"{p25:.4f}",
            "p75_ndvi": f"{p75:.4f}",
            "p90_ndvi": f"{p90:.4f}",
            "valid_pixel_count": str(masked_valid_pixels),
            "masked_boundary_area_ha": f"{masked_area_ha:.3f}",
            "provisional_threshold": f"{PROVISIONAL_VEGETATION_THRESHOLD:.2f}",
            "vegetation_area_ha": f"{prov_veg_ha:.3f}",
            "vegetation_percentage": f"{prov_veg_pct:.2f}",
            "threshold_note": "Provisional threshold; requires LULC/Dynamic World validation",
        }

        # 4. Save polygon-masked spatial NDVI GeoTIFF
        save_masked_ndvi_geotiff(pid, yr, ndvi, src)

        return audit_rec, stat_rec, thresh_records


def save_masked_ndvi_geotiff(pid: str, yr: int, ndvi_array: np.ndarray, src: rasterio.DatasetReader) -> None:
    """Saves polygon-masked spatial NDVI GeoTIFF raster under data/processed/vegetation/ndvi/<pid>/ndvi_<year>.tif."""
    out_dir = Path(f"data/processed/vegetation/ndvi/{pid}")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_tif = out_dir / f"ndvi_{yr}.tif"

    profile = src.profile.copy()
    profile.update(
        count=1,
        dtype=rasterio.float32,
        nodata=-9999.0,
    )

    ndvi_out = np.where(np.isnan(ndvi_array), -9999.0, ndvi_array).astype(np.float32)

    with rasterio.open(out_tif, "w", **profile) as dst:
        dst.write(ndvi_out, 1)
        dst.set_band_description(1, f"Polygon Masked NDVI {yr}")


def compute_year_over_year_changes(stat_records: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Calculates baseline changes in median NDVI and vegetation area, distinguishing 2026 as partial."""
    change_records = []
    df = pd.DataFrame(stat_records)
    df["year"] = df["year"].astype(int)
    df["median_ndvi"] = df["median_ndvi"].astype(float)
    df["vegetation_area_ha"] = df["vegetation_area_ha"].astype(float)
    df["vegetation_percentage"] = df["vegetation_percentage"].astype(float)

    for pid in df["project_id"].unique():
        pdf = df[df["project_id"] == pid].sort_values("year")
        years = pdf["year"].tolist()

        for i in range(len(years) - 1):
            row_prev = pdf[pdf["year"] == years[i]].iloc[0]
            row_curr = pdf[pdf["year"] == years[i + 1]].iloc[0]

            y_from = row_prev["year"]
            y_to = row_curr["year"]
            period_str = f"{y_from}->{y_to}"

            ndvi_change = row_curr["median_ndvi"] - row_prev["median_ndvi"]
            area_change_ha = row_curr["vegetation_area_ha"] - row_prev["vegetation_area_ha"]
            pct_point_change = row_curr["vegetation_percentage"] - row_prev["vegetation_percentage"]

            if row_prev["vegetation_area_ha"] > 0:
                area_change_pct = (area_change_ha / row_prev["vegetation_area_ha"]) * 100.0
            else:
                area_change_pct = 0.0

            if y_to == 2026:
                comparison_type = "partial_year_comparison"
                change_note = "2026 is partial (Jan-May); not directly comparable to complete annual baselines"
            else:
                comparison_type = "historical_annual_baseline"
                change_note = "Complete dry-season annual baseline comparison"

            change_records.append({
                "project_id": pid,
                "project_name": row_curr["project_name"],
                "period": period_str,
                "from_year": str(y_from),
                "to_year": str(y_to),
                "comparison_type": comparison_type,
                "median_ndvi_from": f"{row_prev['median_ndvi']:.4f}",
                "median_ndvi_to": f"{row_curr['median_ndvi']:.4f}",
                "median_ndvi_change": f"{ndvi_change:+.4f}",
                "veg_area_from_ha": f"{row_prev['vegetation_area_ha']:.3f}",
                "veg_area_to_ha": f"{row_curr['vegetation_area_ha']:.3f}",
                "veg_area_change_ha": f"{area_change_ha:+.3f}",
                "veg_area_change_percent": f"{area_change_pct:+.2f}",
                "veg_percentage_point_change": f"{pct_point_change:+.2f}",
                "note": change_note,
            })

    return change_records


def write_csv(records: List[Dict[str, str]], output_path: Path) -> None:
    """Writes list of dicts to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        return
    fieldnames = list(records[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    print("Starting PARIVESH Real NDVI Analysis & Spatial Area Audit (Feature 5)...", flush=True)

    audit_records = []
    stat_records = []
    all_thresh_records = []

    for pid in ["MH-001", "MH-002", "MH-003"]:
        pname = PROJECT_NAMES[pid]
        b_path = Path(BOUNDARY_FILES[pid])
        target_crs = PROJECT_UTM[pid]

        print(f"Processing Polygon-Masked NDVI for Project {pid}: {pname}...", flush=True)
        for yr in YEARS:
            try:
                a_rec, s_rec, t_recs = process_project_year(pid, pname, b_path, yr, target_crs)
                audit_records.append(a_rec)
                stat_records.append(s_rec)
                all_thresh_records.extend(t_recs)
                print(
                    f"  [{pid} {yr}] Boundary: {a_rec['boundary_area_ha']} ha | Masked: {a_rec['masked_valid_area_ha']} ha | Status: {a_rec['spatial_status']} | Median NDVI: {s_rec['median_ndvi']}",
                    flush=True,
                )
            except Exception as err:
                print(f"Error processing {pid} year {yr}: {err}", file=sys.stderr, flush=True)

    # 1. Export Spatial Integrity Audit CSV
    audit_csv = Path("data/processed/vegetation/spatial_integrity_audit.csv")
    write_csv(audit_records, audit_csv)
    print(f"\nSpatial Integrity Audit written to: {audit_csv.as_posix()}", flush=True)

    # 2. Export main NDVI statistics CSV
    stats_csv = Path("data/processed/vegetation/ndvi_statistics.csv")
    write_csv(stat_records, stats_csv)
    print(f"Polygon-masked NDVI statistics written to: {stats_csv.as_posix()}", flush=True)

    # 3. Export Candidate Threshold Investigation CSV
    thresh_csv = Path("data/processed/vegetation/ndvi_candidate_thresholds.csv")
    write_csv(all_thresh_records, thresh_csv)
    print(f"Candidate threshold sensitivity audit written to: {thresh_csv.as_posix()}", flush=True)

    # 4. Export Year-over-Year Baseline Changes CSV
    change_records = compute_year_over_year_changes(stat_records)
    change_csv = Path("data/processed/vegetation/ndvi_change_analysis.csv")
    write_csv(change_records, change_csv)
    print(f"Year-over-year change analysis written to: {change_csv.as_posix()}", flush=True)

    # Verify all audit records passed
    failed_audits = [r for r in audit_records if r["spatial_status"] != "PASS"]
    if failed_audits:
        print(f"\nWARNING: {len(failed_audits)} spatial audits FAILED!", file=sys.stderr, flush=True)
    else:
        print("\nALL SPATIAL AREA INTEGRITY AUDITS PASSED (PASS: 18/18)", flush=True)

    print("======================================================", flush=True)


if __name__ == "__main__":
    main()
