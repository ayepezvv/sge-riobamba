// third-party
import { FormattedMessage } from 'react-intl';

// assets
import { IconUsers, IconBuildingCommunity, IconUserCircle } from '@tabler/icons-react';
import { NavItemType } from 'types';

const icons = {
  IconUsers: IconUsers,
  IconBuildingCommunity: IconBuildingCommunity,
  IconUserCircle: IconUserCircle
};

// ==============================|| MENU ITEMS - ADMINISTRATIVO ||============================== //

const administrativo: NavItemType = {
  id: 'administrativo',
  title: <FormattedMessage id="talento-humano" defaultMessage="Talento Humano" />,
  icon: icons.IconUsers,
  type: 'group',
  children: [
    {
      id: 'direcciones',
      title: <FormattedMessage id="direcciones" defaultMessage="Direcciones" />,
      type: 'item',
      url: '/administrativo/direcciones',
      icon: icons.IconBuildingCommunity,
      breadcrumbs: false
    },
    {
      id: 'unidades',
      title: <FormattedMessage id="unidades" defaultMessage="Unidades" />,
      type: 'item',
      url: '/administrativo/unidades',
      icon: icons.IconBuildingCommunity,
      breadcrumbs: false
    },
    {
      id: 'personal',
      title: <FormattedMessage id="personal" defaultMessage="Personal" />,
      type: 'item',
      url: '/administrativo/personal',
      icon: icons.IconUserCircle,
      breadcrumbs: false
    }
  ]
};

export default administrativo;
