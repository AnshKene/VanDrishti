import { useEffect, useState } from 'react';
import { api } from '../api';
import type { OverviewStats } from '../types';
import StatCard from '../components/StatCard';
import MapView from '../components/MapView';
import { Map, MapPin, AlertTriangle, ShieldCheck } from 'lucide-react';

const Dashboard = () => {
  const [stats, setStats] = useState<OverviewStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getDashboardOverview()
      .then(data => {
        setStats(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setError('Failed to load dashboard overview.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="p-8 text-center text-gray-500">Loading dashboard...</div>;
  if (error || !stats) return <div className="p-8 text-center text-red-500">{error}</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Dashboard Overview</h2>
          <p className="mt-1 text-sm text-gray-500">Global metrics across all monitored projects.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Projects" value={stats.total_projects} icon={<Map className="w-6 h-6" />} color="blue" />
        <StatCard title="Total Hotspots" value={stats.total_hotspots} icon={<MapPin className="w-6 h-6" />} color="gray" />
        <StatCard title="High Priority" value={stats.high_priority} icon={<AlertTriangle className="w-6 h-6" />} color="red" />
        <StatCard title="Supported Candidates" value={stats.supported_hotspots} subtitle={`${stats.unsupported} unsupported / monitor`} icon={<ShieldCheck className="w-6 h-6" />} color="green" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white shadow rounded-lg p-4 border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Global Candidate Map</h3>
          <MapView mode="global" className="w-full h-96" />
        </div>
        
        <div className="bg-white shadow rounded-lg p-4 border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Project Distribution</h3>
          <ul className="divide-y divide-gray-200">
            {stats.project_distribution.map((proj: any) => (
              <li key={proj.project_id} className="py-4 flex justify-between">
                <span className="font-medium text-gray-900">{proj.project_id}</span>
                <span className="text-gray-500">{proj.hotspot_count} hotspots ({proj.high_priority} high)</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
