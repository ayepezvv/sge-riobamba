import { IconPackage, IconBox, IconTags } from '@tabler/icons-react';

const icons = {
    IconPackage,
    IconBox,
    IconTags
};

const bodega = {
    id: 'bodega',
    title: 'Bodega y Activos',
    type: 'group',
    children: [
        {
            id: 'activos-fijos',
            title: 'Control de Activos Fijos',
            type: 'item',
            url: '/bodega/activos',
            icon: icons.IconPackage,
            breadcrumbs: false
        },
        {
            id: 'categorias-bienes',
            title: 'Categorías y Tipos',
            type: 'item',
            url: '/bodega/categorias',
            icon: icons.IconTags,
            breadcrumbs: false
        }
    ]
};

export default bodega;
