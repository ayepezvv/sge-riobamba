'use client';

// material-ui
import { useTheme } from '@mui/material/styles';
import Stack from '@mui/material/Stack';
import { DataGrid } from '@mui/x-data-grid';
import { useDemoData } from '@mui/x-data-grid-generator';
import Box from '@mui/material/Box';

// project imports
import useDataGrid from 'hooks/useDataGrid';
import MainCard from 'ui-component/cards/MainCard';
import CardSecondaryAction from 'ui-component/cards/CardSecondaryAction';
import { CSVExport } from 'views/forms/tables/TableExports';

// ==============================|| INITIALIZE COLUMN VISIBILITY DATA GRID ||============================== //

export default function VisibleColumnsModelInitialState() {
  const theme = useTheme();
  const dataGridStyles = useDataGrid();
  const { data, loading } = useDemoData({
    dataSet: 'Commodity',
    rowLength: 20,
    maxColumns: 20
  });

  const headers: any = [];
  data.columns.map((item) => {
    return headers.push({ label: item.headerName, key: item.field });
  });

  return (
    <MainCard
      content={false}
      title="Initialize Column Visibility"
      secondary={
        <Stack direction="row" sx={{ alignItems: 'center', gap: 2 }}>
          <CSVExport data={data.rows} filename={'column-visibility-data-grid-table.csv'} header={headers} />
          <CardSecondaryAction link="https://mui.com/x/react-data-grid/column-visibility/#initialize-the-visible-columns" />
        </Stack>
      }
    >
      <Box
        sx={{
          width: '100%',
          ...dataGridStyles,
          '& .MuiDataGrid-root': {
            '& .MuiDataGrid-cell--withRenderer > .positive': {
              color: 'success.main',
              ...theme.applyStyles('dark', { color: 'success.dark' })
            },
            '& .MuiDataGrid-cell--withRenderer > .negative': {
              color: 'error.main',
              ...theme.applyStyles('dark', { color: 'error.dark' })
            }
          }
        }}
      >
        <DataGrid
          {...data}
          loading={loading}
          hideFooterSelectedRowCount
          initialState={{
            ...data.initialState,
            pagination: { paginationModel: { pageSize: 5 } },
            columns: { ...data.initialState?.columns, columnVisibilityModel: { id: false, brokerId: false, status: false } }
          }}
        />
      </Box>
    </MainCard>
  );
}
