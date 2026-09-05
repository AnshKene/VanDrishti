import React from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  color?: 'blue' | 'green' | 'amber' | 'red' | 'gray';
}

const colorMap = {
  blue: 'bg-blue-50 text-blue-700',
  green: 'bg-green-50 text-green-700',
  amber: 'bg-amber-50 text-amber-700',
  red: 'bg-red-50 text-red-700',
  gray: 'bg-gray-50 text-gray-700',
};

const StatCard: React.FC<StatCardProps> = ({ title, value, subtitle, icon, color = 'blue' }) => {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg border border-gray-200">
      <div className="p-5">
        <div className="flex items-center">
          {icon && (
            <div className="flex-shrink-0">
              <div className={`rounded-md p-3 ${colorMap[color]}`}>
                {icon}
              </div>
            </div>
          )}
          <div className={icon ? "ml-5 w-0 flex-1" : "w-full"}>
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd>
                <div className="text-2xl font-semibold text-gray-900">{value}</div>
              </dd>
            </dl>
          </div>
        </div>
      </div>
      {subtitle && (
        <div className="bg-gray-50 px-5 py-3">
          <div className="text-sm text-gray-500">{subtitle}</div>
        </div>
      )}
    </div>
  );
};

export default StatCard;
