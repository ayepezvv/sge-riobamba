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
const polarChartOptions: ApexOptions = {
  chart: {
    width: 450,
    height: 450,
    type: 'polarArea',
    background: 'transparent'
  },
  fill: { opacity: 1 },
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
      options: { chart: { width: 280, height: 280 }, legend: { show: false } }
    }
  ]
};

// ==============================|| POLAR CHART ||============================== //

export default function ApexPolarChart() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { fontFamily }
  } = useConfig();

  const line = theme.vars.palette.divider;
  const textPrimary = theme.vars.palette.text.primary;
  const backColor = theme.vars.palette.background.paper;

  const [series] = useState<number[]>([13.5, 18, 11, 5, 10, 12]);
  const [options, setOptions] = useState(polarChartOptions);

  const primaryMain = theme.vars.palette.primary.main;
  const secondaryMain = theme.vars.palette.secondary.main;
  const successDark = theme.vars.palette.success.dark;
  const errorMain = theme.vars.palette.error.main;
  const warningDark = theme.vars.palette.warning.dark;
  const grey500 = theme.vars.palette.grey[500];

  useEffect(() => {
    setOptions({
      ...polarChartOptions,
      chart: { ...polarChartOptions.chart, fontFamily: fontFamily },
      colors: [secondaryMain, primaryMain, successDark, errorMain, warningDark, primaryMain],
      yaxis: { labels: { style: { colors: textPrimary } } },
      grid: { borderColor: line },
      legend: { ...(polarChartOptions.legend ?? {}), labels: { ...(polarChartOptions.legend?.labels ?? {}), colors: grey500 } },
      stroke: { colors: [backColor] },
      plotOptions: { polarArea: { rings: { strokeColor: line }, spokes: { connectorColors: line } } },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });
  }, [colorScheme, fontFamily, textPrimary, line, backColor, primaryMain, successDark, secondaryMain, warningDark, errorMain, grey500]);

  return <ReactApexChart options={options} series={series} type="polarArea" />;
}
