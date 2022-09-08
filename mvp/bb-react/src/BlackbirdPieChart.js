import React, { useState, useEffect } from 'react'
import { useTheme } from '@mui/material/styles';
import { PieChart, Pie, ResponsiveContainer, Tooltip, Label } from 'recharts';
import Title from './dashboard/Title.js';

const BlackbirdPieChart = () => {
  const [activeWalletPercent, setActiveWalletPercent] = useState(30)
  const [inactiveWalletPercent, setInactiveWalletPercent] = useState(70)
  var baseUrl = "https://gradient.pythonanywhere.com/getSherlockStakerWalletStats";

  useEffect(() => {
    const fetchSherlockActiveWalletStats = async () => {
      await fetch(`${baseUrl}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': "*"
        }
      })
        .then((response) => {
          if (response.ok) {
            response.json().then((json) => {
              let active_wallet_percent = Math.round(json.isActiveWalletPercent*100)/100;
              let inactive_wallet_percent = Math.round((1 - active_wallet_percent)*100)/100;
              console.log("active wallet percent:", active_wallet_percent);
              setActiveWalletPercent(active_wallet_percent*100);
              setInactiveWalletPercent(inactive_wallet_percent*100);
            });
          }
        }).catch((error) => {
          console.log(error);
        });
    };
    fetchSherlockActiveWalletStats()
  }, [baseUrl])

  var sherlockActiveWalletData = [
      {
        "name": "Active Wallets",
        "value": activeWalletPercent,
        "fill" : "#4caf50"
      },
      {
        "name": "Inactive Wallets",
        "value": inactiveWalletPercent,
        "fill" : "#FFBB28"
      }
    ];


  // const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
  //   const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  //   const x = cx + radius * Math.cos(-midAngle * RADIAN);
  //   const y = cy + radius * Math.sin(-midAngle * RADIAN);
  //   return (
  //     <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
  //       {`${(percent * 100).toFixed(0)}%`}
  //     </text>
  //   );
  // };

  let renderLabel = function(entry) {
      return entry.value.toString() + "%";
  }

  return (
    <React.Fragment>
      <Title>Active Sherlock Wallets</Title>
        <ResponsiveContainer>
          <PieChart width={730} height={250}>
              <Pie
                data={sherlockActiveWalletData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                label={renderLabel}
                paddingAngle={5}
                innerRadius={60}
                outerRadius={80} />
              <Tooltip></Tooltip>
          </PieChart>
        </ResponsiveContainer>
    </React.Fragment>
  );
}

export default BlackbirdPieChart;
