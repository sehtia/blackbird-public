import logo from './logo.svg';
import './App.css';
import * as React from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Pie, PieChart, Cell} from 'recharts';
import { anotherFileData } from './PieChartData.js';
import BlackbirdPieChart from './BlackbirdPieChart.js';
import BlackbirdLineChart from './BlackbirdLineChart.js';
import Button from '@mui/material/Button';
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import Dashboard from './dashboard/Dashboard.js';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";


function App() {

  const data = [
    {"name" : "5/31/22", "value": 550},
    {"name" : "6/31/22", "value": 500},
    {"name" : "7/21/22", "value": 400}
  ];

  const data001 = [
    {
      "name": "Group A",
      "value": 400
    },
    {
      "name": "Group B",
      "value": 300
    },
    {
      "name": "Group C",
      "value": 300
    },
    {
      "name": "Group D",
      "value": 200
    },
    {
      "name": "Group E",
      "value": 278
    },
    {
      "name": "Group F",
      "value": 189
    }
  ];
  const data002 = [
    {
      "name": "Active Wallets",
      "value": 2400,
      "fill" : "#FF8042"
    },
    {
      "name": "Inactive Wallets",
      "value": 4567,
      "fill" : "#FFBB28"
    }
  ];

  //source: https://mui.com/material-ui/react-table/

  const columns = [
    { field: 'id', headerName: 'Rank', width: 70 },
    { field: 'smartContract', headerName: 'Smart Contract', width: 130 },
    {
      field: 'valueStaked',
      headerName: 'Value Staked ($k)',
      type: 'number',
      width: 150,
    }
  ];

  const rows = [
    { id: 1, lastName: 'Uniswap', smartContract: 'Uniswap', valueStaked: 35 },
    { id: 2, lastName: 'AAVE', smartContract: 'AAVE', valueStaked: 42 },
    { id: 3, lastName: 'Compound', smartContract: 'Compound', valueStaked: 45 },
    { id: 4, lastName: 'DxDy', smartContract: 'DxDy', valueStaked: 16 },
    { id: 5, lastName: 'Sherlock', smartContract: 'Sherlock', valueStaked: 50 },

  ];



  return (

    <div className="App">


      <Dashboard></Dashboard>

      <Router>
        <div>
          {/* A <Switch> looks through its children <Route>s and
              renders the first one that matches the current URL. */}
          <Routes>
            <Route path="/dash" element={<Button>Dash</Button>}>
              {/* <Dashboard></Dashboard> */}
            </Route>
            <Route path="/profile" element={<Button>Profile</Button>}>
            </Route>
            <Route path="/" element={<Button>Root</Button>}>
              {/* <Dashboard></Dashboard>
              <Dashboard></Dashboard>
              <Dashboard></Dashboard> */}
            </Route>
          </Routes>
        </div>
    </Router>

      <h3 align="left" margin="100px" >Average Wallet Value Over Time</h3>
      <LineChart width={400} height={400} data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <Line type="monotone" dataKey="value" stroke="#8884d8" />
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip/>
      </LineChart>



      <h3 align="left" margin="100px" >Blackbird Pie Chart XYZ</h3>
      <BlackbirdPieChart />

      <BlackbirdLineChart />




      <div style={{ height: 400, width: '100%' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          pageSize={5}
          rowsPerPageOptions={[5]}
          checkboxSelection
        />
      </div>

      <Button variant="contained">Hello World</Button>



      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>





        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
