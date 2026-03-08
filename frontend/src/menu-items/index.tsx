import admin from './admin';
import catastro from './catastro';
import contratacion from './contratacion';
import gis from './gis';
import { NavItemType } from 'types';

const menuItems: { items: NavItemType[] } = {
  items: [admin, contratacion, catastro, gis]
};

export default menuItems;
