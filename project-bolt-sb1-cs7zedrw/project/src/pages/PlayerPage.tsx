import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DashboardLayout from '../layouts/DashboardLayout';
import PlayerDetail from '../components/PlayerDetail';
import { PlayerDetail as PlayerDetailType, PlacementDistribution } from '../types';
import { getPlayerDetail, getPlacementDistribution } from '../utils/mockData';
import { ArrowLeft } from 'lucide-react';

const PlayerPage: React.FC = () => {
  const { playerId } = useParams<{ playerId: string }>();
  const navigate = useNavigate();
  
  const [player, setPlayer] = useState<PlayerDetailType | null>(null);
  const [placementDistribution, setPlacementDistribution] = useState<PlacementDistribution[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    if (!playerId) {
      setError("Player ID is required");
      setLoading(false);
      return;
    }
    
    try {
      // Simulate API call delay
      const timeoutId = setTimeout(() => {
        const playerData = getPlayerDetail(playerId);
        setPlayer(playerData);
        
        const distribution = getPlacementDistribution(playerData);
        setPlacementDistribution(distribution);
        
        setLoading(false);
      }, 500);
      
      return () => clearTimeout(timeoutId);
    } catch (err) {
      setError("Failed to load player data");
      setLoading(false);
    }
  }, [playerId]);
  
  const handleBack = () => {
    navigate('/');
  };
  
  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
        </div>
      </DashboardLayout>
    );
  }
  
  if (error || !player) {
    return (
      <DashboardLayout>
        <div className="bg-red-900 text-white p-4 rounded-lg">
          <h2 className="text-xl font-bold">Error</h2>
          <p>{error || "Player not found"}</p>
          <button 
            onClick={handleBack}
            className="mt-4 bg-white text-red-900 px-4 py-2 rounded-md font-medium hover:bg-gray-100 transition-colors"
          >
            Back to Leaderboard
          </button>
        </div>
      </DashboardLayout>
    );
  }
  
  return (
    <DashboardLayout>
      <button 
        onClick={handleBack}
        className="flex items-center text-indigo-400 hover:text-indigo-300 mb-6 transition-colors"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Leaderboard
      </button>
      
      <PlayerDetail player={player} placementDistribution={placementDistribution} />
    </DashboardLayout>
  );
};

export default PlayerPage;