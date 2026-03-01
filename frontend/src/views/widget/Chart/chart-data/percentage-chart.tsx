import { ApexOptions } from 'apexcharts';

// ==============================|| WIDGET - PERCENTAGE CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    id: 'percentage-chart',
    sparkline: { enabled: true },
    background: 'transparent'
  },
  plotOptions: {
    bar: {
      columnWidth: '55%',
      distributed: true
    }
  },
  dataLabels: { enabled: false },
  stroke: { width: 0 },
  xaxis: { categories: ['Desktop', 'Mobile', 'Tablet', 'Laptop'] }
};

export default chartOptions;
