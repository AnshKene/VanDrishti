from typing import List, Optional, Any
from pydantic import BaseModel

class Project(BaseModel):
    project_id: str
    project_name: Optional[str] = None
    location: Optional[str] = None
    boundary: Optional[Any] = None
    total_hotspots: int
    high_priority_count: int
    medium_priority_count: int
    low_priority_count: int
    unsupported_count: int
    last_updated: Optional[str] = None

class Hotspot(BaseModel):
    hotspot_id: str
    project_id: str
    centroid_lat: float
    centroid_lon: float
    geometry: Optional[Any] = None
    patch_count: int
    mean_cnn_score: float
    max_cnn_score: float
    cnn_score_percentile: float
    priority_score: float
    priority_level: str
    feature10_evidence_class: str
    recommended_action: str

class Evidence(BaseModel):
    hotspot_id: str
    ndvi_change: Optional[float] = None
    ndvi_evidence: int
    dynamic_world_evidence: int
    temporal_evidence: str
    spatial_evidence: int
    evidence_class: str
    evidence_summary: str

class Provenance(BaseModel):
    hotspot_id: str
    source_feature: str
    source_file: str
    source_patch_ids: List[str]
    model_name: str
    model_feature: str
    model_version: str
    threshold: float
    input_years: List[int]
    data_checksum: str
    generated_at: str

class PaginatedHotspots(BaseModel):
    items: List[Hotspot]
    page: int
    page_size: int
    total: int
    total_pages: int

class OverviewStats(BaseModel):
    total_projects: int
    total_hotspots: int
    high_priority: int
    medium_priority: int
    low_priority: int
    unsupported: int
    supported_hotspots: int
    project_distribution: List[dict]

class SatelliteMetadata(BaseModel):
    project_id: str
    year: int
    sensor: str
    composite_type: str
    crs: str
    width: int
    height: int
    bounds: List[float]
    coordinates: List[List[float]]
    image_url: str
    tile_url_template: str
    resolution_description: str
    band_names: List[str]
    stretch_range: List[float]
    is_reference_year: bool
    is_regional: Optional[bool] = False

class SatelliteYearsResponse(BaseModel):
    available_years: List[int]
    operational_years: List[int]
    reference_years: List[int]
