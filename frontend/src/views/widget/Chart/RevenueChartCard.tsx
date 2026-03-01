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

// ===========================|| REVENUE CHART CARD ||=========================== //

export default function RevenueChartCard({ chartData }: { chartData: ChartProps }) {
  return (
    <MainCard title="Total Revenue">
      <Chart {...chartData} />
      <Stack direction="row" sx={{ justifyContent: 'space-around', mt: 2 }}>
        <Box>
          <Typography variant="h6" sx={{ textAlign: 'center' }}>
            Youtube
          </Typography>
          <Typography variant="subtitle1" sx={{ color: 'error.main' }}>
            + 16.85%
          </Typography>
        </Box>
        <Box>
          <Typography variant="h6" sx={{ textAlign: 'center' }}>
            Facebook
          </Typography>
          <Box sx={{ color: 'primary.main' }}>
            <Typography variant="subtitle1" color="inherit">
              + 45.36%
            </Typography>
          </Box>
        </Box>
        <Box>
          <Typography variant="h6" sx={{ textAlign: 'center' }}>
            Twitter
          </Typography>
          <Typography variant="subtitle1" sx={{ color: 'secondary.main' }}>
            - 50.69%
          </Typography>
        </Box>
      </Stack>
    </MainCard>
  );
}
