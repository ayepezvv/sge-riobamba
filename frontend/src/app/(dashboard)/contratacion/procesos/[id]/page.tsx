'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Snackbar, Alert, Typography, Grid, IconButton, Tooltip, FormControl, InputLabel, Select, MenuItem, Chip } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DownloadIcon from '@mui/icons-material/Download';
import AddIcon from '@mui/icons-material/Add';
import MainCard from 'ui-component/cards/MainCard';
import axios from 'utils/axios';

export default function ProcesoDetailPage() {
  const params = useParams();
  const router = useRouter();
  const procesoId = params.id;
  
  const [proceso, setProceso] = useState<any>(null);
  const [plantillas, setPlantillas] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Dialog Generate / Regenerate
  const [openDoc, setOpenDoc] = useState(false);
  const [editingDocId, setEditingDocId] = useState<number | null>(null);
  
  // We use a simple JSON editor/text field for now, normally this would be a dynamic form
  const [docForm, setDocForm] = useState({
    plantilla_id: '',
    datos_json: '{\n  "nombre_proyecto": "",\n  "fecha": ""\n}'
  });

  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });

  const fetchData = async () => {
    setLoading(true);
    try {
      const [resProc, resPlan] = await Promise.all([
        axios.get(`/api/contratacion/procesos/${procesoId}`),
        axios.get('/api/contratacion/plantillas')
      ]);
      setProceso(resProc.data);
      setPlantillas(resPlan.data);
      
      // Auto-fill project name in JSON template
      setDocForm(prev => ({
          ...prev, 
          datos_json: `{\n  "nombre_proyecto": "${resProc.data.nombre_proyecto}",\n  "fecha": "${new Date().toISOString().split('T')[0]}"\n}`
      }));
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { if (procesoId) fetchData(); }, [procesoId]);

  const handleOpenNewDoc = () => {
    setEditingDocId(null);
    setDocForm(prev => ({ ...prev, plantilla_id: plantillas.length > 0 ? plantillas[0].id : '' }));
    setOpenDoc(true);
  };

  const handleOpenEditDoc = async (doc: any) => {
    try {
      const res = await axios.get(`/api/contratacion/documento/${doc.id}/datos`);
      setDocForm({
        plantilla_id: doc.plantilla_id,
        datos_json: JSON.stringify(res.data, null, 2)
      });
      setEditingDocId(doc.id);
      setOpenDoc(true);
    } catch (error) {
      setToast({ open: true, message: 'Error al recuperar datos del documento', severity: 'error' });
    }
  };

  const handleDocSubmit = async () => {
    try {
      let parsedData;
      try {
        parsedData = JSON.parse(docForm.datos_json);
      } catch(e) {
        setToast({ open: true, message: 'El JSON es inválido', severity: 'error' });
        return;
      }

      if (editingDocId) {
        await axios.put(`/api/contratacion/documento/${editingDocId}/regenerar`, { datos: parsedData });
        setToast({ open: true, message: 'Documento regenerado exitosamente', severity: 'success' });
      } else {
        await axios.post('/api/contratacion/documento', {
          proceso_contratacion_id: parseInt(procesoId as string),
          plantilla_id: docForm.plantilla_id,
          datos: parsedData
        });
        setToast({ open: true, message: 'Documento generado exitosamente', severity: 'success' });
      }
      setOpenDoc(false);
      fetchData(); // Refresh list
    } catch (error: any) {
      setToast({ open: true, message: error.response?.data?.detail || 'Error al generar', severity: 'error' });
    }
  };

  const handleDownload = (path: string) => {
    // In a real app we would have a download endpoint, for now we just show a toast
    setToast({ open: true, message: `Simulando descarga de: ${path}`, severity: 'info' });
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { 
      field: 'plantilla_id', 
      headerName: 'Plantilla', 
      flex: 1,
      renderCell: (params) => {
        const p = plantillas.find((pl: any) => pl.id === params.value);
        return p ? p.nombre : `ID: ${params.value}`;
      }
    },
    { 
      field: 'version', 
      headerName: 'Versión', 
      width: 100,
      renderCell: (params) => <Chip label={`v${params.value}`} color="primary" size="small" />
    },
    { field: 'fecha_generacion', headerName: 'Última Generación', width: 200, valueGetter: (params) => new Date(params.value).toLocaleString() },
    {
      field: 'acciones', headerName: 'Acciones', width: 150, sortable: false,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title="Editar y Regenerar">
            <IconButton color="warning" onClick={() => handleOpenEditDoc(params.row)}>
              <EditIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Descargar DOCX">
            <IconButton color="success" onClick={() => handleDownload(params.row.ruta_archivo_generado)}>
              <DownloadIcon />
            </IconButton>
          </Tooltip>
        </Box>
      )
    }
  ];

  if (!proceso) return <Typography>Cargando expediente...</Typography>;

  return (
    <MainCard 
      title={`Expediente: ${proceso.codigo_proceso} - ${proceso.nombre_proyecto}`}
      secondary={<Button variant="contained" color="secondary" startIcon={<AddIcon />} onClick={handleOpenNewDoc}>Generar Documento</Button>}
    >
      <Box sx={{ height: 400, width: '100%', mt: 2 }}>
        <DataGrid rows={proceso.documentos || []} columns={columns} loading={loading} disableRowSelectionOnClick />
      </Box>

      {/* Modal de Generación / Edición */}
      <Dialog open={openDoc} onClose={() => setOpenDoc(false)} maxWidth="md" fullWidth>
        <DialogTitle>{editingDocId ? 'Editar y Regenerar Documento' : 'Generar Nuevo Documento'}</DialogTitle>
        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 3, mt: 1 }}>
            <FormControl fullWidth disabled={!!editingDocId}>
              <InputLabel>Plantilla</InputLabel>
              <Select 
                value={docForm.plantilla_id} 
                label="Plantilla" 
                onChange={(e) => setDocForm({...docForm, plantilla_id: e.target.value})}
              >
                {plantillas.map((p: any) => (
                  <MenuItem key={p.id} value={p.id}>{p.nombre}</MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <Typography variant="subtitle2" color="primary">Diccionario de Datos (JSON)</Typography>
            <Typography variant="caption" color="textSecondary">Edita los valores aquí. Al regenerar, el sistema creará un nuevo archivo DOCX con esta información actualizada.</Typography>
            <TextField 
              multiline 
              rows={10} 
              value={docForm.datos_json} 
              onChange={(e) => setDocForm({...docForm, datos_json: e.target.value})} 
              fullWidth 
              sx={{ fontFamily: 'monospace' }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDoc(false)} color="error">Cancelar</Button>
          <Button onClick={handleDocSubmit} variant="contained" color="primary">
            {editingDocId ? 'Guardar y Regenerar' : 'Generar Documento'}
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({...toast, open: false})} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
        <Alert severity={toast.severity as any} variant="filled">{toast.message}</Alert>
      </Snackbar>
    </MainCard>
  );
}
