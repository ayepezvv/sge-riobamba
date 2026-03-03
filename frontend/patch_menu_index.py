path = "src/menu-items/index.tsx"

content = """import admin from './admin';
import catastro from './catastro';
import gis from './gis';
import { NavItemType } from 'types';

const menuItems: { items: NavItemType[] } = {
  items: [admin, catastro, gis]
};

export default menuItems;
"""

with open(path, "w") as f:
    f.write(content)
