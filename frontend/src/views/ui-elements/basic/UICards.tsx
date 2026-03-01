'use client';

// material-ui
import { useTheme } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';

// project imports
import UserDetailsCard from 'ui-component/cards/UserDetailsCard';
import UserProfileCard from 'ui-component/cards/UserProfileCard';
import UserSimpleCard from 'ui-component/cards/UserSimpleCard';
import FollowerCard from 'ui-component/cards/FollowerCard';
import FriendsCard from 'ui-component/cards/FriendsCard';

import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SecondaryAction from 'ui-component/cards/CardSecondaryAction';
import { gridSpacing } from 'store/constant';

// assets
const Card1 = '/assets/images/cards/card-1.jpg';
const Card2 = '/assets/images/cards/card-2.jpg';
const Card3 = '/assets/images/cards/card-3.jpg';

const userDetails = {
  id: '#1Card_Phoebe',
  avatar: 'avatar-2.png',
  name: 'Gaetano',
  role: 'Investor Division Strategist',
  about: 'Try to connect the SAS transmitter, maybe it will index the optical hard drive!',
  email: 'alia_shields25@yahoo.com',
  contact: '253-418-5940',
  location: 'Herminahaven'
};

const userProfile = {
  id: '#9Card_Madyson',
  avatar: 'avatar-5.png',
  profile: 'profile-back-9.png',
  name: 'Madyson',
  role: 'Product Tactics Facilitator',
  status: 'Active'
};

const simpleCard = {
  id: '#6Card_Joanne',
  avatar: 'avatar-6.png',
  name: 'Joanne',
  status: 'Active'
};

const friend = {
  id: '#4Friends_Henderson',
  avatar: 'avatar-4.png',
  name: 'Henderson',
  location: 'South Antonina'
};

const follower = {
  id: '#4Followers_Henderson',
  avatar: 'avatar-8.png',
  name: 'Henderson',
  location: 'South Antonina',
  follow: 1
};

// ===============================|| UI CARDS ||=============================== //

export default function UICards() {
  const theme = useTheme();

  const cardStyle = {
    bgcolor: 'grey.50',
    border: '1px solid',
    borderColor: 'grey.100',
    ...theme.applyStyles('dark', { bgcolor: 'dark.main', borderColor: 'dark.main' })
  };

  const cardColor = { color: 'background.paper', ...theme.applyStyles('dark', { color: 'common.white' }) };

  return (
    <>
      <MainCard title="Cards" secondary={<SecondaryAction link="https://next.material-ui.com/components/cards/" />}>
        <Grid container spacing={gridSpacing}>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="User simple card">
              <UserSimpleCard {...simpleCard} />
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="Friend card">
              <FriendsCard {...friend} />
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="Follower card">
              <FollowerCard {...follower} />
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="User details card">
              <UserDetailsCard {...userDetails} />
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="User profile card">
              <UserProfileCard {...userProfile} />
            </SubCard>
          </Grid>
        </Grid>
      </MainCard>
      <MainCard
        title="Cards"
        secondary={<SecondaryAction link="https://next.material-ui.com/components/cards/" />}
        sx={{ mt: gridSpacing }}
      >
        <Grid container spacing={gridSpacing}>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="Body Content">
              <Card sx={cardStyle}>
                <CardContent>
                  <Typography variant="subtitle2">This is some text within a card body.</Typography>
                </CardContent>
              </Card>
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="Titles, Text, and Links">
              <Card sx={cardStyle}>
                <CardContent>
                  <Grid container spacing={1}>
                    <Grid size={12}>
                      <Typography variant="h5" sx={{ color: 'text.dark' }}>
                        Card Title
                      </Typography>
                    </Grid>
                    <Grid size={12}>
                      <Typography variant="subtitle1">Card Subtitle</Typography>
                    </Grid>
                    <Grid size={12}>
                      <Typography variant="subtitle2">
                        Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
                <CardActions>
                  <Button variant="text">Card Link</Button>
                  <Button variant="text" color="secondary">
                    Another
                  </Button>
                </CardActions>
              </Card>
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="Header and Footer">
              <Card sx={cardStyle}>
                <CardHeader title="Featured" />
                <Divider />
                <CardContent>
                  <Grid container spacing={1}>
                    <Grid>
                      <Typography variant="subtitle1">Special title treatment</Typography>
                    </Grid>
                    <Grid>
                      <Typography variant="subtitle2">With supporting text below as a natural lead-in to additional content.</Typography>
                    </Grid>
                  </Grid>
                </CardContent>
                <Divider />
                <CardActions>
                  <Grid container sx={{ justifyContent: 'flex-end', width: 1 }}>
                    <Grid>
                      <Button variant="contained">Go Somewhere</Button>
                    </Grid>
                  </Grid>
                </CardActions>
              </Card>
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="Left Align (Default)">
              <Card sx={cardStyle}>
                <CardContent>
                  <Grid container spacing={1}>
                    <Grid>
                      <Typography variant="subtitle1">Special title treatment</Typography>
                    </Grid>
                    <Grid>
                      <Typography variant="subtitle2">With supporting text below as a natural lead-in to additional content.</Typography>
                    </Grid>
                  </Grid>
                </CardContent>
                <CardActions>
                  <Grid container>
                    <Grid>
                      <Button variant="contained">Go Somewhere</Button>
                    </Grid>
                  </Grid>
                </CardActions>
              </Card>
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="Center Align">
              <Card sx={cardStyle}>
                <CardContent>
                  <Grid container spacing={1} sx={{ justifyContent: 'center', alignItems: 'center' }}>
                    <Grid>
                      <Typography variant="subtitle1">Special title treatment</Typography>
                    </Grid>
                    <Grid>
                      <Typography variant="subtitle2" sx={{ textAlign: 'center' }}>
                        With supporting text below as a natural lead-in to additional content.
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
                <CardActions>
                  <Grid container sx={{ justifyContent: 'center', width: 1 }}>
                    <Grid>
                      <Button variant="contained">Go Somewhere</Button>
                    </Grid>
                  </Grid>
                </CardActions>
              </Card>
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="Right Align">
              <Card sx={cardStyle}>
                <CardContent>
                  <Grid container spacing={1} sx={{ justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                    <Grid>
                      <Typography variant="subtitle1">Special title treatment</Typography>
                    </Grid>
                    <Grid>
                      <Typography variant="subtitle2" sx={{ textAlign: 'right' }}>
                        With supporting text below as a natural lead-in to additional content.
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
                <CardActions>
                  <Grid container sx={{ justifyContent: 'flex-end', width: 1 }}>
                    <Grid>
                      <Button variant="contained">Go Somewhere</Button>
                    </Grid>
                  </Grid>
                </CardActions>
              </Card>
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="Image Cap">
              <Card sx={cardStyle}>
                <CardMedia component="img" image={Card1} title="Card 1" />
                <CardContent>
                  <Grid container spacing={1} sx={{ alignItems: 'center' }}>
                    <Grid>
                      <Typography variant="subtitle1">Special title</Typography>
                    </Grid>
                    <Grid>
                      <Typography variant="subtitle2">With supporting text below as a natural lead-in to additional content.</Typography>
                    </Grid>
                  </Grid>
                </CardContent>
                <CardActions>
                  <Grid container>
                    <Grid>
                      <Typography variant="caption">Last updated 3 mins ago</Typography>
                    </Grid>
                  </Grid>
                </CardActions>
              </Card>
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="Image Cap">
              <Card sx={cardStyle}>
                <CardContent>
                  <Grid container spacing={1} sx={{ alignItems: 'center' }}>
                    <Grid>
                      <Typography variant="subtitle1">Special title</Typography>
                    </Grid>
                    <Grid>
                      <Typography variant="subtitle2">With supporting text below as a natural lead-in to additional content.</Typography>
                    </Grid>
                  </Grid>
                </CardContent>
                <CardActions>
                  <Grid container>
                    <Grid>
                      <Typography variant="caption">Last updated 3 mins ago</Typography>
                    </Grid>
                  </Grid>
                </CardActions>
                <CardMedia component="img" image={Card2} title="Card 2" />
              </Card>
            </SubCard>
          </Grid>
          <Grid size={{ xs: 12, lg: 4 }}>
            <SubCard title="Image Overlay">
              <Card sx={cardStyle}>
                <CardMedia image={Card3} title="Card 3">
                  <CardContent sx={{ minHeight: 240, color: 'common.white' }}>
                    <Grid container spacing={1} sx={{ alignItems: 'center' }}>
                      <Grid>
                        <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                          Special title
                        </Typography>
                      </Grid>
                      <Grid>
                        <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                          With supporting text below as a natural lead-in to additional content.
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                  <CardActions>
                    <Grid container>
                      <Grid>
                        <Typography variant="caption" sx={{ color: 'common.white' }}>
                          Last updated 3 mins ago
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardActions>
                </CardMedia>
              </Card>
            </SubCard>
          </Grid>
          <Grid size={12}>
            <SubCard title="Color Card">
              <Grid container spacing={gridSpacing}>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ bgcolor: 'primary.main', ...cardColor }}>
                    <CardHeader
                      title={
                        <Typography variant="h5" sx={{ ...cardColor }}>
                          Primary
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Primary Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card
                    sx={{ bgcolor: 'secondary.main', color: 'secondary.light', ...theme.applyStyles('dark', { color: 'common.white' }) }}
                  >
                    <CardHeader
                      title={
                        <Typography variant="h5" sx={{ color: 'secondary.light', ...theme.applyStyles('dark', { color: 'common.white' }) }}>
                          Secondary
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Secondary Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ bgcolor: 'error.main', ...cardColor }}>
                    <CardHeader
                      title={
                        <Typography variant="h5" sx={{ ...cardColor }}>
                          Error
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Error Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ bgcolor: 'success.dark', ...cardColor }}>
                    <CardHeader
                      title={
                        <Typography variant="h5" sx={{ ...cardColor }}>
                          Success
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Success Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ bgcolor: 'warning.dark', ...cardColor }}>
                    <CardHeader
                      title={
                        <Typography variant="h5" sx={{ ...cardColor }}>
                          Warning
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'common.white' }}>
                            Warning Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'common.white' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ bgcolor: 'info.main', ...cardColor }}>
                    <CardHeader
                      title={
                        <Typography variant="h5" sx={{ ...cardColor }}>
                          Info
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Info Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ bgcolor: 'dark.main', color: 'common.white' }}>
                    <CardHeader
                      title={
                        <Typography variant="h5" sx={{ color: 'common.white' }}>
                          Dark
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Dark Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </SubCard>
          </Grid>
          <Grid size={12}>
            <SubCard title="Outlined Card">
              <Grid container spacing={gridSpacing}>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ border: '1px solid', borderColor: 'primary.main' }}>
                    <CardHeader
                      sx={{ borderBottom: '1px solid', borderBottomColor: 'primary.main' }}
                      title={
                        <Typography variant="h5" sx={{ color: 'primary.main' }}>
                          Primary
                        </Typography>
                      }
                    />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Primary Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ border: '1px solid', borderColor: 'secondary.main' }}>
                    <CardHeader
                      sx={{ borderBottom: '1px solid', borderBottomColor: 'secondary.main' }}
                      title={
                        <Typography variant="h5" sx={{ color: 'secondary.main' }}>
                          Secondary
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Secondary Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ border: '1px solid', borderColor: 'error.main' }}>
                    <CardHeader
                      sx={{ borderBottom: '1px solid', borderBottomColor: 'error.main' }}
                      title={
                        <Typography variant="h5" sx={{ color: 'error.main' }}>
                          Error
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Error Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ border: '1px solid', borderColor: 'orange.main' }}>
                    <CardHeader
                      sx={{ borderBottom: '1px solid', borderBottomColor: 'orange.main' }}
                      title={
                        <Typography variant="h5" sx={{ color: 'orange.main' }}>
                          Orange
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Orange Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ border: '1px solid', borderColor: 'success.main' }}>
                    <CardHeader
                      sx={{ borderBottom: '1px solid', borderBottomColor: 'success.main' }}
                      title={
                        <Typography variant="h5" sx={{ color: 'success.main' }}>
                          Success
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Success Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ border: '1px solid', borderColor: 'warning.main' }}>
                    <CardHeader
                      sx={{ borderBottom: '1px solid', borderBottomColor: 'warning.main' }}
                      title={
                        <Typography variant="h5" sx={{ color: 'warning.main' }}>
                          Warning
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Warning Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ border: '1px solid', borderColor: 'info.main' }}>
                    <CardHeader
                      sx={{ borderBottom: '1px solid', borderBottomColor: 'info.main' }}
                      title={
                        <Typography variant="h5" sx={{ color: 'info.main' }}>
                          Info
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Info Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Card sx={{ border: '1px solid', borderColor: 'grey.500' }}>
                    <CardHeader
                      sx={{ borderBottom: '1px solid', borderBottomColor: 'grey.500' }}
                      title={
                        <Typography variant="h5" sx={{ color: 'dark.main', ...theme.applyStyles('dark', { color: 'dark.light' }) }}>
                          Dark
                        </Typography>
                      }
                    />
                    <Divider />
                    <CardContent>
                      <Grid container spacing={1}>
                        <Grid>
                          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
                            Dark Card Title
                          </Typography>
                        </Grid>
                        <Grid>
                          <Typography variant="subtitle2" sx={{ color: 'inherit' }}>
                            Some quick example text to build on the card title and make up the bulk of the card&apos;s content.
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </SubCard>
          </Grid>
        </Grid>
      </MainCard>
    </>
  );
}
