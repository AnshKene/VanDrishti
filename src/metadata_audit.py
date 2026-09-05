"""
PARIVESH Project Metadata & Boundary Audit Utility (Feature 2)

Performs automated metadata extraction and boundary auditing from real PARIVESH
clearance documents and KML spatial files for Maharashtra projects MH-001, MH-002, MH-003.

Generates data/processed/project_metadata.csv and data/processed/boundary_candidates.csv.
"""

import csv
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pypdf

# Define strict mappings for project IDs and source directories
PROJECT_MAPPING: Dict[str, str] = {
    "Gondkhari": "MH-001",
    "Gadchiroli": "MH-002",
    "Bhivpuri PSP": "MH-003",
}


def extract_kml_bbox_center(kml_path: Path) -> Optional[Tuple[float, float]]:
    """
    Parses coordinates from a KML file and returns the (center_latitude, center_longitude)
    or None if coordinates cannot be extracted.
    """
    if not kml_path.exists():
        return None

    try:
        content = kml_path.read_text(encoding="utf-8", errors="ignore")
        # Extract content inside <coordinates>...</coordinates> tags using regex to bypass XML namespace issues
        coord_blocks = re.findall(r"<coordinates>(.*?)</coordinates>", content, re.DOTALL | re.IGNORECASE)
        all_lats: List[float] = []
        all_lons: List[float] = []

        for block in coord_blocks:
            # Tokens separated by whitespace
            tokens = block.strip().split()
            for token in tokens:
                parts = token.split(",")
                if len(parts) >= 2:
                    try:
                        lon = float(parts[0])
                        lat = float(parts[1])
                        # Filter out invalid or zero coordinates
                        if -180.0 <= lon <= 180.0 and -90.0 <= lat <= 90.0 and (lon != 0.0 or lat != 0.0):
                            all_lons.append(lon)
                            all_lats.append(lat)
                    except ValueError:
                        continue

        if all_lats and all_lons:
            center_lat = round(sum(all_lats) / len(all_lats), 5)
            center_lon = round(sum(all_lons) / len(all_lons), 5)
            return (center_lat, center_lon)
    except Exception as err:
        print(f"Warning: Failed to parse KML '{kml_path.name}': {err}", file=sys.stderr)

    return None


def extract_pdf_clearance_info(doc_dir: Path) -> Dict[str, str]:
    """
    Extracts clearance type, proposal number, and clearance date from PDF clearance letters.
    """
    info = {
        "clearance_type": "Not yet verified",
        "clearance_date": "Not yet verified",
        "proposal_no": "Not yet verified",
    }

    if not doc_dir.exists():
        return info

    pdf_files = sorted(doc_dir.glob("fc_ministry*.pdf"))
    if not pdf_files:
        return info

    # Prioritize Stage-II final clearance if present, else Stage-I
    selected_pdf = pdf_files[-1]
    is_stage_2 = "stage_ii" in selected_pdf.name.lower() or "stage_2" in selected_pdf.name.lower()

    try:
        reader = pypdf.PdfReader(selected_pdf)
        text = ""
        for page in reader.pages[:3]:
            text += page.extract_text() + "\n"

        # Search for Proposal No.
        prop_match = re.search(r"FP/[A-Z0-9/_]+", text)
        if prop_match:
            info["proposal_no"] = prop_match.group(0)

        # Search for Dated
        date_match = re.search(r"Dated:\s*([0-9]{2}/[0-9]{2}/[0-9]{4})", text, re.IGNORECASE)
        if date_match:
            info["clearance_date"] = date_match.group(1)

        # Set Clearance Type
        if is_stage_2:
            info["clearance_type"] = "Forest Clearance (Stage-II Final)"
        else:
            info["clearance_type"] = "Forest Clearance (Stage-I In-Principle)"
    except Exception as err:
        print(f"Warning: Could not read PDF '{selected_pdf.name}': {err}", file=sys.stderr)

    return info


def audit_project_metadata(raw_dir: Path) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """
    Audits raw dataset for all projects, extracting real metadata and boundary candidate files.
    """
    project_metadata_list: List[Dict[str, str]] = []
    boundary_candidates_list: List[Dict[str, str]] = []

    # Ground-truth verified details from PARIVESH documents
    verified_project_facts: Dict[str, Dict[str, str]] = {
        "MH-001": {
            "project_name": "Gondkhari",
            "project_type": "Mining (Underground Coal)",
            "district": "Nagpur",
            "state": "Maharashtra",
            "project_area_ha": "87.351 (Forest) / 862.00 (Total Mine Lease)",
            "default_kml": "kml/970858_FC_KML_1672903420512_Lease limit.kml",
        },
        "MH-002": {
            "project_name": "Gadchiroli",
            "project_type": "Mining (Iron Ore)",
            "district": "Gadchiroli",
            "state": "Maharashtra",
            "project_area_ha": "937.077 (Forest) / 990.265 (CA Land)",
            "default_kml": "kml/30227102_FC_KML_1702025392040_FC_937.077_Area_1.kml",
        },
        "MH-003": {
            "project_name": "Bhivpuri PSP",
            "project_type": "Hydro (Pumped Storage Project 1000 MW)",
            "district": "Pune & Raigad",
            "state": "Maharashtra",
            "project_area_ha": "20.15 (Forest) / 20.15 (CA Land)",
            "default_kml": "kml/6958645_FC_KML_1696507173302_Bhivpuri Off Stream Open Loop Pumped Storage Project (1800 MW).kml",
        },
    }

    for proj_folder, proj_id in PROJECT_MAPPING.items():
        proj_dir = raw_dir / proj_folder
        facts = verified_project_facts.get(proj_id, {})
        doc_dir = proj_dir / "documents"
        kml_dir = proj_dir / "kml"

        # Extract clearance PDF info
        clearance_info = extract_pdf_clearance_info(doc_dir)

        # Discover candidate KML files
        candidate_kml_files: List[Path] = []
        if kml_dir.exists():
            candidate_kml_files = sorted(list(kml_dir.glob("*.kml")) + list(kml_dir.glob("*.kmz")))

        rel_kml_paths: List[str] = []
        center_coords: Optional[Tuple[float, float]] = None

        for kml_file in candidate_kml_files:
            rel_path = f"kml/{kml_file.name}"
            rel_kml_paths.append(rel_path)

            # Record candidate in detailed candidates list
            boundary_candidates_list.append({
                "project_id": proj_id,
                "project_name": proj_folder,
                "relative_path": rel_path,
                "filename": kml_file.name,
                "file_size_kb": f"{kml_file.stat().st_size / 1024.0:.2f}",
                "boundary_status": "Candidate identified",
            })

            # Check for coordinates from primary project boundary KML if not yet found
            if center_coords is None:
                default_rel = facts.get("default_kml", "")
                if rel_path == default_rel or "lease" in kml_file.name.lower() or "937.077" in kml_file.name or "1800 MW" in kml_file.name:
                    coords = extract_kml_bbox_center(kml_file)
                    if coords:
                        center_coords = coords

        # Fallback coordinate calculation if default KML didn't parse
        if center_coords is None and candidate_kml_files:
            for kml_file in candidate_kml_files:
                coords = extract_kml_bbox_center(kml_file)
                if coords:
                    center_coords = coords
                    break

        lat_str = f"{center_coords[0]:.5f}" if center_coords else "Not yet verified"
        lon_str = f"{center_coords[1]:.5f}" if center_coords else "Not yet verified"

        metadata_record = {
            "project_id": proj_id,
            "project_name": proj_folder,
            "project_type": facts.get("project_type", "Not yet verified"),
            "district": facts.get("district", "Not yet verified"),
            "state": facts.get("state", "Not yet verified"),
            "latitude": lat_str,
            "longitude": lon_str,
            "project_area_ha": facts.get("project_area_ha", "Not yet verified"),
            "clearance_type": clearance_info["clearance_type"],
            "clearance_date": clearance_info["clearance_date"],
            "candidate_boundary_files": "; ".join(rel_kml_paths),
            "boundary_status": "Candidate identified",
        }

        project_metadata_list.append(metadata_record)

    return project_metadata_list, boundary_candidates_list


def write_csv(records: List[Dict[str, str]], fieldnames: List[str], output_path: Path) -> None:
    """Writes list of dictionaries to specified CSV output path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    raw_dir = Path("data/raw")
    output_metadata_csv = Path("data/processed/project_metadata.csv")
    output_candidates_csv = Path("data/processed/boundary_candidates.csv")

    metadata_records, candidate_records = audit_project_metadata(raw_dir)

    metadata_fieldnames = [
        "project_id",
        "project_name",
        "project_type",
        "district",
        "state",
        "latitude",
        "longitude",
        "project_area_ha",
        "clearance_type",
        "clearance_date",
        "candidate_boundary_files",
        "boundary_status",
    ]

    candidate_fieldnames = [
        "project_id",
        "project_name",
        "relative_path",
        "filename",
        "file_size_kb",
        "boundary_status",
    ]

    write_csv(metadata_records, metadata_fieldnames, output_metadata_csv)
    write_csv(candidate_records, candidate_fieldnames, output_candidates_csv)

    print("PARIVESH Project Metadata & Boundary Audit")
    print("------------------------------------------")
    print(f"Projects audited: {len(metadata_records)}")
    print(f"Total candidate spatial files: {len(candidate_records)}")
    print()

    for rec in metadata_records:
        pid = rec["project_id"]
        pname = rec["project_name"]
        ptype = rec["project_type"]
        dist = rec["district"]
        area = rec["project_area_ha"]
        cle_type = rec["clearance_type"]
        cle_date = rec["clearance_date"]
        lat = rec["latitude"]
        lon = rec["longitude"]
        cand_count = len([c for c in candidate_records if c["project_id"] == pid])

        print(f"Project {pid}: {pname}")
        print(f"  Type:           {ptype}")
        print(f"  Location:       {dist}, {rec['state']} ({lat}, {lon})")
        print(f"  Project Area:   {area} ha")
        print(f"  Clearance:      {cle_type} ({cle_date})")
        print(f"  Spatial KMLs:   {cand_count} candidate files identified")
        print(f"  Boundary Status:{rec['boundary_status']}")
        print()

    print("Primary metadata written to:")
    print(output_metadata_csv.as_posix())
    print("Detailed boundary candidates written to:")
    print(output_candidates_csv.as_posix())


if __name__ == "__main__":
    main()
