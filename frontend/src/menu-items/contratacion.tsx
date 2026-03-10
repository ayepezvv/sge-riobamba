import { IconFileInvoice, IconReportMoney, IconSearch } from '@tabler/icons-react';

const contratacion = {
  id: 'contratacion',
  title: 'Compras Públicas',
  type: 'group',
  children: [
    {
      id: 'planificacion',
      title: 'Planificación',
      type: 'collapse',
      icon: IconReportMoney,
      children: [
                { id: 'pac', title: 'Plan Anual (PAC)', type: 'item', url: '/contratacion/pac' },
        { id: 'pac_explorador', title: 'Explorador de Ítems', type: 'item', url: '/contratacion/pac/explorador', icon: IconSearch }
      ]
    },
    {
      id: 'ejecucion',
      title: 'Ejecución',
      type: 'collapse',
      icon: IconFileInvoice,
      children: [
        { id: 'procesos', title: 'Mis Procesos', type: 'item', url: '/contratacion/procesos' }
      ]
    }
  ]
};

export default contratacion;
