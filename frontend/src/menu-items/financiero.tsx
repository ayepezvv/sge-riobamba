import {
  IconCoins,
  IconReceipt2,
  IconTransfer,
  IconBuildingStore,
} from '@tabler/icons-react';

const financiero = {
  id: 'financiero',
  title: 'Financiero',
  type: 'group',
  children: [
    {
      id: 'modulo-financiero',
      title: 'Módulo Financiero',
      type: 'collapse',
      icon: IconCoins,
      children: [
        {
          id: 'facturas',
          title: 'Facturas (AR/AP)',
          type: 'item',
          url: '/financiero/facturas',
          icon: IconReceipt2,
        },
        {
          id: 'pagos-cobros',
          title: 'Pagos y Cobros',
          type: 'item',
          url: '/financiero/pagos',
          icon: IconTransfer,
        },
        {
          id: 'cierres-recaudacion',
          title: 'Cierres de Recaudación',
          type: 'item',
          url: '/financiero/cierres-recaudacion',
          icon: IconBuildingStore,
        },
      ],
    },
  ],
};

export default financiero;
