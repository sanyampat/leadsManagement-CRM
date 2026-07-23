import React, { useState } from 'react';
import { searchBusinesses, DiscoveredBusiness } from '../../services/api';
import { BusinessCard } from './BusinessCard';
import { MapView } from './MapView';

export const DiscoveryDashboard: React.FC = () => {
  const [businessType, setBusinessType] = useState('Restaurant');
  const [location, setLocation] = useState('Mumbai');
  const [country, setCountry] = useState('India');
  const [maxResults, setMaxResults] = useState(20);
  
  const [loading, setLoading] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'map'>('grid');
  const [filterStatus, setFilterStatus] = useState<string>('ALL');
  const [results, setResults] = useState<DiscoveredBusiness[]>([]);
  const [selectedLeadId, setSelectedLeadId] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await searchBusinesses({ business_type: businessType, location, country, max_results: maxResults });
      setResults(data);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredResults = results.filter(b => {
    if (filterStatus === 'ALL') return true;
    return b.website_status === filterStatus;
  });

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 font-sans">
      <header className="mb-8">
        <h1 className="text-3xl font-extrabold tracking-tight text-white mb-2">AI Lead Discovery Engine</h1>
        <p className="text-sm text-slate-400">Discover localized high-opportunity businesses and sync directly into your Outreach CRM.</p>
      </header>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-8 shadow-xl">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label className="block text-xs font-semibold uppercase text-slate-400 mb-1">Business Type</label>
            <input 
              type="text" 
              value={businessType} 
              onChange={e => setBusinessType(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500" 
              required 
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase text-slate-400 mb-1">City / Location</label>
            <input 
              type="text" 
              value={location} 
              onChange={e => setLocation(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500" 
              required 
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase text-slate-400 mb-1">Country</label>
            <input 
              type="text" 
              value={country} 
              onChange={e => setCountry(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500" 
              required 
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase text-slate-400 mb-1">Max Results</label>
            <select 
              value={maxResults} 
              onChange={e => setMaxResults(Number(e.target.value))}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500"
            >
              <option value={10}>10 Leads</option>
              <option value={20}>20 Leads</option>
              <option value={50}>50 Leads</option>
            </select>
          </div>
        </div>

        <button 
          type="submit" 
          disabled={loading}
          className="w-full md:w-auto bg-indigo-600 hover:bg-indigo-500 font-semibold px-8 py-3 rounded-xl text-sm transition-all shadow-lg shadow-indigo-600/30 disabled:opacity-50"
        >
          {loading ? 'Scraping Local Graph & Auditing...' : '🔍 Discover Businesses'}
        </button>
      </form>

      {/* Controls & Filter Bar */}
      {results.length > 0 && (
        <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-6 bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <div className="flex gap-2 flex-wrap">
            {['ALL', 'No Website', 'Social Media Only', 'Website Broken', 'Has Official Website'].map((status) => (
              <button
                key={status}
                onClick={() => setFilterStatus(status)}
                className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                  filterStatus === status ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                }`}
              >
                {status}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2 bg-slate-800 p-1 rounded-lg border border-slate-700">
            <button 
              onClick={() => setViewMode('grid')}
              className={`text-xs px-3 py-1.5 rounded-md font-medium ${viewMode === 'grid' ? 'bg-indigo-600 text-white' : 'text-slate-400'}`}
            >
              Grid View
            </button>
            <button 
              onClick={() => setViewMode('map')}
              className={`text-xs px-3 py-1.5 rounded-md font-medium ${viewMode === 'map' ? 'bg-indigo-600 text-white' : 'text-slate-400'}`}
            >
              Map View
            </button>
          </div>
        </div>
      )}

      {/* Results Rendering */}
      {loading ? (
        <div className="text-center py-20">
          <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-slate-400 text-sm">Querying maps, filtering listicles, and computing opportunity scores...</p>
        </div>
      ) : filteredResults.length === 0 ? (
        <div className="text-center py-20 bg-slate-900/40 rounded-2xl border border-slate-800/80">
          <p className="text-slate-500 text-sm">No businesses discovered yet. Execute a search above to begin.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredResults.map(business => (
            <BusinessCard key={business.id} business={business} onSelect={setSelectedLeadId} />
          ))}
        </div>
      ) : (
        <MapView businesses={filteredResults} onSelect={setSelectedLeadId} />
      )}
    </div>
  );
};