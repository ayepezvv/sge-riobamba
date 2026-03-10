import admin from './admin';
import catastro from './catastro';
import contratacion from './contratacion';
import gis from './gis';
import administrativo from './administrativo';
import { NavItemType } from 'types';

// ==============================|| MENU ITEMS ||============================== //

const menuItems: { items: NavItemType[] } = {
  items: [admin, administrativo, contratacion, catastro, gis]
};

export default menuItems;
