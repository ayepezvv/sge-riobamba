import { IconPackages, IconList, IconArrowsExchange, IconDashboard } from "@tabler/icons-react";

const icons = { IconPackages, IconList, IconArrowsExchange, IconDashboard };

const inventario = {
  id: "inventario",
  title: "Inventario / Existencias",
  type: "group",
  children: [
    {
      id: "inv-resumen",
      title: "Resumen por Año",
      type: "item",
      url: "/inventario",
      icon: icons.IconDashboard,
      breadcrumbs: false,
    },
    {
      id: "inv-articulos",
      title: "Catálogo de Artículos",
      type: "item",
      url: "/inventario/articulos",
      icon: icons.IconPackages,
      breadcrumbs: false,
    },
    {
      id: "inv-movimientos",
      title: "Movimientos de Bodega",
      type: "item",
      url: "/inventario/movimientos",
      icon: icons.IconArrowsExchange,
      breadcrumbs: false,
    },
  ],
};

export default inventario;
