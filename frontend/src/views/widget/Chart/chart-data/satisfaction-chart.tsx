import { ApexOptions } from 'apexcharts';

// ==============================|| WIDGET - SATISFACTION CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    id: 'satisfaction-chart',
    background: 'transparent'
  },
  labels: ['Extremely Satisfied', 'Satisfied', 'Poor', 'Very Poor'],
  legend: {
    show: true,
    position: 'bottom',
    fontFamily: 'inherit',
    labels: { colors: 'inherit' },
    markers: { size: 6, strokeWidth: 0 }
  },
  dataLabels: {
    enabled: true,
    dropShadow: { enabled: false }
  }
};

export default chartOptions;
