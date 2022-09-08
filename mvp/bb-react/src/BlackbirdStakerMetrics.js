import React, { useState, useEffect } from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './dashboard/Title.js';

const BlackbirdSherlockCustomerMetrics = () => {
  const [stakerMetrics, setStakerMetrics] = useState([])
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
              var walletData = createData(1, "Unique Wallets", json.totalWallets);
              var meanEthBalance = createData(2, "Average ETH Balance", json.meanEthBalance.toFixed(2));
              var meanNftCount = createData(3, "Average NFT Count", json.mean_nft_count.toFixed(2));
              var metrics = [walletData, meanEthBalance, meanNftCount];

              setStakerMetrics(metrics);
            });
          }
        }).catch((error) => {
          console.log(error);
        });
    };
    fetchSherlockActiveWalletStats()
  }, [baseUrl])

  // Generate Order Data
  function createData(id, name, amount) {
    return { id, name, amount };
  }

  // href="https://etherscan.io/address/"+row.name


  return (
    <React.Fragment>
      <Title>Sherlock Staker Metrics</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Metric Name</TableCell>
            <TableCell align="right">Metric Value</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {stakerMetrics.map((row) => (
            <TableRow key={row.id}>
              <TableCell>
                {row.name}
              </TableCell>
              <TableCell align="right">{`${row.amount}`}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {/* <Link color="primary" href="#" onClick={preventDefault} sx={{ mt: 3 }}>
        See more orders
      </Link> */}
    </React.Fragment>
  );
}

export default BlackbirdSherlockCustomerMetrics;
