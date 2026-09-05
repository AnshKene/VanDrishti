import { useEffect, useState } from 'react';
import { api } from '../api';
import type { Project } from '../types';
import { useParams, Link } from 'react-router-dom';
import MapView from '../components/MapView';
import StatCard from '../components/StatCard';
import { MapPin, AlertTriangle, ArrowLeft } from 'lucide-react';

const ProjectDetail = () => {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      api.getProject(id).then(data => {
        setProject(data);
        setLoading(false);
      }).catch(err => {
        console.error(err);
        setLoading(false);
      });
    }
  }, [id]);

  if (loading) return <div className="p-8 text-center text-gray-500">Loading project details...</div>;
  if (!project) return <div className="p-8 text-center text-red-500">Project not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Link to="/projects" className="text-gray-400 hover:text-gray-600">
          <ArrowLeft className="w-6 h-6" />
        </Link>
        <div>
          <h2 className="text-2xl font-bold text-gray-900">{project.project_id} {project.project_name ? `— ${project.project_name}` : ''}</h2>
          <p className="mt-1 text-sm text-gray-500">Project Candidate Overview</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Candidates" value={project.total_hotspots} icon={<MapPin className="w-6 h-6" />} color="blue" />
        <StatCard title="High Priority" value={project.high_priority_count} icon={<AlertTriangle className="w-6 h-6" />} color="red" />
        <StatCard title="Medium Priority" value={project.medium_priority_count} color="amber" />
        <StatCard title="Unsupported" value={project.unsupported_count} color="gray" />
      </div>

      <div className="bg-white shadow rounded-lg p-4 border border-gray-200">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-medium text-gray-900">Project Map</h3>
          <Link to={`/hotspots?project=${project.project_id}`} className="text-sm font-medium text-blue-600 hover:text-blue-500">
            View Investigator Queue
          </Link>
        </div>
        <MapView mode="project" projectId={project.project_id} className="w-full h-[500px]" />
      </div>
    </div>
  );
};

export default ProjectDetail;
