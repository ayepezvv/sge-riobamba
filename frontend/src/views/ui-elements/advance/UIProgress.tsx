'use client';

import React from 'react';

// material-ui
import { styled } from '@mui/material/styles';
import { linearProgressClasses } from '@mui/material/LinearProgress';
import CircularProgress, { CircularProgressProps } from '@mui/material/CircularProgress';
import Grid from '@mui/material/Grid';
import LinearProgress, { LinearProgressProps } from '@mui/material/LinearProgress';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SecondaryAction from 'ui-component/cards/CardSecondaryAction';
import { gridSpacing } from 'store/constant';

// customized with label
function CircularProgressWithLabel({ value, ...other }: CircularProgressProps) {
  return (
    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
      <CircularProgress variant="determinate" value={value} {...other} />
      <Box
        sx={{
          top: 0,
          left: 0,
          bottom: 0,
          right: 0,
          position: 'absolute',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>{`${Math.round(value!)}%`}</Typography>
      </Box>
    </Box>
  );
}

function LinearProgressWithLabel({ value, ...other }: LinearProgressProps) {
  return (
    <Stack direction="row" sx={{ alignItems: 'center' }}>
      <Box sx={{ width: 1, mr: 1 }}>
        <LinearProgress variant="determinate" value={value} {...other} />
      </Box>
      <Box sx={{ minWidth: 35 }}>
        <Typography variant="body2" sx={{ color: 'text.secondary' }}>{`${Math.round(value!)}%`}</Typography>
      </Box>
    </Stack>
  );
}

// style constant
const BorderLinearProgress = styled(LinearProgress)(() => ({
  height: 10,
  borderRadius: 5,
  [`& .${linearProgressClasses.bar}`]: { borderRadius: 5 }
}));

// ==============================|| UI PROGRESS ||============================== //

export default function UIProgress() {
  const [progress, setProgress] = React.useState(0);
  const [buffer, setBuffer] = React.useState(10);

  const progressRef = React.useRef(() => {});
  React.useEffect(() => {
    progressRef.current = () => {
      if (progress > 100) {
        setProgress(0);
        setBuffer(10);
      } else {
        const diff = Math.random() * 10;
        const diff2 = Math.random() * 10;
        setProgress(progress + diff);
        setBuffer(progress + diff + diff2);
      }
    };
  });

  React.useEffect(() => {
    const timer = setInterval(() => {
      progressRef.current();
    }, 500);

    return () => {
      clearInterval(timer);
    };
  }, []);

  return (
    <MainCard title="Progress" secondary={<SecondaryAction link="https://next.material-ui.com/components/progress/" />}>
      <Grid container spacing={gridSpacing}>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <SubCard title="Circular Indeterminate">
            <Stack direction="row" sx={{ justifyContent: 'center', gap: 2 }}>
              <CircularProgress aria-label="progress" />
              <CircularProgress color="secondary" aria-label="progress with secondary color" />
            </Stack>
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <SubCard title="Circular Determinate">
            <Stack direction="row" sx={{ justifyContent: 'center', gap: 2 }}>
              <CircularProgress variant="determinate" value={25} aria-label="progress 25%" />
              <CircularProgress variant="determinate" value={50} aria-label="progress 50%" />
              <CircularProgress variant="determinate" value={75} aria-label="progress 75%" />
              <CircularProgress variant="determinate" value={100} aria-label="progress 100%" />
              <CircularProgress variant="determinate" value={50} aria-label="progress 50%" />
              <CircularProgress variant="determinate" value={progress} aria-label="progress" />
            </Stack>
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <SubCard title="Circular Label">
            <Stack direction="row" sx={{ justifyContent: 'center' }}>
              <CircularProgressWithLabel value={progress} aria-label="circular progress" />
            </Stack>
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6 }}>
          <SubCard title="Linear Indeterminate">
            <Stack sx={{ gap: 2 }}>
              <LinearProgress aria-label="linear progress" />
              <LinearProgress color="secondary" aria-label="linear progress with secondary color" />
            </Stack>
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6 }}>
          <SubCard title="Linear Label">
            <LinearProgressWithLabel value={progress} aria-label="linear label progress" />
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6 }}>
          <SubCard title="Linear Determinate">
            <LinearProgress variant="determinate" value={progress} aria-label="linear Determinate progress" />
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6 }}>
          <SubCard title="Linear Buffer">
            <LinearProgress variant="buffer" value={progress} valueBuffer={buffer} aria-label="linear Buffer progress" />
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6 }}>
          <SubCard title="Color">
            <Stack sx={{ gap: 3 }}>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 2 }}>
                <Typography variant="caption">Progress</Typography>
                <LinearProgress
                  variant="determinate"
                  color="secondary"
                  value={progress}
                  sx={{ width: 1 }}
                  aria-label="secondary color progress"
                />

                <Typography variant="h6">{Math.round(progress)}%</Typography>
              </Stack>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 2 }}>
                <Typography variant="caption">Progress</Typography>
                <LinearProgress
                  color="success"
                  variant="determinate"
                  value={progress}
                  aria-label="success color progress"
                  sx={{ width: 1 }}
                />
                <Typography variant="h6">{Math.round(progress)}%</Typography>
              </Stack>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 2 }}>
                <Typography variant="caption">Progress</Typography>
                <LinearProgress color="error" variant="determinate" value={progress} aria-label="danger color progress" sx={{ width: 1 }} />
                <Typography variant="h6">{Math.round(progress)}%</Typography>
              </Stack>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 2 }}>
                <Typography variant="caption">Progress</Typography>
                <LinearProgress
                  color="warning"
                  variant="determinate"
                  value={progress}
                  aria-label="warning color progress"
                  sx={{ width: 1 }}
                />
                <Typography variant="h6">{Math.round(progress)}%</Typography>
              </Stack>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 2 }}>
                <Typography variant="caption">Progress</Typography>
                <LinearProgress color="info" variant="determinate" value={progress} aria-label="info color progress" sx={{ width: 1 }} />
                <Typography variant="h6">{Math.round(progress)}%</Typography>
              </Stack>
            </Stack>
          </SubCard>
        </Grid>
        <Grid size={{ xs: 12, sm: 6 }}>
          <SubCard title="Color With Height">
            <Stack sx={{ gap: 3 }}>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 2 }}>
                <Typography variant="caption">Progress</Typography>
                <BorderLinearProgress
                  variant="determinate"
                  color="secondary"
                  value={progress}
                  aria-label="secondary color progress"
                  sx={{ width: 1 }}
                />
                <Typography variant="h6">{Math.round(progress)}%</Typography>
              </Stack>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 2 }}>
                <Typography variant="caption">Progress</Typography>
                <BorderLinearProgress
                  color="success"
                  variant="determinate"
                  value={progress}
                  aria-label="success color progress"
                  sx={{ width: 1 }}
                />
                <Typography variant="h6">{Math.round(progress)}%</Typography>
              </Stack>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 2 }}>
                <Typography variant="caption">Progress</Typography>
                <BorderLinearProgress
                  color="error"
                  variant="determinate"
                  value={progress}
                  aria-label="danger color progress"
                  sx={{ width: 1 }}
                />
                <Typography variant="h6">{Math.round(progress)}%</Typography>
              </Stack>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 2 }}>
                <Typography variant="caption">Progress</Typography>
                <BorderLinearProgress
                  color="warning"
                  variant="determinate"
                  value={progress}
                  aria-label="warning color progress"
                  sx={{ width: 1 }}
                />
                <Typography variant="h6">{Math.round(progress)}%</Typography>
              </Stack>
              <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', gap: 2 }}>
                <Typography variant="caption">Progress</Typography>
                <BorderLinearProgress
                  color="info"
                  variant="determinate"
                  value={progress}
                  aria-label="info color progress"
                  sx={{ width: 1 }}
                />
                <Typography variant="h6">{Math.round(progress)}%</Typography>
              </Stack>
            </Stack>
          </SubCard>
        </Grid>
      </Grid>
    </MainCard>
  );
}
