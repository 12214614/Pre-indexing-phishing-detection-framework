// Mock database for demonstration purposes
// In production, this would be fetched from backend API

export const mockUrlDatabase = [
  { 
    id: 1, 
    url: 'https://secure-banking.com', 
    status: 'SAFE', 
    risk: 5, 
    ssl: true, 
    domainAge: 2456, 
    complexity: 'Low',
    timestamp: '2026-02-01 10:30:00'
  },
  { 
    id: 2, 
    url: 'https://paypa1-verify.tk', 
    status: 'PHISHING', 
    risk: 95, 
    ssl: false, 
    domainAge: 3, 
    complexity: 'High',
    timestamp: '2026-02-01 11:15:00'
  },
  { 
    id: 3, 
    url: 'https://amazon-login.xyz', 
    status: 'SUSPICIOUS', 
    risk: 68, 
    ssl: true, 
    domainAge: 12, 
    complexity: 'Medium',
    timestamp: '2026-02-01 12:00:00'
  },
  { 
    id: 4, 
    url: 'https://microsoft.com', 
    status: 'SAFE', 
    risk: 2, 
    ssl: true, 
    domainAge: 8234, 
    complexity: 'Low',
    timestamp: '2026-02-01 09:45:00'
  },
  { 
    id: 5, 
    url: 'https://free-netflix-premium.ml', 
    status: 'PHISHING', 
    risk: 92, 
    ssl: false, 
    domainAge: 1, 
    complexity: 'High',
    timestamp: '2026-02-01 14:20:00'
  },
  { 
    id: 6, 
    url: 'https://github.com', 
    status: 'SAFE', 
    risk: 1, 
    ssl: true, 
    domainAge: 5840, 
    complexity: 'Low',
    timestamp: '2026-02-01 08:30:00'
  },
];

export const mockSearchResults = [
  { 
    id: 1, 
    title: 'Secure Banking Portal', 
    url: 'https://secure-banking.com', 
    description: 'Official banking services with enterprise security standards and SSL encryption.' 
  },
  { 
    id: 2, 
    title: 'Microsoft Corporation', 
    url: 'https://microsoft.com', 
    description: 'Leading technology company providing cloud services, software, and enterprise solutions.' 
  },
  { 
    id: 3, 
    title: 'GitHub - Developer Platform', 
    url: 'https://github.com', 
    description: 'World\'s leading platform for code hosting, version control, and collaboration.' 
  },
];

export const systemStats = {
  totalAnalyzed: 12847,
  threatsBlocked: 2341,
  accuracyRate: 97.3,
  avgResponseTime: 0.8
};
