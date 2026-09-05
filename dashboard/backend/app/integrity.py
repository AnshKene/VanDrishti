import hashlib
import pandas as pd
from pathlib import Path
import sys

# Assume backend runs from the repository root, or paths are absolute.
# We'll compute paths relative to the repository root by going up from this file's location.
# dashboard/backend/app/integrity.py -> root is ../../../
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

def compute_sha256(filepath: Path) -> str:
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def verify_manifest(manifest_path: Path, path_col: str = "relative_path") -> list:
    failures = []
    if not manifest_path.exists():
        return [f"MANIFEST MISSING: {manifest_path}"]
        
    df = pd.read_csv(manifest_path)
    for _, row in df.iterrows():
        fp = REPO_ROOT / str(row[path_col])
        if not fp.exists():
            failures.append(f"MISSING ARTIFACT: {fp}")
            continue
        actual_hash = compute_sha256(fp)
        expected_hash = str(row["sha256"]).strip()
        if actual_hash != expected_hash:
            failures.append(f"HASH MISMATCH: {fp} (Expected: {expected_hash}, Got: {actual_hash})")
            
    return failures

def verify_all_checksums():
    """Run all critical checksums. Raise exception if any fail."""
    manifests = [
        REPO_ROOT / "data/processed/modeling/candidate_prioritization/feature11_checksums_sha256.csv",
        REPO_ROOT / "data/processed/modeling/dashboard/feature12a_source_manifest.csv"
    ]
    
    all_failures = []
    for mf in manifests:
        fails = verify_manifest(mf)
        all_failures.extend(fails)
        
    if all_failures:
        print("IMMUTABLE ARTIFACT INTEGRITY CHECK FAILED", file=sys.stderr)
        for f in all_failures:
            print(f" - {f}", file=sys.stderr)
        raise RuntimeError("IMMUTABLE ARTIFACT INTEGRITY CHECK FAILED")
        
    print("Integrity check passed.")
