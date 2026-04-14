// Utility functions for URL analysis
// These simulate ML model predictions for demonstration

export const getStatusColor = (status) => {
  switch (status) {
    case 'SAFE': 
      return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
    case 'SUSPICIOUS': 
      return 'text-amber-400 bg-amber-500/10 border-amber-500/30';
    case 'PHISHING': 
      return 'text-red-400 bg-red-500/10 border-red-500/30';
    default: 
      return 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30';
  }
};

export const getRiskColor = (risk) => {
  if (risk < 30) return 'bg-emerald-500';
  if (risk < 70) return 'bg-amber-500';
  return 'bg-red-500';
};

export const calculateStats = (data) => {
  return {
    total: data.length,
    safe: data.filter(u => u.status === 'SAFE').length,
    phishing: data.filter(u => u.status === 'PHISHING').length,
    suspicious: data.filter(u => u.status === 'SUSPICIOUS').length,
  };
};

export const filterByStatus = (data, status) => {
  if (status === 'ALL') return data;
  return data.filter(item => item.status === status);
};

// Simulate ML model prediction delay
export const simulateAnalysis = (callback, delay = 2000) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(callback());
    }, delay);
  });
};
