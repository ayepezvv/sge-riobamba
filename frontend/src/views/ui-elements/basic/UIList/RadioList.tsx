'use client';

import React from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Stack from '@mui/material/Stack';
import Switch from '@mui/material/Switch';
import Typography from '@mui/material/Typography';

// ================================|| UI LIST - RADIO ||================================ //

export default function RadioList() {
  const theme = useTheme();
  const [sdm, setSdm] = React.useState(true);
  const [notification, setNotification] = React.useState(false);

  return (
    <Card sx={{ bgcolor: 'primary.light', ...theme.applyStyles('dark', { bgcolor: 'dark.800' }), mb: 2, mt: 2 }}>
      <CardContent>
        <Stack sx={{ gap: 3 }}>
          <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="subtitle1">Start DND Mode</Typography>
            <Switch size="small" color="primary" checked={sdm} onChange={(e) => setSdm(e.target.checked)} name="sdm" />
          </Stack>
          <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="subtitle1">Allow Notifications</Typography>
            <Switch size="small" checked={notification} onChange={(e) => setNotification(e.target.checked)} name="sdm" />
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}
