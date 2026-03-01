// material-ui
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// types
import { GenericCardProps } from 'types';

interface UserCountCardProps {
  primary: string;
  secondary: string;
  iconPrimary: GenericCardProps['iconPrimary'];
  color: string;
}

// =============================|| USER NUM CARD ||============================= //

export default function UserCountCard({ primary, secondary, iconPrimary, color }: UserCountCardProps) {
  const IconPrimary = iconPrimary!;
  const primaryIcon = iconPrimary ? <IconPrimary fontSize="large" /> : null;

  return (
    <Card sx={{ bgcolor: color, position: 'relative', color: '#fff' }}>
      <CardContent>
        <Box
          sx={{
            position: 'absolute',
            left: -17,
            bottom: 0 - 27,
            color: '#fff',
            transform: 'rotate(25deg)',
            '&> svg': {
              width: 100,
              height: 100,
              opacity: 0.35
            }
          }}
        >
          {primaryIcon}
        </Box>
        <Stack sx={{ gap: 1 }}>
          <Typography variant="h3" align="center" sx={{ color: 'inherit' }}>
            {secondary}
          </Typography>
          <Typography variant="body1" align="center" sx={{ color: 'inherit' }}>
            {primary}
          </Typography>
        </Stack>
      </CardContent>
    </Card>
  );
}
