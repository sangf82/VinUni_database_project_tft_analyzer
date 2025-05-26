import React from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell
} from 'recharts';
import { PlacementDistribution } from '../types';
import { formatPercentage } from '../utils/formatters';

interface PlacementDistributionChartProps {
  distribution: PlacementDistribution[];
}

const PlacementDistributionChart: React.FC<PlacementDistributionChartProps> = ({ distribution }) => {
  // Sort by placement
  const sortedData = [...distribution].sort((a, b) => a.placement - b.placement);

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const dataPoint = payload[0].payload;
      return (
        <div className="bg-gray-900 p-3 rounded shadow-lg border border-gray-700">
          <p className="font-bold text-white">{getPlacementText(dataPoint.placement)}</p>
          <p className="text-gray-300">Count: {dataPoint.count}</p>
          <p className="text-gray-300">Percentage: {formatPercentage(dataPoint.percentage)}</p>
        </div>
      );
    }
    return null;
  };

  // Helper function to get placement text
  const getPlacementText = (placement: number): string => {
    if (placement === 1) return "1st Place";
    if (placement === 2) return "2nd Place";
    if (placement === 3) return "3rd Place";
    return `${placement}th Place`;
  };

  // Get color based on placement
  const getBarColor = (placement: number): string => {
    if (placement === 1) return "#FBBF24"; // Yellow
    if (placement <= 4) return "#10B981"; // Green
    return "#EF4444"; // Red
  };

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        data={sortedData}
        margin={{ top: 10, right: 10, left: 10, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#2D3748" vertical={false} />
        <XAxis 
          dataKey="placement" 
          tick={{ fill: '#A0AEC0' }}
          axisLine={{ stroke: '#4A5568' }}
          tickLine={{ stroke: '#4A5568' }}
          tickFormatter={(value) => `${value}`}
        />
        <YAxis 
          tick={{ fill: '#A0AEC0' }}
          axisLine={{ stroke: '#4A5568' }}
          tickLine={{ stroke: '#4A5568' }}
          tickFormatter={(value) => `${value}%`}
        />
        <Tooltip content={<CustomTooltip />} />
        <Bar 
          dataKey="percentage" 
          radius={[4, 4, 0, 0]}
          isAnimationActive={true}
          animationDuration={1000}
        >
          {sortedData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={getBarColor(entry.placement)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default PlacementDistributionChart;