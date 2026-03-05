// assets
import { IconAddressBook, IconMapPin } from '@tabler/icons-react';

// types
import { NavItemType } from 'types';

const icons = {
  IconAddressBook: IconAddressBook,
  IconMapPin: IconMapPin
};

const catastro: NavItemType = {
  id: 'catastro-comercial',
  title: 'catastro-comercial',
  icon: icons.IconAddressBook,
  type: 'group',
  children: [
    {
      id: 'padron-ciudadanos',
      title: 'padron-ciudadanos',
      type: 'item',
      url: '/catastro/ciudadanos',
      icon: icons.IconAddressBook,
      breadcrumbs: false
    }
  ]
};

export default catastro;
