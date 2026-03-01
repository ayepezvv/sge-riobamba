'use client';

import { useEffect, useState } from 'react';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';
import Grid from '@mui/material/Grid';

// project imports
import useConfig from 'hooks/useConfig';
import QuickAdd from './QuickAdd';
import SeoChartCard from 'ui-component/cards/SeoChartCard';
import { gridSpacing } from 'store/constant';

// third party
import { ApexOptions } from 'apexcharts';

// chart data
import invoiceLineChartOption from '../chart-data/invoice-line-chart';
import RevenueBarChart from './RevenueBarChart';
import ClientInsights from './ClientInsights';
import RecentActivity from './RecentActivity';
import SupportHelp from './SupportHelp';
import { ThemeMode } from 'config';

const chartsData = [
  { id: 'new', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '180', title: 'New' },
  { id: 'paid', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '25,890', title: 'Paid' },
  { id: 'pending', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '3400', title: 'Pending' },
  { id: 'overdue', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '55,865', title: 'Overdue' }
];

// ==============================|| INVOICE DASHBOARD PAGE ||============================== //

export default function InvoiceDashBoard() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { fontFamily }
  } = useConfig();

  const [isLoading, setLoading] = useState(true);
  const [chartOptions, setChartOptions] = useState<
    { id: string; options: ApexOptions; value: string; title: string; series: ApexOptions['series'] }[]
  >([]);

  useEffect(() => {
    const options: ApexOptions = {
      ...invoiceLineChartOption,
      chart: { ...invoiceLineChartOption.chart, fontFamily: fontFamily },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    };

    const colors: Record<string, string> = {
      new: theme.vars.palette.grey[500],
      paid: theme.vars.palette.success.dark,
      pending: theme.vars.palette.secondary.main,
      overdue: theme.vars.palette.orange.main
    };

    const data = chartsData.map((item) => ({
      ...item,
      options: { ...options, colors: [colors[item.id]], tooltip: { ...options.tooltip, y: { title: { formatter: () => item.title } } } }
    }));

    setChartOptions(data);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [colorScheme, fontFamily]);

  useEffect(() => {
    setLoading(false);
  }, []);

  return (
    <Grid container spacing={gridSpacing} sx={{ alignItems: 'center' }}>
      <Grid size={12}>
        <QuickAdd />
      </Grid>
      {chartOptions.map((item, index) => (
        <Grid key={index} size={{ xs: 12, sm: 6, md: 4, lg: 3 }}>
          <SeoChartCard
            type={1}
            chartData={{ options: item.options, series: item.series, type: 'line', height: 30 }}
            value={item.value}
            title={item.title}
          />
        </Grid>
      ))}
      <Grid size={12}>
        <Grid container spacing={gridSpacing}>
          <Grid size={{ xs: 12, md: 8 }}>
            <RevenueBarChart isLoading={isLoading} />
          </Grid>
          <Grid size={{ xs: 12, md: 4 }}>
            <ClientInsights isLoading={isLoading} />
          </Grid>
        </Grid>
      </Grid>
      <Grid size={12}>
        <Grid container spacing={gridSpacing}>
          <Grid size={{ xs: 12, md: 7 }}>
            <RecentActivity isLoading={isLoading} />
          </Grid>
          <Grid size={{ xs: 12, md: 5 }}>
            <SupportHelp isLoading={isLoading} />
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
}
