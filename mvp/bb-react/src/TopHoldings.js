import * as React from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './dashboard/Title.js';

// Generate Order Data
function createData(id, name, amount) {
  return { id, name, amount };
}

const rows = [
  createData(
    0,
    'BTC 0',
    312.44,
  ),
  createData(
    1,
    'BTC 1',
    312.44,
  ),
  createData(
    2,
    'BTC 2',
    312.44,
  ),
  createData(
    3,
    'BTC 3',
    312.44,
  ),
];

function preventDefault(event) {
  event.preventDefault();
}

export default function TopHoldings() {
  return (
    <React.Fragment>
      <Title>Top Holdings</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Cryptocurrency</TableCell>
            <TableCell align="right">Avg, Amount Held</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.name}</TableCell>
              <TableCell align="right">{`$${row.amount}`}</TableCell>
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
