'use client';

import { MouseEvent, SyntheticEvent, useEffect, useState } from 'react';

// next
import dynamic from 'next/dynamic';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Stack from '@mui/material/Stack';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// project imports
import { ThemeDirection, ThemeMode } from 'config';
import useConfig from 'hooks/useConfig';
import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SkeletonTotalGrowthBarChart from 'ui-component/cards/Skeleton/TotalGrowthBarChart';

// chart data
import barChartOptions from '../chart-data/analytics-bar-charts';

// assets
import MoreHorizOutlinedIcon from '@mui/icons-material/MoreHorizOutlined';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

// ==============================|| ANALYTICS BAR CHART ||============================== //

interface TotalGrowthBarChartProps {
  isLoading: boolean;
}

export default function AnalyticsBarChart({ isLoading }: TotalGrowthBarChartProps) {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();

  const downSM = useMediaQuery(theme.breakpoints.down('sm'));
  const {
    state: { borderRadius, fontFamily, themeDirection }
  } = useConfig();

  const [tabValue, setTabValue] = useState(1);
  const [chartOptions, setChartOptions] = useState(barChartOptions);
  const [series, setSeries] = useState([
    {
      name: 'Blog views',
      data: [0, 0, 0, 0, 6, 7, 10, 18, 10, 12, 0, 14, 11, 7, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 12, 6, 4, 2]
    },
    {
      name: 'None',
      data: [4, 16, 7, 7, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 22, 6, 11, 7, 3, 4, 6, 8, 10, 8, 0, 0, 0, 0, 0]
    }
  ]);

  const textPrimary = theme.vars.palette.text.primary;
  const divider = theme.vars.palette.divider;

  const grey500 = theme.vars.palette.grey[500];
  const primaryMain = theme.vars.palette.primary.main;

  const [anchorEl, setAnchorEl] = useState<Element | (() => Element) | null | undefined>(null);

  const handleClick = (event: MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleChange = (_event: SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    switch (newValue) {
      case 0:
        setSeries([
          {
            name: 'Blog views',
            data: [0, 5, 0, 0, 0, 8, 0, 0, 3, 0, 7, 0, 0, 0, 9, 0, 0, 0, 13, 0, 12, 0, 0, 0, 0, 0, 0, 6, 11, 0]
          },
          {
            name: 'None',
            data: [12, 0, 8, 4, 5, 0, 7, 10, 0, 6, 0, 9, 11, 14, 0, 7, 5, 8, 0, 2, 0, 4, 8, 10, 6, 5, 9, 0, 0, 3]
          }
        ]);
        break;
      case 1:
        setSeries([
          {
            name: 'Blog views',
            data: [0, 0, 0, 0, 6, 7, 10, 18, 10, 12, 0, 14, 11, 7, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 12, 6, 4, 2]
          },
          {
            name: 'None',
            data: [4, 16, 7, 7, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 22, 6, 11, 7, 3, 4, 6, 8, 10, 8, 0, 0, 0, 0, 0]
          }
        ]);
        break;
      case 2:
      default:
        setSeries([
          {
            name: 'Blog views',
            data: [8, 0, 7, 9, 0, 3, 0, 7, 0, 15, 15, 12, 7, 0, 6, 8, 0, 7, 4, 0, 10, 13, 0, 8, 6, 9, 0, 2, 7, 0]
          },
          {
            name: 'None',
            data: [0, 12, 0, 0, 6, 0, 10, 0, 9, 0, 0, 0, 0, 11, 0, 0, 10, 0, 0, 7, 0, 0, 12, 0, 0, 0, 14, 0, 0, 5]
          }
        ]);
        break;
    }
  };

  useEffect(() => {
    setChartOptions({
      ...barChartOptions,
      chart: { ...barChartOptions.chart, fontFamily: fontFamily },
      colors: [primaryMain, divider],
      xaxis: { ...barChartOptions.xaxis, labels: { style: { colors: textPrimary } } },
      yaxis: { labels: { style: { colors: textPrimary }, offsetX: -10 } },
      legend: { ...barChartOptions.legend, labels: { colors: grey500 } },
      theme: { mode: colorScheme === ThemeMode.DARK ? 'dark' : 'light' }
    });
  }, [colorScheme, fontFamily, textPrimary, divider, primaryMain, grey500]);

  if (isLoading) return <SkeletonTotalGrowthBarChart />;

  return (
    <MainCard
      title="Analytics Summary"
      secondary={
        <IconButton size="small" onClick={handleClick}>
          <MoreHorizOutlinedIcon fontSize="small" sx={{ opacity: 0.6 }} aria-controls="menu-popular-card" aria-haspopup="true" />
        </IconButton>
      }
      contentSX={{ '&:last-child': { pb: 0 } }}
    >
      <Stack sx={{ gap: 3 }}>
        <SubCard
          content={false}
          sx={{ border: 'none', p: 1.25, bgcolor: 'grey.100', ...theme.applyStyles('dark', { bgcolor: 'background.default' }) }}
        >
          <Box sx={{ width: '100%' }}>
            <Tabs
              value={tabValue}
              variant={downSM ? 'scrollable' : 'fullWidth'}
              onChange={handleChange}
              slotProps={{ indicator: { sx: { display: 'none' } } }}
              sx={{
                '& .MuiTab-root': {
                  width: 1,
                  maxWidth: 1,
                  borderBottom: 'none',
                  border: 1,
                  borderColor: 'grey.200',
                  minHeight: 'auto',
                  minWidth: 10,
                  py: 1.5,
                  px: 1,
                  color: 'grey.900',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'flex-start',
                  justifyContent: 'center',
                  borderRadius: `${borderRadius}px`,
                  bgcolor: 'common.white',
                  '&.Mui-selected': {
                    color: 'common.white',
                    bgcolor: theme.vars.palette.primary.main,
                    '& .MuiTypography-root': {
                      color: 'common.white'
                    }
                  }
                },
                '& .MuiTabs-flexContainer': {
                  justifyContent: 'space-between',
                  gap: 1.5,
                  borderBottom: 'none',
                  flexDirection: { xs: 'column', sm: 'row' }
                },

                ...theme.applyStyles('dark', { '& .MuiTab-root': { borderColor: 'divider', color: 'grey.600', bgcolor: 'dark.main' } })
              }}
            >
              <Tab
                label={
                  <Stack sx={{ gap: 0.5, alignItems: 'flex-start', p: { xs: 1.5, md: 2 } }}>
                    <Typography variant="h2" sx={{ fontWeight: 900, color: 'inherit' }}>
                      50
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Views (7 days)
                    </Typography>
                  </Stack>
                }
              />
              <Tab
                label={
                  <Stack sx={{ gap: 0.5, alignItems: 'flex-start', p: { xs: 1.5, md: 2 } }}>
                    <Typography variant="h2" sx={{ fontWeight: 900, color: 'inherit' }}>
                      1230
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Views (30 days)
                    </Typography>
                  </Stack>
                }
              />
              <Tab
                label={
                  <Stack sx={{ gap: 0.5, alignItems: 'flex-start', p: { xs: 1.5, md: 2 } }}>
                    <Typography variant="h2" sx={{ fontWeight: 900, color: 'inherit' }}>
                      20,987
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Views (All time)
                    </Typography>
                  </Stack>
                }
              />
            </Tabs>
          </Box>
        </SubCard>
        <Box sx={{ '& .apexcharts-legend-text': { pl: themeDirection === ThemeDirection.RTL ? 0 : 1 } }}>
          <Chart options={chartOptions} series={series} height={downSM ? 300 : 346} type="bar" />
        </Box>
      </Stack>
      <Menu
        id="menu-popular-card"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
        variant="selectedMenu"
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right'
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right'
        }}
      >
        <MenuItem onClick={handleClose}>Today</MenuItem>
        <MenuItem onClick={handleClose}>This Month</MenuItem>
        <MenuItem onClick={handleClose}>This Year </MenuItem>
      </Menu>
    </MainCard>
  );
}
