'use client';
import { useEffect, useState } from 'react';
import API_BASE_URL from "@/config/api";
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

export default function PuestosPage() {
  const [data, setData] = useState([]);
  const [open, setOpen] = useState(false);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });
  const [formData, setFormData] = useState<any>({
    denominacion: '', escala_ocupacional: '', remuneracion_mensual: 0, partida_presupuestaria: '', es_activo: true
  });
  const [editingId, setEditingId] = useState<number | null>(null);

  const fetchPuestos = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/administrativo/puestos`, { headers: { 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` } });
      if (res.ok) setData(await res.json());
    } catch (e) { console.error(e); }
  };

  useEffect(() => { fetchPuestos(); }, []);

  const handleOpen = (item = null) => {
    if (item) {
      setEditingId(item.id);
      setFormData(item);
    } else {
      setEditingId(null);
      setFormData({ denominacion: '', escala_ocupacional: '', remuneracion_mensual: 0, partida_presupuestaria: '', es_activo: true });
    }
    setOpen(true);
  };

  const handleSave = async () => {
    const url = editingId ? `${API_BASE_URL}/api/administrativo/puestos/${editingId}` : `${API_BASE_URL}/api/administrativo/puestos`;
    const method = editingId ? 'PUT' : 'POST';
    try {
      const payload = { ...formData, remuneracion_mensual: parseFloat(formData.remuneracion_mensual) || 0 };
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        setToast({ open: true, message: 'Registro guardado exitosamente', severity: 'success' });
        setOpen(false);
        fetchPuestos();
      } else {
        setToast({ open: true, message: 'Error al guardar', severity: 'error' });
      }
    } catch (e) {
      setToast({ open: true, message: 'Error de red', severity: 'error' });
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'denominacion', headerName: 'Denominación', flex: 1 },
    { field: 'escala_ocupacional', headerName: 'Escala', width: 120 },
    { field: 'partida_presupuestaria', headerName: 'Partida', width: 120 },
    { field: 'remuneracion_mensual', headerName: 'Remuneración', width: 130, renderCell: (p) => `$${p.value?.toFixed(2)}` },
    { field: 'es_activo', headerName: 'Estado', width: 100, renderCell: (p) => p.value ? 'Activo' : 'Inactivo' },
    {
      field: 'acciones', headerName: 'Acciones', width: 120,
      renderCell: (params) => (
        <Button size="small" variant="contained" onClick={() => handleOpen(params.row)}>Editar</Button>
      )
    }
  ];

  return (
    <Box>
      <Card>
        <CardHeader title="Catálogo de Puestos Institucionales" action={<Button variant="contained" onClick={() => handleOpen()}>+ Nuevo</Button>} />
        <CardContent>
          <DataGrid rows={data} columns={columns} autoHeight />
        </CardContent>
      </Card>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingId ? 'Editar' : 'Nuevo'} Puesto</DialogTitle>
        <DialogContent dividers>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField fullWidth label="Denominación del Puesto" value={formData.denominacion} onChange={(e) => setFormData({ ...formData, denominacion: e.target.value })} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth label="Escala Ocupacional" value={formData.escala_ocupacional} onChange={(e) => setFormData({ ...formData, escala_ocupacional: e.target.value })} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth label="Remuneración Mensual" type="number" value={formData.remuneracion_mensual} onChange={(e) => setFormData({ ...formData, remuneracion_mensual: e.target.value })} />
            </Grid>
            <Grid item xs={12}>
              <TextField fullWidth label="Partida Presupuestaria" value={formData.partida_presupuestaria} onChange={(e) => setFormData({ ...formData, partida_presupuestaria: e.target.value })} />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Estado</InputLabel>
                <Select value={formData.es_activo} label="Estado" onChange={(e) => setFormData({ ...formData, es_activo: e.target.value })}>
                  <MenuItem value={true}>Activo</MenuItem>
                  <MenuItem value={false}>Inactivo</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
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
