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

// types
import { KeyedObject } from 'types';

const ReactApexChart = dynamic(() => import('react-apexcharts'), { ssr: false });

// chart options
const redialBarChartOptions: ApexOptions = {
  chart: {
    type: 'radialBar',
    width: 450,
    height: 450,
    background: 'transparent'
  },
  plotOptions: {
    radialBar: {
      offsetY: 0,
      startAngle: 0,
      endAngle: 270,
      hollow: { margin: 5, size: '30%', background: 'transparent', image: undefined },
      dataLabels: { name: { show: false }, value: { show: false } }
    }
  },
  labels: ['Vimeo', 'Messenger', 'Facebook', 'LinkedIn'],
  legend: {
    show: true,
    floating: true,
    fontSize: '16px',
    position: 'left',
    offsetX: 0,
    offsetY: 15,
    labels: { useSeriesColors: true },
    markers: { size: 0 },
    formatter(seriesName: string, opts: KeyedObject) {
      return `${seriesName}:  ${opts.w.globals.series[opts.seriesIndex]}`;
    },
    itemMargin: { vertical: 3 }
  },
  responsive: [
    {
      breakpoint: 450,
      options: {
        chart: { width: 280, height: 280 },
        legend: {
          show: true,
          floating: true,
          fontSize: '16px',
          position: 'left',
          offsetX: -20,
          offsetY: -10,
          labels: { useSeriesColors: true },
          markers: { size: 0 },
          formatter(seriesName: string, opts: KeyedObject) {
            return `${seriesName}:  ${opts.w.globals.series[opts.seriesIndex]}`;
          },
          itemMargin: { vertical: 3 }
        }
      }
    }
  ]
};

// ==============================|| RADIAL BAR CHART ||============================== //

export default function ApexRedialBarChart() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { fontFamily }
  } = useConfig();

  const line = theme.vars.palette.divider;

  const [series] = useState<number[]>([76, 67, 61, 90]);
  const [options, setOptions] = useState(redialBarChartOptions);

  const primaryMain = theme.vars.palette.primary.main;
  const secondaryMain = theme.vars.palette.secondary.main;
  const successDark = theme.vars.palette.success.dark;
  const errorMain = theme.vars.palette.error.main;

  useEffect(() => {
    setOptions({
      ...redialBarChartOptions,
      chart: { ...redialBarChartOptions.chart, fontFamily: fontFamily },
      colors: [secondaryMain, primaryMain, successDark, errorMain],
      grid: { borderColor: line },
      plotOptions: {
        ...redialBarChartOptions.plotOptions,
        radialBar: { ...redialBarChartOptions.plotOptions?.radialBar, track: { background: line } }
      },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });
  }, [colorScheme, fontFamily, line, secondaryMain, primaryMain, successDark, errorMain]);

  return <ReactApexChart options={options} series={series} type="radialBar" />;
}
