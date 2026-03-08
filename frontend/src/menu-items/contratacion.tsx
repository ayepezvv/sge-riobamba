// assets
import { IconBriefcase, IconFileAnalytics, IconSettings } from '@tabler/icons-react';

// types
import { NavItemType } from 'types';

const icons = {
  IconBriefcase, IconFileAnalytics, IconSettings
};

const contratacion: NavItemType = {
  id: 'contratacion',
  title: 'contratacion',
  icon: icons.IconBriefcase,
  type: 'group',
  children: [
    {
      id: 'mis-procesos',
      title: 'mis-procesos',
      type: 'item',
      url: '/contratacion/procesos',
      icon: icons.IconFileAnalytics,
      breadcrumbs: false
    },
    {
      id: 'admin-plantillas',
      title: 'admin-plantillas',
      type: 'item',
      url: '/contratacion/administracion',
      icon: icons.IconSettings,
      breadcrumbs: false
    }
  ]
};

export default contratacion;
