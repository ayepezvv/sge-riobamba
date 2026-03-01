// material-ui
import Stack from '@mui/material/Stack';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import SimpleBar from 'ui-component/third-party/SimpleBar';

type ProductCreateDataType = { sales: string; product: string; price: string; colorClass: string };

// table data
function createData(sales: string, product: string, price: string, colorClass: string = '') {
  return { sales, product, price, colorClass };
}

const rows: ProductCreateDataType[] = [
  createData('2136', 'HeadPhone', '$ 926.23'),
  createData('2546', 'Iphone 6', '$ 485.85'),
  createData('2681', 'Jacket', '$ 786.4'),
  createData('2756', 'HeadPhone', '$ 563.45'),
  createData('8765', 'Sofa', '$ 769.45'),
  createData('3652', 'Iphone 7', '$ 754.45'),
  createData('7456', 'Jacket', '$ 743.23'),
  createData('6502', 'T-Shirt', '$ 642.23')
];

// ===========================|| DATA WIDGET - PRODUCT SALES CARD ||=========================== //

export default function ProductSales() {
  return (
    <MainCard title="Product Sales" content={false}>
      <Stack direction="row" sx={{ justifyContent: 'space-around', alignItems: 'center', p: 2.5 }}>
        <Stack sx={{ gap: 1, alignItems: 'center', justifyContent: 'center' }}>
          <Typography variant="subtitle2">Earning</Typography>
          <Typography variant="h3">20,569$</Typography>
        </Stack>
        <Stack sx={{ gap: 1, alignItems: 'center', justifyContent: 'center' }}>
          <Typography variant="subtitle2">Yesterday</Typography>
          <Typography variant="h3">580$</Typography>
        </Stack>
        <Stack sx={{ gap: 1, alignItems: 'center', justifyContent: 'center' }}>
          <Typography variant="subtitle2">This Week</Typography>
          <Typography variant="h3">5,789$</Typography>
        </Stack>
      </Stack>
      <SimpleBar style={{ height: 345, padding: 0 }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ pl: 3 }}>Last Sales</TableCell>
                <TableCell>Name Product</TableCell>
                <TableCell align="right" sx={{ pr: 3 }}>
                  Price
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row, index) => (
                <TableRow hover key={index}>
                  <TableCell sx={{ pl: 3 }}>
                    <span className={row.colorClass}>{row.sales}</span>
                  </TableCell>
                  <TableCell>{row.product}</TableCell>
                  <TableCell align="right" sx={{ pr: 3 }}>
                    <span>{row.price}</span>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </SimpleBar>
    </MainCard>
  );
}
