export interface Project {
  project_id: string;
  project_name?: string | null;
  location?: string | null;
  boundary?: any | null;
  total_hotspots: number;
  high_priority_count: number;
  medium_priority_count: number;
  low_priority_count: number;
  unsupported_count: number;
  last_updated?: string | null;
}

export interface Hotspot {
  hotspot_id: string;
  project_id: string;
  centroid_lat: number;
  centroid_lon: number;
  geometry?: any | null;
  patch_count: number;
  mean_cnn_score: number;
  max_cnn_score: number;
  cnn_score_percentile: number;
  priority_score: number;
  priority_level: 'HIGH PRIORITY' | 'MEDIUM PRIORITY' | 'LOW PRIORITY' | 'UNSUPPORTED / MONITOR';
  feature10_evidence_class: 'STRONG_SUPPORT' | 'MODERATE_SUPPORT' | 'WEAK_SUPPORT' | 'NO_INDEPENDENT_SUPPORT';
  recommended_action: string;
}

export interface Evidence {
  hotspot_id: string;
  ndvi_change?: number | null;
  ndvi_evidence: number;
  dynamic_world_evidence: number;
  temporal_evidence: string;
  spatial_evidence: number;
  evidence_class: string;
  evidence_summary: string;
}

export interface Provenance {
  hotspot_id: string;
  source_feature: string;
  source_file: string;
  source_patch_ids: string[];
  model_name: string;
  model_feature: string;
  model_version: string;
  threshold: number;
  input_years: number[];
  data_checksum: string;
  generated_at: string;
}

export interface PaginatedHotspots {
  items: Hotspot[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface OverviewStats {
  total_projects: number;
  total_hotspots: number;
  high_priority: number;
  medium_priority: number;
  low_priority: number;
  unsupported: number;
  supported_hotspots: number;
  project_distribution: any[];
}

export interface SatelliteMetadata {
  project_id: string;
  year: number;
  sensor: string;
  composite_type: string;
  crs: string;
  width: number;
  height: number;
  bounds: [number, number, number, number];
  coordinates: [[number, number], [number, number], [number, number], [number, number]];
  image_url: string;
  tile_url_template: string;
  resolution_description: string;
  band_names: string[];
  stretch_range: [number, number];
  is_reference_year: boolean;
}

export interface SatelliteYearsResponse {
  available_years: number[];
  operational_years: number[];
  reference_years: number[];
}

