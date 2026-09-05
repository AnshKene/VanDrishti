"""
PARIVESH Data Inventory Utility

Scans data/raw/ recursively for project dataset files across Gondkhari,
Gadchiroli, and Bhivpuri PSP, extracts metadata, and writes an inventory CSV.
"""

import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Project Mappings (Folder Name -> Project ID)
PROJECT_MAPPING: Dict[str, str] = {
    "Gondkhari": "MH-001",
    "Gadchiroli": "MH-002",
    "Bhivpuri PSP": "MH-003",
}

# Recognized file extension to file type mapping (extension normalized with leading dot)
EXTENSION_TO_FILE_TYPE: Dict[str, str] = {
    ".pdf": "PDF",
    ".kml": "KML",
    ".kmz": "KMZ",
    ".doc": "DOC",
    ".docx": "DOCX",
    ".xls": "XLS",
    ".xlsx": "XLSX",
    ".csv": "CSV",
    ".png": "PNG",
    ".jpg": "JPG",
    ".jpeg": "JPEG",
    ".tiff": "TIFF",
    ".tif": "TIF",
    ".zip": "ZIP",
    ".txt": "TXT",
}


def get_file_type(extension: str) -> str:
    """Return recognized file type for extension, or 'Other' if unknown."""
    return EXTENSION_TO_FILE_TYPE.get(extension.lower(), "Other")


def scan_inventory(raw_dir: Path) -> Tuple[List[Dict[str, str]], Dict[str, int]]:
    """
    Recursively scan project folders in raw_dir and build metadata records.
    
    Returns a tuple of:
    - List of metadata dictionaries matching CSV schema
    - Dictionary mapping project name to file count
    """
    inventory_records: List[Dict[str, str]] = []
    project_counts: Dict[str, int] = {proj_name: 0 for proj_name in PROJECT_MAPPING}

    if not raw_dir.exists() or not raw_dir.is_dir():
        print(f"Warning: Raw data directory '{raw_dir}' does not exist.", file=sys.stderr)
        return inventory_records, project_counts

    for project_name, project_id in PROJECT_MAPPING.items():
        project_dir = raw_dir / project_name
        if not project_dir.exists() or not project_dir.is_dir():
            print(f"Warning: Project directory '{project_name}' not found inside '{raw_dir}'.", file=sys.stderr)
            continue

        # Recursively scan all files within the project directory
        # Sorting ensures deterministic row order in the generated CSV
        for file_path in sorted(project_dir.rglob("*")):
            if file_path.is_file():
                try:
                    rel_path = file_path.relative_to(project_dir).as_posix()
                    ext = file_path.suffix.lower()
                    file_type = get_file_type(ext)
                    file_size_kb = f"{file_path.stat().st_size / 1024.0:.2f}"

                    record = {
                        "project_id": project_id,
                        "project_name": project_name,
                        "relative_path": rel_path,
                        "filename": file_path.name,
                        "extension": ext,
                        "file_type": file_type,
                        "file_size_kb": file_size_kb,
                    }
                    inventory_records.append(record)
                    project_counts[project_name] += 1
                except Exception as err:
                    print(f"Error processing file '{file_path}': {err}", file=sys.stderr)

    return inventory_records, project_counts


def write_inventory_csv(records: List[Dict[str, str]], output_file: Path) -> None:
    """Write inventory records to CSV file using standard schema."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "project_id",
        "project_name",
        "relative_path",
        "filename",
        "extension",
        "file_type",
        "file_size_kb",
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def print_summary(project_counts: Dict[str, int], output_file: Path) -> None:
    """Print terminal summary of inventory scan."""
    total_files = sum(project_counts.values())
    scanned_projects_count = sum(1 for count in project_counts.values() if count >= 0)

    print("PARIVESH Data Inventory")
    print("-----------------------")
    print(f"Projects scanned: {scanned_projects_count}")
    print(f"Total files: {total_files}")
    print()
    for proj_name, proj_id in PROJECT_MAPPING.items():
        count = project_counts.get(proj_name, 0)
        print(f"{proj_id} {proj_name}: {count} files")
    print()
    print("Inventory written to:")
    print(output_file.as_posix())


def main() -> None:
    raw_dir = Path("data/raw")
    output_file = Path("data/processed/data_inventory.csv")

    records, project_counts = scan_inventory(raw_dir)
    write_inventory_csv(records, output_file)
    print_summary(project_counts, output_file)


if __name__ == "__main__":
    main()
