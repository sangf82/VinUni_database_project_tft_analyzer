export type Rank = {
  tier: string;
  division: string;
  lp: number;
};

export type Player = {
  id: string;
  name: string;
  rank: Rank;
  avatar: string;
  winRate: number;
  gamesPlayed: number;
  topFourRate: number;
};

export type Item = {
  id: number;
  name: string;
  icon: string;
};

export type Champion = {
  id: number;
  name: string;
  cost: number;
  icon: string;
  items?: Item[];
};

export type TeamComp = {
  champions: Champion[];
  traits: string[];
};

export type Match = {
  id: string;
  date: string;
  placement: number;
  lpChange: number;
  teamComp: TeamComp;
};

export type LPHistory = {
  date: string;
  lp: number;
  change: number;
};

export type PlayerDetail = {
  id: string;
  name: string;
  rank: Rank;
  avatar: string;
  winRate: number;
  gamesPlayed: number;
  topFourRate: number;
  averagePlacement: number;
  matches: Match[];
  lpHistory: LPHistory[];
};

export type PlacementDistribution = {
  placement: number;
  count: number;
  percentage: number;
};