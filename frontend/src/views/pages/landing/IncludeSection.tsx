'use client';

// material-ui
import { useTheme } from '@mui/material/styles';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';

// third party
import Marquee from 'react-fast-marquee';

// =============================|| LANDING - INCLUDE SECTION ||============================= //

export default function IncludeSection() {
  const theme = useTheme();

  const marqueeSX = {
    display: 'flex',
    width: '100%',
    gap: 6,
    justifyContent: 'space-around',
    '.MuiTypography-root': {
      fontWeight: 600,
      cursor: 'pointer',
      color: 'text.secondary',
      '&:hover': { color: 'grey.900' },
      ...theme.applyStyles('dark', {
        color: 'text.primary',
        '&:hover': { color: 'text.secondary' }
      })
    }
  };

  const margueeFirst = [
    'Live Customizer',
    '7+ Conceptual Apps',
    'Highly Flexible',
    'Always Updated',
    'Beautiful Design',
    'TypeScript Support',
    'Figma Design System',
    'Dark/Light Layouts',
    'RTL',
    'Prettier Code Standard',
    'i18n Multi Language Support',
    'Auth Methods'
  ];
  const margueeSecond = [
    'Auth Methods',
    'i18n Multi Language Support',
    'Prettier Code Standard',
    'RTL',
    'Dark/Light Layouts',
    'Figma Design System',
    'TypeScript Support',
    'Beautiful Design',
    'Highly Flexible',
    '7+ Conceptual Apps',
    'Live Customizer',
    'Always Updated'
  ];

  return (
    <Box sx={{ '.overlay': { display: 'none' } }}>
      <Container>
        <Stack sx={{ alignItems: 'center', gap: 1.25 }}>
          <Typography variant="h2" sx={{ fontSize: { xs: '1.5rem', sm: '2.125rem' } }}>
            Features that are well-liked
          </Typography>
          <Typography variant="h4" sx={{ fontWeight: 400 }} align="center">
            Multiple categories with app concepts and demo content
          </Typography>
        </Stack>
      </Container>
      <Stack sx={{ mt: 9, direction: 'initial', gap: 4 }}>
        <Marquee className="marquee-section">
          <Box sx={marqueeSX}>
            {margueeFirst.map((item, index) => (
              <Typography key={index} variant="h2" {...(index === 0 && { sx: { ml: 1 } })}>
                {item}
              </Typography>
            ))}
          </Box>
        </Marquee>
        <Marquee className="marquee-section" direction="right">
          <Box sx={marqueeSX}>
            {margueeSecond.map((item, index) => (
              <Typography key={index} variant="h2" {...(index === 0 && { sx: { ml: 5 } })}>
                {item}
              </Typography>
            ))}
          </Box>
        </Marquee>
      </Stack>
    </Box>
  );
}
