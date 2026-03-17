import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Activity } from 'lucide-react';
import { getStatusColor } from '../utils/helpers';

const StatusBadge = ({ status }) => {
  const getStatusIcon = () => {
    switch (status) {
      case 'SAFE': 
        return <CheckCircle className="w-4 h-4" />;
      case 'SUSPICIOUS': 
        return <AlertTriangle className="w-4 h-4" />;
      case 'PHISHING': 
        return <XCircle className="w-4 h-4" />;
      default: 
        return <Activity className="w-4 h-4" />;
    }
  };

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-bold border inline-flex items-center gap-1 ${getStatusColor(status)}`}>
      {getStatusIcon()}
      {status}
    </span>
  );
};

export default StatusBadge;
