import { ApexOptions } from 'apexcharts';

// ==============================|| WIDGET - MARKET SHARE CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    id: 'market-sale-chart',
    toolbar: { show: false },
    zoom: { enabled: false },
    sparkline: { enabled: true },
    background: 'transparent'
  },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 2 },
  legend: { show: false },
  yaxis: {
    min: 1,
    max: 100,
    labels: { show: false }
  }
};

export default chartOptions;
