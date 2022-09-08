import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import { PieChart, Pie, ResponsiveContainer, Tooltip } from 'recharts';
import { anotherFileData } from './PieChartData.js';
import Title from './dashboard/Title.js';

// Generate Sales Data
function createData(time, amount) {
  return { time, amount };
}

const data = [
  createData('00:00', 0),
  createData('03:00', 300),
  createData('06:00', 600),
  createData('09:00', 800),
  createData('12:00', 1500),
  createData('15:00', 2000),
  createData('18:00', 2400),
  createData('21:00', 2400),
  createData('24:00', undefined),
];

export default function MyPieChart() {
  const theme = useTheme();

  return (
    <React.Fragment>
      <Title>Active Wallets</Title>
      <ResponsiveContainer>
        <PieChart width={730} height={250}>
            <Pie data={anotherFileData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={60} outerRadius={80} />
            <Tooltip></Tooltip>
        </PieChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}
