import { IconUsers, IconAddressBook, IconBuildingArch } from '@tabler/icons-react';

const rrhh = {
  id: 'rrhh',
  title: 'Talento Humano V3',
  type: 'group',
  children: [
    {
      id: 'rrhh-collapse',
      title: 'RRHH',
      type: 'collapse',
      icon: IconUsers,
      children: [
        {
          id: 'rrhh-personal',
          title: 'Directorio de Personal',
          type: 'item',
          url: '/rrhh/personal',
          icon: IconAddressBook,
        },
        {
          id: 'rrhh-areas',
          title: 'Áreas Organizacionales',
          type: 'item',
          url: '/rrhh/areas',
          icon: IconBuildingArch,
        },
      ]
    }
  ]
};

export default rrhh;
