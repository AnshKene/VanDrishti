import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Map, MapPin } from 'lucide-react';

const Sidebar = () => {
  return (
    <div className="flex flex-col w-64 bg-gray-800 border-r border-gray-700">
      <div className="flex items-center justify-center h-16 bg-gray-900 px-4">
        <span className="text-white font-bold text-sm tracking-wider uppercase">Environmental Monitor</span>
      </div>
      <div className="flex flex-col flex-1 overflow-y-auto">
        <nav className="flex-1 px-2 py-4 space-y-1">
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                isActive ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`
            }
          >
            <LayoutDashboard className="mr-3 h-5 w-5" />
            Dashboard
          </NavLink>
          <NavLink
            to="/projects"
            className={({ isActive }) =>
              `group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                isActive ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`
            }
          >
            <Map className="mr-3 h-5 w-5" />
            Projects
          </NavLink>
          <NavLink
            to="/hotspots"
            className={({ isActive }) =>
              `group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                isActive ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`
            }
          >
            <MapPin className="mr-3 h-5 w-5" />
            Investigator Queue
          </NavLink>
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
