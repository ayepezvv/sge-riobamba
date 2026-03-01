'use client';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import CardMedia from '@mui/material/CardMedia';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

// project imports
import { ThemeMode } from 'config';
import { gridSpacing } from 'store/constant';

// assets
const imageEmpty = '/assets/images/e-commerce/empty.svg';
const imageDarkEmpty = '/assets/images/e-commerce/empty-dark.svg';

// ==============================|| CHECKOUT CART - NO/EMPTY CART ITEMS ||============================== //

export default function CartEmpty() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();
  const downLG = useMediaQuery(theme.breakpoints.down('lg'));

  return (
    <Grid container spacing={gridSpacing} sx={{ justifyContent: 'center', my: 3 }}>
      <Grid size={{ xs: 12, sm: 8, md: 6 }}>
        <CardMedia component="img" image={colorScheme === ThemeMode.DARK ? imageDarkEmpty : imageEmpty} title="Slider5 image" />
      </Grid>
      <Grid size={{ xs: 12, sm: 8 }}>
        <Stack sx={{ gap: 1 }}>
          <Typography variant={downLG ? 'h3' : 'h1'} sx={{ textAlign: 'center', color: 'inherit' }}>
            Cart is Empty
          </Typography>
          <Typography variant="body2" align="center">
            Look like you have no items in your shopping cart.
          </Typography>
        </Stack>
      </Grid>
    </Grid>
  );
}
