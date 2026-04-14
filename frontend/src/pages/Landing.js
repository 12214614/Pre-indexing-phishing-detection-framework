import React from 'react';
import { Shield, Activity, Lock, TrendingUp } from 'lucide-react';

const Landing = ({ setCurrentPage }) => {
  const features = [
    {
      icon: Shield,
      title: 'Pre-Index Detection',
      description: 'Identifies phishing sites before search engine indexing using advanced ML algorithms',
      color: 'cyan'
    },
    {
      icon: Activity,
      title: 'Real-Time Analysis',
      description: 'Analyzes URL patterns, SSL certificates, and domain characteristics instantly',
      color: 'blue'
    },
    {
      icon: Lock,
      title: 'Multi-Layer Protection',
      description: 'Combines Random Forest and Gradient Boosting models for 97%+ accuracy',
      color: 'purple'
    }
  ];

  const stats = [
    { label: 'URLs Analyzed', value: '12,847', color: 'cyan' },
    { label: 'Threats Blocked', value: '2,341', color: 'red' },
    { label: 'Accuracy Rate', value: '97.3%', color: 'emerald' },
    { label: 'Avg Response', value: '0.8s', color: 'purple' }
  ];

  return (
    <div className="space-y-16 animate-fadeIn">
      {/* Hero Section */}
      <div className="text-center space-y-6 py-12">
        <div className="inline-block">
          <div className="relative">
            <h1 className="text-5xl sm:text-7xl font-black mb-4 tracking-tighter" 
                style={{fontFamily: "'Orbitron', monospace"}}>
              <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 text-transparent bg-clip-text">
                PIPPF
              </span>
            </h1>
            <div className="absolute -inset-4 bg-gradient-to-r from-cyan-500/20 to-purple-600/20 blur-3xl -z-10"></div>
          </div>
          <p className="text-xl sm:text-2xl text-cyan-400 font-bold tracking-wide">
            Pre-Indexing Phishing Prevention Framework
          </p>
        </div>
        
        <p className="max-w-2xl mx-auto text-slate-400 text-lg leading-relaxed">
          Advanced machine learning system that detects and blocks phishing websites 
          <span className="text-cyan-400 font-semibold"> before they reach search engines</span>, 
          protecting users at the infrastructure level.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
          <button 
            onClick={() => setCurrentPage('verify')}
            className="group px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg font-bold text-white 
              hover:from-cyan-400 hover:to-blue-500 transition-all shadow-lg shadow-cyan-500/25 
              hover:shadow-cyan-500/50 hover:scale-105 flex items-center justify-center gap-2"
          >
            <Shield className="w-5 h-5 group-hover:rotate-12 transition-transform" />
            Verify URL
          </button>
          <button 
            onClick={() => setCurrentPage('search')}
            className="px-8 py-4 bg-slate-800 border-2 border-cyan-500/30 rounded-lg font-bold text-cyan-400 
              hover:bg-slate-700 hover:border-cyan-500/60 transition-all flex items-center justify-center gap-2"
          >
            <Activity className="w-5 h-5" />
            Secure Search
          </button>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="grid md:grid-cols-3 gap-6">
        {features.map((feature, idx) => {
          const Icon = feature.icon;
          return (
            <div 
              key={idx}
              className="group p-6 bg-slate-900/50 border border-slate-800 rounded-xl hover:border-cyan-500/40 
                transition-all hover:bg-slate-900/80 relative overflow-hidden"
            >
              <div className="relative">
                <div className={`w-12 h-12 bg-${feature.color}-500/10 rounded-lg flex items-center justify-center mb-4 
                  group-hover:scale-110 transition-transform`}>
                  <Icon className={`w-6 h-6 text-${feature.color}-400`} />
                </div>
                <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
                <p className="text-slate-400 leading-relaxed">{feature.description}</p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Stats Preview */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <TrendingUp className="w-6 h-6 text-cyan-400" />
          System Performance
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {stats.map((stat, idx) => (
            <div key={idx} className="text-center">
              <div className={`text-3xl font-black text-${stat.color}-400 mb-1`}>
                {stat.value}
              </div>
              <div className="text-sm text-slate-500 uppercase tracking-wide">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Landing;
