'use client';

// material-ui
import { styled } from '@mui/material/styles';
import ButtonBase from '@mui/material/ButtonBase';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// project imports
import SubCard from 'ui-component/cards/SubCard';

// assets
const banner = '/assets/images/profile/profile-back-10.png';

// styled constant
const BannerImg = styled('img')({
  margin: 'auto',
  display: 'block',
  maxWidth: '100%',
  maxHeight: '100%'
});

// ===============================|| GRID - COMPLEX ||=============================== //

export default function ComplexGrid() {
  return (
    <SubCard content={false} sx={{ p: 2, margin: 'auto', maxWidth: 500, flexGrow: 1 }}>
      <Stack direction={{ xs: 'column', sm: 'row' }} sx={{ gap: 2, alignItems: 'flex-start' }}>
        <ButtonBase sx={{ width: { xs: '100%', sm: 215 } }}>
          <BannerImg alt="complex" src={banner} />
        </ButtonBase>
        <Stack direction="row" sx={{ justifyContent: 'space-between', gap: 2 }}>
          <Stack sx={{ gap: 2 }}>
            <Box>
              <Typography gutterBottom variant="subtitle1">
                Standard license
              </Typography>
              <Typography variant="body2" gutterBottom>
                Full resolution 1920x1080 • JPEG
              </Typography>
              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                ID: 1030114
              </Typography>
            </Box>
            <Typography sx={{ cursor: 'pointer', color: 'error.main' }} variant="body2">
              Remove
            </Typography>
          </Stack>
          <Typography variant="subtitle1">$19.00</Typography>
        </Stack>
      </Stack>
    </SubCard>
  );
}
