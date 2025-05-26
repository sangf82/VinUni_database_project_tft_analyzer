import React from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { LPHistory } from '../types';
import { formatDate, formatLP } from '../utils/formatters';

interface LPHistoryChartProps {
  lpHistory: LPHistory[];
}

const LPHistoryChart: React.FC<LPHistoryChartProps> = ({ lpHistory }) => {
  // Create data points that include both LP and the change
  const data = lpHistory.map((point, index) => {
    const nextPoint = index < lpHistory.length - 1 ? lpHistory[index + 1] : null;
    return {
      ...point,
      formattedDate: formatDate(point.date),
      // Calculate the LP after the change for the actual point to plot
      lpAfterChange: nextPoint ? point.lp + point.change : point.lp
    };
  });

  // Get min and max LP values for setting chart domain
  const lpValues = data.map(d => d.lp).concat(data.map(d => d.lpAfterChange));
  const minLP = Math.min(...lpValues);
  const maxLP = Math.max(...lpValues);
  
  // Add padding to the domain
  const yDomainMin = Math.max(0, minLP - 50);
  const yDomainMax = maxLP + 50;

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const dataPoint = payload[0].payload;
      return (
        <div className="bg-gray-900 p-3 rounded shadow-lg border border-gray-700">
          <p className="text-gray-300">{dataPoint.formattedDate}</p>
          <p className="font-bold text-white">LP: {dataPoint.lpAfterChange}</p>
          <p className={`${dataPoint.change > 0 ? 'text-green-500' : dataPoint.change < 0 ? 'text-red-500' : 'text-gray-400'}`}>
            Change: {formatLP(dataPoint.change)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart
        data={data}
        margin={{ top: 10, right: 30, left: 10, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#2D3748" />
        <XAxis 
          dataKey="formattedDate" 
          tick={{ fill: '#A0AEC0' }}
          interval="preserveStartEnd"
          tickMargin={10}
          axisLine={{ stroke: '#4A5568' }}
          tickLine={{ stroke: '#4A5568' }}
          minTickGap={30}
        />
        <YAxis 
          domain={[yDomainMin, yDomainMax]}
          tick={{ fill: '#A0AEC0' }}
          axisLine={{ stroke: '#4A5568' }}
          tickLine={{ stroke: '#4A5568' }}
          tickFormatter={(value) => `${value}`}
        />
        <Tooltip content={<CustomTooltip />} />
        <ReferenceLine y={0} stroke="#4A5568" />
        <Line
          type="monotone"
          dataKey="lpAfterChange"
          stroke="#7C3AED"
          strokeWidth={2}
          dot={{ r: 3, strokeWidth: 1, fill: '#7C3AED' }}
          activeDot={{ r: 6, strokeWidth: 0, fill: '#7C3AED' }}
          isAnimationActive={true}
          animationDuration={1000}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default LPHistoryChart;