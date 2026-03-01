'use client';

// next
import dynamic from 'next/dynamic';

// material-ui
import { useTheme } from '@mui/material/styles';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// third party
import { Props as ChartProps } from 'react-apexcharts';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import { withAlpha } from 'utils/colorUtils';

// assets
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import { IconBrandFacebook, IconBrandYoutube, IconBrandTwitter } from '@tabler/icons-react';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

// ===========================|| MARKET SHARE CHART CARD ||=========================== //

export default function MarketChartCard({ chartData }: { chartData: ChartProps }) {
  const theme = useTheme();

  return (
    <MainCard content={false}>
      <Box sx={{ p: 3 }}>
        <Stack sx={{ gap: 3 }}>
          <Box>
            <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
              <Typography variant="h3">Market Share</Typography>
              <Stack direction="row" sx={{ gap: 1 }}>
                <TrendingDownIcon color="error" sx={{ mb: -0.5 }} />
                <Typography variant="h3">27, 695.65</Typography>
              </Stack>
            </Stack>
            <Typography sx={{ fontWeight: 400, mt: 0.5, color: 'inherit' }} variant="h5">
              Department wise monthly sales report
            </Typography>
          </Box>
          <Stack direction="row" sx={{ alignItems: 'center', gap: 3, flexWrap: 'wrap' }}>
            <Stack direction="row" sx={{ alignItems: 'center', gap: 1 }}>
              <Typography
                sx={{
                  width: 40,
                  height: 40,
                  color: 'secondary.main',
                  borderRadius: '12px',
                  padding: 1,
                  bgcolor: 'secondary.light',
                  ...theme.applyStyles('dark', { bgcolor: 'background.default' })
                }}
              >
                <IconBrandFacebook stroke={1.5} />
              </Typography>
              <Typography variant="h4">+ 45.36%</Typography>
            </Stack>
            <Stack direction="row" sx={{ alignItems: 'center', gap: 1 }}>
              <Typography
                sx={{
                  width: 40,
                  height: 40,
                  color: 'primary.main',
                  borderRadius: '12px',
                  padding: 1,
                  bgcolor: 'primary.light',
                  ...theme.applyStyles('dark', { bgcolor: 'background.default' })
                }}
              >
                <IconBrandTwitter stroke={1.5} />
              </Typography>
              <Typography variant="h4">- 50.69%</Typography>
            </Stack>
            <Stack direction="row" sx={{ alignItems: 'center', gap: 1 }}>
              <Typography
                sx={{
                  width: 40,
                  height: 40,
                  color: 'error.main',
                  borderRadius: '12px',
                  padding: 1,
                  bgcolor: withAlpha(theme.vars.palette.error.light, 0.25),
                  ...theme.applyStyles('dark', { bgcolor: 'background.default' })
                }}
              >
                <IconBrandYoutube stroke={2} />
              </Typography>
              <Typography variant="h4">+ 16.85%</Typography>
            </Stack>
          </Stack>
        </Stack>
      </Box>
      <Chart {...chartData} />
    </MainCard>
  );
}
