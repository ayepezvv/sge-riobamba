import { IconNetwork, IconRouter } from '@tabler/icons-react';
import { NavItemType } from 'types';

const icons = {
    IconNetwork,
    IconRouter
};

export const informatica: NavItemType = {
    id: 'informatica',
    title: 'IT & Sistemas',
    type: 'group',
    children: [
        {
            id: 'gestion-redes',
            title: 'Gestión de Redes & IPAM',
            type: 'item',
            url: '/informatica/redes',
            icon: icons.IconNetwork,
            breadcrumbs: false
        }
    ]
};
