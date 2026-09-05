import React from 'react';

interface EvidenceBadgeProps {
  evidenceClass: string;
}

const EvidenceBadge: React.FC<EvidenceBadgeProps> = ({ evidenceClass }) => {
  let colorClass = 'bg-gray-100 text-gray-800 border-gray-200';
  let label = 'UNSUPPORTED';
  
  if (evidenceClass === 'STRONG_SUPPORT') {
    colorClass = 'bg-blue-100 text-blue-800 border-blue-200';
    label = 'STRONG';
  } else if (evidenceClass === 'MODERATE_SUPPORT') {
    colorClass = 'bg-indigo-100 text-indigo-800 border-indigo-200';
    label = 'MODERATE';
  } else if (evidenceClass === 'WEAK_SUPPORT') {
    colorClass = 'bg-purple-100 text-purple-800 border-purple-200';
    label = 'WEAK';
  } else if (evidenceClass === 'NO_INDEPENDENT_SUPPORT') {
    label = 'NONE';
  }

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${colorClass}`}>
      {label}
    </span>
  );
};

export default EvidenceBadge;
