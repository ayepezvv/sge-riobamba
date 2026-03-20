import {
  IconUsers, IconAddressBook, IconBuildingArch,
  IconMoneybag, IconBriefcase, IconContract
} from '@tabler/icons-react';

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
        {
          id: 'rrhh-escalas',
          title: 'Escalas Salariales',
          type: 'item',
          url: '/rrhh/escalas',
          icon: IconMoneybag,
        },
        {
          id: 'rrhh-cargos',
          title: 'Catálogo de Cargos',
          type: 'item',
          url: '/rrhh/cargos',
          icon: IconBriefcase,
        },
        {
          id: 'rrhh-contratos',
          title: 'Gestión de Contratos',
          type: 'item',
          url: '/rrhh/contratos',
          icon: IconContract,
        },
      ]
    }
  ]
};

export default rrhh;
