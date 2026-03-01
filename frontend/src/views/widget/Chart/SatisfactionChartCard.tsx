'use client';

// next
import dynamic from 'next/dynamic';

// material-ui
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// third party
import { Props as ChartProps } from 'react-apexcharts';

// project imports
import MainCard from 'ui-component/cards/MainCard';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

// =========================|| SATISFACTION CHART CARD ||========================= //

export default function SatisfactionChartCard({ chartData }: { chartData: ChartProps }) {
  return (
    <MainCard>
      <Stack sx={{ gap: 1 }}>
        <Typography variant="subtitle1">Customer Satisfaction</Typography>
        <Box sx={{ '& .apexcharts-tooltip.apexcharts-theme-light': { color: 'common.white' } }}>
          <Chart {...chartData} />
        </Box>
      </Stack>
    </MainCard>
  );
}
