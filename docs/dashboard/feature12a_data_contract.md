# Feature 12-A: Data Contract

This data contract defines the exact schemas required for the dashboard's API layer. The dashboard frontend expects JSON payloads strictly matching these models. All fields are directly sourced from the authoritative Feature 11 artifacts.

## 1. PROJECT Schema
Represents an aggregate view of an environmental monitoring project.

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `project_id` | String | Yes | Unique identifier (e.g., "MH-001") |
| `project_name` | String | No | Human-readable name of the project area |
| `location` | String | No | Geographical context/region |
| `boundary` | GeoJSON | No | Polygon defining the project extent |
| `total_hotspots` | Integer | Yes | Total candidate hotspots generated |
| `high_priority_count` | Integer | Yes | Number of hotspots assigned HIGH priority |
| `medium_priority_count` | Integer | Yes | Number of hotspots assigned MEDIUM priority |
| `low_priority_count` | Integer | Yes | Number of hotspots assigned LOW priority |
| `unsupported_count` | Integer | Yes | Number of hotspots assigned UNSUPPORTED |
| `last_updated` | String (ISO) | Yes | Timestamp of the underlying ML artifact creation |

## 2. HOTSPOT Schema
Represents a prioritized candidate location.

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `hotspot_id` | String | Yes | Unique identifier (e.g., "HS_001") |
| `project_id` | String | Yes | Foreign key to PROJECT |
| `centroid_lat` | Float | Yes | Latitude of hotspot center |
| `centroid_lon` | Float | Yes | Longitude of hotspot center |
| `geometry` | GeoJSON | No | Feature polygon boundary of the hotspot patches |
| `patch_count` | Integer | Yes | Number of CNN spatial patches comprising the hotspot |
| `mean_cnn_score` | Float | Yes | Average model score across all patches |
| `max_cnn_score` | Float | Yes | Maximum model score within the hotspot |
| `cnn_score_percentile` | Float | Yes | Relative ranking percentile (0-100) across pilot population |
| `priority_score` | Float | Yes | Deterministic evidence prioritization score (0-100) |
| `priority_level` | Enum | Yes | HIGH_PRIORITY, MEDIUM_PRIORITY, LOW_PRIORITY, UNSUPPORTED |
| `feature10_evidence_class` | Enum | Yes | STRONG_SUPPORT, MODERATE_SUPPORT, WEAK_SUPPORT, NO_INDEPENDENT_SUPPORT |
| `recommended_action` | String | Yes | Actionable instruction for the investigator |

## 3. EVIDENCE Schema
Details the independent satellite proxy metrics supporting a hotspot.

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `hotspot_id` | String | Yes | Foreign key to HOTSPOT |
| `ndvi_change` | Float | No | Mean NDVI delta (2021-2025) across the hotspot |
| `ndvi_evidence` | Integer | Yes | Contribution score from NDVI change (0-30) |
| `dynamic_world_evidence` | Integer | Yes | Contribution score from DW transition (0-30) |
| `temporal_evidence` | String | Yes | Descriptive text of temporal consistency |
| `spatial_evidence` | Integer | Yes | Contribution score from patch size/concentration |
| `evidence_class` | Enum | Yes | F10 classification (STRONG/MODERATE/WEAK/UNSUPPORTED) |
| `evidence_summary` | String | Yes | Human-readable explanation of proxy evidence |

## 4. PROVENANCE Schema
Maintains strict traceability from final recommendation back to raw inference artifacts.

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `hotspot_id` | String | Yes | Foreign key to HOTSPOT |
| `source_feature` | String | Yes | "Feature 11" |
| `source_file` | String | Yes | Filename of authoritative CSV |
| `source_patch_ids` | List[String] | Yes | Array of underlying spatial patch IDs |
| `model_name` | String | Yes | "Delta Temporal CNN" |
| `model_feature` | String | Yes | "Feature 8.7-B" |
| `model_version` | String | Yes | Associated commit hash or frozen checkpoint ID |
| `threshold` | Float | Yes | Official validation threshold (0.10) |
| `input_years` | List[Int] | Yes | Temporal sequence used [2021, 2022, 2023, 2024, 2025] |
| `data_checksum` | String | Yes | SHA-256 hash of the source artifact |
| `generated_at` | String (ISO) | Yes | Timestamp of artifact generation |
