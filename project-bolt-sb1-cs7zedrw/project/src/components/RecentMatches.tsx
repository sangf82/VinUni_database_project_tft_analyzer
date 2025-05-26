import React, { useState } from 'react';
import { Match } from '../types';
import { formatDate, formatPlacement, formatLP, getPlacementColor, getLPChangeColor } from '../utils/formatters';
import TeamComp from './TeamComp';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface RecentMatchesProps {
  matches: Match[];
}

const RecentMatches: React.FC<RecentMatchesProps> = ({ matches }) => {
  const [expandedMatch, setExpandedMatch] = useState<string | null>(null);

  const toggleMatchExpansion = (matchId: string) => {
    if (expandedMatch === matchId) {
      setExpandedMatch(null);
    } else {
      setExpandedMatch(matchId);
    }
  };

  return (
    <div className="space-y-4">
      {matches.map((match) => (
        <div 
          key={match.id}
          className="bg-gray-700 rounded-lg overflow-hidden transition-shadow duration-200 hover:shadow-md"
        >
          <div 
            className="p-4 flex flex-col sm:flex-row sm:items-center justify-between cursor-pointer"
            onClick={() => toggleMatchExpansion(match.id)}
          >
            {/* Match summary - left side */}
            <div className="flex items-center space-x-4">
              {/* Placement indicator */}
              <div className={`flex-shrink-0 w-12 h-12 rounded-md flex items-center justify-center text-xl font-bold ${match.placement <= 4 ? 'bg-green-600' : 'bg-red-600'}`}>
                {match.placement}
              </div>
              
              {/* Match info */}
              <div>
                <div className={`text-lg font-semibold ${getPlacementColor(match.placement)}`}>
                  {formatPlacement(match.placement)} Place
                </div>
                <div className="text-sm text-gray-400">{formatDate(match.date)}</div>
              </div>
            </div>
            
            {/* LP change and expand - right side */}
            <div className="flex items-center mt-4 sm:mt-0">
              <div className={`text-lg font-semibold ${getLPChangeColor(match.lpChange)} mr-6`}>
                {formatLP(match.lpChange)}
              </div>
              {expandedMatch === match.id ? (
                <ChevronUp className="h-5 w-5 text-gray-400" />
              ) : (
                <ChevronDown className="h-5 w-5 text-gray-400" />
              )}
            </div>
          </div>
          
          {/* Expanded content */}
          {expandedMatch === match.id && (
            <div className="px-4 pb-4 pt-2 border-t border-gray-600">
              <div className="text-sm font-medium text-gray-300 mb-2">Team Composition</div>
              <TeamComp teamComp={match.teamComp} />
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default RecentMatches;