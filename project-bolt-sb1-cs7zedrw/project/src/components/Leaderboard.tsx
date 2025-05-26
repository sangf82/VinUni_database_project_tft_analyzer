import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowUpDown, Search, Trophy } from 'lucide-react';
import { Player } from '../types';
import { formatRank, formatPercentage } from '../utils/formatters';

interface LeaderboardProps {
  players: Player[];
}

const Leaderboard: React.FC<LeaderboardProps> = ({ players }) => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<keyof Player | 'rank.lp'>('rank.lp');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');

  const handleSort = (key: keyof Player | 'rank.lp') => {
    if (sortBy === key) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(key);
      setSortDirection('desc');
    }
  };

  const sortedPlayers = [...players].sort((a, b) => {
    let valueA, valueB;

    if (sortBy === 'rank.lp') {
      const tierOrder = {
        'Challenger': 9,
        'Grandmaster': 8,
        'Master': 7,
        'Diamond': 6,
        'Platinum': 5,
        'Gold': 4,
        'Silver': 3,
        'Bronze': 2,
        'Iron': 1
      };
      
      const tierA = tierOrder[a.rank.tier as keyof typeof tierOrder] || 0;
      const tierB = tierOrder[b.rank.tier as keyof typeof tierOrder] || 0;
      
      if (tierA !== tierB) {
        return sortDirection === 'desc' ? tierB - tierA : tierA - tierB;
      }
      
      if (a.rank.division && b.rank.division) {
        const divisionOrder = { 'I': 4, 'II': 3, 'III': 2, 'IV': 1 };
        const divA = divisionOrder[a.rank.division as keyof typeof divisionOrder] || 0;
        const divB = divisionOrder[b.rank.division as keyof typeof divisionOrder] || 0;
        
        if (divA !== divB) {
          return sortDirection === 'desc' ? divB - divA : divA - divB;
        }
      }
      
      valueA = a.rank.lp;
      valueB = b.rank.lp;
    } else {
      valueA = a[sortBy];
      valueB = b[sortBy];
    }
    
    if (typeof valueA === 'string' && typeof valueB === 'string') {
      return sortDirection === 'desc' 
        ? valueB.localeCompare(valueA) 
        : valueA.localeCompare(valueB);
    }
    
    return sortDirection === 'desc' 
      ? (valueB as number) - (valueA as number) 
      : (valueA as number) - (valueB as number);
  });

  const filteredPlayers = sortedPlayers.filter(player => 
    player.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handlePlayerClick = (playerId: string) => {
    navigate(`/player/${playerId}`);
  };

  return (
    <div className="bg-vintage-wood rounded-lg shadow-xl overflow-hidden border border-vintage-leather">
      <div className="p-4 sm:p-6 bg-gradient-to-r from-vintage-leather to-vintage-wood">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
          <h2 className="text-2xl font-bold text-vintage-cream flex items-center gap-2 font-serif">
            <Trophy className="h-6 w-6 text-vintage-sand" />
            Ranked Leaderboard
          </h2>
          <div className="relative w-full sm:w-64">
            <input
              type="text"
              placeholder="Search players..."
              className="w-full py-2 pl-10 pr-4 bg-vintage-shadow text-vintage-cream rounded-lg focus:outline-none focus:ring-2 focus:ring-vintage-sand border border-vintage-leather"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-vintage-coffee" />
          </div>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-vintage-leather">
          <thead className="bg-vintage-wood">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-vintage-sand uppercase tracking-wider">
                Rank
              </th>
              <th 
                scope="col" 
                className="px-6 py-3 text-left text-xs font-medium text-vintage-sand uppercase tracking-wider cursor-pointer"
                onClick={() => handleSort('name')}
              >
                <div className="flex items-center gap-1">
                  Player
                  <ArrowUpDown className="h-3 w-3" />
                </div>
              </th>
              <th 
                scope="col" 
                className="px-6 py-3 text-left text-xs font-medium text-vintage-sand uppercase tracking-wider cursor-pointer"
                onClick={() => handleSort('rank.lp')}
              >
                <div className="flex items-center gap-1">
                  Tier/LP
                  <ArrowUpDown className="h-3 w-3" />
                </div>
              </th>
              <th 
                scope="col" 
                className="px-6 py-3 text-right text-xs font-medium text-vintage-sand uppercase tracking-wider cursor-pointer hidden md:table-cell"
                onClick={() => handleSort('winRate')}
              >
                <div className="flex items-center justify-end gap-1">
                  Win Rate
                  <ArrowUpDown className="h-3 w-3" />
                </div>
              </th>
              <th 
                scope="col" 
                className="px-6 py-3 text-right text-xs font-medium text-vintage-sand uppercase tracking-wider cursor-pointer hidden sm:table-cell"
                onClick={() => handleSort('topFourRate')}
              >
                <div className="flex items-center justify-end gap-1">
                  Top 4 Rate
                  <ArrowUpDown className="h-3 w-3" />
                </div>
              </th>
              <th 
                scope="col" 
                className="px-6 py-3 text-right text-xs font-medium text-vintage-sand uppercase tracking-wider cursor-pointer hidden lg:table-cell"
                onClick={() => handleSort('gamesPlayed')}
              >
                <div className="flex items-center justify-end gap-1">
                  Games
                  <ArrowUpDown className="h-3 w-3" />
                </div>
              </th>
            </tr>
          </thead>
          <tbody className="bg-vintage-wood divide-y divide-vintage-leather">
            {filteredPlayers.map((player, index) => (
              <tr 
                key={player.id} 
                className="hover:bg-vintage-leather cursor-pointer transition-colors"
                onClick={() => handlePlayerClick(player.id)}
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-vintage-cream">#{index + 1}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 h-10 w-10">
                      <img className="h-10 w-10 rounded-full border-2 border-vintage-leather" src={player.avatar} alt="" />
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-vintage-cream">{player.name}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex flex-col">
                    <div className="text-sm text-vintage-cream">{formatRank(player.rank)}</div>
                    <div className="text-sm text-vintage-sand">{player.rank.lp} LP</div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium hidden md:table-cell">
                  <span className="text-vintage-cream">{formatPercentage(player.winRate)}</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium hidden sm:table-cell">
                  <span className="text-vintage-cream">{formatPercentage(player.topFourRate)}</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium hidden lg:table-cell">
                  <span className="text-vintage-cream">{player.gamesPlayed}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Leaderboard;