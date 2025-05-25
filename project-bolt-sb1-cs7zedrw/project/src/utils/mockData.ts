import { Player, PlayerDetail, PlacementDistribution } from '../types';
import { format, subDays, subHours } from 'date-fns';

// Generate random LP changes
const generateLPChanges = (count: number, startingLP: number, isTopPlayer = false): { lpHistory: PlayerDetail['lpHistory'], currentLP: number } => {
  let currentLP = startingLP;
  const lpHistory = [];
  
  for (let i = count; i > 0; i--) {
    const date = format(subHours(new Date(), i * 4 + Math.floor(Math.random() * 3)), 'yyyy-MM-dd HH:mm');
    
    // Top players tend to gain more LP on average
    const baseChange = isTopPlayer ? 
      Math.floor(Math.random() * 50) - 15 : 
      Math.floor(Math.random() * 40) - 20;
    
    // Add some variance
    const change = Math.max(-100, Math.min(100, baseChange));
    
    // Update current LP
    const previousLP = currentLP;
    currentLP += change;
    currentLP = Math.max(0, currentLP); // LP can't go below 0
    
    lpHistory.push({
      date,
      lp: previousLP,
      change
    });
  }
  
  return { lpHistory, currentLP };
};

// Generate random matches
const generateMatches = (count: number): PlayerDetail['matches'] => {
  const traits = [
    'Dawnbringer', 'Nightbringer', 'Forgotten', 'Ironclad', 'Mystic', 
    'Cavalier', 'Legionnaire', 'Skirmisher', 'Dragonslayer', 'Assassin'
  ];
  
  const championNames = [
    'Aatrox', 'Ahri', 'Akali', 'Aphelios', 'Ashe', 
    'Aurelion Sol', 'Azir', 'Bard', 'Blitzcrank', 'Brand',
    'Caitlyn', 'Camille', 'Cassiopeia', 'Cho\'Gath', 'Darius',
    'Diana', 'Dr. Mundo', 'Draven', 'Ekko', 'Elise'
  ];
  
  const itemNames = [
    'Infinity Edge', 'Bloodthirster', 'Guardian Angel', 'Rabadon\'s Deathcap',
    'Spear of Shojin', 'Statikk Shiv', 'Titan\'s Resolve', 'Warmog\'s Armor',
    'Zeke\'s Herald', 'Zephyr', 'Blue Buff', 'Hand of Justice'
  ];
  
  return Array.from({ length: count }).map((_, i) => {
    const date = format(subDays(new Date(), Math.floor(i / 3)), 'yyyy-MM-dd HH:mm');
    const placement = Math.floor(Math.random() * 8) + 1;
    const lpChange = placement <= 4 ? 
      Math.floor(Math.random() * 30) + 10 : 
      -Math.floor(Math.random() * 30) - 10;
    
    // Generate random team comp
    const teamSize = Math.floor(Math.random() * 4) + 5; // 5-8 champions
    const champions = Array.from({ length: teamSize }).map((_, j) => {
      const numItems = Math.min(3, Math.floor(Math.random() * 4));
      return {
        id: j + 1,
        name: championNames[Math.floor(Math.random() * championNames.length)],
        cost: Math.floor(Math.random() * 5) + 1,
        icon: `https://via.placeholder.com/40x40.png?text=${j+1}`,
        items: Array.from({ length: numItems }).map((_, k) => ({
          id: k + 1,
          name: itemNames[Math.floor(Math.random() * itemNames.length)],
          icon: `https://via.placeholder.com/20x20.png?text=${k+1}`
        }))
      };
    });
    
    // Pick 2-4 random traits
    const numTraits = Math.floor(Math.random() * 3) + 2;
    const teamTraits = Array.from({ length: numTraits })
      .map(() => traits[Math.floor(Math.random() * traits.length)])
      .filter((trait, index, self) => self.indexOf(trait) === index); // Remove duplicates
    
    return {
      id: `match-${i}`,
      date,
      placement,
      lpChange,
      teamComp: {
        champions,
        traits: teamTraits
      }
    };
  });
};

// Generate placement distribution
const generatePlacementDistribution = (matches: PlayerDetail['matches']): PlacementDistribution[] => {
  const distribution = Array.from({ length: 8 }).map((_, i) => ({
    placement: i + 1,
    count: 0,
    percentage: 0
  }));
  
  matches.forEach(match => {
    distribution[match.placement - 1].count += 1;
  });
  
  const totalMatches = matches.length;
  distribution.forEach(item => {
    item.percentage = (item.count / totalMatches) * 100;
  });
  
  return distribution;
};

// Generate players
export const generatePlayers = (count: number): Player[] => {
  const tiers = ['Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master', 'Grandmaster', 'Challenger'];
  const divisions = ['IV', 'III', 'II', 'I'];
  
  return Array.from({ length: count }).map((_, i) => {
    const isHighRanked = i < count * 0.2; // Top 20% players
    
    // Higher ranks for top players
    const tierIndex = isHighRanked ? 
      Math.min(8, Math.floor(Math.random() * 3) + 6) : // Master, Grandmaster, Challenger
      Math.floor(Math.random() * 6); // Iron to Diamond
    
    const tier = tiers[tierIndex];
    
    // Only tiers below Master have divisions
    const division = tierIndex < 6 ? divisions[Math.floor(Math.random() * 4)] : '';
    
    // LP is higher for top tiers
    const baseLp = isHighRanked ? 
      Math.floor(Math.random() * 900) + 100 : // 100-1000 for high ranks
      Math.floor(Math.random() * 80) + 20; // 20-100 for lower ranks
    
    const winRate = isHighRanked ?
      Math.floor(Math.random() * 20) + 55 : // 55-75% for top players
      Math.floor(Math.random() * 30) + 35; // 35-65% for regular players
    
    const topFourRate = Math.min(98, winRate + Math.floor(Math.random() * 15));
    
    return {
      id: `player-${i}`,
      name: `Player ${i + 1}`,
      rank: {
        tier,
        division,
        lp: baseLp
      },
      avatar: `https://i.pravatar.cc/150?img=${i % 70}`,
      winRate,
      gamesPlayed: Math.floor(Math.random() * 400) + 100,
      topFourRate
    };
  });
};

// Generate player details
export const generatePlayerDetail = (player: Player): PlayerDetail => {
  // Generate match history (20 matches)
  const matches = generateMatches(20);
  
  // Generate LP history (100 points)
  const { lpHistory, currentLP } = generateLPChanges(
    100, 
    player.rank.lp, 
    ['Master', 'Grandmaster', 'Challenger'].includes(player.rank.tier)
  );
  
  // Update player's current LP
  player.rank.lp = currentLP;
  
  // Calculate average placement
  const averagePlacement = matches.reduce((sum, match) => sum + match.placement, 0) / matches.length;
  
  return {
    ...player,
    averagePlacement,
    matches,
    lpHistory
  };
};

// Get placement distribution
export const getPlacementDistribution = (player: PlayerDetail): PlacementDistribution[] => {
  return generatePlacementDistribution(player.matches);
};

// Generate initial players list
export const players = generatePlayers(50);

// Pre-generate some player details for demo purposes
export const playerDetails: Record<string, PlayerDetail> = {};
players.slice(0, 10).forEach(player => {
  playerDetails[player.id] = generatePlayerDetail(player);
});

// Get player detail (generates on demand if not already generated)
export const getPlayerDetail = (playerId: string): PlayerDetail => {
  if (!playerDetails[playerId]) {
    const player = players.find(p => p.id === playerId);
    if (!player) {
      throw new Error(`Player with ID ${playerId} not found`);
    }
    playerDetails[playerId] = generatePlayerDetail(player);
  }
  return playerDetails[playerId];
};