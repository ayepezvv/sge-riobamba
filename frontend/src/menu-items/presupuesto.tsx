import {
  IconReportMoney,
  IconFileText,
  IconCertificate,
  IconClipboardList,
  IconChartBar,
} from '@tabler/icons-react';

const presupuesto = {
  id: 'presupuesto',
  title: 'Presupuesto',
  type: 'group',
  children: [
    {
      id: 'modulo-presupuesto',
      title: 'Módulo Presupuesto',
      type: 'collapse',
      icon: IconReportMoney,
      children: [
        {
          id: 'partidas-presupuestarias',
          title: 'Partidas Presupuestarias',
          type: 'item',
          url: '/presupuesto/partidas',
          icon: IconFileText,
        },
        {
          id: 'presupuestos-anuales',
          title: 'Presupuestos Anuales',
          type: 'item',
          url: '/presupuesto/presupuestos',
          icon: IconClipboardList,
        },
        {
          id: 'certificados-presupuestarios',
          title: 'Certificados Presupuestarios',
          type: 'item',
          url: '/presupuesto/certificados',
          icon: IconCertificate,
        },
        {
          id: 'compromisos-devengados',
          title: 'Compromisos y Devengados',
          type: 'item',
          url: '/presupuesto/compromisos',
          icon: IconClipboardList,
        },
        {
          id: 'ejecucion-presupuestaria',
          title: 'Ejecución Presupuestaria',
          type: 'item',
          url: '/presupuesto/ejecucion',
          icon: IconChartBar,
        },
      ],
    },
  ],
};

export default presupuesto;
