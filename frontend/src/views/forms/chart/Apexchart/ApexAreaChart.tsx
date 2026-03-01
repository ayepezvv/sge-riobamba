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
const areaChartOptions: ApexOptions = {
  chart: { height: 350, type: 'area', background: 'transparent' },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth' },
  xaxis: {
    type: 'datetime',
    categories: [
      '2025-09-12T00:00:00.000Z',
      '2025-09-12T01:30:00.000Z',
      '2025-09-12T02:30:00.000Z',
      '2025-09-12T03:30:00.000Z',
      '2025-09-12T04:30:00.000Z',
      '2025-09-12T05:30:00.000Z',
      '2025-09-12T06:30:00.000Z'
    ]
  },
  tooltip: { x: { format: 'dd/MM/yy HH:mm' } },
  legend: {
    show: true,
    position: 'bottom',
    offsetX: 10,
    offsetY: 10,
    labels: { useSeriesColors: false },
    markers: { size: 8, shape: 'square', strokeWidth: 0 },
    itemMargin: { horizontal: 15, vertical: 8 }
  }
};

// ==============================|| AREA CHART ||============================== //

export default function ApexAreaChart() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { fontFamily }
  } = useConfig();

  const textPrimary = theme.vars.palette.text.primary;
  const line = theme.vars.palette.divider;

  const primaryMain = theme.vars.palette.primary.main;
  const secondaryMain = theme.vars.palette.secondary.main;
  const grey500 = theme.vars.palette.grey[500];

  const [series] = useState([
    { name: 'Series 1', data: [31, 40, 28, 51, 42, 109, 100] },
    { name: 'Series 2', data: [11, 32, 45, 32, 34, 52, 41] }
  ]);

  const [options, setOptions] = useState(areaChartOptions);
  useEffect(() => {
    setOptions({
      ...areaChartOptions,
      chart: { ...areaChartOptions.chart, fontFamily: fontFamily },
      colors: [secondaryMain, primaryMain],
      fill: {
        gradient: {
          colorStops: [
            [
              { offset: 0, color: secondaryMain, opacity: 0.4 },
              { offset: 100, color: secondaryMain, opacity: 0.1 }
            ],
            [
              { offset: 0, color: primaryMain, opacity: 0.4 },
              { offset: 100, color: primaryMain, opacity: 0.1 }
            ]
          ]
        }
      },
      xaxis: { ...areaChartOptions.xaxis, labels: { style: { colors: textPrimary } } },
      yaxis: { labels: { style: { colors: textPrimary } } },
      grid: { borderColor: line },
      legend: { ...(areaChartOptions.legend ?? {}), labels: { ...(areaChartOptions.legend?.labels ?? {}), colors: grey500 } },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });
  }, [colorScheme, fontFamily, textPrimary, primaryMain, secondaryMain, line, grey500]);

  return <ReactApexChart options={options} series={series} type="area" height={350} />;
}
