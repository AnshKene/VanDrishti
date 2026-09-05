import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as maplibregl from 'maplibre-gl';
import type { Map as MapLibreMap } from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { api } from '../api';
import { useNavigate } from 'react-router-dom';
import type { SatelliteMetadata } from '../types';

interface MapViewProps {
  mode: 'global' | 'project' | 'hotspot';
  projectId?: string;
  hotspotId?: string;
  className?: string;
}

type MapDisplayMode = 'map' | 'satellite' | 'hybrid';

const colorMap = {
  'HIGH PRIORITY': '#ef4444',
  'MEDIUM PRIORITY': '#f59e0b',
  'LOW PRIORITY': '#eab308',
  'UNSUPPORTED / MONITOR': '#9ca3af',
};

const AVAILABLE_YEARS = [2021, 2022, 2023, 2024, 2025, 2026];

// Generic GeoJSON bounds calculator
function extendBoundsWithGeoJSON(bounds: maplibregl.LngLatBounds, geojson: any) {
  if (!geojson) return;
  if (geojson.type === 'FeatureCollection') {
    geojson.features.forEach((f: any) => extendBoundsWithGeoJSON(bounds, f));
  } else if (geojson.type === 'Feature') {
    extendBoundsWithGeoJSON(bounds, geojson.geometry);
  } else if (geojson.type === 'Point') {
    bounds.extend(geojson.coordinates as [number, number]);
  } else if (geojson.type === 'MultiPoint' || geojson.type === 'LineString') {
    geojson.coordinates.forEach((c: any) => bounds.extend(c as [number, number]));
  } else if (geojson.type === 'MultiLineString' || geojson.type === 'Polygon') {
    geojson.coordinates.forEach((ring: any) => ring.forEach((c: any) => bounds.extend(c as [number, number])));
  } else if (geojson.type === 'MultiPolygon') {
    geojson.coordinates.forEach((poly: any) => poly.forEach((ring: any) => ring.forEach((c: any) => bounds.extend(c as [number, number]))));
  } else if (geojson.type === 'GeometryCollection') {
    geojson.geometries.forEach((g: any) => extendBoundsWithGeoJSON(bounds, g));
  }
}

const MapView: React.FC<MapViewProps> = ({ mode, projectId, hotspotId, className = 'w-full h-96' }) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<MapLibreMap | null>(null);
  const navigate = useNavigate();
  
  const [displayMode, setDisplayMode] = useState<MapDisplayMode>('map');
  const [selectedYear, setSelectedYear] = useState<number>(2025);
  const [activeProject, setActiveProject] = useState<string>(projectId || 'MH-001');
  const [satelliteMeta, setSatelliteMeta] = useState<SatelliteMetadata | null>(null);
  const [loadingSatellite, setLoadingSatellite] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Update active project if prop changes
  useEffect(() => {
    if (projectId) {
      setActiveProject(projectId);
    }
  }, [projectId]);

  // Satellite tiled layer updater
  const updateSatelliteLayer = useCallback(async (currentMap: MapLibreMap, projId: string, yr: number, dispMode: MapDisplayMode) => {
    if (!currentMap || !currentMap.isStyleLoaded()) return;

    const sourceId = 'satellite-tiles-source';
    const layerId = 'satellite-tiles-layer';

    if (dispMode === 'map') {
      // Remove or hide satellite layer
      if (currentMap.getLayer(layerId)) {
        currentMap.removeLayer(layerId);
      }
      if (currentMap.getSource(sourceId)) {
        currentMap.removeSource(sourceId);
      }
      if (currentMap.getLayer('osm-tiles-layer')) {
        currentMap.setLayoutProperty('osm-tiles-layer', 'visibility', 'visible');
      }
      setSatelliteMeta(null);
      return;
    }

    // Satellite or Hybrid mode: Fetch regional metadata and inject real XYZ raster tile source
    try {
      setLoadingSatellite(true);
      const meta = await api.getSatelliteRegionalMetadata(projId, yr);
      setSatelliteMeta(meta);

      if (currentMap.getLayer(layerId)) {
        currentMap.removeLayer(layerId);
      }
      if (currentMap.getSource(sourceId)) {
        currentMap.removeSource(sourceId);
      }

      // Add XYZ raster tile source
      currentMap.addSource(sourceId, {
        type: 'raster',
        tiles: [
          api.getSatelliteRegionalTileUrl(projId, yr)
        ],
        tileSize: 256,
        bounds: meta.bounds,
        minzoom: 8,
        maxzoom: 19
      });

      // Place satellite raster underneath project boundary and hotspot markers
      const beforeId = currentMap.getLayer('projects-line') 
        ? 'projects-line' 
        : (currentMap.getLayer('hotspots-fill') ? 'hotspots-fill' : undefined);

      currentMap.addLayer({
        id: layerId,
        type: 'raster',
        source: sourceId,
        minzoom: 8,
        maxzoom: 19,
        paint: {
          'raster-opacity': 1.0,
          'raster-fade-duration': 150
        }
      }, beforeId);

      // Layer visibilities based on display mode
      if (currentMap.getLayer('osm-tiles-layer')) {
        currentMap.setLayoutProperty(
          'osm-tiles-layer',
          'visibility',
          'visible'
        );
      }

      if (currentMap.getLayer('projects-line')) {
        currentMap.setLayoutProperty(
          'projects-line',
          'visibility',
          dispMode === 'satellite' ? 'none' : 'visible'
        );
      }

      if (currentMap.getLayer('hotspots-fill')) {
        currentMap.setLayoutProperty(
          'hotspots-fill',
          'visibility',
          dispMode === 'satellite' ? 'none' : 'visible'
        );
      }

    } catch (err) {
      console.error('[MapView] Failed to load satellite raster metadata', err);
    } finally {
      setLoadingSatellite(false);
    }
  }, []);

  useEffect(() => {
    if (!mapContainer.current) return;

    let isMounted = true;
    const currentMap = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          'osm-tiles': {
            type: 'raster',
            tiles: [
              'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
            ],
            tileSize: 256,
            attribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors'
          }
        },
        layers: [
          {
            id: 'osm-tiles-layer',
            type: 'raster',
            source: 'osm-tiles',
            minzoom: 0,
            maxzoom: 19
          }
        ]
      },
      center: [73.5, 19.5],
      zoom: 6,
      attributionControl: false
    });

    map.current = currentMap;
    currentMap.addControl(new maplibregl.NavigationControl(), 'top-right');
    (window as any).maplibreMap = currentMap;

    const initializeMap = async () => {
      try {
        const [hotspotsGeojson, projectsGeojson] = await Promise.all([
          api.getHotspotMap(),
          api.getProjectMap()
        ]);
        
        if (!isMounted) return;
        
        if (!currentMap.isStyleLoaded()) {
          await new Promise(resolve => currentMap.once('load', resolve));
        }
        
        if (!isMounted) return;

        // Filter hotspots based on mode
        let filteredHotspots = hotspotsGeojson;
        if (mode === 'project' && projectId) {
          filteredHotspots = {
            ...hotspotsGeojson,
            features: hotspotsGeojson.features.filter((f: any) => f.properties?.project_id === projectId)
          };
        } else if (mode === 'hotspot' && hotspotId) {
          filteredHotspots = {
            ...hotspotsGeojson,
            features: hotspotsGeojson.features.filter((f: any) => f.properties?.hotspot_id === hotspotId)
          };
        }

        // Filter projects based on mode
        let filteredProjects = projectsGeojson;
        let detectedProjectId = projectId || 'MH-001';

        if (mode === 'project' && projectId) {
          filteredProjects = {
            ...projectsGeojson,
            features: projectsGeojson.features.filter((f: any) => f.properties?.project_id === projectId)
          };
        } else if (mode === 'hotspot' && hotspotId) {
          const hs = filteredHotspots.features[0];
          const pId = hs?.properties?.project_id;
          if (pId) {
            detectedProjectId = pId;
            setActiveProject(pId);
          }
          filteredProjects = {
            ...projectsGeojson,
            features: projectsGeojson.features.filter((f: any) => f.properties?.project_id === pId)
          };
        }

        // Add Projects Layer
        currentMap.addSource('projects', {
          type: 'geojson',
          data: filteredProjects
        });

        currentMap.addLayer({
          id: 'projects-line',
          type: 'line',
          source: 'projects',
          paint: {
            'line-color': '#1e3a8a',
            'line-width': 2.5,
            'line-dasharray': [2, 1.5]
          }
        });

        // Add Hotspots Layer
        currentMap.addSource('hotspots', {
          type: 'geojson',
          data: filteredHotspots
        });

        currentMap.addLayer({
          id: 'hotspots-fill',
          type: 'circle',
          source: 'hotspots',
          paint: {
            'circle-radius': 6,
            'circle-color': [
              'match',
              ['get', 'priority_level'],
              'HIGH PRIORITY', colorMap['HIGH PRIORITY'],
              'MEDIUM PRIORITY', colorMap['MEDIUM PRIORITY'],
              'LOW PRIORITY', colorMap['LOW PRIORITY'],
              colorMap['UNSUPPORTED / MONITOR']
            ],
            'circle-stroke-width': 1.5,
            'circle-stroke-color': '#ffffff'
          }
        });

        // Fit bounds
        const bounds = new maplibregl.LngLatBounds();
        extendBoundsWithGeoJSON(bounds, filteredProjects);
        extendBoundsWithGeoJSON(bounds, filteredHotspots);
        
        if (!bounds.isEmpty()) {
          currentMap.fitBounds(bounds, { padding: 40 });
        }

        // Interactivity
        currentMap.on('click', 'hotspots-fill', (e) => {
          if (!e.features || e.features.length === 0) return;
          const feature = e.features[0];
          const props = feature.properties;
          
          if (mode !== 'hotspot' && props && props.hotspot_id) {
            new maplibregl.Popup()
              .setLngLat(e.lngLat)
              .setHTML(`
                <div class="p-2">
                  <div class="font-bold mb-1">${props.hotspot_id}</div>
                  <div class="text-sm mb-1">Priority: ${props.priority_level}</div>
                  <div class="text-xs text-blue-600 cursor-pointer underline" id="popup-link-${props.hotspot_id}">
                    View Details
                  </div>
                </div>
              `)
              .addTo(currentMap);
              
            setTimeout(() => {
              const el = document.getElementById(`popup-link-${props.hotspot_id}`);
              if (el) {
                el.addEventListener('click', () => {
                  navigate(`/hotspots/${props.hotspot_id}`);
                });
              }
            }, 100);
          }
        });

        currentMap.on('mouseenter', 'hotspots-fill', () => {
          currentMap.getCanvas().style.cursor = 'pointer';
        });
        currentMap.on('mouseleave', 'hotspots-fill', () => {
          currentMap.getCanvas().style.cursor = '';
        });

        // Initial satellite layer if already active
        if (displayMode !== 'map') {
          await updateSatelliteLayer(currentMap, detectedProjectId, selectedYear, displayMode);
        }

      } catch (err) {
        console.error('[MapView] Failed to load map data', err);
        setError('Failed to load map geometry.');
      }
    };

    initializeMap();

    currentMap.on('error', (e) => {
      console.error('[MapView] MapLibre internal error:', e);
    });

    return () => {
      isMounted = false;
      currentMap.remove();
      if (map.current === currentMap) {
        map.current = null;
      }
    };
  }, [mode, projectId, hotspotId, navigate]);

  // Effect to update satellite layer whenever displayMode, selectedYear, or activeProject changes
  useEffect(() => {
    if (map.current) {
      updateSatelliteLayer(map.current, activeProject, selectedYear, displayMode);
    }
  }, [displayMode, selectedYear, activeProject, updateSatelliteLayer]);

  if (error) {
    return <div className={`flex items-center justify-center bg-gray-100 text-gray-500 rounded-lg ${className}`}>{error}</div>;
  }

  return (
    <div className="relative flex flex-col space-y-2">
      {/* Map Header Toolbar: Modes & Years */}
      <div className="flex flex-wrap items-center justify-between gap-2 p-2 bg-gray-50 rounded-md border border-gray-200 text-xs">
        {/* Layer Mode Selector */}
        <div className="flex items-center space-x-1">
          <span className="font-semibold text-gray-700 mr-1">Layer:</span>
          <button
            type="button"
            onClick={() => setDisplayMode('map')}
            className={`px-2.5 py-1 rounded font-medium transition ${
              displayMode === 'map'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
            }`}
          >
            Map (OSM)
          </button>
          <button
            type="button"
            onClick={() => setDisplayMode('satellite')}
            className={`px-2.5 py-1 rounded font-medium transition ${
              displayMode === 'satellite'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
            }`}
          >
            Satellite
          </button>
          <button
            type="button"
            onClick={() => setDisplayMode('hybrid')}
            className={`px-2.5 py-1 rounded font-medium transition ${
              displayMode === 'hybrid'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
            }`}
          >
            Hybrid
          </button>
        </div>

        {/* Global project selector (if in global mode and satellite active) */}
        {mode === 'global' && displayMode !== 'map' && (
          <div className="flex items-center space-x-1">
            <span className="font-semibold text-gray-700 mr-1">Project:</span>
            <select
              value={activeProject}
              onChange={(e) => setActiveProject(e.target.value)}
              className="px-2 py-0.5 rounded bg-white border border-gray-300 text-gray-800 font-medium"
            >
              <option value="MH-001">MH-001 (Gondkhari)</option>
              <option value="MH-002">MH-002 (Gadchiroli)</option>
              <option value="MH-003">MH-003 (Bhivpuri PSP)</option>
            </select>
          </div>
        )}

        {/* Year Selector (Active in Satellite / Hybrid modes) */}
        {displayMode !== 'map' && (
          <div className="flex items-center space-x-1">
            <span className="font-semibold text-gray-700 mr-1">Observation Year:</span>
            {AVAILABLE_YEARS.map((yr) => (
              <button
                key={yr}
                type="button"
                onClick={() => setSelectedYear(yr)}
                className={`px-2 py-0.5 rounded font-medium transition ${
                  selectedYear === yr
                    ? 'bg-emerald-700 text-white shadow-sm'
                    : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
                }`}
              >
                {yr} {yr === 2026 ? '(Ref)' : ''}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Map Container */}
      <div className="relative">
        <div ref={mapContainer} className={`rounded-lg overflow-hidden border border-gray-300 shadow-sm ${className}`} style={{ minHeight: '350px' }} />

        {/* Satellite Metadata Overlay Badge */}
        {displayMode !== 'map' && satelliteMeta && (
          <div className="absolute bottom-2 left-2 bg-slate-900/85 backdrop-blur-sm text-white px-2.5 py-1.5 rounded text-[11px] font-mono border border-slate-700 max-w-sm pointer-events-none">
            <div className="font-semibold text-emerald-400">
              {satelliteMeta.sensor} — {satelliteMeta.year} {satelliteMeta.is_reference_year ? '(Reference Period)' : 'Observation'}
            </div>
            <div className="text-slate-300 text-[10px]">
              {satelliteMeta.resolution_description || 'True Color (B4/B3/B2) • ~30 m grid'} • Tiled Layer
            </div>
            {satelliteMeta.is_reference_year && (
              <div className="text-amber-300 text-[10px] mt-0.5 font-sans">
                * Note: 2026 is a reference observation year excluded from ML training.
              </div>
            )}
          </div>
        )}

        {/* Loading Spinner */}
        {loadingSatellite && (
          <div className="absolute top-2 left-2 bg-white/90 text-gray-800 px-3 py-1 rounded shadow text-xs flex items-center space-x-2 border border-gray-300">
            <div className="w-3 h-3 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
            <span>Loading satellite raster...</span>
          </div>
        )}
      </div>

      {/* Scientific & Regulatory Disclaimer Footer */}
      <div className="text-[11px] text-gray-500 italic px-1">
        * Sentinel-2 imagery represents actual visual satellite observations. CNN anomaly outputs are candidate ranking signals; NDVI and Dynamic World metrics are supporting proxy evidence, not regulatory non-compliance determinations.
      </div>
    </div>
  );
};

export default MapView;

