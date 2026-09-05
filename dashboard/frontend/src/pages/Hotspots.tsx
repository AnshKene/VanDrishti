import { useEffect, useState } from 'react';
import { api } from '../api';
import type { Hotspot } from '../types';
import HotspotTable from '../components/HotspotTable';
import { useSearchParams } from 'react-router-dom';
import { Filter } from 'lucide-react';

const Hotspots = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [hotspots, setHotspots] = useState<Hotspot[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  
  const page = parseInt(searchParams.get('page') || '1');
  const project = searchParams.get('project') || '';
  const priority = searchParams.get('priority') || '';
  const evidence = searchParams.get('evidence') || '';

  useEffect(() => {
    setLoading(true);
    api.getHotspots({
      page,
      page_size: 25,
      project: project || undefined,
      priority: priority || undefined,
      evidence: evidence || undefined
    }).then(data => {
      setHotspots(data.items);
      setTotal(data.total);
      setTotalPages(data.total_pages);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, [page, project, priority, evidence]);

  const updateParam = (key: string, value: string) => {
    const newParams = new URLSearchParams(searchParams);
    if (value) {
      newParams.set(key, value);
    } else {
      newParams.delete(key);
    }
    newParams.set('page', '1');
    setSearchParams(newParams);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Investigator Queue</h2>
        <p className="mt-1 text-sm text-gray-500">Prioritized candidate locations based on CNN spatial signals and independent proxy evidence.</p>
      </div>

      <div className="bg-white shadow rounded-lg p-4 border border-gray-200">
        <div className="flex flex-col sm:flex-row sm:items-center space-y-3 sm:space-y-0 sm:space-x-4 mb-4">
          <div className="flex items-center text-gray-700 font-medium mr-4">
            <Filter className="w-4 h-4 mr-2" /> Filters:
          </div>
          <select 
            className="block w-full sm:w-auto pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md border"
            value={project}
            onChange={(e) => updateParam('project', e.target.value)}
          >
            <option value="">All Projects</option>
            <option value="MH-001">MH-001 (Gondkhari)</option>
            <option value="MH-002">MH-002 (Gadchiroli)</option>
            <option value="MH-003">MH-003 (Bhivpuri PSP)</option>
          </select>

          <select 
            className="block w-full sm:w-auto pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md border"
            value={priority}
            onChange={(e) => updateParam('priority', e.target.value)}
          >
            <option value="">All Priorities</option>
            <option value="HIGH">High Priority</option>
            <option value="MEDIUM">Medium Priority</option>
            <option value="LOW">Low Priority</option>
            <option value="UNSUPPORTED">Unsupported</option>
          </select>

          <select 
            className="block w-full sm:w-auto pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md border"
            value={evidence}
            onChange={(e) => updateParam('evidence', e.target.value)}
          >
            <option value="">All Evidence</option>
            <option value="STRONG">Strong Support</option>
            <option value="MODERATE">Moderate Support</option>
            <option value="WEAK">Weak Support</option>
            <option value="NO_INDEPENDENT">No Support</option>
          </select>
        </div>
        
        {loading ? (
          <div className="py-12 text-center text-gray-500">Loading queue...</div>
        ) : (
          <>
            <HotspotTable hotspots={hotspots} />
            <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 mt-2">
              <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm text-gray-700">
                    Showing <span className="font-medium">{hotspots.length > 0 ? (page - 1) * 25 + 1 : 0}</span> to <span className="font-medium">{Math.min(page * 25, total)}</span> of <span className="font-medium">{total}</span> candidates
                  </p>
                </div>
                <div>
                  <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                    <button
                      onClick={() => updateParam('page', (page - 1).toString())}
                      disabled={page <= 1}
                      className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                    >
                      Previous
                    </button>
                    <button
                      onClick={() => updateParam('page', (page + 1).toString())}
                      disabled={page >= totalPages}
                      className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                    >
                      Next
                    </button>
                  </nav>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Hotspots;
