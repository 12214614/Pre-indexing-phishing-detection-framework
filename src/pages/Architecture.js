import React from 'react';
import { Activity, Database, BarChart3, Shield, TrendingUp, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';

const Architecture = () => {
  const workflowPhases = [
    {
      step: '1',
      title: 'Website Detection & Crawler Initiation',
      description: 'When a newly hosted website is detected, the crawler initiates a multi-stage security verification process before allowing the website to be indexed',
      color: 'cyan'
    },
    {
      step: '2',
      title: 'Stage-1: URL-Based ML Detection',
      description: 'First hybrid detection stage analyzes URL patterns, lexical features, domain characteristics using machine learning classifiers (Random Forest, Gradient Boosting)',
      color: 'blue'
    },
    {
      step: '3',
      title: 'Stage-2: JavaScript Malicious Behavior Analysis',
      description: 'Simultaneous analysis of JavaScript code for malicious behaviors including obfuscation, suspicious API calls, data exfiltration attempts, and dynamic code execution',
      color: 'purple'
    },
    {
      step: '4',
      title: 'Stage-3: DOM Rendering & NCD Similarity Analysis',
      description: 'Crawler renders webpage using real browser engine to obtain fully executed HTML DOM. Performs similarity-based phishing detection using Normalized Compression Distance (NCD) against known phishing and legitimate prototypes',
      color: 'pink'
    },
    {
      step: '5',
      title: 'Consensus-Based Decision',
      description: 'Final decision uses consensus rule: All stages agree = LEGITIMATE (indexed) / All stages agree = PHISHING (blocked) / Disagreement = SUSPICIOUS (flagged for review)',
      color: 'emerald'
    }
  ];

  const features = [
    'URL lexical analysis (Stage-1)',
    'Domain reputation scoring (Stage-1)',
    'SSL certificate validation (Stage-1)',
    'JavaScript obfuscation detection (Stage-2)',
    'Malicious API call analysis (Stage-2)',
    'DOM rendering & NCD similarity (Stage-3)',
    'Visual phishing prototype matching (Stage-3)',
    'Consensus-based multi-stage voting'
  ];

  const benefits = [
    {
      icon: Shield,
      title: 'Proactive Defense',
      description: 'Stops threats before they reach users'
    },
    {
      icon: TrendingUp,
      title: 'High Accuracy',
      description: '97%+ detection rate with low false positives'
    },
    {
      icon: Activity,
      title: 'Real-Time',
      description: 'Sub-second analysis and response'
    }
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fadeIn">
      <div className="text-center space-y-3">
        <h2 className="text-4xl font-black text-white" style={{fontFamily: "'Orbitron', monospace"}}>
          System Architecture
        </h2>
        <p className="text-slate-400">How PIPPF protects users from phishing attacks</p>
      </div>

      {/* System Workflow */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 space-y-6">
        <h3 className="text-2xl font-bold text-white flex items-center gap-2">
          <Activity className="w-6 h-6 text-cyan-400" />
          Detection Workflow
        </h3>
        
        <div className="space-y-4">
          {workflowPhases.map((phase, idx) => (
            <div key={idx} className="flex gap-4 items-start">
              <div className={`w-12 h-12 bg-${phase.color}-500/20 border-2 border-${phase.color}-500 rounded-lg 
                flex items-center justify-center flex-shrink-0 font-black text-${phase.color}-400 text-lg`}>
                {phase.step}
              </div>
              <div className="flex-1 pt-1">
                <h4 className="text-lg font-bold text-white mb-1">{phase.title}</h4>
                <p className="text-slate-400">{phase.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Feature Extraction */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Database className="w-5 h-5 text-cyan-400" />
            Multi-Stage Analysis Features
          </h3>
          <ul className="space-y-3">
            {features.map((feature, idx) => (
              <li key={idx} className="flex items-center gap-2 text-slate-300">
                <div className="w-2 h-2 bg-cyan-400 rounded-full"></div>
                {feature}
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-purple-400" />
            Detection Algorithms
          </h3>
          <div className="space-y-4">
            <div className="p-4 bg-slate-950 rounded-lg border border-slate-700">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-white">Stage-1: Random Forest + Gradient Boosting</span>
                <span className="text-emerald-400 font-bold">96.8%</span>
              </div>
              <p className="text-sm text-slate-400">URL-based machine learning detection using ensemble classifiers</p>
            </div>
            <div className="p-4 bg-slate-950 rounded-lg border border-slate-700">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-white">Stage-2: JavaScript Behavior Analysis</span>
                <span className="text-emerald-400 font-bold">94.2%</span>
              </div>
              <p className="text-sm text-slate-400">Dynamic analysis of malicious JavaScript patterns and behaviors</p>
            </div>
            <div className="p-4 bg-slate-950 rounded-lg border border-slate-700">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-white">Stage-3: NCD Similarity Detection</span>
                <span className="text-emerald-400 font-bold">97.9%</span>
              </div>
              <p className="text-sm text-slate-400">Normalized Compression Distance against known phishing prototypes</p>
            </div>
          </div>
        </div>
      </div>

      {/* Key Benefits */}
      <div className="bg-gradient-to-br from-cyan-500/10 to-blue-600/10 border border-cyan-500/30 rounded-xl p-8">
        <h3 className="text-2xl font-bold text-white mb-6">Consensus-Based Decision Rules</h3>
        <div className="space-y-4">
          <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
            <div className="flex items-center gap-3 mb-2">
              <CheckCircle className="w-6 h-6 text-emerald-400" />
              <h4 className="text-lg font-bold text-emerald-400">All Stages → LEGITIMATE</h4>
            </div>
            <p className="text-slate-300 text-sm">
              If all stages (Stage-1, Stage-2, Stage-3) classify the website as legitimate, 
              it is <span className="font-bold text-emerald-400">indexed and made searchable</span>.
            </p>
          </div>

          <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
            <div className="flex items-center gap-3 mb-2">
              <XCircle className="w-6 h-6 text-red-400" />
              <h4 className="text-lg font-bold text-red-400">All Stages → PHISHING</h4>
            </div>
            <p className="text-slate-300 text-sm">
              If all stages classify the website as phishing, 
              it is <span className="font-bold text-red-400">blocked entirely and not indexed</span>.
            </p>
          </div>

          <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg">
            <div className="flex items-center gap-3 mb-2">
              <AlertTriangle className="w-6 h-6 text-amber-400" />
              <h4 className="text-lg font-bold text-amber-400">Disagreement → SUSPICIOUS</h4>
            </div>
            <p className="text-slate-300 text-sm">
              If there is disagreement between stages, the website is <span className="font-bold text-amber-400">flagged as suspicious 
              and held for further manual review</span>.
            </p>
          </div>
        </div>
        <p className="mt-6 text-slate-400 text-sm">
          This architecture ensures robust, multi-layered detection and significantly reduces both false positives and zero-day phishing risks.
        </p>
      </div>

      {/* Original Key Benefits */}
      <div className="bg-gradient-to-br from-purple-500/10 to-pink-600/10 border border-purple-500/30 rounded-xl p-8">
        <h3 className="text-2xl font-bold text-white mb-6">Key Benefits</h3>
        <div className="grid md:grid-cols-3 gap-6">
          {benefits.map((benefit, idx) => {
            const Icon = benefit.icon;
            return (
              <div key={idx} className="text-center">
                <div className="w-16 h-16 bg-cyan-500/20 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Icon className="w-8 h-8 text-cyan-400" />
                </div>
                <h4 className="text-lg font-bold text-white mb-2">{benefit.title}</h4>
                <p className="text-slate-400 text-sm">{benefit.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Architecture;
