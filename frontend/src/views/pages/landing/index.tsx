'use client';

import { useEffect } from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';

// project imports
import HeaderSection from './HeaderSection';
import CardSection from './CardSection';
import FeatureSection from './FeatureSection';
import PeopleSection from './PeopleSection';
import FrameworkSection from './FrameworkSection';
import FooterSection from './FooterSection';
import CustomizeSection from './CustomizeSection';
import PreBuildDashBoard from './PreBuildDashBoard';
import StartupProjectSection from './StartupProjectSection';
//import IncludeSection from './IncludeSection';
//import RtlInfoSection from './RtlInfoSection';

import Customization from 'layout/Customization';
import AppBar from 'ui-component/extended/AppBar';

// Prefetch critical routes using Vite's prefetch
const prefetchRoutes = () => {
  // Use dynamic imports to trigger Vite's prefetching
  // These will be prefetched when the landing page loads
  import('views/dashboard/Default');
  import('views/dashboard/Analytics');
  import('views/pages/authentication/Login');
  import('views/pages/authentication/Register');
  import('views/application/e-commerce/Products');
  import('views/application/crm/LeadManagement/Overview');
  import('views/application/invoice/Dashboard');
};

// =============================|| LANDING MAIN ||============================= //

export default function Landing() {
  const theme = useTheme();

  useEffect(() => {
    // Prefetch routes after initial render
    prefetchRoutes();
  }, []);

  return (
    <>
      {/* 1. header and hero section */}
      <Box
        id="home"
        sx={{
          overflowX: 'hidden',
          overflowY: 'clip',
          background: `linear-gradient(360deg, ${theme.vars.palette.grey[100]} 1.09%, ${theme.vars.palette.background.paper} 100%)`,
          ...theme.applyStyles('dark', {
            background: theme.vars.palette.background.default
          })
        }}
      >
        <AppBar />
        <HeaderSection />
      </Box>

      {/* 2. card section */}
      <Box sx={{ py: 12.5, bgcolor: 'background.default', ...theme.applyStyles('dark', { bgcolor: 'dark.dark' }) }}>
        <CardSection />
      </Box>

      {/* 4. Developer Experience section */}
      <Box sx={{ py: 12.5, bgcolor: 'grey.100', ...theme.applyStyles('dark', { bgcolor: 'background.default' }) }}>
        <CustomizeSection />
      </Box>

      {/* 3. about section */}
      <Box sx={{ py: 12.5, bgcolor: 'background.default', ...theme.applyStyles('dark', { bgcolor: 'dark.dark' }) }}>
        <FeatureSection />
      </Box>

      {/* 4. Apps */}
      <Box sx={{ py: 12.5, bgcolor: 'grey.100', ...theme.applyStyles('dark', { bgcolor: 'background.default' }) }}>
        <PreBuildDashBoard />
      </Box>

      {/* 5. people section */}
      <Box sx={{ py: 12.5, bgcolor: 'background.default', ...theme.applyStyles('dark', { bgcolor: 'dark.dark' }) }}>
        <PeopleSection />
      </Box>

      {/* 6. startup section */}
      <Box sx={{ py: 0 }}>
        <StartupProjectSection />
      </Box>

      {/* multi-language section */}

      {/*  <Box sx={{ py: 0 }}>
                <RtlInfoSection />
            </Box> */}

      {/* framework section */}
      <Box sx={{ py: 12.5, bgcolor: 'background.default', ...theme.applyStyles('dark', { bgcolor: 'dark.dark' }) }}>
        <FrameworkSection />
      </Box>

      {/* 7. inculde section */}
      {/* <Box sx={{ py: 12.5, bgcolor:'background.default', ...theme.applyStyles('dark', {bgcolor: 'dark.dark'}) }}>
                <IncludeSection />
            </Box>
            */}
      {/* footer section */}
      <Box sx={{ py: 12.5, bgcolor: 'dark.900', ...theme.applyStyles('dark', { bgcolor: 'background.default' }), pb: 0 }}>
        <FooterSection />
      </Box>
      <Customization />
    </>
  );
}
