import type { Hotspot, OverviewStats, PaginatedHotspots, Project, Evidence, Provenance, SatelliteMetadata, SatelliteYearsResponse } from './types';

const BASE_URL = 'http://localhost:8000/api';

async function fetchApi<T>(endpoint: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${endpoint}`);
  if (!response.ok) {
    throw new Error(`API error: ${response.statusText} (${response.status})`);
  }
  return response.json();
}

export const api = {
  getHealth: () => fetchApi<{status: string}>('/health'),
  getDashboardOverview: () => fetchApi<OverviewStats>('/dashboard/overview'),
  getProjects: () => fetchApi<Project[]>('/projects'),
  getProject: (id: string) => fetchApi<Project>(`/projects/${id}`),
  getHotspots: (params?: {
    project?: string;
    priority?: string;
    evidence?: string;
    search?: string;
    page?: number;
    page_size?: number;
  }) => {
    const query = new URLSearchParams();
    if (params) {
      if (params.project) query.append('project', params.project);
      if (params.priority) query.append('priority', params.priority);
      if (params.evidence) query.append('evidence', params.evidence);
      if (params.search) query.append('search', params.search);
      if (params.page) query.append('page', params.page.toString());
      if (params.page_size) query.append('page_size', params.page_size.toString());
    }
    return fetchApi<PaginatedHotspots>(`/hotspots?${query.toString()}`);
  },
  getHotspot: (id: string) => fetchApi<Hotspot>(`/hotspots/${id}`),
  getHotspotEvidence: (id: string) => fetchApi<Evidence>(`/hotspots/${id}/evidence`),
  getHotspotProvenance: (id: string) => fetchApi<Provenance>(`/hotspots/${id}/provenance`),
  getHotspotMap: () => fetchApi<any>('/maps/hotspots'),
  getProjectMap: () => fetchApi<any>('/maps/projects'),
  getSatelliteYears: () => fetchApi<SatelliteYearsResponse>('/satellite/years'),
  getSatelliteMetadata: (projectId: string, year: number) => fetchApi<SatelliteMetadata>(`/satellite/${projectId}/${year}/metadata`),
  getSatelliteImageUrl: (projectId: string, year: number) => `${BASE_URL}/satellite/${projectId}/${year}/image.png`,
  getSatelliteTileUrl: (projectId: string, year: number) => `${BASE_URL}/satellite/${projectId}/${year}/tiles/{z}/{x}/{y}.png`,
  getSatelliteRegionalMetadata: (projectId: string, year: number) => fetchApi<SatelliteMetadata>(`/satellite/regional/${projectId}/${year}/metadata`),
  getSatelliteRegionalTileUrl: (projectId: string, year: number) => `${BASE_URL}/satellite/regional/${projectId}/${year}/tiles/{z}/{x}/{y}.png`
};



