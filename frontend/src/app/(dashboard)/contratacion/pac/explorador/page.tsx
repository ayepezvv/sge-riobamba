'use client';
import { useEffect, useState } from 'react';
import API_BASE_URL from "@/config/api";
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  TextField,
  Typography,
  InputAdornment
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';
import { IconSearch } from '@tabler/icons-react';

export default function ExploradorPacPage() {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchItems = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/contratacion/pac/items/all`, {
        headers: { 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` }
      });
      if (res.ok) {
        const items = await res.json();
        setData(items);
        setFilteredData(items);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  useEffect(() => {
    if (!searchTerm) {
      setFilteredData(data);
      return;
    }
    const lower = searchTerm.toLowerCase();
    const filtered = data.filter((row: any) => 
      (row.descripcion && row.descripcion.toLowerCase().includes(lower)) ||
      (row.cpc && row.cpc.toLowerCase().includes(lower)) ||
      (row.partida_presupuestaria && row.partida_presupuestaria.toLowerCase().includes(lower))
    );
    setFilteredData(filtered);
  }, [searchTerm, data]);

  const columns: GridColDef[] = [
    { field: 'pac', headerName: 'Año PAC', width: 90, renderCell: (p) => p.row.pac?.anio || 'N/A' },
    { field: 'reforma', headerName: 'Reforma', width: 90, renderCell: (p) => p.row.pac?.version_reforma || '0' },
    { field: 'status', headerName: 'Estado', width: 120, renderCell: (p) => <Typography variant="caption" sx={{ fontWeight: 'bold', color: p.value === 'ACTIVO' ? 'success.main' : 'error.main' }}>{p.value?.replace('_POR_REFORMA', '')}</Typography> },
    { field: 'partida_presupuestaria', headerName: 'Partida', width: 130 },
    { field: 'cpc', headerName: 'CPC', width: 110 },
    { field: 'descripcion', headerName: 'Descripción', flex: 1, minWidth: 300 },
    { field: 'tipo_compra', headerName: 'Tipo', width: 120 },
    { field: 'procedimiento', headerName: 'Procedimiento', width: 150 },
    { field: 'cantidad', headerName: 'Cant.', width: 80 },
    { field: 'costo_unitario', headerName: 'V. Unit.', width: 110, renderCell: (p) => `$${p.value?.toFixed(2)}` },
    { field: 'valor_total', headerName: 'V. Total', width: 120, renderCell: (p) => `$${p.value?.toFixed(2)}` }
  ];

  return (
    <Box>
      <Card>
        <CardHeader 
            title="Explorador Global del PAC" 
            subheader="Busca en tiempo real entre miles de líneas presupuestarias de todos los años fiscales."
        />
        <CardContent>
          <Box mb={3}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Buscar por CPC, Partida o palabras clave en la descripción..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <IconSearch />
                  </InputAdornment>
                ),
              }}
            />
          </Box>
          <DataGrid 
            rows={filteredData} 
            columns={columns} 
            loading={loading}
            autoHeight 
            slots={{ toolbar: GridToolbar }}
            slotProps={{
              toolbar: {
                showQuickFilter: false, // We use our custom big one, but toolbar brings export/columns features
              },
            }}
            initialState={{
              pagination: { paginationModel: { pageSize: 25 } },
            }}
            pageSizeOptions={[25, 50, 100]}
          />
        </CardContent>
      </Card>
    </Box>
  );
}
