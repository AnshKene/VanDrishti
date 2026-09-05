# Feature 12-A: Provenance Specification

Data integrity and traceability are mandatory for this decision-support system. The dashboard is not permitted to generate new ML insights; it only renders existing insights. Provenance proves to the investigator that the data on the screen perfectly matches the output of the frozen pipeline.

## Provenance Chain Display

On the `/hotspots/:hotspotId` page, the UI must render a "Data Lineage" or "Provenance" card.

This card must display:

1. **Prioritization Layer**: 
   - Source: `feature11_hotspot_priority.csv`
   - Hash: SHA-256 of the file at dashboard startup.
2. **Validation Layer**: 
   - Source: `validated_hotspots.csv` (Feature 10)
   - Evidence rules applied (NDVI & DW parameters).
3. **Inference Layer**:
   - Source: `pilot_predictions.csv` (Feature 9)
   - Patches: List of `temporal_sample_id` making up the hotspot.
   - Threshold: `0.10`
4. **Model Layer**:
   - Checkpoint: `Delta Temporal CNN`
   - Source Feature: `Feature 8.7-B`

## Integrity Guarantees

The dashboard backend must verify the checksums of all source CSV/GeoJSON files against their authoritative Feature 11 `feature11_checksums_sha256.csv` file during backend startup. If the checksums fail, the backend API should refuse to start and log a critical data corruption error.
