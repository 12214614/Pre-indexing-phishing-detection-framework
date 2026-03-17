import React, { useState, useEffect } from 'react';
import { Shield } from 'lucide-react';
import Header from './components/Header';
import Landing from './pages/Landing';
import VerifyUrl from './pages/VerifyUrl';
import SecureSearch from './pages/SecureSearch';
import Dashboard from './pages/Dashboard';
import Architecture from './pages/Architecture';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('landing');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [glitchActive, setGlitchActive] = useState(false);

  // Glitch effect on page change
  useEffect(() => {
    setGlitchActive(true);
    const timer = setTimeout(() => setGlitchActive(false), 800);
    return () => clearTimeout(timer);
  }, [currentPage]);

  const renderPage = () => {
    switch(currentPage) {
      case 'landing':
        return <Landing setCurrentPage={setCurrentPage} />;
      case 'verify':
        return <VerifyUrl />;
      case 'search':
        return <SecureSearch />;
      case 'dashboard':
        return <Dashboard />;
      case 'about':
        return <Architecture />;
      default:
        return <Landing setCurrentPage={setCurrentPage} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans relative overflow-hidden">
      {/* Animated background grid */}
      <div className="fixed inset-0 opacity-20 pointer-events-none">
        <div className="absolute inset-0 grid-background"></div>
      </div>

      {/* Glitch overlay */}
      {glitchActive && (
        <div className="fixed inset-0 pointer-events-none z-50 animate-pulse">
          <div className="absolute inset-0 bg-cyan-500/5"></div>
        </div>
      )}

      {/* Header/Navigation */}
      <Header 
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        mobileMenuOpen={mobileMenuOpen}
        setMobileMenuOpen={setMobileMenuOpen}
      />

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {renderPage()}
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-slate-800 bg-slate-950/80 backdrop-blur-xl mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-3">
              <Shield className="w-6 h-6 text-cyan-400" />
              <span className="text-slate-400">
                <span className="text-cyan-400 font-bold">PIPPF</span> - B.Tech Final Year Project
              </span>
            </div>
            <p className="text-slate-500 text-sm">
              © 2026 Pre-Indexing Phishing Prevention Framework
            </p>
          </div>
        </div>        # Terminal 1 — Backend
        cd /e/pippf-project-updated/phishing_backend/backend
        E:/pippf-project-updated/.venv/Scripts/python.exe manage.py runserver
        
        # Terminal 2 — Frontend
        cd /e/pippf-project-updated/pippf-project
        npm start        # Terminal 1 — Backend
        cd /e/pippf-project-updated/phishing_backend/backend
        E:/pippf-project-updated/.venv/Scripts/python.exe manage.py runserver
        
        # Terminal 2 — Frontend
        cd /e/pippf-project-updated/pippf-project
        npm start        # Terminal 1 — Backend
        cd /e/pippf-project-updated/phishing_backend/backend
        E:/pippf-project-updated/.venv/Scripts/python.exe manage.py runserver
        
        # Terminal 2 — Frontend
        cd /e/pippf-project-updated/pippf-project
        npm start
      </footer>
    </div>
  );
}

export default App;
