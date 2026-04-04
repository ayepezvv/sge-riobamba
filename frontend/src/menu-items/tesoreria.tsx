import {
  IconBuildingBank,
  IconCreditCard,
  IconFileText,
  IconChecklist,
  IconCash,
} from '@tabler/icons-react';

const tesoreria = {
  id: 'tesoreria',
  title: 'Tesorería',
  type: 'group',
  children: [
    {
      id: 'modulo-tesoreria',
      title: 'Módulo Tesorería',
      type: 'collapse',
      icon: IconBuildingBank,
      children: [
        {
          id: 'cuentas-bancarias',
          title: 'Cuentas Bancarias',
          type: 'item',
          url: '/tesoreria/cuentas-bancarias',
          icon: IconCreditCard,
        },
        {
          id: 'extractos-bancarios',
          title: 'Extractos Bancarios',
          type: 'item',
          url: '/tesoreria/extractos',
          icon: IconFileText,
        },
        {
          id: 'conciliacion-bancaria',
          title: 'Conciliación Bancaria',
          type: 'item',
          url: '/tesoreria/conciliaciones',
          icon: IconChecklist,
        },
        {
          id: 'caja-chica',
          title: 'Caja Chica',
          type: 'item',
          url: '/tesoreria/caja',
          icon: IconCash,
        },
      ],
    },
  ],
};

export default tesoreria;
