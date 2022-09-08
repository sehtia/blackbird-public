import React, { useState, useEffect } from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './dashboard/Title.js';



const BlackbirdSherlockCustomerContracts = () => {
  const [topContracts, setTopContracts] = useState([])
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
              let contracts = [];
              Object.entries(json.topThreeNftContracts).map(([key, value]) =>
                contracts.push([key, value]));
              contracts.sort(function(first,second) {
                return second[1] - first[1];
              });
              let orderedTopContracts = [];
              let id = 0;
              for (var i = 0; i < contracts.length; i++) {
                id = i + 1;
                var data = createData(i+1, contracts[i][0].substring(0,25), contracts[i][1]);
                orderedTopContracts.push(data);
                // orderedTopContracts.push({id, contracts[i][0], contracts[i][1]})
              }
              setTopContracts(orderedTopContracts)
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
      <Title>Top 3 Contracts Used by Sher Customers</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Contract Address</TableCell>
            <TableCell align="right">Contract Interactions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {topContracts.map((row) => (
            <TableRow key={row.id}>
              <TableCell
                component="a"
                href="https://etherscan.io/address/"
                onclick="location.href=this.href+row.name;return false;"
              >
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

export default BlackbirdSherlockCustomerContracts;
