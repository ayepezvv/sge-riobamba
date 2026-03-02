// assets
import { IconUsers } from '@tabler/icons-react';

// types
import { NavItemType } from 'types';

const icons = {
  IconUsers: IconUsers
};

// ==============================|| MENU ITEMS - ADMINISTRACION ||============================== //

const admin: NavItemType = {
  id: 'admin',
  title: 'admin',
  icon: icons.IconUsers,
  type: 'group',
  children: [
    {
      id: 'user-management',
      title: 'user-management',
      type: 'item',
      url: '/usuarios',
      icon: icons.IconUsers,
      breadcrumbs: false
    }
  ]
};

export default admin;
