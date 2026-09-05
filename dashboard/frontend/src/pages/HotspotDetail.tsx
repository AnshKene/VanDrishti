import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../api';
import type { Hotspot, Evidence, Provenance } from '../types';
import MapView from '../components/MapView';
import PriorityBadge from '../components/PriorityBadge';
import EvidenceBadge from '../components/EvidenceBadge';
import { ArrowLeft, Target, Shield, Server, Navigation, Layers } from 'lucide-react';

const HotspotDetail = () => {
  const { id } = useParams<{ id: string }>();
  const [hotspot, setHotspot] = useState<Hotspot | null>(null);
  const [evidence, setEvidence] = useState<Evidence | null>(null);
  const [provenance, setProvenance] = useState<Provenance | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      Promise.all([
        api.getHotspot(id),
        api.getHotspotEvidence(id),
        api.getHotspotProvenance(id)
      ]).then(([hData, eData, pData]) => {
        setHotspot(hData);
        setEvidence(eData);
        setProvenance(pData);
        setLoading(false);
      }).catch(err => {
        console.error(err);
        setLoading(false);
      });
    }
  }, [id]);

  if (loading) return <div className="p-8 text-center text-gray-500">Loading candidate details...</div>;
  if (!hotspot) return <div className="p-8 text-center text-red-500">Candidate not found</div>;

  return (
    <div className="space-y-6 pb-12">
      <div className="flex items-center space-x-4">
        <Link to="/hotspots" className="text-gray-400 hover:text-gray-600">
          <ArrowLeft className="w-6 h-6" />
        </Link>
        <div>
          <div className="flex items-center space-x-3">
            <h2 className="text-2xl font-bold text-gray-900">{hotspot.hotspot_id}</h2>
            <PriorityBadge level={hotspot.priority_level} />
          </div>
          <p className="mt-1 text-sm text-gray-500">Project: {hotspot.project_id}</p>
        </div>
      </div>

      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <Shield className="h-5 w-5 text-yellow-400" />
          </div>
          <div className="ml-3">
            <p className="text-sm text-yellow-700">
              <strong className="font-bold">Scientific Disclaimer:</strong> Candidate locations are identified from model-derived spatial signals and independent satellite proxy evidence. They are not confirmed environmental violations or illegal activities. Independent field or regulatory verification is required.
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white shadow rounded-lg p-5 border border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <Navigation className="w-5 h-5 mr-2 text-gray-400" /> Spatial Context
            </h3>
            <MapView mode="hotspot" hotspotId={hotspot.hotspot_id} className="w-full h-80" />
            <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-500">Centroid Lat:</span> <span className="font-medium text-gray-900">{hotspot.centroid_lat.toFixed(6)}</span>
              </div>
              <div>
                <span className="text-gray-500">Centroid Lon:</span> <span className="font-medium text-gray-900">{hotspot.centroid_lon.toFixed(6)}</span>
              </div>
              <div>
                <span className="text-gray-500">Spatial Patches:</span> <span className="font-medium text-gray-900">{hotspot.patch_count}</span>
              </div>
            </div>
          </div>

          <div className="bg-white shadow rounded-lg p-5 border border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <Layers className="w-5 h-5 mr-2 text-gray-400" /> Independent Satellite Evidence
            </h3>
            {evidence ? (
              <div className="space-y-4">
                <div className="flex items-center space-x-3 mb-4">
                  <span className="text-sm font-medium text-gray-700">Overall Classification:</span>
                  <EvidenceBadge evidenceClass={evidence.evidence_class} />
                </div>
                <div className="bg-gray-50 p-3 rounded-md text-sm text-gray-700 mb-4">
                  {evidence.evidence_summary}
                </div>
                <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">NDVI Change (2021-2025)</dt>
                    <dd className="mt-1 text-sm text-gray-900">{evidence.ndvi_change ? evidence.ndvi_change.toFixed(3) : 'N/A'}</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Temporal Dynamic</dt>
                    <dd className="mt-1 text-sm text-gray-900">{evidence.temporal_evidence}</dd>
                  </div>
                </dl>
              </div>
            ) : (
              <p className="text-gray-500">Evidence data unavailable.</p>
            )}
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white shadow rounded-lg p-5 border border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <Target className="w-5 h-5 mr-2 text-gray-400" /> Model Signal (CNN)
            </h3>
            <dl className="space-y-4">
              <div>
                <dt className="text-sm font-medium text-gray-500">Maximum Score</dt>
                <dd className="mt-1 text-2xl font-semibold text-blue-600">{hotspot.max_cnn_score.toFixed(4)}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Mean Score (Across Patches)</dt>
                <dd className="mt-1 text-lg font-medium text-gray-900">{hotspot.mean_cnn_score.toFixed(4)}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Population Percentile</dt>
                <dd className="mt-1 text-sm text-gray-900">{hotspot.cnn_score_percentile.toFixed(1)}th percentile</dd>
              </div>
            </dl>
          </div>

          <div className="bg-white shadow rounded-lg p-5 border border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <Server className="w-5 h-5 mr-2 text-gray-400" /> Data Provenance
            </h3>
            {provenance ? (
              <div className="text-sm space-y-3 text-gray-600">
                <p><strong className="font-medium text-gray-900">Source Feature:</strong> {provenance.source_feature}</p>
                <p><strong className="font-medium text-gray-900">Source File:</strong> {provenance.source_file}</p>
                <p><strong className="font-medium text-gray-900">Model Name:</strong> {provenance.model_name}</p>
                <p><strong className="font-medium text-gray-900">Model Feature:</strong> {provenance.model_feature}</p>
                <p><strong className="font-medium text-gray-900">Validation Threshold:</strong> {provenance.threshold}</p>
                <p><strong className="font-medium text-gray-900">Input Sequence:</strong> {provenance.input_years.join(', ')}</p>
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <p className="text-xs text-gray-400 break-all"><strong className="text-gray-500">Integrity:</strong> {provenance.data_checksum}</p>
                </div>
              </div>
            ) : (
              <p className="text-gray-500">Provenance data unavailable.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HotspotDetail;
