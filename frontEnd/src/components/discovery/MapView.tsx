import React from 'react';
import { DiscoveredBusiness } from '../../services/api';

interface Props {
  businesses: DiscoveredBusiness[];
  onSelect: (id: string) => void;
}

export const MapView: React.FC<Props> = ({ businesses, onSelect }) => {
  const withCoords = businesses.filter(b => b.latitude && b.longitude);

  return (
    <div className="bg-slate-900 border border-slate-700/60 rounded-2xl p-6 min-h-[500px] relative overflow-hidden flex flex-col items-center justify-center">
      <div className="absolute inset-0 opacity-15 bg-[radial-gradient(#3b82f6_1px,transparent_1px)] [background-size:16px_16px]"></div>
      
      <div className="z-10 text-center mb-6">
        <h3 className="text-lg font-bold text-white mb-1">Geographic Opportunity Distribution</h3>
        <p className="text-xs text-slate-400">Displaying spatial pin data for {withCoords.length} localized leads</p>
      </div>

      <div className="w-full max-w-4xl h-96 bg-slate-800/50 border border-slate-700/80 rounded-xl relative p-4 flex flex-wrap gap-4 items-center justify-center overflow-auto z-10">
        {withCoords.map((business) => (
          <div 
            key={business.id}
            onClick={() => onSelect(business.id)}
            className="group relative cursor-pointer"
          >
            <div className="w-8 h-8 rounded-full bg-indigo-600/20 border-2 border-indigo-500 flex items-center justify-center text-white text-xs font-bold shadow-lg hover:scale-110 transition-transform">
              📍
            </div>
            
            {/* Hover Tooltip */}
            <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 hidden group-hover:block w-48 bg-slate-900 border border-slate-700 p-2 rounded-lg shadow-xl z-20 pointer-events-none">
              <p className="text-xs font-bold text-white truncate">{business.business_name}</p>
              <p className="text-[10px] text-indigo-400">Score: {business.opportunity?.score}/100</p>
              <p className="text-[10px] text-slate-400">{business.website_status}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};