import React, { useState, useEffect } from 'react'
import { PieChart, Pie, Tooltip } from 'recharts';

const axios = require('axios');

/**
 ! Incomplete and unused !
 This component is to act as the parent component of all the chart
 shown on the UI and is made to avoid having an api call for each chart.
**/

const BlackbirdMetrics = () => {
  const [activeWalletPercent, setActiveWalletPercent] = useState(30)
  const [inactiveWalletPercent, setInactiveWalletPercent] = useState(70)


  useEffect(() => {
    const fetchSherlockData = async () => {
      const stakerWalletStats = await axios(
        `https://gradient.pythonanywhere.com/getSherlockStakerWalletStats`
      );
      const stakingPositions = await axios(
        `https://gradient.pythonanywhere.com/getSherlockStakingPositions`
      );

      stakerWalletStats.json().then((json) => {
        console.log(json.data);
        let active_wallet_percent = Math.round(json.isActiveWalletPercent*100)/100;
        let inactive_wallet_percent = Math.round((1 - active_wallet_percent)*100)/100;
        console.log("active wallet percent:", active_wallet_percent);
        setActiveWalletPercent(active_wallet_percent);
        setInactiveWalletPercent(inactive_wallet_percent);
      });

    };
    fetchSherlockData();
  }, []);

}


export default BlackbirdMetrics;
