import React from 'react';
import { TeamComp as TeamCompType, Champion } from '../types';
import { getChampionCostColor } from '../utils/formatters';

interface TeamCompProps {
  teamComp: TeamCompType;
  compact?: boolean;
}

const TeamComp: React.FC<TeamCompProps> = ({ teamComp, compact = false }) => {
  return (
    <div className={`${compact ? 'space-y-1' : 'space-y-3'}`}>
      {/* Traits */}
      {!compact && (
        <div className="flex flex-wrap gap-2">
          {teamComp.traits.map((trait, index) => (
            <span 
              key={index} 
              className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-800 text-indigo-200"
            >
              {trait}
            </span>
          ))}
        </div>
      )}
      
      {/* Champions */}
      <div className="flex flex-wrap gap-2">
        {teamComp.champions.map((champion) => (
          <ChampionIcon key={champion.id} champion={champion} compact={compact} />
        ))}
      </div>
    </div>
  );
};

interface ChampionIconProps {
  champion: Champion;
  compact?: boolean;
}

const ChampionIcon: React.FC<ChampionIconProps> = ({ champion, compact = false }) => {
  const borderColor = getChampionCostColor(champion.cost);
  
  return (
    <div className="relative group">
      <div className={`
        ${compact ? 'w-8 h-8' : 'w-12 h-12'} 
        rounded-md overflow-hidden 
        border-2 ${borderColor}
        relative
      `}>
        <img 
          src={champion.icon} 
          alt={champion.name} 
          className="w-full h-full object-cover" 
        />
        {!compact && champion.items && champion.items.length > 0 && (
          <div className="absolute bottom-0 left-0 right-0 flex justify-center gap-0.5 bg-black bg-opacity-60 p-0.5">
            {champion.items.map((item, i) => (
              <img 
                key={i}
                src={item.icon}
                alt={item.name}
                className="w-3 h-3"
                title={item.name}
              />
            ))}
          </div>
        )}
      </div>
      
      {/* Tooltip */}
      {!compact && (
        <div className="absolute z-10 bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-48 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none">
          <div className="bg-gray-900 p-2 rounded shadow-lg text-sm text-white border border-gray-700">
            <div className="font-medium">{champion.name}</div>
            <div className="text-xs text-gray-400">Cost: {champion.cost}</div>
            {champion.items && champion.items.length > 0 && (
              <div className="mt-1">
                <div className="text-xs text-gray-400">Items:</div>
                <div className="flex flex-wrap gap-1 mt-1">
                  {champion.items.map((item, i) => (
                    <div key={i} className="text-xs text-gray-300">{item.name}</div>
                  ))}
                </div>
              </div>
            )}
          </div>
          <div className="h-2 w-2 bg-gray-900 transform rotate-45 absolute -bottom-1 left-1/2 ml-[-4px] border-r border-b border-gray-700"></div>
        </div>
      )}
    </div>
  );
};

export default TeamComp;