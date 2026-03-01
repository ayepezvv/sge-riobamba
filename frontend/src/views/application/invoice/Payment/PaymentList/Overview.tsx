'use client';

import { useEffect, useState } from 'react';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';

// third party
import { ApexOptions } from 'apexcharts';

// project imports
import { ThemeMode } from 'config';
import invoiceLineChartOption from '../../chart-data/invoice-line-chart';
import useConfig from 'hooks/useConfig';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';
import SeoChartCard from 'ui-component/cards/SeoChartCard';

const chartsData = [
  { id: 'total-invoice', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '180', title: 'Total Invoice' },
  { id: 'paid', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '25,890', title: 'Paid' },
  { id: 'pending', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '3400', title: 'Pending' },
  { id: 'overdue', series: [{ data: [2, 1, 2, 1, 1, 3, 0] }], value: '55,865', title: 'Overdue' }
];

// ==============================|| PAYMENT LIST - OVERVIEW ||============================== //

export default function Overview() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { fontFamily }
  } = useConfig();

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
      'total-invoice': theme.vars.palette.grey[500],
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

  return (
    <MainCard>
      <Grid container spacing={2.5} sx={{ alignItems: 'center' }}>
        <Grid size={12}>
          <Typography variant="h4">Overview</Typography>
        </Grid>
        {chartOptions.map((item, index) => (
          <Grid key={index} size={{ xs: 12, sm: 6, md: 3 }}>
            <SubCard content={false}>
              <SeoChartCard
                type={1}
                chartData={{ options: item.options, series: item.series, type: 'line', height: 30 }}
                value={item.value}
                title={item.title}
              />
            </SubCard>
          </Grid>
        ))}
      </Grid>
    </MainCard>
  );
}
