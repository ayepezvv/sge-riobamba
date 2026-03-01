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
const barChartOptions: ApexOptions = {
  chart: {
    type: 'bar',
    height: 350,
    background: 'transparent',
    toolbar: { show: false }
  },
  plotOptions: { bar: { borderRadius: 4, horizontal: true } },
  dataLabels: { enabled: false },
  xaxis: {
    categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan', 'United States', 'China', 'Germany'],
    axisBorder: { show: false },
    axisTicks: { show: false }
  },
  grid: { show: false }
};

// ==============================|| BAR CHART ||============================== //

export default function ApexBarChart() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { fontFamily }
  } = useConfig();

  const textPrimary = theme.vars.palette.text.primary;
  const successDark = theme.vars.palette.success.dark;

  const [series] = useState([{ data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380] }]);

  const [options, setOptions] = useState(barChartOptions);

  useEffect(() => {
    setOptions({
      ...barChartOptions,
      chart: { ...barChartOptions.chart, fontFamily: fontFamily },
      colors: [successDark],
      xaxis: { ...barChartOptions.xaxis, labels: { style: { colors: textPrimary } } },
      yaxis: { labels: { style: { colors: textPrimary } } },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });
  }, [colorScheme, fontFamily, textPrimary, successDark]);

  return <ReactApexChart options={options} series={series} type="bar" height={350} />;
}
