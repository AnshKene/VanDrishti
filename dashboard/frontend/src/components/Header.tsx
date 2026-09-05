import { ShieldAlert } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm h-16 flex items-center justify-between px-6 z-10 border-b border-gray-200">
      <h1 className="text-xl font-semibold text-gray-800">Decision Support Dashboard</h1>
      <div className="flex items-center text-amber-600 text-sm font-medium bg-amber-50 px-3 py-1.5 rounded-full border border-amber-200">
        <ShieldAlert className="w-4 h-4 mr-2" />
        Read-Only Projection
      </div>
    </header>
  );
};

export default Header;
