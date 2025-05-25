import React from 'react';
import { PlayerDetail as PlayerDetailType, PlacementDistribution } from '../types';
import { formatRank, formatLP, formatPercentage, formatNumber } from '../utils/formatters';
import { Trophy, Target, TowerControl as GameController, BarChart } from 'lucide-react';
import LPHistoryChart from './LPHistoryChart';
import PlacementDistributionChart from './PlacementDistributionChart';
import RecentMatches from './RecentMatches';

interface PlayerDetailProps {
  player: PlayerDetailType;
  placementDistribution: PlacementDistribution[];
}

const PlayerDetail: React.FC<PlayerDetailProps> = ({ player, placementDistribution }) => {
  return (
    <div className="space-y-6">
      {/* Player Header */}
      <div className="bg-gradient-to-r from-indigo-900 to-purple-900 rounded-lg shadow-xl p-6">
        <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
          <div className="flex-shrink-0">
            <img 
              src={player.avatar} 
              alt={player.name} 
              className="h-24 w-24 rounded-full border-4 border-indigo-500"
            />
          </div>
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-white mb-2">{player.name}</h1>
            <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-6">
              <div className="flex items-center gap-2">
                <Trophy className="h-5 w-5 text-yellow-400" />
                <span className="text-lg font-semibold text-white">
                  {formatRank(player.rank)} • {player.rank.lp} LP
                </span>
              </div>
              <div className="flex items-center gap-2">
                <Target className="h-5 w-5 text-green-400" />
                <span className="text-white">
                  Avg. Placement: {player.averagePlacement.toFixed(2)}
                </span>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mt-4 md:mt-0 w-full md:w-auto">
            <div className="bg-gray-800 p-3 rounded-lg text-center">
              <div className="text-sm text-gray-400">Win Rate</div>
              <div className="text-xl font-bold text-white">{formatPercentage(player.winRate)}</div>
            </div>
            <div className="bg-gray-800 p-3 rounded-lg text-center">
              <div className="text-sm text-gray-400">Top 4 Rate</div>
              <div className="text-xl font-bold text-white">{formatPercentage(player.topFourRate)}</div>
            </div>
            <div className="bg-gray-800 p-3 rounded-lg text-center col-span-2 md:col-span-1">
              <div className="text-sm text-gray-400">Games Played</div>
              <div className="text-xl font-bold text-white">{formatNumber(player.gamesPlayed)}</div>
            </div>
          </div>
        </div>
      </div>

      {/* LP History */}
      <div className="bg-gray-800 rounded-lg shadow-xl p-4 sm:p-6">
        <div className="flex items-center gap-2 mb-4">
          <BarChart className="h-5 w-5 text-indigo-400" />
          <h2 className="text-xl font-bold text-white">LP History (Last 100 Matches)</h2>
        </div>
        <div className="h-80">
          <LPHistoryChart lpHistory={player.lpHistory} />
        </div>
      </div>

      {/* Stats Overview - 2 columns layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Placement Distribution */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-4 sm:p-6">
          <div className="flex items-center gap-2 mb-4">
            <Target className="h-5 w-5 text-green-400" />
            <h2 className="text-xl font-bold text-white">Placement Distribution (Last 50 Matches)</h2>
          </div>
          <div className="h-64">
            <PlacementDistributionChart distribution={placementDistribution} />
          </div>
        </div>

        {/* Recent Placements */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-4 sm:p-6">
          <div className="flex items-center gap-2 mb-4">
            <GameController className="h-5 w-5 text-blue-400" />
            <h2 className="text-xl font-bold text-white">Recent Placements (Last 20 Matches)</h2>
          </div>
          <div className="grid grid-cols-5 gap-2">
            {player.matches.slice(0, 20).map((match, index) => {
              let bgColor = "bg-gray-700";
              if (match.placement === 1) bgColor = "bg-yellow-500";
              else if (match.placement <= 4) bgColor = "bg-green-600";
              else bgColor = "bg-red-600";
              
              return (
                <div 
                  key={match.id} 
                  className={`${bgColor} rounded-md h-12 flex items-center justify-center text-white font-bold text-lg transition-transform hover:scale-105`}
                  title={`Game ${index + 1}: ${match.placement}${match.placement === 1 ? 'st' : match.placement === 2 ? 'nd' : match.placement === 3 ? 'rd' : 'th'} place (${formatLP(match.lpChange)})`}
                >
                  {match.placement}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Recent Matches */}
      <div className="bg-gray-800 rounded-lg shadow-xl p-4 sm:p-6">
        <div className="flex items-center gap-2 mb-4">
          <GameController className="h-5 w-5 text-purple-400" />
          <h2 className="text-xl font-bold text-white">Recent Matches</h2>
        </div>
        <RecentMatches matches={player.matches.slice(0, 20)} />
      </div>
    </div>
  );
};

export default PlayerDetail;