'use client';

import { useEffect, useState } from 'react';

// next
import dynamic from 'next/dynamic';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

// project imports
import { ThemeMode } from 'config';
import useConfig from 'hooks/useConfig';
import MainCard from 'ui-component/cards/MainCard';
import SkeletonTotalGrowthBarChart from 'ui-component/cards/Skeleton/TotalGrowthBarChart';

// chart data
import revenueChartOption from '../chart-data/revenue-bar-chart';

// assets
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

const status = [
  { value: 'month', label: 'This Month' },
  { value: 'today', label: 'Today' },
  { value: 'year', label: 'This Year' }
];

const series = [
  { name: 'Investment', data: [2, 2.3, 2.5, 2.3, 2, 2.3, 2.7] },
  { name: 'Loss', data: [1.8, 2.3, 1.8, 2.5, 2.3, 1.8, 2.5] }
];

// ==============================|| REVENUE BAR CHART ||============================== //

interface TotalGrowthBarChartProps {
  isLoading: boolean;
}

export default function RevenueBarChart({ isLoading }: TotalGrowthBarChartProps) {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { fontFamily }
  } = useConfig();

  const [value, setValue] = useState('month');
  const [chartOptions, setChartOptions] = useState(revenueChartOption);

  const textPrimary = theme.vars.palette.text.primary;
  const divider = theme.vars.palette.divider;
  const grey500 = theme.vars.palette.grey[500];

  const primaryMain = theme.vars.palette.primary.main;
  const primaryLight = theme.vars.palette.primary.light;

  useEffect(() => {
    setChartOptions({
      ...revenueChartOption,
      chart: { ...revenueChartOption.chart, fontFamily: fontFamily },
      colors: [primaryMain, primaryLight],
      xaxis: { ...revenueChartOption.xaxis, labels: { style: { colors: textPrimary } } },
      yaxis: { ...revenueChartOption.yaxis, labels: { style: { colors: textPrimary } } },
      grid: { borderColor: divider },
      legend: { ...(revenueChartOption.legend ?? {}), labels: { ...(revenueChartOption.legend?.labels ?? {}), colors: grey500 } },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });
  }, [colorScheme, fontFamily, primaryMain, primaryLight, textPrimary, divider, grey500]);

  if (isLoading) return <SkeletonTotalGrowthBarChart />;

  return (
    <MainCard>
      <Grid container spacing={{ xs: 2.5, sm: 1.5 }}>
        <Grid size={12}>
          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            sx={{ alignItems: { xs: 'flex-start', sm: 'center' }, justifyContent: 'space-between', gap: { xs: 2, sm: 1 } }}
          >
            <Stack sx={{ gap: 0.5 }}>
              <Typography sx={{ color: 'grey.600', fontSize: '1rem' }}>Total Revenue Trends</Typography>
              <Typography variant="h1">$999.00</Typography>
            </Stack>
            <Stack direction="row" sx={{ gap: 1 }}>
              <TextField
                id="standard-select-currency"
                select
                value={value}
                onChange={(e) => setValue(e.target.value)}
                slotProps={{
                  htmlInput: { sx: { py: 1, px: 1.5, color: 'grey.900', ...theme.applyStyles('dark', { color: 'grey.600' }) } }
                }}
                sx={{
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderRadius: Number(theme.shape.borderRadius) / 2,
                    borderColor: 'divider'
                  }
                }}
              >
                {status.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
              <Button
                variant="outlined"
                sx={{
                  borderRadius: Number(theme.shape.borderRadius) / 2,
                  py: 0.5,
                  px: 1.25,
                  ml: 1,
                  borderColor: 'divider',
                  color: 'grey.900',
                  ...theme.applyStyles('dark', { color: 'grey.600' })
                }}
                endIcon={<OpenInNewIcon color="disabled" sx={{ fontSize: 18 }} />}
              >
                Export
              </Button>
            </Stack>
          </Stack>
        </Grid>
        <Grid
          sx={{
            ...theme.applyStyles('light', {
              '& .apexcharts-series:nth-of-type(2) path:hover': {
                filter: `brightness(0.95)` /* Darken the bar */,
                transition: 'all 0.3s ease' /* Smooth transition */
              }
            })
          }}
          size={12}
        >
          <Chart options={chartOptions} series={series} type="bar" height={364} />
        </Grid>
      </Grid>
    </MainCard>
  );
}
