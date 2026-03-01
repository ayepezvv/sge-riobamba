'use client';

import { ReactNode, useEffect, useState } from 'react';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';
import Grid from '@mui/material/Grid';

// third party
import { ApexOptions } from 'apexcharts';

// project imports
import MarketSaleChartCard from './MarketSaleChartCard';
import RevenueChartCard from './RevenueChartCard';
import ConversionsChartCard from './ConversionsChartCard';
import SatisfactionChartCard from './SatisfactionChartCard';

import { ThemeMode } from 'config';
import useConfig from 'hooks/useConfig';
import TotalLineChartCard from 'ui-component/cards/TotalLineChartCard';
import SeoChartCard from 'ui-component/cards/SeoChartCard';
import SalesLineChartCard from 'ui-component/cards/SalesLineChartCard';
import AnalyticsChartCard from 'ui-component/cards/AnalyticsChartCard';
import { gridSpacing } from 'store/constant';

// chart data
import chartData from './chart-data';

// assets
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ArrowDropUpIcon from '@mui/icons-material/ArrowDropUp';
import ImportantDevicesIcon from '@mui/icons-material/ImportantDevices';
import PhonelinkLockIcon from '@mui/icons-material/PhonelinkLock';
import TabletAndroidIcon from '@mui/icons-material/TabletAndroid';
import LaptopIcon from '@mui/icons-material/Laptop';

const totalValueChartsData = [
  {
    id: 'total-sales',
    percentage: 42,
    value: 4000,
    series: [{ data: [20, 10, 18, 12, 25, 10, 20] }],
    title: 'Total Sales',
    bgcolor: 'primary.dark'
  },
  {
    id: 'total-comment',
    percentage: 15,
    value: 2500,
    series: [{ data: [20, 10, 18, 12, 25, 10, 20] }],
    title: 'Total Comment',
    bgcolor: 'error.main'
  },
  {
    id: 'total-status',
    percentage: 95,
    value: 2500,
    series: [{ data: [20, 10, 18, 12, 25, 10, 20] }],
    title: 'Total Status',
    bgcolor: 'success.dark'
  },
  {
    id: 'total-visitors',
    percentage: 75,
    value: 12500,
    series: [{ data: [20, 10, 18, 12, 25, 10, 20] }],
    title: 'Total Visitors',
    bgcolor: 'secondary.main'
  }
];

const seoChartsData = [
  { id: 'users', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '798', title: 'Users' },
  { id: 'timeout', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '486', title: 'Timeout' },
  { id: 'pending', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '9,454', title: 'Views' },
  { id: 'overdue', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '7.15', title: 'Session' },
  { id: 'avg-session', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '04:30', title: 'Avg. Session' },
  { id: 'bounce-rate', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '1.55%', title: 'Bounce Rate' }
];

const sellsLineChartsData = [
  {
    id: 'sales-per-day',
    series: [{ data: [55, 35, 75, 25, 90, 50] }],
    title: 'Sales Per Day',
    percentage: 3,
    bgcolor: 'error.main',
    icon: <TrendingDownIcon />,
    footerData: [
      { value: '$4230', label: 'Total Revenue' },
      { value: '321', label: 'Today Sales' }
    ]
  },
  {
    id: 'order-per-month',
    series: [{ data: [55, 35, 75, 25, 90, 50] }],
    title: 'Order Per Month',
    percentage: 28,
    icon: <TrendingDownIcon />,
    footerData: [
      { value: '1695', label: 'Total Orders' },
      { value: '321', label: 'Today Orders' }
    ]
  }
];

const analyticsSeries = [{ name: 'Requests', data: [66.6, 29.7, 32.8, 50] }];
const marketShareSeries = [
  { name: 'Facebook', data: [50, 30, 25, 15, 60, 10, 25] },
  { name: 'Twitter', data: [5, 50, 40, 55, 20, 40, 20] },
  { name: 'Youtube', data: [10, 90, 65, 85, 40, 80, 30] }
];
const seoChartSeries1 = [{ data: [9, 66, 41, 89, 63, 25, 44, 12, 36, 20, 54, 25, 9] }];
const seoChartSeries2 = [{ data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54, 25, 66, 41, 89, 63] }];
const seoChartSeries3 = [{ data: [9, 66, 41, 89, 63, 25, 44, 12, 36, 20, 54, 25, 9] }];
const conversionsChartSeries = [
  { data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54, 25, 66, 41, 89, 63, 54, 25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54] }
];
const satisfactionChartSeries = [66, 50, 40, 30];

type FooterDataItem = {
  value: string;
  label: string;
};

// ================================|| CHART ||================================ //

export default function Chart() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { fontFamily }
  } = useConfig();

  const [chartOptions, setChartOptions] = useState<
    { id: string; percentage: number; options: ApexOptions; value: number; title: string; series: ApexOptions['series']; bgcolor: string }[]
  >([]);

  const [marketChartOptions, setMarketChartOptions] = useState(chartData.MarketChartCardData);
  const [revenueChartOptions, setRevenueChartOptions] = useState(chartData.RevenueChartCardData);

  const [seoChartOptions, setSeoChartOptions] = useState<
    { id: string; options: ApexOptions; value: string; title: string; series: ApexOptions['series'] }[]
  >([]);

  const [sellsChartOptions, setSellsChartOptions] = useState<
    {
      id: string;
      percentage: number;
      options: ApexOptions;
      title: string;
      series: ApexOptions['series'];
      bgcolor?: string;
      icon: ReactNode;
      footerData: FooterDataItem[];
    }[]
  >([]);

  const [analyticsChartOptions, setAnalyticsChartOptions] = useState(chartData.AnalyticsChartCardData);
  const [seoChart1Options, setSeoChart1Options] = useState(chartData.SeoChartCardData1);
  const [seoChart2Options, setSeoChart2Options] = useState(chartData.SeoChartCardData2);
  const [seoChart3Options, setSeoChart3Options] = useState(chartData.SeoChartCardData3);
  const [conversionsChartOptions, setConversionsChartOptions] = useState(chartData.ConversionsChartCardData);
  const [satisfactionChartOptions, setSatisfactionChartOptions] = useState(chartData.SatisfactionChartCardData);

  const backColor = theme.vars.palette.background.paper;
  const primaryMain = theme.vars.palette.primary.main;
  const secondaryMain = theme.vars.palette.secondary.main;
  const errorMain = theme.vars.palette.error.main;
  const primaryDark = theme.vars.palette.primary.dark;
  const orangeMain = theme.vars.palette.orange.main;
  const orangeDark = theme.vars.palette.orange.dark;
  const successDark = theme.vars.palette.success.dark;
  const backgroundPaper = theme.vars.palette.background.paper;

  const colors: Record<string, string> = {
    users: orangeMain,
    timeout: secondaryMain,
    pending: errorMain,
    overdue: secondaryMain,
    'avg-session': primaryMain,
    'bounce-rate': successDark
  };

  useEffect(() => {
    const totalValueOptions: ApexOptions = {
      ...chartData.totalValueChartOptions,
      chart: { ...chartData.totalValueChartOptions.chart, fontFamily: fontFamily },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    };

    const data = totalValueChartsData.map((item) => ({
      ...item,
      options: { ...totalValueOptions, tooltip: { ...totalValueOptions.tooltip, y: { title: { formatter: () => item.title } } } }
    }));

    setChartOptions(data);

    setMarketChartOptions({
      ...chartData.MarketChartCardData,
      chart: { ...chartData.MarketChartCardData.chart, fontFamily: fontFamily },
      colors: [secondaryMain, primaryDark, errorMain],
      fill: {
        gradient: {
          colorStops: [
            [
              { offset: 0, color: secondaryMain, opacity: 0.2 },
              { offset: 100, color: backgroundPaper, opacity: 0 }
            ],
            [
              { offset: 0, color: primaryDark, opacity: 0.2 },
              { offset: 100, color: backgroundPaper, opacity: 0 }
            ],
            [
              { offset: 0, color: errorMain, opacity: 0.2 },
              { offset: 100, color: backgroundPaper, opacity: 0 }
            ]
          ]
        }
      },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });

    setRevenueChartOptions({
      ...chartData.RevenueChartCardData,
      chart: { ...chartData.RevenueChartCardData.chart, fontFamily: fontFamily },
      colors: [errorMain, primaryMain, secondaryMain],
      stroke: { colors: [backColor] },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });

    const seoOptions: ApexOptions = {
      ...chartData.seoChartOptions,
      chart: { ...chartData.seoChartOptions.chart, fontFamily: fontFamily },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    };

    const seoData = seoChartsData.map((item) => ({
      ...item,
      options: {
        ...seoOptions,
        colors: [colors[item.id]],
        tooltip: { ...seoOptions.tooltip, y: { title: { formatter: () => item.title } } }
      }
    }));

    setSeoChartOptions(seoData);

    const sellsOptions: ApexOptions = {
      ...chartData.sellsLineChartOptions,
      chart: { ...chartData.sellsLineChartOptions.chart, fontFamily: fontFamily },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    };

    const sellsData = sellsLineChartsData.map((item) => ({
      ...item,
      options: {
        ...sellsOptions,
        colors: [colors[item.id]],
        tooltip: { ...sellsOptions.tooltip, y: { title: { formatter: () => item.title } } }
      }
    }));

    setSellsChartOptions(sellsData);

    setAnalyticsChartOptions({
      ...chartData.AnalyticsChartCardData,
      chart: { ...chartData.AnalyticsChartCardData.chart, fontFamily: fontFamily },
      colors: [primaryMain, successDark, errorMain, orangeDark],
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });

    setSeoChart1Options({
      ...chartData.SeoChartCardData1,
      chart: { ...chartData.SeoChartCardData1.chart, fontFamily: fontFamily },
      colors: [primaryMain],
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });

    setSeoChart2Options({
      ...chartData.SeoChartCardData2,
      chart: { ...chartData.SeoChartCardData2.chart, fontFamily: fontFamily },
      colors: [successDark],
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });

    setSeoChart3Options({
      ...chartData.SeoChartCardData3,
      chart: { ...chartData.SeoChartCardData3.chart, fontFamily: fontFamily },
      colors: [errorMain],
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });

    setConversionsChartOptions({
      ...chartData.ConversionsChartCardData,
      chart: { ...chartData.ConversionsChartCardData.chart, fontFamily: fontFamily },
      colors: [secondaryMain],
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });

    setSatisfactionChartOptions({
      ...chartData.SatisfactionChartCardData,
      chart: { ...chartData.SatisfactionChartCardData.chart, fontFamily: fontFamily },
      stroke: { colors: [backColor] },
      theme: { monochrome: { enabled: true, color: theme.palette.orange.dark } }
    });

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [colorScheme, fontFamily]);

  const [isLoading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false);
  }, []);

  useEffect(() => {
    const styleElement = document.createElement('style');
    styleElement.innerHTML = `
            .apexcharts-tooltip {
                color: ${colorScheme === ThemeMode.DARK ? theme.vars.palette.common.white : theme.vars.palette.common.black} !important;
                background-color: ${theme.vars.palette.background.paper} !important;
            }
        `;
    document.head.appendChild(styleElement);

    return () => {
      document.head.removeChild(styleElement);
    };
  }, [colorScheme, theme.vars]);

  if (isLoading) return null;

  return (
    <Grid container spacing={gridSpacing} sx={{ alignItems: 'center' }}>
      {chartOptions.map((item, index) => (
        <Grid key={index} size={{ xs: 12, sm: 6, lg: 3 }}>
          <TotalLineChartCard
            chartData={{ options: item.options, series: item.series, type: 'area', height: 100, style: { marginBottom: '-2px' } }}
            value={item.value}
            title={item.title}
            percentage={`${item.percentage}%`}
            bgColor={item.bgcolor}
          />
        </Grid>
      ))}

      <Grid size={{ xs: 12, md: 6, lg: 7 }}>
        <MarketSaleChartCard chartData={{ options: marketChartOptions, series: marketShareSeries, type: 'area', height: 200 }} />
      </Grid>

      <Grid size={{ xs: 12, md: 6, lg: 5 }}>
        <RevenueChartCard chartData={{ options: revenueChartOptions, series: [1258, 975, 500], type: 'donut', height: 200 }} />
      </Grid>

      {seoChartOptions.map((item, index) => (
        <Grid key={index} size={{ xs: 12, sm: 6, md: 4, lg: 2 }}>
          <SeoChartCard
            type={1}
            chartData={{ options: item.options, series: item.series, type: 'line', height: 30 }}
            value={item.value}
            title={item.title}
          />
        </Grid>
      ))}

      {sellsChartOptions.map((item, index) => (
        <Grid key={index} size={{ xs: 12, sm: 6, lg: 4 }}>
          <SalesLineChartCard
            chartData={{ options: item.options, series: item.series, type: 'line', height: 115 }}
            bgColor={item.bgcolor}
            title={item.title}
            percentage={`${item.percentage}%`}
            icon={item.icon}
            footerData={item.footerData}
          />
        </Grid>
      ))}

      <Grid size={{ xs: 12, sm: 12, lg: 4 }}>
        <AnalyticsChartCard
          chartData={{ options: analyticsChartOptions, series: analyticsSeries, type: 'bar', height: 224 }}
          title="Page view by device"
          dropData={{
            title: 'Weekly',
            options: [
              { value: 1, label: '1 Week' },
              { value: 104, label: '2 Years' },
              { value: 12, label: '3 Monthes' }
            ]
          }}
          listData={[
            {
              color: theme.vars.palette.primary.main,
              icon: <ImportantDevicesIcon color="inherit" fontSize="small" />,
              value: 66.6,
              percentage: 2,
              state: 1
            },
            {
              color: theme.vars.palette.success.dark,
              icon: <PhonelinkLockIcon color="inherit" fontSize="small" />,
              value: 29.7,
              percentage: 3,
              state: 1
            },
            {
              color: theme.vars.palette.error.main,
              icon: <TabletAndroidIcon color="inherit" fontSize="small" />,
              value: 32.8,
              percentage: 8,
              state: 0
            },
            {
              color: theme.vars.palette.orange.dark,
              icon: <LaptopIcon color="inherit" fontSize="small" />,
              value: 50.2,
              percentage: 5,
              state: 1
            }
          ]}
        />
      </Grid>
      <Grid size={{ xs: 12, sm: 6, lg: 4 }}>
        <SeoChartCard
          chartData={{ options: seoChart1Options, series: seoChartSeries1, type: 'area', height: 40 }}
          value="$16,756"
          title="Visits"
          icon={<ArrowDropDownIcon color="error" />}
          areaOpacity={0.3}
        />
      </Grid>
      <Grid size={{ xs: 12, sm: 6, lg: 4 }}>
        <SeoChartCard
          chartData={{ options: seoChart2Options, series: seoChartSeries2, type: 'bar', height: 40 }}
          value="49.54%"
          title="Bounce Rate"
          icon={<ArrowDropUpIcon color="primary" />}
        />
      </Grid>
      <Grid size={{ xs: 12, sm: 12, lg: 4 }}>
        <SeoChartCard
          chartData={{ options: seoChart3Options, series: seoChartSeries3, type: 'line', height: 40 }}
          value="1,62,564"
          title="Products"
          icon={<ArrowDropDownIcon color="error" />}
        />
      </Grid>
      <Grid size={{ xs: 12, md: 6, lg: 6 }}>
        <ConversionsChartCard chartData={{ options: conversionsChartOptions, series: conversionsChartSeries, type: 'bar', height: 260 }} />
      </Grid>
      <Grid size={{ xs: 12, md: 6, lg: 6 }}>
        <SatisfactionChartCard
          chartData={{ options: satisfactionChartOptions, series: satisfactionChartSeries, type: 'pie', height: 280 }}
        />
      </Grid>
    </Grid>
  );
}
