import React, { useState } from 'react';
import { Shield, Activity, Lock, Unlock, Clock } from 'lucide-react';
import { getStatusColor, getRiskColor } from '../utils/helpers';
import { API_BASE_URL, verifyUrl } from '../utils/api';
import StatusBadge from '../components/StatusBadge';

const VerifyUrl = () => {
  const [urlInput, setUrlInput] = useState('');
  const [verificationResult, setVerificationResult] = useState(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [error, setError] = useState(null);

  const handleVerifyUrl = async () => {
    if (!urlInput) return;
    setIsVerifying(true);
    setError(null);
    setVerificationResult(null);
    try {
      const data = await verifyUrl(urlInput);
      const mappedStatus = data.prediction === 'phishing' ? 'PHISHING' : 'SAFE';
      const risk = Math.round((data.confidence || 0.5) * 100);
      const ssl = urlInput.startsWith('https://');
      const urlLen = urlInput.length;
      const complexity = urlLen >= 60 ? 'High' : urlLen >= 30 ? 'Medium' : 'Low';
      const domainAge = data.domain_age_days >= 0 ? data.domain_age_days : 'Unknown';
      setVerificationResult({
        url: urlInput,
        status: mappedStatus,
        risk,
        ssl,
        domainAge,
        complexity,
        timestamp: new Date().toLocaleString(),
      });
    } catch (err) {
      console.error('Verification failed:', err);
      setError(`Backend is unreachable. Check REACT_APP_API_BASE_URL. Current API base: ${API_BASE_URL}`);
    } finally {
      setIsVerifying(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fadeIn">
      <div className="text-center space-y-3">
        <h2 className="text-4xl font-black text-white" style={{fontFamily: "'Orbitron', monospace"}}>
          URL Verification
        </h2>
        <p className="text-slate-400">Enter a URL to analyze its security status and risk level</p>
      </div>

      {/* Input Section */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 space-y-6">
        <div className="space-y-3">
          <label className="block text-sm font-semibold text-slate-300 uppercase tracking-wide">
            Enter URL
          </label>
          <div className="flex gap-3">
            <input
              type="text"
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
              placeholder="https://example.com"
              className="flex-1 px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white 
                placeholder-slate-500 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 
                outline-none transition-all"
              onKeyPress={(e) => e.key === 'Enter' && handleVerifyUrl()}
            />
            <button
              onClick={handleVerifyUrl}
              disabled={isVerifying || !urlInput}
              className="px-8 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg font-bold text-white 
                hover:from-cyan-400 hover:to-blue-500 transition-all shadow-lg shadow-cyan-500/25 
                disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isVerifying ? (
                <>
                  <Activity className="w-5 h-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Shield className="w-5 h-5" />
                  Verify
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 rounded-lg border bg-red-500/10 border-red-500/30">
          <p className="text-red-400 font-semibold">⚠ {error}</p>
        </div>
      )}

      {/* Results Section */}
      {verificationResult && (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 space-y-6 animate-slideUp">
          {/* Status Header */}
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h3 className="text-2xl font-bold text-white mb-1">{verificationResult.status}</h3>
              <p className="text-sm text-slate-500">Verified at {verificationResult.timestamp}</p>
            </div>
            <div className={`px-6 py-3 rounded-lg border font-bold text-lg ${getStatusColor(verificationResult.status)}`}>
              Risk: {verificationResult.risk}%
            </div>
          </div>

          {/* URL Display */}
          <div className="p-4 bg-slate-950 rounded-lg border border-slate-700">
            <p className="text-sm text-slate-500 mb-1">Analyzed URL</p>
            <p className="text-cyan-400 font-mono break-all">{verificationResult.url}</p>
          </div>

          {/* Risk Score Bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400 font-semibold">Risk Assessment</span>
              <span className="text-white font-bold">{verificationResult.risk}%</span>
            </div>
            <div className="h-3 bg-slate-950 rounded-full overflow-hidden">
              <div 
                className={`h-full transition-all duration-1000 ease-out ${getRiskColor(verificationResult.risk)}`}
                style={{width: `${verificationResult.risk}%`}}
              ></div>
            </div>
          </div>

          {/* Security Indicators */}
          <div className="grid md:grid-cols-3 gap-4">
            <div className="p-4 bg-slate-950 rounded-lg border border-slate-700">
              <div className="flex items-center gap-2 mb-2">
                {verificationResult.ssl ? (
                  <Lock className="w-5 h-5 text-emerald-400" />
                ) : (
                  <Unlock className="w-5 h-5 text-red-400" />
                )}
                <span className="text-sm font-semibold text-slate-400">SSL Certificate</span>
              </div>
              <p className={`text-lg font-bold ${verificationResult.ssl ? 'text-emerald-400' : 'text-red-400'}`}>
                {verificationResult.ssl ? 'Valid' : 'Invalid'}
              </p>
            </div>
            
            <div className="p-4 bg-slate-950 rounded-lg border border-slate-700">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="w-5 h-5 text-cyan-400" />
                <span className="text-sm font-semibold text-slate-400">Domain Age</span>
              </div>
              <p className="text-lg font-bold text-white">
                {typeof verificationResult.domainAge === 'number' 
                  ? `${verificationResult.domainAge} days` 
                  : verificationResult.domainAge}
              </p>
            </div>
            
            <div className="p-4 bg-slate-950 rounded-lg border border-slate-700">
              <div className="flex items-center gap-2 mb-2">
                <Activity className="w-5 h-5 text-purple-400" />
                <span className="text-sm font-semibold text-slate-400">URL Complexity</span>
              </div>
              <p className="text-lg font-bold text-white">
                {verificationResult.complexity}
              </p>
            </div>
          </div>

          {/* Recommendation */}
          <div className={`p-4 rounded-lg border ${
            verificationResult.status === 'SAFE' ? 'bg-emerald-500/10 border-emerald-500/30' :
            verificationResult.status === 'SUSPICIOUS' ? 'bg-amber-500/10 border-amber-500/30' :
            'bg-red-500/10 border-red-500/30'
          }`}>
            <p className="font-semibold text-white mb-1">
              {verificationResult.status === 'SAFE' ? '✓ Safe to proceed' :
               verificationResult.status === 'SUSPICIOUS' ? '⚠ Exercise caution' :
               '✗ Do not visit this site'}
            </p>
            <p className="text-sm text-slate-300">
              {verificationResult.status === 'SAFE' 
                ? 'This URL appears legitimate based on our analysis.'
                : verificationResult.status === 'SUSPICIOUS'
                ? 'This URL shows suspicious characteristics. Verify before proceeding.'
                : 'This URL exhibits strong phishing indicators. Avoid at all costs.'}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default VerifyUrl;
