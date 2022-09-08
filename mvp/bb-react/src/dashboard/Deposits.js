import * as React from 'react';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Title from './Title';

function preventDefault(event) {
  event.preventDefault();
}

export default function Deposits() {
  return (
    <React.Fragment>
      <Title>Avg. Wallet Value</Title>
      <Typography component="p" variant="h4">
        $3,024.00
      </Typography>
      <Typography color="text.secondary" sx={{ flex: 1 }}>
        on 28 July, 2022
      </Typography>
      <div>
        <Link color="primary" href="#" onClick={preventDefault}>
          View holdings
        </Link>
      </div>
    </React.Fragment>
  );
}
