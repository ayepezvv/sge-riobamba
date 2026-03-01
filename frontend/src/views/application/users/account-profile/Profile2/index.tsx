'use client';

import React from 'react';

// material-ui
import Button from '@mui/material/Button';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Typography from '@mui/material/Typography';

// project imports
import UserProfile from './UserProfile';
import Billing from './Billing';
import Payment from './Payment';
import ChangePassword from './ChangePassword';
import useConfig from 'hooks/useConfig';
import MainCard from 'ui-component/cards/MainCard';
import AnimateButton from 'ui-component/extended/AnimateButton';
import { gridSpacing } from 'store/constant';

// assets
import PersonOutlineTwoToneIcon from '@mui/icons-material/PersonOutlineTwoTone';
import DescriptionTwoToneIcon from '@mui/icons-material/DescriptionTwoTone';
import CreditCardTwoToneIcon from '@mui/icons-material/CreditCardTwoTone';
import VpnKeyTwoToneIcon from '@mui/icons-material/VpnKeyTwoTone';

// types
import { TabsProps } from 'types';

// tabs
function TabPanel({ children, value, index, ...other }: TabsProps) {
  return (
    <div role="tabpanel" hidden={value !== index} id={`simple-tabpanel-${index}`} aria-labelledby={`simple-tab-${index}`} {...other}>
      {value === index && <div>{children}</div>}
    </div>
  );
}

function a11yProps(index: number) {
  return { id: `simple-tab-${index}`, 'aria-controls': `simple-tabpanel-${index}` };
}

// tabs option
const tabsOption = [
  { label: 'User Profile', icon: <PersonOutlineTwoToneIcon />, caption: 'Profile Settings' },
  { label: 'Billing', icon: <DescriptionTwoToneIcon />, caption: 'Billing Information' },
  { label: 'Payment', icon: <CreditCardTwoToneIcon />, caption: 'Add & Update Card' },
  { label: 'Change Password', icon: <VpnKeyTwoToneIcon />, caption: 'Update Profile Security' }
];

// ==============================|| PROFILE 2 ||============================== //

export default function Profile2() {
  const {
    state: { borderRadius }
  } = useConfig();
  const [value, setValue] = React.useState<number>(0);

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <MainCard title="Account Settings" content={false}>
      <Grid container spacing={gridSpacing}>
        <Grid size={{ xs: 12, lg: 4 }}>
          <CardContent>
            <Tabs
              value={value}
              onChange={handleChange}
              orientation="vertical"
              variant="scrollable"
              sx={(theme) => ({
                '& .MuiTabs-flexContainer': { borderBottom: 'none' },
                '& button': {
                  color: 'grey.900',
                  minHeight: 'auto',
                  minWidth: '100%',
                  py: 1.5,
                  px: 2,
                  display: 'flex',
                  flexDirection: 'row',
                  alignItems: 'flex-start',
                  textAlign: 'left',
                  justifyContent: 'flex-start',
                  borderRadius: `${borderRadius}px`
                },
                '& button.Mui-selected': { color: 'primary.main', bgcolor: 'grey.50' },
                '& button > svg': { marginBottom: '0px !important', marginRight: 1.25, marginTop: 1.25, height: 20, width: 20 },
                '& button > div > span': { display: 'block' },
                '& > div > span': { display: 'none' },

                ...theme.applyStyles('dark', {
                  '& button': { color: 'grey.600' },
                  '& button.Mui-selected': { bgcolor: 'dark.main' }
                })
              })}
            >
              {tabsOption.map((tab, index) => (
                <Tab
                  key={index}
                  icon={tab.icon}
                  label={
                    <Stack>
                      <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                        {tab.label}
                      </Typography>
                      <Typography variant="caption" sx={{ textTransform: 'capitalize' }}>
                        {tab.caption}
                      </Typography>
                    </Stack>
                  }
                  {...a11yProps(index)}
                />
              ))}
            </Tabs>
          </CardContent>
        </Grid>
        <Grid size={{ xs: 12, lg: 8 }}>
          <CardContent sx={{ borderLeft: '1px solid', borderColor: 'divider', height: '100%' }}>
            <TabPanel value={value} index={0}>
              <UserProfile />
            </TabPanel>
            <TabPanel value={value} index={1}>
              <Billing />
            </TabPanel>
            <TabPanel value={value} index={2}>
              <Payment />
            </TabPanel>
            <TabPanel value={value} index={3}>
              <ChangePassword />
            </TabPanel>
          </CardContent>
        </Grid>
      </Grid>
      <Divider />
      <CardActions>
        <Grid container sx={{ width: 1, alignContent: 'center', justifyContent: 'space-between' }}>
          <Grid>
            {value > 0 && (
              <AnimateButton>
                <Button variant="outlined" size="large" onClick={(e) => handleChange(e, value - 1)}>
                  Back
                </Button>
              </AnimateButton>
            )}
          </Grid>
          <Grid>
            {value < 3 && (
              <AnimateButton>
                <Button variant="contained" size="large" onClick={(e) => handleChange(e, 1 + value)}>
                  Continue
                </Button>
              </AnimateButton>
            )}
          </Grid>
        </Grid>
      </CardActions>
    </MainCard>
  );
}
