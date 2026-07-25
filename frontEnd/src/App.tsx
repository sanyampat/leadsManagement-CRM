import { useState } from 'react';
import { DiscoveryDashboard } from './components/discovery/DiscoveryDashboard';
import './App.css';

// This acts as a placeholder wrapper for your Existing React Outreach CRM.
// Replace this component's interior with your original CRM components or dashboard!
const ExistingCRMView = () => (
  <div className="p-8 text-slate-100">
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 max-w-4xl">
      <div className="flex items-center gap-3 mb-4">
        <span className="bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          System of Record
        </span>
      </div>
      <h2 className="text-2xl font-bold text-white mb-2">Existing Outreach CRM</h2>
      <p className="text-slate-400 text-sm mb-6">
        Your legacy manual lead management, email templates, and outreach tracking campaigns remain intact here. 
        Leads discovered and saved from the AI engine will populate into your tables automatically.
      </p>
      <div className="p-6 bg-slate-950 rounded-xl border border-slate-800/80 text-center text-slate-500 text-sm">
        [ Mount your original CRM tables, campaign lists, and reply tracking components here ]
      </div>
    </div>
  </div>
);

function App() {
  const [activeTab, setActiveTab] = useState<'discovery' | 'crm'>('discovery');

  return (
    <div className="flex min-h-screen bg-slate-950 font-sans antialiased text-slate-100">
      {/* Dark Sidebar Navigation */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between hidden md:flex shrink-0">
        <div>
          {/* App Brand Header */}
          <div className="h-16 flex items-center px-6 border-b border-slate-800/80">
            <span className="text-lg font-black tracking-tight text-white flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-indigo-500 inline-block animate-pulse"></span>
              Outreach AI
            </span>
          </div>

          {/* Navigation Links */}
          <nav className="p-4 space-y-1.5">
            <div className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider text-slate-500">
              Growth Engine
            </div>
            
            <button
              onClick={() => setActiveTab('discovery')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                activeTab === 'discovery'
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <span>🔍</span>
              <span>Lead Discovery</span>
            </button>

            <button
              onClick={() => setActiveTab('crm')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                activeTab === 'crm'
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <span>📁</span>
              <span>Outreach CRM</span>
            </button>

            <div className="pt-4 px-3 py-2 text-[11px] font-bold uppercase tracking-wider text-slate-500">
              Outreach Tools
            </div>
            
            <button 
              onClick={() => setActiveTab('crm')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 text-left"
            >
              <span>✉️</span>
              <span>Email Templates</span>
            </button>
            
            <button 
              onClick={() => setActiveTab('crm')}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 text-left"
            >
              <span>📊</span>
              <span>Reply Analytics</span>
            </button>
          </nav>
        </div>

        {/* Sidebar Footer */}
        <div className="p-4 border-t border-slate-800/80">
          <div className="bg-slate-950/60 rounded-xl p-3 border border-slate-800/80 flex items-center justify-between">
            <div className="flex items-center gap-2.5 overflow-hidden">
              <div className="w-8 h-8 rounded-full bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400 font-bold text-xs shrink-0">
                AI
              </div>
              <div className="truncate">
                <p className="text-xs font-bold text-white truncate">Pro Plan</p>
                <p className="text-[10px] text-slate-400 truncate">v2.0 Architecture</p>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto min-w-0">
        {/* Mobile Header Toggle (Only visible on small screens) */}
        <div className="md:hidden bg-slate-900 border-b border-slate-800 p-4 flex justify-between items-center">
          <span className="font-bold text-white">Outreach AI</span>
          <div className="flex gap-2 bg-slate-950 p-1 rounded-lg border border-slate-800">
            <button 
              onClick={() => setActiveTab('discovery')}
              className={`text-xs px-3 py-1.5 rounded font-medium ${activeTab === 'discovery' ? 'bg-indigo-600 text-white' : 'text-slate-400'}`}
            >
              Discovery
            </button>
            <button 
              onClick={() => setActiveTab('crm')}
              className={`text-xs px-3 py-1.5 rounded font-medium ${activeTab === 'crm' ? 'bg-indigo-600 text-white' : 'text-slate-400'}`}
            >
              CRM
            </button>
          </div>
        </div>

        {/* View Switcher */}
        {activeTab === 'discovery' ? (
          <DiscoveryDashboard />
        ) : (
          <ExistingCRMView />
        )}
      </main>
    </div>
  );
}

export default App;