'use client';

// material-ui
import { useTheme } from '@mui/material/styles';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// third party icons
import SkypeIcon from './SkypeIcon';
import MeetIcon from './MeetIcon';
import LinkedInIcon from './LinkedIn';

// project imports
import Avatar from 'ui-component/extended/Avatar';
import MainCard from 'ui-component/cards/MainCard';

// types
import { DataCardMiddleware } from 'types/org-chart';

// ==============================|| DATACARD ORGANIZATION CHART ||============================== //

function DataCard({ name, role, avatar, linkedin, meet, skype, root }: DataCardMiddleware) {
  const theme = useTheme();
  const linkHandler = (link: string) => {
    if (typeof window !== 'undefined') {
      window.open(link);
    }
  };

  return (
    <MainCard
      sx={{
        bgcolor: root ? 'secondary.light' : 'grey.100',
        ...theme.applyStyles('dark', { bgcolor: root ? 'dark.900' : 'dark.800' }),
        border: '1px solid',
        borderColor: root ? 'primary.main' : 'divider',
        width: 'max-content',
        m: '0px auto',
        direction: 'ltr'
      }}
      content={false}
    >
      <List sx={{ width: '100%', border: 'transparent', p: 1.5 }}>
        <ListItem sx={{ p: 0, alignItems: 'flex-start' }}>
          <ListItemAvatar>
            <Avatar src={avatar} size="sm" alt="user images" />
          </ListItemAvatar>
          <ListItemText
            sx={{ m: 0 }}
            primary={
              <Typography variant="subtitle1" sx={{ color: root ? `primary.dark` : `secondary.dark` }}>
                {name}
              </Typography>
            }
          />
        </ListItem>
        <Stack sx={{ pl: 7, mt: -1.75, gap: 2 }}>
          <Box sx={{ display: 'flex' }}>
            {!root && (
              <Chip
                label={role}
                slotProps={{ label: { sx: { px: 0.75 } } }}
                sx={{ fontSize: '0.625rem', height: 20 }}
                color="primary"
                variant="outlined"
                size="small"
              />
            )}
            {root && (
              <Typography sx={{ color: `secondary.dark` }} variant="caption">
                {role}
              </Typography>
            )}
          </Box>
          <Stack direction="row" sx={{ alignItems: 'center', gap: 1 }}>
            <IconButton
              onClick={() => linkHandler(linkedin)}
              size="small"
              sx={{
                bgcolor: 'background.paper',
                ...theme.applyStyles('dark', { bgcolor: 'dark.main' }),
                borderRadius: 1,
                p: 0.25
              }}
              aria-label="linkedin"
            >
              <LinkedInIcon />
            </IconButton>
            <IconButton
              onClick={() => linkHandler(meet)}
              size="small"
              sx={{
                bgcolor: 'background.paper',
                ...theme.applyStyles('dark', { bgcolor: 'dark.main' }),
                borderRadius: 1,
                p: 0.25
              }}
              aria-label="Google Meet"
            >
              <MeetIcon />
            </IconButton>
            <IconButton
              onClick={() => linkHandler(skype)}
              size="small"
              sx={{
                bgcolor: 'background.paper',
                ...theme.applyStyles('dark', { bgcolor: 'dark.main' }),
                borderRadius: 1,
                p: 0.25
              }}
              aria-label="skype"
            >
              <SkypeIcon />
            </IconButton>
          </Stack>
        </Stack>
      </List>
    </MainCard>
  );
}

export default DataCard;
