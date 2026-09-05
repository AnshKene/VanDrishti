"""
PARIVESH Boundary Geometry Validation and Monitoring Boundary Selection (Feature 3)

Inspects candidate KML geometries, calculates projected areas using local UTM projections,
validates geometry topology, cross-references stated document areas, selects verified
monitoring boundaries, and exports clean GeoJSON boundary datasets.
"""

import csv
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pyproj
from shapely.geometry import MultiPolygon, Polygon, mapping
from shapely.ops import transform, unary_union
from shapely.validation import make_valid

# Define CRS settings for projects
# West Maharashtra (Pune, Raigad, Ratnagiri) -> EPSG:32643 (UTM Zone 43N)
# East Maharashtra (Nagpur, Gadchiroli)       -> EPSG:32644 (UTM Zone 44N)
PROJECT_CRS_MAPPING: Dict[str, str] = {
    "MH-001": "EPSG:32644",
    "MH-002": "EPSG:32644",
    "MH-003": "EPSG:32643",
}

# Ground-truth document stated areas for cross-validation
DOCUMENT_AREAS: Dict[str, Dict[str, float]] = {
    "MH-001": {
        "lease_area_ha": 862.00,
        "forest_diversion_area_ha": 87.351,
    },
    "MH-002": {
        "forest_diversion_area_ha": 937.077,
        "ca_land_area_ha": 990.265,
    },
    "MH-003": {
        "forest_diversion_area_ha": 20.15,
        "ca_land_area_ha": 20.15,
        "total_operational_footprint_ha": 117.024,
    },
}


def parse_kml_geometry(kml_path: Path) -> Tuple[Optional[object], int, bool]:
    """
    Parses Polygon and MultiPolygon geometries from a KML file.
    Returns (shapely_geometry, polygon_count, raw_is_valid).
    """
    if not kml_path.exists():
        return None, 0, False

    try:
        content = kml_path.read_text(encoding="utf-8", errors="ignore")
        poly_blocks = re.findall(r"<Polygon>(.*?)</Polygon>", content, re.DOTALL | re.IGNORECASE)
        polygons: List[Polygon] = []

        for pb in poly_blocks:
            outer_match = re.search(r"<outerBoundaryIs>.*?<coordinates>(.*?)</coordinates>.*?</outerBoundaryIs>", pb, re.DOTALL | re.IGNORECASE)
            if not outer_match:
                outer_match = re.search(r"<coordinates>(.*?)</coordinates>", pb, re.DOTALL | re.IGNORECASE)

            if outer_match:
                coord_str = outer_match.group(1).strip()
                pts = []
                for token in coord_str.split():
                    parts = token.split(",")
                    if len(parts) >= 2:
                        try:
                            lon = float(parts[0])
                            lat = float(parts[1])
                            pts.append((lon, lat))
                        except ValueError:
                            pass
                if len(pts) >= 3:
                    if pts[0] != pts[-1]:
                        pts.append(pts[0])
                    poly = Polygon(pts)
                    if not poly.is_valid:
                        poly = make_valid(poly)
                    polys_cleaned = clean_polygon_geom(poly)
                    if polys_cleaned is not None:
                        if isinstance(polys_cleaned, Polygon):
                            polygons.append(polys_cleaned)
                        elif isinstance(polys_cleaned, MultiPolygon):
                            polygons.extend(polys_cleaned.geoms)

        if not polygons:
            return None, 0, False

        poly_count = len(polygons)
        raw_geom = polygons[0] if poly_count == 1 else unary_union(polygons)
        raw_is_valid = raw_geom.is_valid
        return raw_geom, poly_count, raw_is_valid
    except Exception as err:
        print(f"Warning: Failed to parse KML '{kml_path.name}': {err}", file=sys.stderr)
        return None, 0, False


def clean_polygon_geom(geom: object) -> Optional[object]:
    """Extracts only Polygon/MultiPolygon components from geometry, ignoring zero-area lines or points."""
    if isinstance(geom, (Polygon, MultiPolygon)):
        return geom
    elif hasattr(geom, "geoms"):
        polys: List[Polygon] = []
        for g in geom.geoms:
            if isinstance(g, Polygon):
                polys.append(g)
            elif isinstance(g, MultiPolygon):
                polys.extend(g.geoms)
        if not polys:
            return None
        return polys[0] if len(polys) == 1 else MultiPolygon(polys)
    return None


def calculate_projected_area(geom: object, area_crs: str) -> float:
    """
    Reprojects geometry from WGS84 (EPSG:4326) to area_crs (UTM) and returns area in hectares.
    """
    transformer = pyproj.Transformer.from_crs("EPSG:4326", area_crs, always_xy=True).transform
    geom_proj = transform(transformer, geom)
    area_m2 = geom_proj.area
    return round(area_m2 / 10000.0, 3)


def determine_boundary_role(proj_id: str, fname: str, calc_area: float) -> Tuple[str, float]:
    """
    Determines boundary role and stated reference area based on project rules.
    """
    fname_lower = fname.lower()

    if proj_id == "MH-001":
        if "lease" in fname_lower or "970858" in fname or "aoi" in fname_lower or "main" in fname_lower:
            return "project_monitoring_boundary", DOCUMENT_AREAS["MH-001"]["lease_area_ha"]
        elif "forest" in fname_lower:
            return "forest_diversion_boundary", DOCUMENT_AREAS["MH-001"]["forest_diversion_area_ha"]

    elif proj_id == "MH-002":
        if "ca_land" in fname_lower or "ovali" in fname_lower:
            return "compensatory_afforestation_boundary", DOCUMENT_AREAS["MH-002"]["ca_land_area_ha"]
        elif "937.077" in fname or "diversion" in fname_lower or "proposed" in fname_lower:
            return "project_monitoring_boundary", DOCUMENT_AREAS["MH-002"]["forest_diversion_area_ha"]
        elif "trans_road" in fname_lower:
            return "supporting_boundary", 378.823

    elif proj_id == "MH-003":
        if "ca land" in fname_lower or "77112832" in fname or "proposed ca" in fname_lower:
            return "compensatory_afforestation_boundary", DOCUMENT_AREAS["MH-003"]["ca_land_area_ha"]
        elif "1000 mw" in fname_lower or "final bhivpuri" in fname_lower:
            return "project_monitoring_boundary", DOCUMENT_AREAS["MH-003"]["total_operational_footprint_ha"]
        elif "1800 mw" in fname_lower:
            return "supporting_boundary", DOCUMENT_AREAS["MH-003"]["total_operational_footprint_ha"]

    return "supporting_boundary", 0.0


def validate_boundaries() -> Tuple[List[Dict[str, str]], Dict[str, Tuple[Path, object, float]]]:
    """
    Validates all candidate geometries from boundary_candidates.csv and selects monitoring boundaries.
    """
    candidates_csv = Path("data/processed/boundary_candidates.csv")
    if not candidates_csv.exists():
        print("Error: boundary_candidates.csv not found.", file=sys.stderr)
        sys.exit(1)

    validation_records: List[Dict[str, str]] = []
    selected_monitoring_geoms: Dict[str, Tuple[Path, object, float]] = {}

    # Priority selection trackers per project
    selection_candidates: Dict[str, Dict[str, any]] = {}

    with open(candidates_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["project_id"]
            pname = row["project_name"]
            rel_path = row["relative_path"]
            fname = row["filename"]
            kml_path = Path("data/raw") / pname / rel_path

            raw_geom, poly_count, orig_valid = parse_kml_geometry(kml_path)
            if raw_geom is None or raw_geom.is_empty:
                validation_records.append({
                    "project_id": pid,
                    "project_name": pname,
                    "source_file": rel_path,
                    "geometry_type": "None",
                    "geometry_count": "0",
                    "source_crs": "EPSG:4326",
                    "area_crs": PROJECT_CRS_MAPPING.get(pid, "EPSG:32644"),
                    "calculated_area_ha": "0.000",
                    "document_area_ha": "0.000",
                    "area_difference_ha": "0.000",
                    "area_difference_percent": "0.00%",
                    "geometry_valid": "False",
                    "boundary_role": "not_selected",
                    "boundary_status": "not_selected",
                    "validation_notes": "No polygon geometry found in file.",
                })
                continue

            # Check and repair geometry validity if needed
            repair_applied = False
            processed_geom = raw_geom
            if not orig_valid:
                processed_geom = make_valid(raw_geom)
                repair_applied = True

            # If multipart component collection, dissolve overlaps for clean total area
            if isinstance(processed_geom, MultiPolygon) or hasattr(processed_geom, "geoms"):
                processed_geom = unary_union(processed_geom)
                cleaned = clean_polygon_geom(processed_geom)
                if cleaned is not None:
                    processed_geom = cleaned

            final_valid = processed_geom.is_valid
            area_crs = PROJECT_CRS_MAPPING.get(pid, "EPSG:32644")
            calc_area_ha = calculate_projected_area(processed_geom, area_crs)

            role, doc_ref_area = determine_boundary_role(pid, fname, calc_area_ha)

            area_diff_ha = round(calc_area_ha - doc_ref_area, 3) if doc_ref_area > 0 else 0.0
            area_diff_pct = f"{abs(area_diff_ha / doc_ref_area * 100):.2f}%" if doc_ref_area > 0 else "N/A"

            # Determine boundary status based on role and area match
            b_status = "candidate"
            val_notes = []

            if repair_applied:
                val_notes.append("Applied make_valid & unary_union to resolve self-intersecting component rings.")
            else:
                val_notes.append("Geometry topology valid without repairs.")

            if doc_ref_area > 0 and abs(area_diff_ha) / doc_ref_area < 0.05:  # Within 5% variance
                b_status = "validated"
                val_notes.append(f"Area matches document reference ({doc_ref_area} ha) within 5% tolerance.")
            elif doc_ref_area > 0:
                val_notes.append(f"Area differs from document reference ({doc_ref_area} ha).")

            notes_str = " ".join(val_notes)

            validation_records.append({
                "project_id": pid,
                "project_name": pname,
                "source_file": rel_path,
                "geometry_type": processed_geom.geom_type,
                "geometry_count": str(poly_count),
                "source_crs": "EPSG:4326",
                "area_crs": area_crs,
                "calculated_area_ha": f"{calc_area_ha:.3f}",
                "document_area_ha": f"{doc_ref_area:.3f}" if doc_ref_area > 0 else "N/A",
                "area_difference_ha": f"{area_diff_ha:+.3f}" if doc_ref_area > 0 else "N/A",
                "area_difference_percent": area_diff_pct,
                "geometry_valid": str(final_valid),
                "boundary_role": role,
                "boundary_status": b_status,
                "validation_notes": notes_str,
            })

            # Check if candidate is primary monitoring boundary for export
            if role == "project_monitoring_boundary" and b_status == "validated":
                if pid not in selection_candidates:
                    selection_candidates[pid] = {
                        "rel_path": rel_path,
                        "geom": processed_geom,
                        "area_ha": calc_area_ha,
                    }

    for pid, data in selection_candidates.items():
        selected_monitoring_geoms[pid] = (data["rel_path"], data["geom"], data["area_ha"])

    return validation_records, selected_monitoring_geoms


def export_geojson_boundaries(selected_geoms: Dict[str, Tuple[Path, object, float]]) -> Dict[str, Path]:
    """
    Exports selected validated monitoring boundaries to GeoJSON files in data/processed/project_boundaries/.
    """
    out_dir = Path("data/processed/project_boundaries")
    out_dir.mkdir(parents=True, exist_ok=True)

    slug_map = {
        "MH-001": "gondkhari_boundary.geojson",
        "MH-002": "gadchiroli_boundary.geojson",
        "MH-003": "bhivpuri_boundary.geojson",
    }

    proj_name_map = {
        "MH-001": "Gondkhari",
        "MH-002": "Gadchiroli",
        "MH-003": "Bhivpuri PSP",
    }

    provenance_map = {
        "MH-001": {
            "approved_capacity": "2.0 MTPA Underground Coal Mine",
            "clearance_proposal_no": "FP/MH/MIN/QRY/408247/2022",
            "supporting_documents": [
                "fc_ministry_stage_i_clearance17041797972232_FP_MH_MIN_QRY_408247_2022_1747850_-signed.pdf",
                "SIR_Gondkhari.pdf",
            ],
        },
        "MH-002": {
            "approved_capacity": "Low Grade Iron Ore Recovery",
            "clearance_proposal_no": "FP/MH/IND/454750/2023",
            "supporting_documents": [
                "fc_ministry_stage_ii_clearance177626169314015_FP_MH_IND_454750_2023_30228292_-signed.pdf",
                "Nodal SIR 937 077 ha.pdf",
            ],
        },
        "MH-003": {
            "approved_capacity": "1000 MW Pumped Storage Project",
            "clearance_proposal_no": "FP/MH/HYD/IRRIG/447097/2023",
            "supporting_documents": [
                "fc_ministry_stage_i_clearance174703400589912_FP_MH_HYD_IRRIG_447097_2023_14807299_-signed.pdf",
                "fc_ministry_stage_ii_clearance17622625603074_FP_MH_HYD_IRRIG_447097_2023_14807299_-signed.pdf",
                "diversion order - 20.14 ha. (1).pdf",
                "Project Report-Bhivpuri-PSP.pdf",
            ],
        },
    }

    exported_files: Dict[str, Path] = {}

    for pid, (rel_path, geom, area_ha) in selected_geoms.items():
        out_file = out_dir / slug_map[pid]
        prov = provenance_map.get(pid, {})

        geojson_data = {
            "type": "FeatureCollection",
            "name": f"{pid}_{proj_name_map[pid]}_Monitoring_Boundary",
            "crs": {
                "type": "name",
                "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"},
            },
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "project_id": pid,
                        "project_name": proj_name_map[pid],
                        "source_kml": str(rel_path),
                        "approved_capacity": prov.get("approved_capacity", "N/A"),
                        "clearance_proposal_no": prov.get("clearance_proposal_no", "N/A"),
                        "supporting_documents": prov.get("supporting_documents", []),
                        "boundary_role": "project_monitoring_boundary",
                        "boundary_status": "validated",
                        "area_ha": area_ha,
                        "area_crs": PROJECT_CRS_MAPPING[pid],
                    },
                    "geometry": mapping(geom),
                }
            ],
        }

        out_file.write_text(json.dumps(geojson_data, indent=2), encoding="utf-8")
        exported_files[pid] = out_file

    return exported_files


def update_project_metadata_csv(selected_geoms: Dict[str, Tuple[Path, object, float]]) -> None:
    """
    Updates data/processed/project_metadata.csv with monitoring boundary file and area.
    """
    metadata_csv = Path("data/processed/project_metadata.csv")
    if not metadata_csv.exists():
        return

    rows: List[Dict[str, str]] = []
    with open(metadata_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])

        # Ensure target columns exist
        for col in ["monitoring_boundary_file", "monitoring_boundary_area_ha"]:
            if col not in fieldnames:
                fieldnames.append(col)

        for row in reader:
            pid = row["project_id"]
            if pid in selected_geoms:
                rel_path, _, area_ha = selected_geoms[pid]
                row["monitoring_boundary_file"] = rel_path
                row["monitoring_boundary_area_ha"] = f"{area_ha:.3f}"
                row["boundary_status"] = "validated"
            else:
                row["monitoring_boundary_file"] = "Requires manual verification"
                row["monitoring_boundary_area_ha"] = "N/A"
                row["boundary_status"] = "requires_manual_verification"
            rows.append(row)

    with open(metadata_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_terminal_summary(
    validation_records: List[Dict[str, str]],
    exported_files: Dict[str, Path],
) -> None:
    """
    Prints human-readable validation summary.
    """
    proj_map = {"MH-001": "Gondkhari", "MH-002": "Gadchiroli", "MH-003": "Bhivpuri PSP"}

    print("PARIVESH Boundary Validation")
    print("============================")
    print()

    for pid, pname in proj_map.items():
        proj_recs = [r for r in validation_records if r["project_id"] == pid]
        inspected_count = len(proj_recs)

        if pid in exported_files:
            exported_path = exported_files[pid]
            sel_rec = next(r for r in proj_recs if r["boundary_role"] == "project_monitoring_boundary" and r["boundary_status"] == "validated")
            status_str = "VALIDATED"
            has_validated = "YES"
            src_file = sel_rec["source_file"]
            calc_area = sel_rec["calculated_area_ha"]
            doc_area = sel_rec["document_area_ha"]
        else:
            status_str = "REQUIRES MANUAL VERIFICATION"
            has_validated = "NO"
            src_file = "None selected"
            calc_area = "N/A"
            doc_area = "N/A"

        print(f"{pid} {pname}")
        print("-" * (len(pid) + len(pname) + 1))
        print(f"Candidates inspected: {inspected_count}")
        print(f"Validated monitoring boundary: {has_validated}")
        print(f"Selected source: {src_file}")
        print(f"Calculated area: {calc_area} ha")
        print(f"Document reference area: {doc_area} ha")
        print(f"Status: {status_str}")
        print()

    print("Boundary validation report written to:")
    print("data/processed/boundary_validation.csv")
    print()
    print("Exported GeoJSON monitoring boundaries written to:")
    for pid, path in exported_files.items():
        print(f"  [{pid}] {path.as_posix()}")


def main() -> None:
    val_records, selected_geoms = validate_boundaries()

    val_csv_path = Path("data/processed/boundary_validation.csv")
    val_csv_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "project_id",
        "project_name",
        "source_file",
        "geometry_type",
        "geometry_count",
        "source_crs",
        "area_crs",
        "calculated_area_ha",
        "document_area_ha",
        "area_difference_ha",
        "area_difference_percent",
        "geometry_valid",
        "boundary_role",
        "boundary_status",
        "validation_notes",
    ]

    with open(val_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(val_records)

    exported_files = export_geojson_boundaries(selected_geoms)
    update_project_metadata_csv(selected_geoms)
    print_terminal_summary(val_records, exported_files)


if __name__ == "__main__":
    main()
