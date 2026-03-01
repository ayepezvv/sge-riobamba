'use client';

import RouterLink from 'next/link';

// material-ui
import { useTheme, styled } from '@mui/material/styles';
import Chip from '@mui/material/Chip';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Link from '@mui/material/Link';
import Box from '@mui/material/Box';

// project imports
import { frameworks } from './FrameworkSection';
import Logo from 'ui-component/Logo';

// assets
import { IconBrandDiscord } from '@tabler/icons-react';

import GitHubIcon from '@mui/icons-material/GitHub';
import InstagramIcon from '@mui/icons-material/Instagram';
import PublicIcon from '@mui/icons-material/Public';
import SportsBasketballIcon from '@mui/icons-material/SportsBasketball';
import XIcon from '@mui/icons-material/X';
import YouTubeIcon from '@mui/icons-material/YouTube';

// Link - custom style
const FooterLink = styled(Link)(({ theme }) => ({
  color: theme.vars.palette.text.hint,
  ...theme.applyStyles('dark', { color: theme.vars.palette.text.secondary }),
  '&:hover, &:active': { color: theme.vars.palette.secondary[200] }
}));

// =============================|| LANDING - FOOTER SECTION ||============================= //

export default function FooterSection() {
  const theme = useTheme();
  const textColor = { color: 'text.hint', ...theme.applyStyles('dark', { color: 'text.secondary' }) };

  return (
    <>
      <Container sx={{ mb: 15 }}>
        <Grid container spacing={6}>
          <Grid size={12}>
            <Grid container spacing={8}>
              <Grid size={{ xs: 12, md: 4 }}>
                <Stack sx={{ gap: { xs: 2, md: 5 } }}>
                  <Typography component={RouterLink} href="/" aria-label="theme-logo">
                    <Logo dark />
                  </Typography>
                  <Typography variant="body2" sx={{ ...textColor }}>
                    Berry React is a dashboard template that utilizes the Material-UI framework and the React JavaScript library. It offers
                    a range of features and customization options to help you create a powerful and user-friendly admin panel.
                  </Typography>
                </Stack>
              </Grid>
              <Grid size={{ xs: 12, md: 8 }}>
                <Grid container spacing={{ xs: 5, md: 2 }}>
                  <Grid size={{ xs: 6, sm: 3 }}>
                    <Stack sx={{ gap: { xs: 3, md: 5 } }}>
                      <Typography variant="h4" sx={{ fontWeight: 500, ...textColor }}>
                        Help
                      </Typography>
                      <Stack sx={{ gap: { xs: 1.5, md: 2.5 } }}>
                        <FooterLink href="https://links.codedthemes.com/HTIBc" target="_blank" underline="none">
                          Blog
                        </FooterLink>
                        <FooterLink href="https://codedthemes.gitbook.io/berry/" target="_blank" underline="none">
                          Documentation
                        </FooterLink>
                        <FooterLink href="https://codedthemes.gitbook.io/berry/support/changelog" target="_blank" underline="none">
                          Change Log
                        </FooterLink>
                        <FooterLink href="https://codedthemes.support-hub.io/" target="_blank" underline="none">
                          Support
                        </FooterLink>
                        <FooterLink href="https://discord.com/invite/p2E2WhCb6s" target="_blank" underline="none">
                          Discord
                        </FooterLink>
                      </Stack>
                    </Stack>
                  </Grid>
                  <Grid size={{ xs: 6, sm: 3 }}>
                    <Stack sx={{ gap: { xs: 3, md: 5 } }}>
                      <Typography variant="h4" sx={{ fontWeight: 500, ...textColor }}>
                        Store Help
                      </Typography>
                      <Stack sx={{ gap: { xs: 1.5, md: 2.5 } }}>
                        <FooterLink href="https://mui.com/store/license/" target="_blank" underline="none">
                          License
                        </FooterLink>
                        <FooterLink href="https://mui.com/store/customer-refund-policy/" target="_blank" underline="none">
                          Refund Policy
                        </FooterLink>
                        <FooterLink
                          href="https://support.mui.com/hc/en-us/sections/360002564979-For-customers"
                          target="_blank"
                          underline="none"
                        >
                          Submit a Request
                        </FooterLink>
                      </Stack>
                    </Stack>
                  </Grid>
                  <Grid size={{ xs: 6, sm: 3 }}>
                    <Stack sx={{ gap: { xs: 3, md: 5 } }}>
                      <Typography variant="h4" sx={{ fontWeight: 500, ...textColor }}>
                        Berry Eco-System
                      </Typography>
                      <Stack sx={{ gap: { xs: 1.5, md: 2.5 } }}>
                        {frameworks.map((item, index) => (
                          <FooterLink href={item.link} target="_blank" underline="none" key={index}>
                            {item.title}
                            {item.isUpcoming && (
                              <Chip
                                variant="outlined"
                                size="small"
                                label="Upcoming"
                                sx={{ ml: 0.5, lineHeight: 1.5, color: 'secondary.200', borderColor: 'secondary.200' }}
                              />
                            )}
                          </FooterLink>
                        ))}
                        <FooterLink href="https://links.codedthemes.com/rjvya" target="_blank" underline="none">
                          Pro Figma UI Kit
                        </FooterLink>
                      </Stack>
                    </Stack>
                  </Grid>
                  <Grid size={{ xs: 6, sm: 3 }}>
                    <Stack sx={{ gap: { xs: 3, md: 5 } }}>
                      <Typography variant="h4" sx={{ fontWeight: 500, ...textColor }}>
                        Free Versions
                      </Typography>
                      <Stack sx={{ gap: { xs: 1.5, md: 2.5 } }}>
                        <FooterLink href="https://links.codedthemes.com/rhhGb" target="_blank" underline="none">
                          Free Figma UI Kit
                        </FooterLink>
                        <FooterLink href="https://links.codedthemes.com/Yfkxg" target="_blank" underline="none">
                          Free React MUI
                        </FooterLink>
                        <FooterLink href="https://links.codedthemes.com/epTmN" target="_blank" underline="none">
                          Free Bootstrap 5
                        </FooterLink>
                        <FooterLink href="https://links.codedthemes.com/seQKN" target="_blank" underline="none">
                          Free Angular
                        </FooterLink>
                        <FooterLink href="https://links.codedthemes.com/zQLHX" target="_blank" underline="none">
                          Free Vue
                        </FooterLink>
                        <FooterLink href="https://links.codedthemes.com/Wfbiy" target="_blank" underline="none">
                          Free Django
                        </FooterLink>
                      </Stack>
                    </Stack>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Container>
      <Box sx={{ bgcolor: 'dark.dark', py: { xs: 3, sm: 1.5 } }}>
        <Container>
          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            sx={{ gap: { xs: 1.5, sm: 1, md: 3 }, alignItems: 'center', justifyContent: 'space-between' }}
          >
            <Typography sx={{ color: 'text.secondary' }}>
              © Berry is managed by{' '}
              <Link href="https://codedthemes.com/" target="_blank" underline="hover">
                CodedThemes
              </Link>
            </Typography>
            <Stack direction="row" sx={{ gap: { xs: 2, sm: 1.5, md: 2 }, alignItems: 'center' }}>
              <IconButton
                size="small"
                aria-label="codedTheme Github"
                component={Link}
                href="https://github.com/codedthemes"
                target="_blank"
              >
                <GitHubIcon sx={{ color: 'text.secondary', '&:hover': { color: 'success.main' } }} />
              </IconButton>
              <IconButton
                size="small"
                aria-label="codedTheme Instagram"
                component={Link}
                href="https://www.instagram.com/codedthemes"
                target="_blank"
              >
                <InstagramIcon sx={{ color: 'text.secondary', '&:hover': { color: 'error.main' } }} />
              </IconButton>
              <IconButton
                size="small"
                aria-label="codedTheme Discord"
                component={Link}
                href="https://discord.com/invite/p2E2WhCb6s"
                target="_blank"
                sx={{ color: 'text.secondary', '&:hover': { color: 'info.main' } }}
              >
                <IconBrandDiscord size={30} />
              </IconButton>
              <IconButton
                size="small"
                aria-label="codedTheme Youtube"
                component={Link}
                href="https://www.youtube.com/channel/UCiZG__BaRkT1OuZl5ifzO6A"
                target="_blank"
              >
                <YouTubeIcon sx={{ color: 'text.secondary', '&:hover': { color: 'error.main' } }} />
              </IconButton>
              <IconButton size="small" aria-label="Berry Blog" component={Link} href="https://links.codedthemes.com/HTIBc" target="_blank">
                <PublicIcon sx={{ color: 'text.secondary', '&:hover': { color: 'error.main' } }} />
              </IconButton>
              <IconButton size="small" aria-label="codedTheme Twitter" component={Link} href="https://x.com/codedthemes" target="_blank">
                <XIcon sx={{ color: 'text.secondary', '&:hover': { color: 'primary.main' } }} />
              </IconButton>
              <IconButton
                size="small"
                aria-label="codedTheme Dribble"
                component={Link}
                href="https://dribbble.com/codedthemes"
                target="_blank"
              >
                <SportsBasketballIcon sx={{ color: 'text.secondary', '&:hover': { color: 'warning.main' } }} />
              </IconButton>
            </Stack>
          </Stack>
        </Container>
      </Box>
    </>
  );
}
