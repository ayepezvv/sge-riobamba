import { ApexOptions } from 'apexcharts';

// ==============================|| WIDGET - SEO 1 CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    id: 'visit-chart',
    sparkline: { enabled: true },
    background: 'transparent'
  },
  dataLabels: { enabled: false },
  fill: { type: 'solid' },
  markers: {
    size: 4,
    strokeWidth: 2,
    hover: { size: 6 }
  },
  stroke: { curve: 'straight', width: 3 },
  tooltip: {
    fixed: { enabled: false },
    x: { show: false },
    y: { title: { formatter: () => 'Visits :' } },
    marker: { show: false }
  }
};

export default chartOptions;
