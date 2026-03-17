import React, { useState, useEffect } from 'react';
import { Database, CheckCircle, XCircle, AlertTriangle, Eye, Filter, Lock, Unlock } from 'lucide-react';
import { mockUrlDatabase } from '../data/mockData';
import { calculateStats, filterByStatus, getRiskColor } from '../utils/helpers';
import { getUrlList } from '../utils/api';
import StatusBadge from '../components/StatusBadge';

const Dashboard = () => {
  const [filterStatus, setFilterStatus] = useState('ALL');
  const [urlData, setUrlData] = useState(mockUrlDatabase);

  useEffect(() => {
    getUrlList()
      .then(data => {
        const mapped = data.map(item => ({
          id: item.id,
          url: item.website_url,
          status: item.status === 'blocked' ? 'PHISHING' : item.status === 'legitimate' ? 'SAFE' : 'SUSPICIOUS',
          risk: Math.round((item.confidence || 0.5) * 100),
          ssl: item.ssl,
          domainAge: 0,
          complexity: item.complexity || 'Medium',
        }));
        if (mapped.length > 0) setUrlData(mapped);
      })
      .catch(() => {});
  }, []);

  const stats = calculateStats(urlData);
  const filteredData = filterByStatus(urlData, filterStatus);

  const statCards = [
    { label: 'Total URLs', value: stats.total, icon: Database, color: 'cyan', trend: '+12%' },
    { label: 'Safe Sites', value: stats.safe, icon: CheckCircle, color: 'emerald', trend: '+8%' },
    { label: 'Phishing Blocked', value: stats.phishing, icon: XCircle, color: 'red', trend: '+23%' },
    { label: 'Under Review', value: stats.suspicious, icon: AlertTriangle, color: 'amber', trend: '+5%' }
  ];

  return (
    <div className="space-y-8 animate-fadeIn">
      <div className="text-center space-y-3">
        <h2 className="text-4xl font-black text-white" style={{fontFamily: "'Orbitron', monospace"}}>
          Admin Dashboard
        </h2>
        <p className="text-slate-400">Real-time monitoring and analytics</p>
      </div>

      {/* Statistics Cards */}
      <div className="grid md:grid-cols-4 gap-6">
        {statCards.map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <div 
              key={idx}
              className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 hover:border-cyan-500/40 
                transition-all relative overflow-hidden group"
            >
              <div className="relative">
                <div className="flex items-center justify-between mb-4">
                  <Icon className={`w-8 h-8 text-${stat.color}-400`} />
                  <span className="text-xs text-emerald-400 font-bold">{stat.trend}</span>
                </div>
                <div className={`text-3xl font-black text-${stat.color}-400 mb-1`}>{stat.value}</div>
                <div className="text-sm text-slate-500 uppercase tracking-wide">{stat.label}</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* URL Table */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl overflow-hidden">
        <div className="p-6 border-b border-slate-800 flex items-center justify-between flex-wrap gap-4">
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <Eye className="w-5 h-5 text-cyan-400" />
            Verified URLs
          </h3>
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-slate-500" />
            {['ALL', 'SAFE', 'SUSPICIOUS', 'PHISHING'].map((status) => (
              <button
                key={status}
                onClick={() => setFilterStatus(status)}
                className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
                  filterStatus === status
                    ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/40'
                    : 'text-slate-400 hover:text-cyan-400 hover:bg-slate-800'
                }`}
              >
                {status}
              </button>
            ))}
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-950">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">URL</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Status</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Risk Score</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">SSL</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Domain Age</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Complexity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filteredData.map((item) => (
                <tr key={item.id} className="hover:bg-slate-900/30 transition-colors">
                  <td className="px-6 py-4">
                    <span className="text-cyan-400 font-mono text-sm">{item.url}</span>
                  </td>
                  <td className="px-6 py-4">
                    <StatusBadge status={item.status} />
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="flex-1 h-2 bg-slate-950 rounded-full overflow-hidden max-w-[100px]">
                        <div 
                          className={`h-full ${getRiskColor(item.risk)}`}
                          style={{width: `${item.risk}%`}}
                        ></div>
                      </div>
                      <span className="text-white font-semibold text-sm">{item.risk}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    {item.ssl ? (
                      <Lock className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <Unlock className="w-4 h-4 text-red-400" />
                    )}
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-slate-300 text-sm">{item.domainAge}d</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`text-sm font-medium ${
                      item.complexity === 'Low' ? 'text-emerald-400' :
                      item.complexity === 'Medium' ? 'text-amber-400' : 'text-red-400'
                    }`}>
                      {item.complexity}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
