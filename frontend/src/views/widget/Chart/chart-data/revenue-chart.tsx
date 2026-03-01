import { ApexOptions } from 'apexcharts';

// ==============================|| WIDGET - REVENUE CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    id: 'revenue-chart',
    background: 'transparent'
  },
  dataLabels: { enabled: false },
  labels: ['Youtube', 'Facebook', 'Twitter'],
  legend: {
    show: true,
    position: 'bottom',
    fontFamily: 'inherit',
    labels: { colors: 'inherit' },
    markers: { size: 6, shape: 'circle', strokeWidth: 0 },
    itemMargin: {
      horizontal: 10,
      vertical: 10
    }
  }
};

export default chartOptions;
