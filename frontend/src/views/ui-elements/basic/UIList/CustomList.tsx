// material-ui
import Avatar from '@mui/material/Avatar';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

// assets
import KeyboardArrowUpOutlinedIcon from '@mui/icons-material/KeyboardArrowUpOutlined';
import KeyboardArrowDownOutlinedIcon from '@mui/icons-material/KeyboardArrowDownOutlined';

// ================================|| UI LIST - CUSTOM ||================================ //

export default function CustomList() {
  const avatarSuccess = {
    width: 16,
    height: 16,
    borderRadius: '5px',
    bgcolor: 'success.light',
    color: 'success.dark',
    ml: 1.875
  };
  const avatarError = {
    width: 16,
    height: 16,
    borderRadius: '5px',
    bgcolor: 'orange.light',
    color: 'orange.dark',
    ml: 1.875
  };

  return (
    <div>
      <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
          Bajaj Finsery
        </Typography>
        <Stack direction="row" sx={{ alignItems: 'center' }}>
          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
            $1839.00
          </Typography>
          <Avatar variant="rounded" sx={avatarSuccess}>
            <KeyboardArrowUpOutlinedIcon fontSize="small" color="inherit" />
          </Avatar>
        </Stack>
      </Stack>
      <Typography variant="subtitle2" sx={{ color: 'success.dark' }}>
        10% Profit
      </Typography>
      <Divider sx={{ mt: 1.5, mb: 1.5 }} />
      <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
          TTML
        </Typography>
        <Stack direction="row" sx={{ alignItems: 'center' }}>
          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
            $100.00
          </Typography>
          <Avatar variant="rounded" sx={avatarError}>
            <KeyboardArrowDownOutlinedIcon fontSize="small" color="inherit" />
          </Avatar>
        </Stack>
      </Stack>
      <Typography variant="subtitle2" sx={{ color: 'orange.dark' }}>
        10% loss
      </Typography>
      <Divider sx={{ mt: 1.5, mb: 1.5 }} />
      <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
          Reliance
        </Typography>
        <Stack direction="row" sx={{ alignItems: 'center' }}>
          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
            $200.00
          </Typography>
          <Avatar variant="rounded" sx={avatarSuccess}>
            <KeyboardArrowUpOutlinedIcon fontSize="small" color="inherit" />
          </Avatar>
        </Stack>
      </Stack>
      <Typography variant="subtitle2" sx={{ color: 'success.dark' }}>
        10% Profit
      </Typography>
      <Divider sx={{ mt: 1.5, mb: 1.5 }} />
      <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
          TTML
        </Typography>
        <Stack direction="row" sx={{ alignItems: 'center' }}>
          <Typography variant="subtitle1" sx={{ color: 'inherit' }}>
            $189.00
          </Typography>
          <Avatar variant="rounded" sx={avatarError}>
            <KeyboardArrowDownOutlinedIcon fontSize="small" color="inherit" />
          </Avatar>
        </Stack>
      </Stack>
      <Typography variant="subtitle2" sx={{ color: 'orange.dark' }}>
        10% loss
      </Typography>
    </div>
  );
}
