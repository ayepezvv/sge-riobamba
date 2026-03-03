// assets
import { IconMap } from '@tabler/icons-react';

// types
import { NavItemType } from 'types';

const icons = {
  IconMap: IconMap
};

const gis: NavItemType = {
  id: 'gis',
  title: 'gis',
  icon: icons.IconMap,
  type: 'group',
  children: [] // Vacío por ahora como solicitó el Jefe de TI
};

export default gis;
