import admin from './admin';
import administrativo from './administrativo';
import rrhh from './rrhh';
import catastro from './catastro';
import contratacion from './contratacion';
import gis from './gis';
import { informatica } from './informatica';
import bodega from './bodega';
import contabilidad from './contabilidad';
import tesoreria from './tesoreria';
import financiero from './financiero';
import presupuesto from './presupuesto';
import { NavItemType } from 'types';

// ==============================|| MENU ITEMS ||============================== //

const menuItems: { items: NavItemType[] } = {
  items: [admin, administrativo, rrhh, contratacion, catastro, gis, informatica, bodega, contabilidad, tesoreria, financiero, presupuesto]
};

export default menuItems;
