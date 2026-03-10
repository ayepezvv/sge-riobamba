import { IconUsers, IconBriefcase, IconAddressBook, IconBuilding } from '@tabler/icons-react';

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
        { id: 'direcciones', title: 'Direcciones', type: 'item', url: '/administrativo/direcciones' },
        { id: 'unidades', title: 'Unidades', type: 'item', url: '/administrativo/unidades' },
        { id: 'personal', title: 'Directorio', type: 'item', url: '/administrativo/personal', icon: IconAddressBook },
        { id: 'puestos', title: 'Puestos', type: 'item', url: '/administrativo/puestos', icon: IconBriefcase }
      ]
    }
  ]
};

export default administrativo;
