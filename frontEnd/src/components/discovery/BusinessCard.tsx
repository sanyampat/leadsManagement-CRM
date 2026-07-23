import React, { useState } from 'react';
import { DiscoveredBusiness, saveToCRM } from '../../services/api';

interface Props {
  business: DiscoveredBusiness;
  onSelect: (id: string) => void;
}

export const BusinessCard: React.FC<Props> = ({ business, onSelect }) => {
  const [isSaved, setIsSaved] = useState(business.crm_saved);
  const [loading, setLoading] = useState(false);

  const handleSave = async (e: React.MouseEvent) => {
    e.stopPropagation();
    setLoading(true);
    try {
      await saveToCRM(business.id);
      setIsSaved(true);
    } catch (error) {
      console.error("Failed to save to CRM", error);
    } finally {
      setLoading(false);
    }
  };

  const getBadgeColor = (score: number = 0) => {
    if (score >= 80) return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    if (score >= 50) return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
    return 'bg-slate-500/10 text-slate-400 border-slate-500/20';
  };

  return (
    <div 
      onClick={() => onSelect(business.id)}
      className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-5 hover:border-slate-600 transition-all cursor-pointer flex flex-col justify-between"
    >
      <div>
        <div className="flex justify-between items-start gap-2 mb-3">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400">
              {business.category}
            </span>
            <h3 className="text-lg font-bold text-white mt-0.5">{business.business_name}</h3>
          </div>
          <span className={`px-2.5 py-1 rounded-full text-xs font-bold border ${getBadgeColor(business.opportunity?.score)}`}>
            {business.opportunity?.score || 0} / 100
          </span>
        </div>

        <p className="text-sm text-slate-400 mb-2">📍 {business.location}</p>
        <p className="text-sm font-medium text-slate-300 mb-4">
          🌐 Status: <span className="text-white font-semibold">{business.website_status}</span>
        </p>

        {business.opportunity?.reason && (
          <div className="bg-slate-900/60 rounded-lg p-3 mb-4 border border-slate-700/40">
            <p className="text-xs text-slate-300 italic">"{business.opportunity.reason}"</p>
          </div>
        )}
      </div>

      <div className="flex items-center gap-2 pt-3 border-t border-slate-700/50">
        <button 
          onClick={() => onSelect(business.id)}
          className="flex-1 bg-slate-700 hover:bg-slate-600 text-white text-xs font-semibold py-2 px-3 rounded-lg transition-colors"
        >
          View Audit
        </button>
        <button 
          onClick={handleSave}
          disabled={isSaved || loading}
          className={`flex-1 text-xs font-semibold py-2 px-3 rounded-lg transition-colors ${
            isSaved 
              ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 cursor-default'
              : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/20'
          }`}
        >
          {loading ? 'Saving...' : isSaved ? '✓ In CRM' : '+ Save Lead'}
        </button>
      </div>
    </div>
  );
};