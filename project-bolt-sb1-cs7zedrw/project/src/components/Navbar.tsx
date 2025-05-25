import React from 'react';
import { Link } from 'react-router-dom';
import { Trophy, BarChart2, Home } from 'lucide-react';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-vintage-wood text-vintage-cream shadow-lg border-b border-vintage-leather">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center gap-2">
              <Trophy className="h-8 w-8 text-vintage-sand" />
              <span className="text-xl font-bold font-serif">TacticsFight</span>
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            <Link 
              to="/" 
              className="flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium hover:bg-vintage-leather transition-colors"
            >
              <Home className="h-5 w-5" />
              <span className="hidden sm:inline">Leaderboard</span>
            </Link>
            <Link 
              to="/stats" 
              className="flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium hover:bg-vintage-leather transition-colors"
            >
              <BarChart2 className="h-5 w-5" />
              <span className="hidden sm:inline">Stats</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;