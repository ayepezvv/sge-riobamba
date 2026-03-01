import { ApexOptions } from 'apexcharts';

// ==============================|| WIDGET - CONVERSION CHART ||============================== //

const chartOptions: ApexOptions = {
  chart: {
    id: 'new-stack-chart',
    sparkline: { enabled: true },
    background: 'transparent'
  },
  dataLabels: { enabled: false },
  plotOptions: { bar: { columnWidth: '80%' } },
  xaxis: { crosshairs: { width: 1 } },
  tooltip: {
    fixed: { enabled: false },
    x: { show: false },
    y: { title: { formatter: () => 'Stock - ' } },
    marker: { show: false }
  }
};

export default chartOptions;
