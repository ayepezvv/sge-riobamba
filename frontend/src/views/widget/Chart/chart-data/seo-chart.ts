import { ApexOptions } from 'apexcharts';

// ==============================|| WIDGET - SEO CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    sparkline: { enabled: true },
    background: 'transparent'
  },
  dataLabels: { enabled: false },
  stroke: { curve: 'straight', width: 2 },
  yaxis: {
    min: -2,
    max: 5,
    labels: { show: false }
  },
  tooltip: {
    fixed: { enabled: false },
    x: { show: false },
    marker: { show: false }
  }
};

export default chartOptions;
