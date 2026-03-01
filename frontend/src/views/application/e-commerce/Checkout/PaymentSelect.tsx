// material-ui
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import { PaymentOptionsProps } from 'types/e-commerce';

// ==============================|| CHECKOUT PAYMENT - OPTIONS ||============================== //

export default function PaymentSelect({ item }: { item: PaymentOptionsProps }) {
  return (
    <SubCard content={false}>
      <Box sx={{ p: 2 }}>
        <FormControlLabel
          value={item.value}
          control={<Radio />}
          label={
            <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'center', width: 1, gap: 1 }}>
              <Stack sx={{ width: 1 }}>
                <Typography variant="subtitle1">{item.title}</Typography>
                <Typography variant="caption">{item.caption}</Typography>
              </Stack>
              <Box
                sx={{
                  backgroundImage: `url(${item.image})`,
                  backgroundSize: 'contain',
                  backgroundPosition: 'right',
                  borderColor: 'error.light',
                  ...item.size
                }}
              />
            </Stack>
          }
          slotProps={{ typography: { sx: { width: 1 } } }}
          sx={{ width: 1, '& .MuiSvgIcon-root': { fontSize: 32 } }}
        />
      </Box>
    </SubCard>
  );
}
