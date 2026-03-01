'use client';

import { useEffect, useState } from 'react';

// next
import dynamic from 'next/dynamic';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

// third party
import { ApexOptions } from 'apexcharts';

// project imports
import { ThemeMode } from 'config';
import useConfig from 'hooks/useConfig';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';

// assets
import FiberManualRecordIcon from '@mui/icons-material/FiberManualRecord';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

const series = [
  { name: 'Investment', data: [43, 125, 75, 36, 95, 30, 20, 75, 30, 40, 55, 150] },
  { name: 'Loss', data: [43, 20, 25, 35, 140, 50, 20, 115, 30, 25, 25, 70] },
  { name: 'Maintenance', data: [43, 125, 75, 36, 35, 10, 20, 20, 40, 55, 20, 250] }
];

// chart options
const overviewChartOptions: ApexOptions = {
  chart: {
    id: 'bar-chart',
    stacked: true,
    toolbar: { show: false },
    zoom: { enabled: true },
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
    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  },
  legend: { show: false },
  fill: { type: 'solid' },
  dataLabels: { enabled: false }
};

const widget = [
  {
    name: 'Total Investment',
    number: 586,
    color: 'primary.dark'
  },
  {
    name: 'Total Maintenance',
    number: 256,
    color: 'primary.200'
  },
  {
    name: 'Total Loss',
    number: 256,
    color: 'secondary.light'
  }
];

const options = ['Last 7 Days', 'Last Month', 'Last Year'];

interface SalesChartProps {
  isLoading: boolean;
}

// ==============================|| REFUND OVERVIEW ||============================== //

export default function Overview({ isLoading }: SalesChartProps) {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const {
    state: { fontFamily }
  } = useConfig();

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedIndex, setSelectedIndex] = useState(1);
  const [chartConfig, setChartConfig] = useState(overviewChartOptions);

  const open = Boolean(anchorEl);

  const handleClickListItem = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuItemClick = (_event: React.MouseEvent<HTMLElement>, index: number) => {
    setSelectedIndex(index);
    setAnchorEl(null);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const textPrimary = theme.vars.palette.text.primary;
  const divider = theme.vars.palette.divider;
  const grey500 = theme.vars.palette.grey[500];

  const primary200 = theme.vars.palette.primary[200];
  const primaryDark = theme.vars.palette.primary.dark;
  const secondaryLight = theme.vars.palette.secondary.light;

  useEffect(() => {
    setChartConfig({
      ...overviewChartOptions,
      chart: { ...overviewChartOptions.chart, fontFamily: fontFamily },
      colors: [primaryDark, primary200, secondaryLight],
      xaxis: { ...overviewChartOptions?.xaxis, labels: { style: { colors: textPrimary } } },
      yaxis: { labels: { style: { colors: textPrimary } } },
      grid: { borderColor: divider },
      legend: { ...overviewChartOptions.legend, labels: { colors: grey500 } },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });
  }, [colorScheme, fontFamily, primaryDark, primary200, secondaryLight, textPrimary, divider, grey500]);

  if (isLoading) return null;

  return (
    <MainCard content={false}>
      <CardContent sx={{ p: 2.5 }}>
        <Grid container spacing={1}>
          <Grid size={12}>
            <Grid container sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
              <Grid>
                <Typography variant="h3">Refund Report</Typography>
              </Grid>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', display: { xs: 'none', sm: 'flex' } }}>
                <Button
                  id="demo-positioned-button"
                  aria-controls="demo-positioned-menu"
                  aria-haspopup="true"
                  aria-expanded={open ? 'true' : undefined}
                  onClick={handleClickListItem}
                  sx={{ color: 'grey.500', fontWeight: 400 }}
                  endIcon={<KeyboardArrowDownIcon sx={{ color: 'grey.900' }} />}
                >
                  {options.length > 0 && options[selectedIndex]}
                </Button>
                <Menu
                  id="lock-menu"
                  anchorEl={anchorEl}
                  open={open}
                  onClose={handleClose}
                  slotProps={{ list: { 'aria-labelledby': 'lock-button', role: 'listbox' } }}
                >
                  {options.map((option, index) => (
                    <MenuItem key={option} selected={index === selectedIndex} onClick={(event) => handleMenuItemClick(event, index)}>
                      {option}
                    </MenuItem>
                  ))}
                </Menu>
              </Stack>
            </Grid>
          </Grid>
          <Grid size={{ xs: 12, md: 10 }}>
            <Chart options={chartConfig} series={series} type="bar" height={320} />
          </Grid>
          <Grid size={{ xs: 12, md: 2 }}>
            <Stack sx={{ gap: 2 }}>
              <SubCard sx={{ bgcolor: divider, ...theme.applyStyles('dark', { bgcolor: 'background.default' }) }}>
                <Stack sx={{ textAlign: 'center', gap: 1 }}>
                  <Typography sx={{ fontSize: 16, color: 'text.secondary' }}>Earnings Report</Typography>
                  <Typography variant="h3" sx={{ fontSize: '1.5rem' }}>
                    $586
                  </Typography>
                </Stack>
              </SubCard>
              <Stack sx={{ alignItems: 'center' }}>
                {widget.map((item, index) => (
                  <Stack key={index} sx={{ py: 1.5, width: 130, gap: 1 }} direction="row">
                    <FiberManualRecordIcon key={index} fontSize="small" sx={{ color: item.color }} />
                    <Stack sx={{ gap: 0.5 }}>
                      <Typography variant="h6" sx={{ color: 'grey.500' }}>
                        {item.name}
                      </Typography>
                      <Typography variant="h4" sx={{ color: 'grey.900', fontWeight: 500 }}>
                        ${item.number}
                      </Typography>
                    </Stack>
                  </Stack>
                ))}
              </Stack>
            </Stack>
          </Grid>
        </Grid>
      </CardContent>
    </MainCard>
  );
}
