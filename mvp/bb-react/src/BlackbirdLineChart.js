import React, { useState, useEffect } from "react";
import { render } from "react-dom";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import Title from './dashboard/Title.js';


const BlackbirdPieChart = () => {
  const [timedStakingValues, setTimedStakingValues] = useState({})
  const [timedStakeValues, setTimedStakeValues] = useState([])

  var baseUrl = "https://gradient.pythonanywhere.com/getSherlockStakingPool";

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
              console.log("staking positions response:", json);
              let lineChartData = [];
              Object.entries(json).map(([key, value]) =>
                lineChartData.push({"name": key, "value":value}));
              setTimedStakingValues(json);
              setTimedStakeValues(lineChartData);
            });
          }
        }).catch((error) => {
          console.log(error);
        });
    };
    fetchSherlockActiveWalletStats()
  }, [baseUrl])

  const data = [];

  const styles = {
    fontFamily: "sans-serif",
    textAlign: "center"
  };

  const DataFormater = (number) => {
    if (number > 1000000000) {
      return (number/1000000000).toString() + 'B';
    } else if(number > 1000000) {
      return (number/1000000).toString() + 'M';
    } else if(number > 1000) {
      return (number/1000).toString() + 'K';
    } else {
      return number.toString();
    }
  }

  return (
    <React.Fragment>
      <Title>Staking Pool (TVC)</Title>
        <ResponsiveContainer>
          <div style={styles}>
            <LineChart
              width={450}
              height={195}
              data={timedStakeValues}
              margin={{ top: 5, right: 5, bottom: 5, left: 0 }}
            >
              <Line type="monotone" dataKey="value" stroke="#8884d8" dot={false} />
              <XAxis dataKey="name" minTickGap={20} />
              <YAxis tickFormatter={(value) => new Intl.NumberFormat('en', { notation: "compact", compactDisplay: "short" }).format(value)}/>
              <Tooltip></Tooltip>
            </LineChart>
          </div>
        </ResponsiveContainer>
    </React.Fragment>
  );
}

export default BlackbirdPieChart;
