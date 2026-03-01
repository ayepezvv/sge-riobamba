'use client';

import React from 'react';

// material-ui
import { styled } from '@mui/material/styles';
import Badge, { BadgeProps } from '@mui/material/Badge';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Grid from '@mui/material/Grid';
import IconButton from '@mui/material/IconButton';
import Stack from '@mui/material/Stack';
import Switch from '@mui/material/Switch';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SecondaryAction from 'ui-component/cards/CardSecondaryAction';
import { gridSpacing } from 'store/constant';

// assets
import MailIcon from '@mui/icons-material/EmailTwoTone';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCartTwoTone';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';

const CustomizedBadge = styled(Badge)<BadgeProps>(({ theme }) => ({
  '& .MuiBadge-badge': {
    right: -3,
    top: 13,
    border: `2px solid ${theme.vars.palette.background.paper}`,
    padding: '0 4px'
  }
}));

const OutlinedBadge = styled(Badge)<BadgeProps>(({ theme }) => ({
  '& .MuiBadge-badge': {
    background: theme.vars.palette.background.paper,
    color: theme.vars.palette.primary.main,
    border: `1px solid ${theme.vars.palette.primary.main}`,
    padding: '0 4px'
  }
}));

const FillBadge = styled(Badge)<BadgeProps>(({ theme }) => ({
  '& .MuiBadge-badge': {
    background: theme.vars.palette.primary.light,
    color: theme.vars.palette.primary.main,
    padding: '0 4px'
  }
}));

// style constant
const shapeStyles = { bgcolor: 'primary.light', width: 40, height: 40 };
const shapeCircleStyles = { borderRadius: '50%' };

// ===============================|| UI BADGES ||=============================== //

export default function UIBadges() {
  const rectangle = <Box sx={shapeStyles} />;
  const circle = <Box sx={{ ...shapeStyles, ...shapeCircleStyles }} />;

  const [count, setCount] = React.useState(1);
  const [invisible, setInvisible] = React.useState(false);
  const handleBadgeVisibility = () => {
    setInvisible(!invisible);
  };

  return (
    <MainCard title="Badges" secondary={<SecondaryAction link="https://next.material-ui.com/components/badges/" />}>
      <Grid container spacing={gridSpacing}>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <SubCard title="Basic">
            <Stack direction="row" sx={{ justifyContent: 'center', gap: 2 }}>
              <Badge badgeContent={4} color="default">
                <MailIcon />
              </Badge>
              <Badge badgeContent={4} color="primary">
                <MailIcon />
              </Badge>
              <Badge badgeContent={4} color="secondary">
                <MailIcon />
              </Badge>
              <Badge badgeContent={4} color="error">
                <MailIcon />
              </Badge>
            </Stack>
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <SubCard title="Maximum Value Badges">
            <Stack direction="row" sx={{ justifyContent: 'center', gap: 4 }}>
              <Badge badgeContent={99} color="primary">
                <MailIcon />
              </Badge>
              <Badge badgeContent={100} color="secondary">
                <MailIcon />
              </Badge>
              <Badge badgeContent={1000} max={999} color="error">
                <MailIcon />
              </Badge>
            </Stack>
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <SubCard title="Dot Badges">
            <Stack direction="row" sx={{ justifyContent: 'center', gap: 2 }}>
              <Badge variant="dot" color="primary">
                <MailIcon />
              </Badge>
              <Badge variant="dot" color="secondary">
                <MailIcon />
              </Badge>
              <Badge variant="dot" color="error">
                <Typography>Typography</Typography>
              </Badge>
            </Stack>
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <SubCard title="Badge Alignment">
            <Stack direction="row" sx={{ justifyContent: 'center', gap: 2 }}>
              <Badge badgeContent={4} color="primary" anchorOrigin={{ vertical: 'top', horizontal: 'right' }}>
                <MailIcon />
              </Badge>
              <Badge variant="dot" color="error" anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
                <MailIcon />
              </Badge>
              <Badge badgeContent={4} color="primary" anchorOrigin={{ vertical: 'top', horizontal: 'left' }}>
                <MailIcon />
              </Badge>
              <Badge variant="dot" color="error" anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}>
                <MailIcon />
              </Badge>
            </Stack>
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <SubCard title="Customized Badges">
            <Stack direction="row" sx={{ justifyContent: 'center', gap: 3, alignItems: 'center' }}>
              <IconButton aria-label="cart" size="large">
                <CustomizedBadge badgeContent={4} color="error">
                  <ShoppingCartIcon />
                </CustomizedBadge>
              </IconButton>
              <FillBadge badgeContent={4}>
                <MailIcon />
              </FillBadge>
              <OutlinedBadge badgeContent={4}>
                <MailIcon />
              </OutlinedBadge>
            </Stack>
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <SubCard title="Badge Visibility">
            <Stack sx={{ gap: 2 }}>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 3 }}>
                <Badge color="secondary" badgeContent={count}>
                  <MailIcon />
                </Badge>
                <ButtonGroup>
                  <Button
                    aria-label="reduce"
                    onClick={() => {
                      setCount(Math.max(count - 1, 0));
                    }}
                  >
                    <RemoveIcon fontSize="small" />
                  </Button>
                  <Button
                    aria-label="increase"
                    onClick={() => {
                      setCount(count + 1);
                    }}
                  >
                    <AddIcon fontSize="small" />
                  </Button>
                </ButtonGroup>
              </Stack>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 3 }}>
                <Badge color="secondary" variant="dot" invisible={invisible}>
                  <MailIcon />
                </Badge>
                <FormControlLabel
                  control={<Switch color="primary" checked={!invisible} onChange={handleBadgeVisibility} />}
                  label="Show Badge"
                />
              </Stack>
            </Stack>
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <SubCard title="Badge Overlap">
            <Stack direction="row" sx={{ justifyContent: 'center', gap: 4 }}>
              <Badge color="secondary" badgeContent=" ">
                {rectangle}
              </Badge>
              <Badge color="secondary" badgeContent=" " variant="dot">
                {rectangle}
              </Badge>
              <Badge color="secondary" overlap="circular" badgeContent=" ">
                {circle}
              </Badge>
              <Badge color="secondary" overlap="circular" badgeContent=" " variant="dot">
                {circle}
              </Badge>
            </Stack>
          </SubCard>
        </Grid>
      </Grid>
    </MainCard>
  );
}
