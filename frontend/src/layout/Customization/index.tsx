'use client';

import { Activity, ReactNode, SyntheticEvent, useState } from 'react';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import Fab from '@mui/material/Fab';
import Grid from '@mui/material/Grid';
import IconButton from '@mui/material/IconButton';
import Stack from '@mui/material/Stack';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// project imports
import FontFamily from './FontFamily';
import BoxContainer from './BoxContainer';
import PresetColor from './PresetColor';
import Layout from './Layout';
import InputFilled from './InputFilled';
import BorderRadius from './BorderRadius';
import ThemeModeLayout from './ThemeMode';
import SidebarDrawer from './SidebarDrawer';
import MenuOrientation from './MenuOrientation';

import { DEFAULT_THEME_MODE } from 'config';
import MainCard from 'ui-component/cards/MainCard';
import AnimateButton from 'ui-component/extended/AnimateButton';
import SimpleBar from 'ui-component/third-party/SimpleBar';
import useConfig from 'hooks/useConfig';

// assets
import { IconSettings, IconPlus, IconTextSize, IconColorSwatch } from '@tabler/icons-react';

// ==============================|| LIVE CUSTOMIZATION ||============================== //
interface TabPanelProps {
  children?: ReactNode;
  index: number;
  value: number;
}

function CustomTabPanel({ children, value, index, ...other }: TabPanelProps) {
  return (
    <div role="tabpanel" hidden={value !== index} id={`simple-tabpanel-${index}`} aria-labelledby={`simple-tab-${index}`} {...other}>
      <Activity mode={value === index ? 'visible' : 'hidden'}>
        <Box>{children}</Box>
      </Activity>
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`
  };
}

export default function Customization() {
  const theme = useTheme();
  const { resetState } = useConfig();
  const { setMode } = useColorScheme();

  // drawer on/off
  const [open, setOpen] = useState(false);
  const handleToggle = () => {
    setOpen(!open);
  };

  const [value, setValue] = useState(0);

  const handleChange = (_event: SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const handleReset = () => {
    setMode(DEFAULT_THEME_MODE);
    resetState();
  };

  return (
    <>
      {/* toggle button */}
      <Tooltip title="Live Customize">
        <Fab
          component="div"
          onClick={handleToggle}
          size="medium"
          variant="circular"
          color="secondary"
          sx={{
            borderRadius: 0,
            borderTopLeftRadius: '50%',
            borderBottomLeftRadius: '50%',
            borderTopRightRadius: '50%',
            borderBottomRightRadius: '4px',
            top: '25%',
            position: 'fixed',
            right: 10,
            zIndex: 1200,
            boxShadow: theme.vars.customShadows.secondary
          }}
        >
          <AnimateButton type="rotate">
            <IconButton color="inherit" size="large" disableRipple aria-label="live customize">
              <IconSettings />
            </IconButton>
          </AnimateButton>
        </Fab>
      </Tooltip>
      <Drawer anchor="right" onClose={handleToggle} open={open} slotProps={{ paper: { sx: { width: 375 } } }}>
        <Activity mode={open ? 'visible' : 'hidden'}>
          <SimpleBar>
            <MainCard content={false} border={false}>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'space-between', p: 2.5, gap: 1.5 }}>
                <Typography variant="h5">Theme Customization</Typography>
                <Stack direction="row" sx={{ alignItems: 'center', gap: 1.25 }}>
                  <Button variant="outlined" color="error" size="small" onClick={handleReset}>
                    Reset
                  </Button>
                  <IconButton sx={{ p: 0, color: 'grey.600' }} onClick={handleToggle}>
                    <IconPlus size={24} style={{ transform: 'rotate(45deg)' }} />
                  </IconButton>
                </Stack>
              </Stack>
              <Divider />
              <Box sx={{ width: '100%' }}>
                <Tabs
                  value={value}
                  sx={{
                    bgcolor: 'grey.50',
                    ...theme.applyStyles('dark', { bgcolor: 'dark.800' }),
                    minHeight: 56,
                    '& .MuiTabs-flexContainer': { height: '100%' }
                  }}
                  centered
                  onChange={handleChange}
                  aria-label="basic tabs example"
                >
                  <Tab label={<IconColorSwatch />} {...a11yProps(0)} sx={{ width: '50%' }} />
                  <Tab label={<IconTextSize />} {...a11yProps(1)} sx={{ width: '50%' }} />
                </Tabs>
              </Box>
              <CustomTabPanel value={value} index={0}>
                <Grid container spacing={2.5}>
                  <Grid size={12}>
                    {/* layout type */}
                    <ThemeModeLayout />
                    <Divider />
                  </Grid>
                  <Grid size={12}>
                    {/* Theme Preset Color */}
                    <PresetColor />
                    <Divider />
                  </Grid>
                  <Grid size={12}>
                    {/* Input Background */}
                    <InputFilled />
                    <Divider />
                  </Grid>
                  <Grid size={12}>
                    {/* Theme Width */}
                    <BoxContainer />
                    <Divider />
                  </Grid>
                  <Grid size={12}>
                    {/* Theme Layout */}
                    <Layout />
                    <Divider />
                  </Grid>
                  <Grid size={12}>
                    {/* Sidebar Drawer */}
                    <SidebarDrawer />
                    <Divider />
                  </Grid>
                  <Grid size={12}>
                    {/* Menu Orientation */}
                    <MenuOrientation />
                    <Divider />
                  </Grid>
                </Grid>
              </CustomTabPanel>
              <CustomTabPanel value={value} index={1}>
                <Grid container spacing={2}>
                  <Grid size={12}>
                    {/* font family */}
                    <FontFamily />
                    <Divider />
                  </Grid>
                  <Grid size={12}>
                    {/* border radius */}
                    <BorderRadius />
                    <Divider />
                  </Grid>
                </Grid>
              </CustomTabPanel>
            </MainCard>
          </SimpleBar>
        </Activity>
      </Drawer>
    </>
  );
}
