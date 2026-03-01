'use client';

import { useState } from 'react';

// material-ui
import Button from '@mui/material/Button';
import CardActions from '@mui/material/CardActions';
import Checkbox from '@mui/material/Checkbox';
import Divider from '@mui/material/Divider';
import FormControlLabel from '@mui/material/FormControlLabel';
import Stack from '@mui/material/Stack';
import Switch from '@mui/material/Switch';
import Typography from '@mui/material/Typography';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import AnimateButton from 'ui-component/extended/AnimateButton';

const titleSX = {
  fontWeight: 600,
  display: 'flex',
  alignItems: 'center',
  '& > svg': {
    mr: 1
  }
};

// ==============================|| PROFILE 1 - SETTINGS ||============================== //

export default function Settings() {
  const [state1, setState1] = useState({ checkedA: true, checkedB: false });
  const [state2, setState2] = useState({ checkedA: true, checkedB: false, checkedC: true });
  const [state3, setState3] = useState({ checkedA: true, checkedB: true, checkedC: false });

  const handleSwitchChange1 = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState1({ ...state1, [event.target.name]: event.target.checked });
  };
  const handleSwitchChange2 = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState2({ ...state2, [event.target.name]: event.target.checked });
  };
  const handleSwitchChange3 = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState3({ ...state3, [event.target.name]: event.target.checked });
  };

  const [state, setState] = useState({ checkedA: true, checkedB: true, checkedC: false, checkedD: false, checkedE: false });
  const handleChangeState = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState({ ...state, [event.target.name]: event.target.checked });
  };

  return (
    <SubCard title="Email Settings">
      <Stack sx={{ gap: 3 }}>
        <Stack>
          <Typography variant="subtitle1">Setup Email Notification</Typography>
          <FormControlLabel
            control={<Switch checked={state1.checkedA} onChange={handleSwitchChange1} name="checkedA" color="primary" />}
            label="Email Notification"
          />
          <FormControlLabel
            control={<Switch checked={state1.checkedB} onChange={handleSwitchChange1} name="checkedB" color="primary" />}
            label="Send Copy To Personal Email"
          />
        </Stack>
        <Divider />
        <Typography variant="h5" component="span" sx={{ ...titleSX, textTransform: 'uppercase' }}>
          Activity Related Emails
        </Typography>
        <Stack>
          <Typography variant="subtitle1">When to email?</Typography>
          <FormControlLabel
            control={<Switch checked={state2.checkedA} onChange={handleSwitchChange2} name="checkedA" color="primary" />}
            label="have new notifications"
          />
          <FormControlLabel
            control={<Switch checked={state2.checkedB} onChange={handleSwitchChange2} name="checkedB" color="primary" />}
            label="you're sent a direct message"
          />
          <FormControlLabel
            control={<Switch checked={state2.checkedC} onChange={handleSwitchChange2} name="checkedC" color="primary" />}
            label="Someone adds you as a connection"
          />
        </Stack>
        <Stack>
          <Typography variant="subtitle1">When to escalate emails?</Typography>
          <FormControlLabel
            control={<Switch checked={state3.checkedA} onChange={handleSwitchChange3} name="checkedA" color="primary" />}
            label="Upon new order"
          />
          <FormControlLabel
            control={<Switch checked={state3.checkedB} onChange={handleSwitchChange3} name="checkedB" color="primary" />}
            label="New membership approval"
          />
          <FormControlLabel
            control={<Switch checked={state3.checkedC} onChange={handleSwitchChange3} name="checkedC" color="primary" />}
            label="Member registration"
          />
        </Stack>
        <Divider />
        <Typography variant="h5" component="span" sx={{ ...titleSX, textTransform: 'uppercase' }}>
          Updates From System Notification
        </Typography>
        <Stack>
          <Typography variant="subtitle1">Email you with?</Typography>
          <FormControlLabel
            control={<Checkbox checked={state.checkedA} onChange={handleChangeState} name="checkedA" color="primary" />}
            label="News about PCT-themes products and feature updates"
          />
          <FormControlLabel
            control={<Checkbox checked={state.checkedB} onChange={handleChangeState} name="checkedB" color="primary" />}
            label="Tips on getting more out of PCT-themes"
          />
          <FormControlLabel
            control={<Checkbox checked={state.checkedC} onChange={handleChangeState} name="checkedC" color="primary" />}
            label="Things you missed since you last logged into PCT-themes"
          />
          <FormControlLabel
            control={<Checkbox checked={state.checkedD} onChange={handleChangeState} name="checkedD" color="primary" />}
            label="News about products and other services"
          />
          <FormControlLabel
            control={<Checkbox checked={state.checkedE} onChange={handleChangeState} name="checkedE" color="primary" />}
            label="Tips and Document business products"
          />
        </Stack>
      </Stack>
      <Divider sx={{ mt: 2 }} />
      <CardActions sx={{ p: 0, pt: 3 }}>
        <Stack direction="row" sx={{ justifyContent: 'flex-end', width: 1, gap: 2 }}>
          <Button sx={{ color: 'error.main' }}>Clear</Button>
          <AnimateButton>
            <Button variant="contained">Update</Button>
          </AnimateButton>
        </Stack>
      </CardActions>
    </SubCard>
  );
}
