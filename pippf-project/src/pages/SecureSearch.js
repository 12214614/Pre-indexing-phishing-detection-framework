import React, { useState } from 'react';
import { Search, Shield, CheckCircle } from 'lucide-react';
import { mockSearchResults } from '../data/mockData';

const SecureSearch = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = () => {
    if (searchQuery.trim()) {
      setSearchResults(mockSearchResults);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fadeIn">
      <div className="text-center space-y-3">
        <h2 className="text-4xl font-black text-white" style={{fontFamily: "'Orbitron', monospace"}}>
          Secure Search Engine
        </h2>
        <p className="text-slate-400">Search the web with phishing protection - only verified safe sites appear</p>
      </div>

      {/* Search Bar */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
        <div className="flex gap-3">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for secure websites..."
            className="flex-1 px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white 
              placeholder-slate-500 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 
              outline-none transition-all"
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button
            onClick={handleSearch}
            className="px-8 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg font-bold text-white 
              hover:from-cyan-400 hover:to-blue-500 transition-all shadow-lg shadow-cyan-500/25 
              flex items-center gap-2"
          >
            <Search className="w-5 h-5" />
            Search
          </button>
        </div>
      </div>

      {/* Protection Notice */}
      <div className="bg-cyan-500/10 border border-cyan-500/30 rounded-xl p-6 flex items-start gap-4">
        <Shield className="w-6 h-6 text-cyan-400 flex-shrink-0 mt-1" />
        <div>
          <h3 className="text-lg font-bold text-cyan-400 mb-2">Protected Search Results</h3>
          <p className="text-slate-300">
            All search results are pre-filtered through our phishing detection system. 
            <span className="text-cyan-400 font-semibold"> Blocked phishing sites are not indexed</span> in these results.
          </p>
        </div>
      </div>

      {/* Search Results */}
      {searchResults.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-slate-400">
              Found <span className="text-white font-bold">{searchResults.length}</span> verified safe results
            </p>
          </div>
          
          {searchResults.map((result) => (
            <div 
              key={result.id}
              className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 hover:border-cyan-500/40 
                transition-all hover:bg-slate-900/80 group cursor-pointer"
            >
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 bg-emerald-500/10 rounded-lg flex items-center justify-center flex-shrink-0">
                  <CheckCircle className="w-5 h-5 text-emerald-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-xl font-bold text-white mb-1 group-hover:text-cyan-400 transition-colors">
                    {result.title}
                  </h3>
                  <p className="text-sm text-cyan-400 mb-2 font-mono break-all">{result.url}</p>
                  <p className="text-slate-400">{result.description}</p>
                  <div className="mt-3 flex items-center gap-2">
                    <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 rounded-full 
                      text-xs font-bold text-emerald-400 flex items-center gap-1">
                      <Shield className="w-3 h-3" />
                      VERIFIED SAFE
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SecureSearch;
