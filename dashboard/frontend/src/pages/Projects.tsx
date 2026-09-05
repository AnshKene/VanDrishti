import { useEffect, useState } from 'react';
import { api } from '../api';
import type { Project } from '../types';
import { Link } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';

const Projects = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getProjects().then(data => {
      setProjects(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-8 text-center text-gray-500">Loading projects...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Project Directory</h2>
        <p className="mt-1 text-sm text-gray-500">All currently monitored project areas.</p>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md border border-gray-200">
        <ul className="divide-y divide-gray-200">
          {projects.map((proj) => (
            <li key={proj.project_id}>
              <Link to={`/projects/${proj.project_id}`} className="block hover:bg-gray-50">
                <div className="px-4 py-4 flex items-center sm:px-6">
                  <div className="min-w-0 flex-1 sm:flex sm:items-center sm:justify-between">
                    <div className="truncate">
                      <div className="flex text-sm">
                        <p className="font-medium text-blue-600 truncate">{proj.project_id}</p>
                        <p className="ml-1 flex-shrink-0 font-normal text-gray-500">
                          {proj.project_name ? `(${proj.project_name})` : ''}
                        </p>
                      </div>
                      <div className="mt-2 flex">
                        <div className="flex items-center text-sm text-gray-500">
                          {proj.total_hotspots} total candidates identified
                        </div>
                      </div>
                    </div>
                    <div className="mt-4 flex-shrink-0 sm:mt-0 sm:ml-5">
                      <div className="flex space-x-4 text-sm text-gray-600">
                        <span><span className="font-semibold text-red-600">{proj.high_priority_count}</span> High</span>
                        <span><span className="font-semibold text-amber-600">{proj.medium_priority_count}</span> Med</span>
                        <span><span className="font-semibold text-yellow-600">{proj.low_priority_count}</span> Low</span>
                      </div>
                    </div>
                  </div>
                  <div className="ml-5 flex-shrink-0">
                    <ChevronRight className="h-5 w-5 text-gray-400" />
                  </div>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Projects;
