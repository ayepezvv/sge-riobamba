'use client';

// material-ui
import { useTheme } from '@mui/material/styles';
import Chip from '@mui/material/Chip';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import { gridSpacing } from 'store/constant';

// assets
import CalendarTodayTwoToneIcon from '@mui/icons-material/CalendarTodayTwoTone';
import EmailTwoToneIcon from '@mui/icons-material/EmailTwoTone';
import PhoneAndroidTwoToneIcon from '@mui/icons-material/PhoneAndroidTwoTone';

const detailsIconSX = {
  width: 15,
  height: 15,
  verticalAlign: 'text-top',
  mr: 0.5,
  mt: 0.25
};

// table data
function createData(product: string, description: string, quantity: string, amount: string, total: string) {
  return { product, description, quantity, amount, total };
}

const rows = [
  createData('Logo Design', 'lorem ipsum dolor sit amat, connecter adieu siccing eliot', '6', '$200.00', '$1200.00'),
  createData('Landing Page', 'lorem ipsum dolor sit amat, connecter adieu siccing eliot', '7', '$100.00', '$700.00'),
  createData('Admin Template', 'lorem ipsum dolor sit amat, connecter adieu siccing eliot', '5', '$150.00', '$750.00')
];

export default function Details() {
  const theme = useTheme();

  return (
    <Grid container spacing={gridSpacing}>
      <Grid size={12}>
        <SubCard title="Customer" secondary={<Typography variant="subtitle1">Placed on 12.07.2018 10:00</Typography>}>
          <Grid container spacing={gridSpacing}>
            <Grid size={12}>
              <Grid container spacing={3}>
                <Grid>
                  <Typography variant="body2">
                    <CalendarTodayTwoToneIcon sx={detailsIconSX} /> Sophia Hale
                  </Typography>
                </Grid>
                <Grid>
                  <Typography variant="body2">
                    <PhoneAndroidTwoToneIcon sx={detailsIconSX} /> 070 123 4567
                  </Typography>
                </Grid>
                <Grid>
                  <Typography variant="body2">
                    <EmailTwoToneIcon sx={detailsIconSX} /> example@mail.com
                  </Typography>
                </Grid>
              </Grid>
            </Grid>
            <Grid size={12}>
              <Divider />
            </Grid>
            <Grid size={12}>
              <Grid container spacing={gridSpacing}>
                <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                  <Stack sx={{ gap: 2 }}>
                    <Typography variant="h4">Payment method</Typography>
                    <Stack sx={{ gap: 0 }}>
                      <Typography variant="h6" sx={{ mb: 1 }}>
                        Credit Card
                      </Typography>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Transaction ID :</Typography>
                        <Typography variant="body2">000001-TXT</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Amount :</Typography>
                        <Typography variant="body2">$2500</Typography>
                      </Stack>
                    </Stack>
                  </Stack>
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                  <Stack sx={{ gap: 2 }}>
                    <Typography variant="h4">Shipping method</Typography>
                    <Stack sx={{ gap: 0 }}>
                      <Typography variant="h6" sx={{ mb: 1 }}>
                        Carrier
                      </Typography>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Tracking Code :</Typography>
                        <Typography variant="body2">FX-012345-6</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Date :</Typography>
                        <Typography variant="body2">12.15.2018</Typography>
                      </Stack>
                    </Stack>
                  </Stack>
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                  <Stack sx={{ mt: { xs: 0, md: 3 }, gap: 0 }}>
                    <Stack direction="row" sx={{ gap: 1 }}>
                      <Typography variant="subtitle1">Fulfillment status :</Typography>
                      <Typography variant="body2">Delivered</Typography>
                    </Stack>
                    <Stack direction="row" sx={{ gap: 1 }}>
                      <Typography variant="subtitle1">Payment status :</Typography>
                      <Chip label="Paid" variant="outlined" size="small" color="success" />
                    </Stack>
                  </Stack>
                </Grid>
              </Grid>
            </Grid>
            <Grid size={12}>
              <Divider />
            </Grid>
            <Grid size={12}>
              <Grid container spacing={gridSpacing}>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Stack sx={{ gap: 2 }}>
                    <Typography variant="h4">Billing address</Typography>
                    <Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">First name :</Typography>
                        <Typography variant="body2">Joseph</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Last name :</Typography>
                        <Typography variant="body2">William</Typography>
                      </Stack>
                    </Stack>
                    <Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Address :</Typography>
                        <Typography variant="body2">4898 Joanne Lane street</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">City :</Typography>
                        <Typography variant="body2">Boston</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Country :</Typography>
                        <Typography variant="body2">United States</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">State :</Typography>
                        <Typography variant="body2">Massachusetts</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Zip code :</Typography>
                        <Typography variant="body2">02110</Typography>
                      </Stack>
                    </Stack>
                    <Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Phone :</Typography>
                        <Typography variant="body2">+1 (070) 123-4567</Typography>
                      </Stack>
                    </Stack>
                  </Stack>
                </Grid>
                <Grid size={{ sm: 6, md: 4 }}>
                  <Stack sx={{ gap: 2 }}>
                    <Typography variant="h4">Shipping address</Typography>
                    <Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">First name :</Typography>
                        <Typography variant="body2">Sara</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Last name :</Typography>
                        <Typography variant="body2">Soudan</Typography>
                      </Stack>
                    </Stack>
                    <Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Address :</Typography>
                        <Typography variant="body2">4898 Joanne Lane street</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">City :</Typography>
                        <Typography variant="body2">Boston</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Country :</Typography>
                        <Typography variant="body2">United States</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">State :</Typography>
                        <Typography variant="body2">Massachusetts</Typography>
                      </Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Zip code :</Typography>
                        <Typography variant="body2">02110</Typography>
                      </Stack>
                    </Stack>
                    <Stack>
                      <Stack direction="row" sx={{ gap: 1 }}>
                        <Typography variant="subtitle1">Phone :</Typography>
                        <Typography variant="body2">+1 (070) 123-4567</Typography>
                      </Stack>
                    </Stack>
                  </Stack>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </SubCard>
      </Grid>
      <Grid size={12}>
        <SubCard title="Products" content={false}>
          <Grid container spacing={3}>
            <Grid size={12}>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell sx={{ pl: 3 }}>Description</TableCell>
                      <TableCell align="right">Quantity</TableCell>
                      <TableCell align="right">Amount</TableCell>
                      <TableCell align="right">Total</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {rows.map((row, index) => (
                      <TableRow key={index}>
                        <TableCell sx={{ pl: 3 }}>
                          <Typography variant="subtitle1">{row.product}</Typography>
                          <Typography variant="body2">{row.description}</Typography>
                        </TableCell>
                        <TableCell align="right">{row.quantity}</TableCell>
                        <TableCell align="right">{row.amount}</TableCell>
                        <TableCell align="right">{row.total}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>
            <Grid size={12}>
              <SubCard sx={{ mx: 3, mb: 3, bgcolor: 'primary.light', ...theme.applyStyles('dark', { bgcolor: 'dark.main' }) }}>
                <Grid container spacing={gridSpacing} sx={{ justifyContent: 'flex-end' }}>
                  <Grid size={{ sm: 6, md: 4 }}>
                    <Grid container spacing={2}>
                      <Grid size={12}>
                        <Grid container spacing={1}>
                          <Grid size={6}>
                            <Typography variant="subtitle1" sx={{ textAlign: 'right' }}>
                              Sub Total :
                            </Typography>
                          </Grid>
                          <Grid size={6}>
                            <Typography variant="body2" sx={{ textAlign: 'right' }}>
                              $2650
                            </Typography>
                          </Grid>
                          <Grid size={6}>
                            <Typography variant="subtitle1" sx={{ textAlign: 'right' }}>
                              Taxes (10%) :
                            </Typography>
                          </Grid>
                          <Grid size={6}>
                            <Typography variant="body2" sx={{ textAlign: 'right' }}>
                              $265
                            </Typography>
                          </Grid>
                          <Grid size={6}>
                            <Typography variant="subtitle1" sx={{ textAlign: 'right' }}>
                              Discount (5%) :
                            </Typography>
                          </Grid>
                          <Grid size={6}>
                            <Typography variant="body2" sx={{ textAlign: 'right' }}>
                              $145.75
                            </Typography>
                          </Grid>
                        </Grid>
                      </Grid>
                      <Grid size={12}>
                        <Divider sx={{ bgcolor: 'dark.main' }} />
                      </Grid>
                      <Grid size={12}>
                        <Grid container spacing={1}>
                          <Grid size={6}>
                            <Typography variant="subtitle1" sx={{ textAlign: 'right', color: 'primary.main' }}>
                              Total :
                            </Typography>
                          </Grid>
                          <Grid size={6}>
                            <Typography variant="subtitle1" sx={{ textAlign: 'right', color: 'primary.main' }}>
                              $2769.25
                            </Typography>
                          </Grid>
                        </Grid>
                      </Grid>
                    </Grid>
                  </Grid>
                </Grid>
              </SubCard>
            </Grid>
          </Grid>
        </SubCard>
      </Grid>
    </Grid>
  );
}
