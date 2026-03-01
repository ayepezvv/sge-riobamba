'use client';

import { useEffect, useState } from 'react';

// next
import dynamic from 'next/dynamic';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';

// third party
import { ApexOptions } from 'apexcharts';

// project imports
import { ThemeMode } from 'config';
import useConfig from 'hooks/useConfig';

const ReactApexChart = dynamic(() => import('react-apexcharts'), { ssr: false });

// chart options
const pieChartOptions: ApexOptions = {
  chart: {
    type: 'pie',
    width: 380,
    height: 380,
    background: 'transparent'
  },
  labels: ['Team A', 'Team B', 'Team C', 'Team D'],
  legend: {
    show: true,
    offsetX: 10,
    offsetY: 10,
    labels: { useSeriesColors: false },
    markers: { size: 6, shape: 'circle', strokeWidth: 0 },
    itemMargin: { horizontal: 25, vertical: 4 }
  },
  responsive: [
    {
      breakpoint: 450,
      options: { chart: { width: 250, height: 250 }, legend: { show: false } }
    }
  ]
};

// ==============================|| PIE CHART ||============================== //

export default function ApexPieChart() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { fontFamily }
  } = useConfig();

  const line = theme.vars.palette.divider;
  const textPrimary = theme.vars.palette.text.primary;
  const backColor = theme.vars.palette.background.paper;

  const [series] = useState([35.5, 29, 19.5, 16]);
  const [options, setOptions] = useState(pieChartOptions);

  const primaryMain = theme.vars.palette.primary.main;
  const secondaryMain = theme.vars.palette.secondary.main;
  const successDark = theme.vars.palette.success.dark;
  const warningDark = theme.vars.palette.warning.dark;
  const grey500 = theme.vars.palette.grey[500];

  useEffect(() => {
    setOptions({
      ...pieChartOptions,
      chart: { ...pieChartOptions.chart, fontFamily: fontFamily },
      colors: [secondaryMain, primaryMain, warningDark, successDark],
      grid: { borderColor: line },
      legend: { ...(pieChartOptions.legend ?? {}), labels: { ...(pieChartOptions.legend?.labels ?? {}), colors: grey500 } },
      stroke: { colors: [backColor] },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });
  }, [colorScheme, fontFamily, textPrimary, line, backColor, primaryMain, secondaryMain, warningDark, successDark, grey500]);

  return <ReactApexChart options={options} series={series} type="pie" />;
}
