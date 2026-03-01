import { ApexOptions } from 'apexcharts';

// ==============================|| WIDGET - SALE CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    sparkline: { enabled: true },
    background: 'transparent'
  },
  dataLabels: { enabled: false },
  colors: ['#fff'],
  markers: { colors: '#fff' },
  stroke: { curve: 'smooth', width: 3 },
  yaxis: { min: 20, max: 100, labels: { show: false } },
  tooltip: {
    fixed: { enabled: false },
    x: { show: false },
    marker: { show: false }
  }
};

export default chartOptions;
