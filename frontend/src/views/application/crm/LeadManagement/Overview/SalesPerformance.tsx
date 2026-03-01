'use client';

import { useEffect, useState } from 'react';

// next
import dynamic from 'next/dynamic';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';
import Grid from '@mui/material/Grid';
import IconButton from '@mui/material/IconButton';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

// third party
import { ApexOptions } from 'apexcharts';

// project imports
import { ThemeMode } from 'config';
import useConfig from 'hooks/useConfig';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';
import SkeletonTotalGrowthBarChart from 'ui-component/cards/Skeleton/TotalGrowthBarChart';

// assets
import MenuIcon from '@mui/icons-material/Menu';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

// chart options
const salesChartOptions: ApexOptions = {
  chart: {
    type: 'bar',
    stacked: true,
    toolbar: { show: false },
    background: 'transparent'
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '40%'
    }
  },
  xaxis: {
    type: 'category',
    categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  legend: { show: false },
  fill: { type: 'solid' },
  dataLabels: { enabled: false }
};

const widgetData = [
  { number: '200', label: 'Conversion Rate' },
  { number: '120', label: 'Average Deal' },
  { number: '234', label: 'Sales Target' }
];

const series = [
  { name: 'Investment', data: [50, 105, 80, 50, 70, 80, 80] },
  { name: 'Loss', data: [50, 55, 30, 50, 140, 80, 40] },
  { name: 'Maintenance', data: [50, 150, 120, 110, 180, 150, 130] }
];

// ==============================|| SALE PERFORMANCE - CHART ||============================== //

export default function SalesPerformance({ isLoading }: { isLoading: boolean }) {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { fontFamily }
  } = useConfig();

  const [chartOptions, setChartOptions] = useState(salesChartOptions);

  const textPrimary = theme.vars.palette.text.primary;
  const divider = theme.vars.palette.divider;

  const primary200 = theme.vars.palette.primary[200];
  const primaryDark = theme.vars.palette.primary.dark;
  const secondaryLight = theme.vars.palette.secondary.light;

  useEffect(() => {
    setChartOptions({
      ...salesChartOptions,
      chart: { ...salesChartOptions.chart, fontFamily: fontFamily },
      colors: [primary200, primaryDark, secondaryLight],
      xaxis: { ...salesChartOptions.xaxis, labels: { style: { colors: textPrimary } } },
      yaxis: { labels: { style: { colors: textPrimary } } },
      grid: { borderColor: divider },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });
  }, [colorScheme, fontFamily, primary200, primaryDark, secondaryLight, textPrimary, divider]);

  if (isLoading) return <SkeletonTotalGrowthBarChart />;

  return (
    <MainCard>
      <Grid container spacing={2.5}>
        <Grid size={12}>
          <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="h3" sx={{ fontWeight: 500 }}>
              Sales Performance
            </Typography>
            <IconButton>
              <MenuIcon />
            </IconButton>
          </Stack>
        </Grid>
        <Grid container size={12} spacing={2.5} sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
          {widgetData.map((data, index) => (
            <Grid key={index} size={{ xs: 12, sm: 4 }}>
              <SubCard sx={{ bgcolor: 'grey.100', ...theme.applyStyles('dark', { bgcolor: 'background.default' }) }}>
                <Stack sx={{ gap: 1 }}>
                  <Typography variant="h3">{data.number}</Typography>
                  <Typography variant="h4" sx={{ fontWeight: 400 }}>
                    {data.label}
                  </Typography>
                </Stack>
              </SubCard>
            </Grid>
          ))}
        </Grid>
        <Grid
          size={12}
          sx={{
            ...theme.applyStyles('light', {
              '& .apexcharts-series:nth-of-type(3) path:hover': {
                filter: `brightness(0.95)` /* Darken the bar */,
                transition: 'all 0.3s ease' /* Smooth transition */
              }
            }),
            pt: '0px !important'
          }}
        >
          <Chart options={chartOptions} series={series} height={320} type="bar" />
        </Grid>
      </Grid>
    </MainCard>
  );
}
