import { IconUsers, IconBriefcase, IconAddressBook, IconDashboard, IconReceipt2 } from '@tabler/icons-react';

const administrativo = {
  id: 'administracion',
  title: 'Administración',
  type: 'group',
  children: [
    {
      id: 'talento-humano',
      title: 'Talento Humano',
      type: 'collapse',
      icon: IconUsers,
      children: [
        { id: 'dashboard-rrhh', title: 'Dashboard RRHH', type: 'item', url: '/administrativo/dashboard', icon: IconDashboard },
        { id: 'direcciones', title: 'Direcciones', type: 'item', url: '/administrativo/direcciones' },
        { id: 'unidades', title: 'Unidades', type: 'item', url: '/administrativo/unidades' },
        { id: 'personal', title: 'Gestor de Personal', type: 'item', url: '/administrativo/personal', icon: IconAddressBook },
        { id: 'puestos', title: 'Puestos', type: 'item', url: '/administrativo/puestos', icon: IconBriefcase },
        { id: 'nomina', title: 'Generador de Nómina', type: 'item', url: '/administrativo/nomina', icon: IconReceipt2 }
      ]
    }
  ]
};

export default administrativo;
