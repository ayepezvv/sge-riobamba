import admin from './admin';
import catastro from './catastro';
import gis from './gis';
import { NavItemType } from 'types';

const menuItems: { items: NavItemType[] } = {
  items: [admin, catastro, gis]
};

export default menuItems;
