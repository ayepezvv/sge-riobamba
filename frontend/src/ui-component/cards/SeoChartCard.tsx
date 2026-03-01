'use client';

import { ReactNode } from 'react';

// next
import dynamic from 'next/dynamic';

// material-ui
import { Theme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

// third party
import { Props as ChartProps } from 'react-apexcharts';

// project imports
import MainCard from './MainCard';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

// =============================|| SEO CHART CARD ||============================= //

interface SeoChartCardProps {
  chartData: ChartProps;
  value?: string | number;
  title?: string;
  icon?: ReactNode | string;
  type?: number;
  areaOpacity?: number;
}

export default function SeoChartCard({ chartData, value, title, icon, type, areaOpacity }: SeoChartCardProps) {
  const downMM = useMediaQuery((theme: Theme) => theme.breakpoints.down('md'));

  return (
    <MainCard
      content={false}
      sx={(theme) => ({
        p: 2.5,
        '& .apexcharts-tooltip-series-group': {
          color: 'text.primary',
          bgcolor: 'background.paper',
          ...theme.applyStyles('dark', { bgcolor: 'background.default' })
        },
        ...(areaOpacity !== undefined && {
          'path.apexcharts-area[fill-opacity]': {
            fillOpacity: `${areaOpacity} !important`
          }
        })
      })}
    >
      <Stack sx={{ justifyContent: 'space-between', gap: 1.25 }}>
        <Stack direction={type === 1 ? 'column-reverse' : 'column'} sx={{ gap: type === 1 ? 0.5 : 1 }}>
          {value && <Typography variant={downMM ? 'h4' : 'h3'}>{value}</Typography>}
          {(title || icon) && (
            <Stack direction="row" sx={{ gap: 1, alignItems: 'center' }}>
              {title && (
                <Typography variant="body1" sx={{ color: 'grey.500' }}>
                  {title}
                </Typography>
              )}
              {icon && icon}
            </Stack>
          )}
        </Stack>
        {chartData && <Chart {...chartData} />}
      </Stack>
    </MainCard>
  );
}
