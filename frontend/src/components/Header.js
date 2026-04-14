import React from 'react';
import { Shield, Globe, Search, BarChart3, Activity, Menu, X } from 'lucide-react';

const Header = ({ currentPage, setCurrentPage, mobileMenuOpen, setMobileMenuOpen }) => {
  const navItems = [
    { id: 'landing', label: 'Home', icon: Globe },
    { id: 'verify', label: 'Verify URL', icon: Shield },
    { id: 'search', label: 'Secure Search', icon: Search },
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'about', label: 'Architecture', icon: Activity },
  ];

  return (
    <nav className="relative z-40 border-b border-cyan-500/20 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div 
            className="flex items-center gap-3 cursor-pointer group" 
            onClick={() => setCurrentPage('landing')}
          >
            <div className="relative">
              <Shield className="w-8 h-8 text-cyan-400 group-hover:text-cyan-300 transition-colors" />
              <div className="absolute inset-0 blur-xl bg-cyan-400/20 group-hover:bg-cyan-400/40 transition-all"></div>
            </div>
            <div>
              <h1 className="text-xl font-black tracking-tighter text-cyan-400 group-hover:text-cyan-300 transition-colors" 
                  style={{fontFamily: "'Orbitron', monospace"}}>
                PIPPF
              </h1>
              <p className="text-xs text-slate-500 font-medium tracking-wide">PRE-INDEX DEFENSE</p>
            </div>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => setCurrentPage(item.id)}
                  className={`px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-semibold transition-all
                    ${currentPage === item.id 
                      ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/40' 
                      : 'text-slate-400 hover:text-cyan-400 hover:bg-cyan-500/10'}`}
                >
                  <Icon className="w-4 h-4" />
                  {item.label}
                </button>
              );
            })}
          </div>

          {/* Mobile Menu Button */}
          <button 
            className="md:hidden text-cyan-400"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setCurrentPage(item.id);
                    setMobileMenuOpen(false);
                  }}
                  className={`w-full px-4 py-3 rounded-lg flex items-center gap-3 text-sm font-semibold transition-all
                    ${currentPage === item.id 
                      ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/40' 
                      : 'text-slate-400 hover:text-cyan-400 hover:bg-cyan-500/10'}`}
                >
                  <Icon className="w-5 h-5" />
                  {item.label}
                </button>
              );
            })}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Header;
