import { ApexOptions } from 'apexcharts';

// ==============================|| WIDGET - SEO 2 CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    id: 'bounce-bar-chart',
    sparkline: { enabled: true },
    background: 'transparent'
  },
  dataLabels: { enabled: false },
  plotOptions: { bar: { columnWidth: '60%' } },
  xaxis: { crosshairs: { width: 1 } },
  tooltip: {
    fixed: { enabled: false },
    x: { show: false },
    y: { title: { formatter: () => 'Bounce Rate :' } },
    marker: { show: false }
  }
};

export default chartOptions;
