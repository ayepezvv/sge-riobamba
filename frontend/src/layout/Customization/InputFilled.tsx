'use client';

// material-ui
import { useColorScheme } from '@mui/material/styles';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Tooltip from '@mui/material/Tooltip';

// project imports
import { ThemeMode } from 'config';
import Avatar from 'ui-component/extended/Avatar';
import useConfig from 'hooks/useConfig';

// ==============================|| CUSTOMIZATION - INPUT FILLED ||============================== //

export default function InputFilled() {
  const { colorScheme } = useColorScheme();
  const {
    state: { outlinedFilled },
    setField
  } = useConfig();

  const changeInputBackground = (e: any) => {
    const newOutlinedFilled = e.target.value === 'filled';
    if (newOutlinedFilled !== outlinedFilled) {
      setField('outlinedFilled', newOutlinedFilled);
    }
  };

  return (
    <Stack direction="row" sx={{ alignItems: 'center', pb: 2, px: 2, justifyContent: 'space-between' }}>
      <Typography variant="h5">INPUT BACKGROUND</Typography>
      <RadioGroup row aria-label="layout" value={outlinedFilled} onChange={changeInputBackground} name="row-radio-buttons-group">
        <Tooltip title="With Background">
          <FormControlLabel
            control={<Radio value="filled" sx={{ display: 'none' }} />}
            label={
              <Avatar
                size="md"
                variant="rounded"
                outline
                sx={{
                  mr: 1,
                  width: 48,
                  height: 30,
                  bgcolor: colorScheme === ThemeMode.DARK ? 'dark.800' : 'grey.50',
                  ...(!outlinedFilled && { borderColor: 'divider' })
                }}
              >
                {' '}
              </Avatar>
            }
          />
        </Tooltip>
        <Tooltip title="WithOut Background">
          <FormControlLabel
            control={<Radio value="outlined" sx={{ display: 'none' }} />}
            label={
              <Avatar size="md" variant="rounded" outline sx={{ width: 48, height: 30, ...(outlinedFilled && { borderColor: 'divider' }) }}>
                {' '}
              </Avatar>
            }
          />
        </Tooltip>
      </RadioGroup>
    </Stack>
  );
}
