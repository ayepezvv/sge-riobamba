'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Snackbar, Alert, IconButton, Tooltip } from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import AddIcon from '@mui/icons-material/Add';
import MainCard from 'ui-component/cards/MainCard';
import axios from 'utils/axios';

export default function ProcesosPage() {
  const router = useRouter();
  const [procesos, setProcesos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });
  const [formData, setFormData] = useState({ codigo_proceso: '', nombre_proyecto: '', descripcion: '' });

  const fetchProcesos = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/contratacion/procesos');
      setProcesos(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchProcesos(); }, []);

  const handleSubmit = async () => {
    try {
      await axios.post('/api/contratacion/procesos', formData);
      setToast({ open: true, message: 'Proceso creado', severity: 'success' });
      setOpen(false);
      setFormData({ codigo_proceso: '', nombre_proyecto: '', descripcion: '' });
      fetchProcesos();
    } catch (error: any) {
      setToast({ open: true, message: error.response?.data?.detail || 'Error', severity: 'error' });
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'codigo_proceso', headerName: 'Código', width: 150 },
    { field: 'nombre_proyecto', headerName: 'Proyecto', flex: 1 },
    { field: 'fecha_creacion', headerName: 'Fecha Creación', width: 200, valueGetter: (params) => new Date(params.value).toLocaleString() },
    {
      field: 'acciones', headerName: 'Acciones', width: 100, sortable: false,
      renderCell: (params) => (
        <Tooltip title="Ver Expediente">
          <IconButton color="primary" onClick={() => router.push(`/contratacion/procesos/${params.row.id}`)}>
            <VisibilityIcon />
          </IconButton>
        </Tooltip>
      )
    }
  ];

  return (
    <MainCard 
      title="Mis Procesos / Expedientes"
      secondary={<Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={() => setOpen(true)}>Nuevo Proceso</Button>}
    >
      <Box sx={{ height: 500, width: '100%', mt: 2 }}>
        <DataGrid rows={procesos} columns={columns} loading={loading} disableRowSelectionOnClick />
      </Box>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Crear Nuevo Proceso</DialogTitle>
        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField label="Código del Proceso" value={formData.codigo_proceso} onChange={(e) => setFormData({...formData, codigo_proceso: e.target.value})} fullWidth required />
            <TextField label="Nombre del Proyecto" value={formData.nombre_proyecto} onChange={(e) => setFormData({...formData, nombre_proyecto: e.target.value})} fullWidth required />
            <TextField label="Descripción" value={formData.descripcion} onChange={(e) => setFormData({...formData, descripcion: e.target.value})} fullWidth multiline rows={3} />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)} color="error">Cancelar</Button>
          <Button onClick={handleSubmit} variant="contained" color="primary">Guardar</Button>
        </DialogActions>
      </Dialog>
      
      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({...toast, open: false})} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
        <Alert severity={toast.severity as any} variant="filled">{toast.message}</Alert>
      </Snackbar>
    </MainCard>
  );
}
