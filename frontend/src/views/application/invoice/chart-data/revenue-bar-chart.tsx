import { ApexOptions } from 'apexcharts';

// ==============================|| INVOICE - TOTAL REVENUE BAR CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    id: 'bar-chart',
    stacked: true,
    toolbar: { show: true },
    zoom: { enabled: true },
    background: 'transparent'
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '50%'
    }
  },
  xaxis: {
    type: 'category',
    categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  legend: { show: false },
  fill: {
    type: 'solid',
    opacity: 1
  },
  dataLabels: { enabled: false }
};

export default chartOptions;
