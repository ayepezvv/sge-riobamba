'use client';

import { useEffect, useState } from 'react';

// next
import dynamic from 'next/dynamic';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

// third party
import { ApexOptions } from 'apexcharts';

// project imports
import { ThemeMode } from 'config';
import useConfig from 'hooks/useConfig';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';

// assets
import FiberManualRecordIcon from '@mui/icons-material/FiberManualRecord';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

const series = [
  { name: 'Investment', data: [40, 110, 85, 20, 94, 95, 64, 104, 75, 80, 29, 15] },
  { name: 'Maintenance', data: [102, 103, 25, 85, 90, 90, 85, 40, 40, 48, 68, 25] },
  { name: 'Loss', data: [70, 52, 72, 50, 60, 40, 95, 86, 67, 41, 19, 9] }
];

// chart options
const earningChartOptions: ApexOptions = {
  chart: {
    id: 'bar-chart',
    toolbar: { show: false },
    zoom: { enabled: true },
    background: 'transparent'
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '50%'
    }
  },
  xaxis: {
    type: 'category',
    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  },
  legend: { show: false },
  fill: { type: 'solid' },
  dataLabels: { enabled: false }
};

const widget = [
  {
    name: 'Total Investment',
    number: 586,
    color: 'secondary.dark'
  },
  {
    name: 'Total Maintenance',
    number: 256,
    color: 'secondary.200'
  },
  {
    name: 'Total Loss',
    number: 256,
    color: 'secondary.light'
  }
];

interface SalesChartProps {
  isLoading: boolean;
}

// ==============================|| EARNING OVERVIEW ||============================== //

export default function Overview({ isLoading }: SalesChartProps) {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { container, fontFamily }
  } = useConfig();

  const [chartConfig, setChartConfig] = useState(earningChartOptions);

  const secondaryText = theme.vars.palette.text.secondary;
  const divider = theme.vars.palette.divider;
  const grey500 = theme.vars.palette.grey[500];

  const secondary200 = theme.vars.palette.secondary[200];
  const secondaryDark = theme.vars.palette.secondary.dark;
  const secondaryLight = theme.vars.palette.secondary.light;

  useEffect(() => {
    setChartConfig({
      ...earningChartOptions,
      chart: { ...earningChartOptions.chart, fontFamily: fontFamily },
      colors: [secondaryDark, secondary200, secondaryLight],
      xaxis: { ...earningChartOptions?.xaxis, labels: { style: { colors: secondaryText } } },
      yaxis: { labels: { style: { colors: secondaryText } } },
      grid: { borderColor: divider },
      legend: { ...earningChartOptions.legend, labels: { colors: grey500 } },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });
  }, [colorScheme, fontFamily, secondaryDark, secondary200, secondaryLight, secondaryText, divider, grey500]);

  if (isLoading) return null;

  return (
    <MainCard content={false}>
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 5 } }}>
        <Grid container spacing={1}>
          <Grid size={12}>
            <Typography variant="h3" sx={{ fontWeight: 500 }}>
              Earning Report
            </Typography>
          </Grid>
          <Grid size={{ xs: 12, lg: container ? 3 : 2 }}>
            <Stack sx={{ gap: 2, mt: 2, justifyContent: 'center', textAlign: 'center' }}>
              <SubCard
                sx={{
                  bgcolor: divider,
                  ...theme.applyStyles('dark', { bgcolor: 'background.default' }),
                  height: { lg: 380, xs: 179 },
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  textAlign: 'center'
                }}
              >
                <Stack sx={{ gap: 1 }}>
                  <Typography sx={{ fontSize: 16, color: 'text.secondary' }}>Your earning this month</Typography>
                  <Typography variant="h3" sx={{ fontSize: 34, fontWeight: 700 }}>
                    $586
                  </Typography>
                </Stack>
                <Button variant="contained" sx={{ mt: 3 }}>
                  Withdraw all earnings
                </Button>
              </SubCard>
            </Stack>
          </Grid>
          <Grid size={{ xs: 12, lg: container ? 9 : 10 }}>
            <Chart options={chartConfig} series={series} type="bar" height={320} />
            <Grid container sx={{ justifyContent: { xs: 'center', sm: 'flex-end' } }} size={12}>
              <Stack direction={{ xs: 'column', sm: 'row' }} sx={{ gap: 2.5 }}>
                {widget.map((item, index) => (
                  <Stack
                    key={index}
                    sx={{ border: '1px solid', borderColor: 'divider', p: '10px 20px', borderRadius: '12px', gap: 1 }}
                    direction="row"
                  >
                    <FiberManualRecordIcon fontSize="small" sx={{ color: item.color }} />
                    <Stack sx={{ gap: 0.5 }}>
                      <Typography variant="h6" sx={{ color: 'grey.500' }}>
                        {item.name}
                      </Typography>
                      <Typography variant="h4" sx={{ color: 'grey.900', fontWeight: 500 }}>
                        ${item.number}
                      </Typography>
                    </Stack>
                  </Stack>
                ))}
              </Stack>
            </Grid>
          </Grid>
        </Grid>
      </CardContent>
    </MainCard>
  );
}
