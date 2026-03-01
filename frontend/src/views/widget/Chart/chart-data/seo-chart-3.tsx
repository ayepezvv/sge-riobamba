import { ApexOptions } from 'apexcharts';

// ==============================|| WIDGET - SEO 3 CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    id: 'product-chart',
    sparkline: { enabled: true },
    background: 'transparent'
  },
  dataLabels: { enabled: false },
  markers: {
    size: 4,
    strokeWidth: 2,
    hover: { size: 6 }
  },
  stroke: {
    curve: 'straight',
    width: 3
  },
  tooltip: {
    fixed: { enabled: false },
    x: { show: false },
    y: { title: { formatter: () => 'Products :' } },
    marker: { show: false }
  }
};

export default chartOptions;
