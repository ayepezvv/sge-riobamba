import admin from './admin';
import administrativo from './administrativo';
import rrhh from './rrhh';
import catastro from './catastro';
import contratacion from './contratacion';
import gis from './gis';
import { informatica } from './informatica';
import bodega from './bodega';
import { NavItemType } from 'types';

// ==============================|| MENU ITEMS ||============================== //

const menuItems: { items: NavItemType[] } = {
  items: [admin, administrativo, rrhh, contratacion, catastro, gis, informatica, bodega]
};

export default menuItems;
