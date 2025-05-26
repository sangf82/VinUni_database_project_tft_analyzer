import { Rank } from "../types";
import { format, parseISO } from "date-fns";

// Format rank as a string (e.g., "Diamond II")
export const formatRank = (rank: Rank): string => {
  if (["Master", "Grandmaster", "Challenger"].includes(rank.tier)) {
    return rank.tier;
  }
  return `${rank.tier} ${rank.division}`;
};

// Format LP value (e.g., "+25 LP" or "-10 LP")
export const formatLP = (lp: number): string => {
  const sign = lp > 0 ? "+" : "";
  return `${sign}${lp} LP`;
};

// Format date to a readable format
export const formatDate = (dateString: string): string => {
  try {
    const date = parseISO(dateString);
    return format(date, "MMM d, h:mm a");
  } catch (e) {
    return dateString;
  }
};

// Format placement with ordinal suffix (1st, 2nd, 3rd, etc.)
export const formatPlacement = (placement: number): string => {
  const suffixes = ["th", "st", "nd", "rd"];
  const suffix = placement <= 3 ? suffixes[placement] : suffixes[0];
  return `${placement}${suffix}`;
};

// Format percentage
export const formatPercentage = (value: number): string => {
  return `${Math.round(value)}%`;
};

// Get color based on placement
export const getPlacementColor = (placement: number): string => {
  if (placement === 1) return "text-yellow-400";
  if (placement <= 4) return "text-green-500";
  return "text-red-500";
};

// Get color based on LP change
export const getLPChangeColor = (change: number): string => {
  if (change > 0) return "text-green-500";
  if (change < 0) return "text-red-500";
  return "text-gray-400";
};

// Get champion cost color
export const getChampionCostColor = (cost: number): string => {
  switch (cost) {
    case 1: return "border-gray-400";
    case 2: return "border-green-500";
    case 3: return "border-blue-500";
    case 4: return "border-purple-500";
    case 5: return "border-yellow-400";
    default: return "border-gray-400";
  }
};

// Format large numbers with comma separators
export const formatNumber = (num: number): string => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};