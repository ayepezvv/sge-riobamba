'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

import { Activity, useEffect, useRef, useState } from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import Avatar from '@mui/material/Avatar';
import ButtonBase from '@mui/material/ButtonBase';
import Chip from '@mui/material/Chip';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';

// project imports
import { handlerActiveItem, handlerDrawerOpen, useGetMenuMaster } from 'api/menu';
import { MenuOrientation, ThemeDirection } from 'config';
import useConfig from 'hooks/useConfig';
import { withAlpha } from 'utils/colorUtils';

// third party
import { FormattedMessage } from 'react-intl';

// assets
import FiberManualRecordIcon from '@mui/icons-material/FiberManualRecord';

// types
import { LinkTarget, NavItemType } from 'types';

// ==============================|| SIDEBAR MENU LIST ITEMS ||============================== //

interface NavItemProps {
  item: NavItemType;
  level: number;
  isParents?: boolean;
  setSelectedID?: () => void;
}

export default function NavItem({ item, level, isParents = false, setSelectedID }: NavItemProps) {
  const theme = useTheme();
  const downMD = useMediaQuery(theme.breakpoints.down('md'));
  const ref = useRef<HTMLSpanElement>(null);

  const pathname = usePathname();
  const {
    state: { menuOrientation, borderRadius, themeDirection }
  } = useConfig();

  const { menuMaster } = useGetMenuMaster();
  const openItem = menuMaster.openedItem;
  const drawerOpen = menuMaster.isDashboardDrawerOpened;
  const isHorizontal = menuOrientation === MenuOrientation.HORIZONTAL && !downMD;
  const isSelected = openItem === item.id;

  const [hoverStatus, setHover] = useState<boolean>(false);

  const compareSize = () => {
    const compare = ref.current && ref.current.scrollWidth > ref.current.clientWidth;
    setHover(compare as boolean);
  };

  useEffect(() => {
    compareSize();
    window.addEventListener('resize', compareSize);

    return () => window.removeEventListener('resize', compareSize);
  }, []);

  const Icon = item?.icon;
  const itemIcon = item?.icon ? (
    <Icon stroke={1.5} size={drawerOpen ? '20px' : '24px'} style={{ ...(isHorizontal && isParents && { fontSize: 20, stroke: '1.5' }) }} />
  ) : (
    <FiberManualRecordIcon sx={{ width: isSelected ? 8 : 6, height: isSelected ? 8 : 6 }} fontSize={level > 0 ? 'inherit' : 'medium'} />
  );

  let itemTarget: LinkTarget = '_self';
  if (item.target) {
    itemTarget = '_blank';
  }

  const itemHandler = () => {
    if (downMD) handlerDrawerOpen(false);

    if (isParents && setSelectedID) {
      setSelectedID();
    }
  };

  // active menu item on page load
  useEffect(() => {
    if (pathname === item.url) handlerActiveItem(item.id!);
    // eslint-disable-next-line
  }, [pathname]);

  return (
    <>
      {!isHorizontal ? (
        <ListItemButton
          component={Link}
          href={item.url!}
          target={itemTarget}
          disabled={item.disabled}
          disableRipple={!drawerOpen}
          sx={{
            zIndex: 1201,
            borderRadius: `${borderRadius}px`,
            mb: 0.5,
            ...(drawerOpen && level !== 1 && { ml: `${level * 18}px` }),
            ...(!drawerOpen && { pl: 1.25 }),
            ...((!drawerOpen || level !== 1) && {
              py: level === 1 ? 0 : 1,
              '&:hover': { bgcolor: 'transparent' },
              '&.Mui-selected': {
                '&:hover': { bgcolor: 'transparent' },
                bgcolor: 'transparent'
              }
            })
          }}
          selected={isSelected}
          onClick={() => itemHandler()}
        >
          <ButtonBase aria-label="theme-icon" sx={{ borderRadius: `${borderRadius}px` }} disableRipple={drawerOpen}>
            <ListItemIcon
              sx={{
                minWidth: level === 1 ? 36 : 18,
                color: isSelected ? 'secondary.main' : 'text.primary',
                ...(!drawerOpen &&
                  level === 1 && {
                    borderRadius: `${borderRadius}px`,
                    width: 46,
                    height: 46,
                    alignItems: 'center',
                    justifyContent: 'center',
                    '&:hover': { bgcolor: 'secondary.light' },
                    ...(isSelected && {
                      bgcolor: 'secondary.light',
                      '&:hover': { bgcolor: 'secondary.light' }
                    })
                  }),

                // dark overrides
                ...theme.applyStyles('dark', {
                  color: isSelected && drawerOpen ? 'text.primary' : 'text.primary',

                  ...(!drawerOpen &&
                    level === 1 && {
                      '&:hover': { bgcolor: withAlpha(theme.vars.palette.secondary.main, 0.25) },
                      ...(isSelected && {
                        bgcolor: withAlpha(theme.vars.palette.secondary.main, 0.25),
                        '&:hover': { bgcolor: withAlpha(theme.vars.palette.secondary.main, 0.3) }
                      })
                    })
                })
              }}
            >
              {itemIcon}
            </ListItemIcon>
          </ButtonBase>

          {(drawerOpen || (!drawerOpen && level !== 1)) && (
            <Tooltip title={<FormattedMessage id={item.title} />} disableHoverListener={!hoverStatus}>
              <ListItemText
                primary={
                  <Typography
                    ref={ref}
                    noWrap
                    variant={isSelected ? 'h5' : 'body1'}
                    sx={{
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      width: 102,
                      color: 'inherit',
                      ...(themeDirection === ThemeDirection.RTL && { textAlign: 'end', direction: 'rtl' })
                    }}
                  >
                    <FormattedMessage id={item.title} />
                  </Typography>
                }
                secondary={
                  item.caption && (
                    <Typography
                      variant="caption"
                      gutterBottom
                      sx={{
                        display: 'block',
                        fontSize: '0.6875rem',
                        fontWeight: 500,
                        color: 'text.secondary',
                        textTransform: 'capitalize',
                        lineHeight: 1.66
                      }}
                    >
                      <FormattedMessage id={item.caption} />
                    </Typography>
                  )
                }
              />
            </Tooltip>
          )}

          <Activity mode={drawerOpen && item.chip ? 'visible' : 'hidden'}>
            <Chip
              color={item.chip?.color}
              variant={item.chip?.variant}
              size={item.chip?.size}
              label={item.chip?.label}
              avatar={
                <Activity mode={item.chip?.avatar ? 'visible' : 'hidden'}>
                  <Avatar>{item.chip?.avatar}</Avatar>
                </Activity>
              }
            />
          </Activity>
        </ListItemButton>
      ) : (
        <ListItemButton
          component={Link}
          href={item.url!}
          target={itemTarget}
          disabled={item.disabled}
          sx={{
            borderRadius: isParents ? `${borderRadius}px` : 0,
            mb: isParents ? 0 : 0.5,
            alignItems: 'flex-start',
            backgroundColor: level > 1 ? 'transparent !important' : 'inherit',
            py: 1,
            pl: 2,
            mr: isParents ? 1 : 0
          }}
          selected={isSelected}
          onClick={() => itemHandler()}
        >
          <ListItemIcon
            sx={{
              my: 'auto',
              minWidth: !item?.icon ? 18 : 36
            }}
          >
            {itemIcon}
          </ListItemIcon>

          <ListItemText
            sx={{ mb: 0.25 }}
            primary={
              <Typography variant={isSelected ? 'h5' : 'body1'} sx={{ color: 'inherit' }}>
                <FormattedMessage id={item.title} />
              </Typography>
            }
            secondary={
              <Activity mode={item.caption ? 'visible' : 'hidden'}>
                <Typography
                  gutterBottom
                  sx={{
                    display: 'block',
                    fontSize: '0.6875rem',
                    fontWeight: 500,
                    color: 'text.secondary',
                    textTransform: 'capitalize',
                    lineHeight: 1.66
                  }}
                >
                  {item.caption}
                </Typography>
              </Activity>
            }
          />

          <Activity mode={item.chip ? 'visible' : 'hidden'}>
            <Chip
              color={item.chip?.color}
              variant={item.chip?.variant}
              size={item.chip?.size}
              label={item.chip?.label}
              avatar={
                <Activity mode={item.chip?.avatar ? 'visible' : 'hidden'}>
                  <Avatar>{item.chip?.avatar}</Avatar>
                </Activity>
              }
            />
          </Activity>
        </ListItemButton>
      )}
    </>
  );
}
