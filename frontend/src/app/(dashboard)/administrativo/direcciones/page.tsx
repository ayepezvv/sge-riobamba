'use client';
import { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  TextField,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Snackbar,
  Alert
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { API_BASE_URL } from 'config/api';

export default function DireccionesPage() {
  const [data, setData] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });
  const [formData, setFormData] = useState<any>({ nombre: '', descripcion: '', es_activo: true });
  const [editingId, setEditingId] = useState<number | null>(null);

  const fetchDirecciones = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/administrativo/direcciones`, { headers: { 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` } });
      if (res.ok) setData(await res.json());
    } catch (e) { console.error(e); }
  };

  useEffect(() => { fetchDirecciones(); }, []);

  const handleOpen = (item: any = null) => {
    if (item) {
      setEditingId(item.id);
      setFormData(item);
    } else {
      setEditingId(null);
      setFormData({ nombre: '', descripcion: '', es_activo: true });
    }
    setOpen(true);
  };

  const handleSave = async () => {
    const url = editingId ? `${API_BASE_URL}/api/administrativo/direcciones/${editingId}` : `${API_BASE_URL}/api/administrativo/direcciones`;
    const method = editingId ? 'PUT' : 'POST';
    try {
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` },
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        setToast({ open: true, message: 'Registro guardado exitosamente', severity: 'success' });
        setOpen(false);
        fetchDirecciones();
      } else {
        setToast({ open: true, message: 'Error al guardar', severity: 'error' });
      }
    } catch (e) {
      setToast({ open: true, message: 'Error de red', severity: 'error' });
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'nombre', headerName: 'Nombre', flex: 1 },
    { field: 'descripcion', headerName: 'Descripción', flex: 1 },
    { field: 'es_activo', headerName: 'Estado', width: 120, renderCell: (p) => p.value ? 'Activo' : 'Inactivo' },
    {
      field: 'acciones', headerName: 'Acciones', width: 150,
      renderCell: (params) => (
        <Button size="small" variant="contained" onClick={() => handleOpen(params.row)}>Editar</Button>
      )
    }
  ];

  return (
    <Box>
      <Card>
        <CardHeader title="Direcciones" action={<Button variant="contained" onClick={() => handleOpen()}>+ Nuevo</Button>} />
        <CardContent>
          <DataGrid rows={data} columns={columns} autoHeight />
        </CardContent>
      </Card>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingId ? 'Editar' : 'Nueva'} Dirección</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid size={12}>
              <TextField fullWidth label="Nombre" value={formData.nombre} onChange={(e) => setFormData({ ...formData, nombre: e.target.value })} />
            </Grid>
            <Grid size={12}>
              <TextField fullWidth label="Descripción" value={formData.descripcion} onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })} />
            </Grid>
            <Grid size={12}>
              <FormControl fullWidth>
                <InputLabel>Estado</InputLabel>
                <Select value={formData.es_activo} label="Estado" onChange={(e) => setFormData({ ...formData, es_activo: e.target.value })}>
                  <MenuItem value="true">Activo</MenuItem>
                  <MenuItem value="false">Inactivo</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleSave}>Guardar</Button>
        </DialogActions>
      </Dialog>
      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({...toast, open: false})}>
        <Alert severity={toast.severity as any}>{toast.message}</Alert>
      </Snackbar>
    </Box>
  );
}
