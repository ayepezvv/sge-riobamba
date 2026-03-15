import { FormattedMessage } from 'react-intl';
import { IconNetwork, IconRouter } from '@tabler/icons-react';
import { NavItemType } from 'types';

const icons = {
    IconNetwork,
    IconRouter
};

export const informatica: NavItemType = {
    id: 'informatica',
    title: <FormattedMessage id="it-sistemas" defaultMessage="IT & Sistemas" />,
    type: 'group',
    children: [
        {
            id: 'gestion-redes',
            title: <FormattedMessage id="gestion-redes" defaultMessage="Gestión de Redes & IPAM" />,
            type: 'item',
            url: '/informatica/redes',
            icon: icons.IconNetwork,
            breadcrumbs: false
        }
    ]
};
