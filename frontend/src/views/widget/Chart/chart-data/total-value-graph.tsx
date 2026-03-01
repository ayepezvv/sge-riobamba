import { ApexOptions } from 'apexcharts';

// ==============================|| WIDGET - TOTAL GRAPH VALUE CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    sparkline: { enabled: true },
    background: 'transparent'
  },
  dataLabels: { enabled: false },
  colors: ['#fff'],
  fill: {
    type: 'solid',
    opacity: 0.4
  },
  stroke: { curve: 'smooth', width: 3 },
  yaxis: { min: 0, max: 30, labels: { show: false } },
  tooltip: {
    fixed: { enabled: false },
    x: { show: false },
    marker: { show: false }
  }
};

export default chartOptions;
