// assets
import { IconBriefcase, IconFileAnalytics } from '@tabler/icons-react';

// types
import { NavItemType } from 'types';

const icons = {
  IconBriefcase, IconFileAnalytics
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
    }
  ]
};

export default contratacion;
