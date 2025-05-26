import React from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import Leaderboard from '../components/Leaderboard';
import { players } from '../utils/mockData';

const HomePage: React.FC = () => {
  return (
    <DashboardLayout>
      <Leaderboard players={players} />
    </DashboardLayout>
  );
};

export default HomePage;