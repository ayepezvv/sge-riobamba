'use client';

// material-ui
import Grid from '@mui/material/Grid';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import { gridSpacing } from 'store/constant';

// charts
import ApexAreaChart from './ApexAreaChart';
import ApexBarChart from './ApexBarChart';
import ApexColumnChart from './ApexColumnChart';
import ApexLineChart from './ApexLineChart';
import ApexMixedChart from './ApexMixedChart';
import ApexPieChart from './ApexPieChart';
import ApexPolarChart from './ApexPolarChart';
import ApexRedialBarChart from './ApexRedialChart';

// ==============================|| APEX CHARTS ||============================== //

export default function Apexchart() {
  return (
    <Grid container spacing={gridSpacing}>
      <Grid size={{ xs: 12, md: 6, lg: 6 }}>
        <MainCard title="Column Chart">
          <ApexColumnChart />
        </MainCard>
      </Grid>
      <Grid size={{ xs: 12, md: 6, lg: 6 }}>
        <MainCard title="Bar Chart">
          <ApexBarChart />
        </MainCard>
      </Grid>
      <Grid size={{ xs: 12, md: 6, lg: 4 }}>
        <MainCard title="Line Chart">
          <ApexLineChart />
        </MainCard>
      </Grid>
      <Grid size={{ xs: 12, md: 6, lg: 4 }}>
        <MainCard title="Area Chart">
          <ApexAreaChart />
        </MainCard>
      </Grid>
      <Grid size={{ xs: 12, md: 6, lg: 4 }}>
        <MainCard title="Mixed Chart">
          <ApexMixedChart />
        </MainCard>
      </Grid>
      <Grid size={{ xs: 12, md: 6, xl: 4 }}>
        <MainCard title="Redial Chart">
          <ApexRedialBarChart />
        </MainCard>
      </Grid>
      <Grid size={{ xs: 12, md: 6, xl: 4 }}>
        <MainCard title="Polar Chart">
          <ApexPolarChart />
        </MainCard>
      </Grid>
      <Grid size={{ xs: 12, md: 6, xl: 4 }}>
        <MainCard title="Pie Chart">
          <ApexPieChart />
        </MainCard>
      </Grid>
    </Grid>
  );
}
