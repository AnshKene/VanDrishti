import React from 'react';

interface PriorityBadgeProps {
  level: string;
}

const PriorityBadge: React.FC<PriorityBadgeProps> = ({ level }) => {
  let colorClass = 'bg-gray-100 text-gray-800 border-gray-200';
  
  if (level === 'HIGH PRIORITY') {
    colorClass = 'bg-red-100 text-red-800 border-red-200';
  } else if (level === 'MEDIUM PRIORITY') {
    colorClass = 'bg-amber-100 text-amber-800 border-amber-200';
  } else if (level === 'LOW PRIORITY') {
    colorClass = 'bg-yellow-100 text-yellow-800 border-yellow-200';
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${colorClass}`}>
      {level.replace(' PRIORITY', '').replace(' / MONITOR', '')}
    </span>
  );
};

export default PriorityBadge;
