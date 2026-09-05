import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Projects from './pages/Projects';
import ProjectDetail from './pages/ProjectDetail';
import Hotspots from './pages/Hotspots';
import HotspotDetail from './pages/HotspotDetail';
import Sidebar from './components/Sidebar';
import Header from './components/Header';

function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-gray-50 overflow-hidden">
        <Sidebar />
        <div className="flex flex-col flex-1 w-0 overflow-hidden">
          <Header />
          <main className="flex-1 relative overflow-y-auto focus:outline-none">
            <div className="py-6">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
                <Routes>
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/projects" element={<Projects />} />
                  <Route path="/projects/:id" element={<ProjectDetail />} />
                  <Route path="/hotspots" element={<Hotspots />} />
                  <Route path="/hotspots/:id" element={<HotspotDetail />} />
                </Routes>
              </div>
            </div>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
