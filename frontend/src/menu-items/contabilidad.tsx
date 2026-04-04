import {
  IconCalculator,
  IconBook,
  IconFileAnalytics,
  IconScale,
  IconClipboardList,
} from '@tabler/icons-react';

const contabilidad = {
  id: 'contabilidad',
  title: 'Contabilidad',
  type: 'group',
  children: [
    {
      id: 'modulo-contabilidad',
      title: 'Módulo Contabilidad',
      type: 'collapse',
      icon: IconCalculator,
      children: [
        {
          id: 'plan-de-cuentas',
          title: 'Plan de Cuentas',
          type: 'item',
          url: '/contabilidad/plan-cuentas',
          icon: IconBook,
        },
        {
          id: 'asientos-contables',
          title: 'Asientos Contables',
          type: 'item',
          url: '/contabilidad/asientos',
          icon: IconClipboardList,
        },
        {
          id: 'mayor-general',
          title: 'Mayor General',
          type: 'item',
          url: '/contabilidad/mayor-general',
          icon: IconFileAnalytics,
        },
        {
          id: 'balances',
          title: 'Balances',
          type: 'item',
          url: '/contabilidad/balances',
          icon: IconScale,
        },
      ],
    },
  ],
};

export default contabilidad;
