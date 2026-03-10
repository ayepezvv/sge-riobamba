'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Snackbar, Alert, IconButton, Tooltip, Stepper, Step, StepLabel, FormControl, InputLabel, Select, MenuItem, Typography } from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import AddIcon from '@mui/icons-material/Add';
import MainCard from 'ui-component/cards/MainCard';
import axios from 'utils/axios';

export default function ProcesosPage() {
  const router = useRouter();
  const [procesos, setProcesos] = useState([]);
  const [tiposProceso, setTiposProceso] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [pacItems, setPacItems] = useState([]);
  const [selectedPacItems, setSelectedPacItems] = useState<number[]>([]);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });
  
  // Wizard State
  const [activeStep, setActiveStep] = useState(0);
  const [wizardData, setWizardData] = useState({
    categoria: '',
    catalogo_electronico: '',
    monto: '',
    // Final data
    codigo_proceso: '',
    nombre_proyecto: '',
    descripcion: ''
  });
  
  const [tipoRecomendado, setTipoRecomendado] = useState<any>(null);

    const fetchPacItems = async () => {
    try {
      const res = await fetch('http://192.168.1.15:8000/api/contratacion/pac', { headers: { 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` } });
      if (res.ok) {
        const pacs = await res.json();
        // Extract active pac items
        let items: any[] = [];
        pacs.forEach((p: any) => {
            if (p.es_activo && p.items) {
                items = [...items, ...p.items];
            }
        });
        setPacItems(items as any);
      }
    } catch (e) { console.error(e); }
  };
  const fetchProcesos = async () => {
    setLoading(true);
    try {
      const [resProc, resTipos] = await Promise.all([
        axios.get('/api/contratacion/procesos'),
        axios.get('/api/contratacion/tipos')
      ]);
      setProcesos(resProc.data);
      setTiposProceso(resTipos.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchProcesos(); }, []);

  const handleNext = () => {
    if (activeStep === 2) {
      let recomendado = null;
      if (wizardData.catalogo_electronico === 'Si') {
        recomendado = tiposProceso.find(t => t.nombre.includes('Catálogo'));
      } else if (wizardData.monto) {
        recomendado = tiposProceso.find(t => t.id === parseInt(wizardData.monto));
      }
      setTipoRecomendado(recomendado);
    }
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => setActiveStep((prev) => prev - 1);

  const handleSubmit = async () => {
    try {
      const payload = {
        codigo_proceso: wizardData.codigo_proceso,
        nombre_proyecto: wizardData.nombre_proyecto,
        descripcion: `[${tipoRecomendado?.nombre || 'Proceso'}] ${wizardData.descripcion}`,
        tipo_proceso_id: tipoRecomendado?.id || null
      };
      await axios.post('/api/contratacion/procesos', payload);
      setToast({ open: true, message: 'Expediente creado correctamente', severity: 'success' });
      setOpen(false);
      setActiveStep(0);
      setWizardData({ categoria: '', catalogo_electronico: '', monto: '', codigo_proceso: '', nombre_proyecto: '', descripcion: '' });
      fetchProcesos();
    } catch (error: any) {
      setToast({ open: true, message: error.response?.data?.detail || 'Error', severity: 'error' });
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'codigo_proceso', headerName: 'Código', width: 150 },
    { field: 'nombre_proyecto', headerName: 'Proyecto', flex: 1 },
    { field: 'fecha_creacion', headerName: 'Fecha Creación', width: 200, valueGetter: (params) => params.value ? new Date(params.value).toLocaleString('es-EC') : 'Sin fecha' },
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

  const steps = ['Naturaleza', 'Catálogo', 'Monto', 'Expediente'];

  return (
    <MainCard 
      title="Mis Procesos / Expedientes"
      secondary={<Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={() => { setOpen(true); setActiveStep(0); }}>Nuevo Expediente</Button>}
    >
      <Box sx={{ height: 500, width: '100%', mt: 2 }}>
        <DataGrid rows={procesos} columns={columns} loading={loading} disableRowSelectionOnClick />
      </Box>

      {/* ASISTENTE WIZARD SERCOP */}
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Asistente de Contratación Pública (LOSNCP)</DialogTitle>
        <DialogContent dividers>
          <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 4 }}>
            {steps.map((label) => (
              <Step key={label}><StepLabel>{label}</StepLabel></Step>
            ))}
          </Stepper>

          <Box sx={{ minHeight: 150 }}>
            {activeStep === 0 && (
              <FormControl fullWidth>
                <InputLabel>¿Qué tipo de compra realizará?</InputLabel>
                <Select value={wizardData.categoria} label="¿Qué tipo de compra realizará?" onChange={(e) => setWizardData({...wizardData, categoria: e.target.value})}>
                  <MenuItem value="Bienes">Adquisición de Bienes</MenuItem>
                  <MenuItem value="Servicios">Prestación de Servicios</MenuItem>
                  <MenuItem value="Obras">Ejecución de Obras</MenuItem>
                  <MenuItem value="Consultoria">Consultoría</MenuItem>
                </Select>
              </FormControl>
            )}

            {activeStep === 1 && (
              <FormControl fullWidth>
                <InputLabel>¿El bien/servicio consta en el Catálogo Electrónico?</InputLabel>
                <Select value={wizardData.catalogo_electronico} label="¿El bien/servicio consta en el Catálogo Electrónico?" onChange={(e) => setWizardData({...wizardData, catalogo_electronico: e.target.value})}>
                  <MenuItem value="Si">Sí, está en el Catálogo Electrónico</MenuItem>
                  <MenuItem value="No">No, no consta en el Catálogo</MenuItem>
                </Select>
                <Typography variant="caption" color="textSecondary" sx={{ mt: 1 }}>Nota: La ley obliga revisar el catálogo antes de cualquier otra modalidad.</Typography>
              </FormControl>
            )}

            {activeStep === 2 && wizardData.catalogo_electronico === 'Si' && (
              <Typography variant="body1" color="success.main" textAlign="center" sx={{ mt: 4 }}>
                Excelente. El proceso recomendado es <strong>Catálogo Electrónico</strong> sin importar el monto.
              </Typography>
            )}

            {activeStep === 2 && wizardData.catalogo_electronico === 'No' && (
              <FormControl fullWidth>
                <InputLabel>Monto Referencial / Condición</InputLabel>
                <Select value={wizardData.monto} label="Monto Referencial / Condición" onChange={(e) => setWizardData({...wizardData, monto: e.target.value})}>
                  {tiposProceso.filter(t => t.is_activo && (t.categoria.includes(wizardData.categoria) || wizardData.categoria.includes(t.categoria.split(' ')[0])) && !t.nombre.includes('Catálogo')).map((t: any) => (
                    <MenuItem key={t.id} value={t.id}>{t.condicion_monto || 'Sin límite específico'} ({t.nombre})</MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}

            {activeStep === 3 && (
              <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Alert severity="info">
                  <strong>Modalidad Recomendada: </strong> {tipoRecomendado?.nombre || 'Evaluando...'}
                </Alert>
                <TextField label="Código del Proceso (Interno)" value={wizardData.codigo_proceso} onChange={(e) => setWizardData({...wizardData, codigo_proceso: e.target.value})} fullWidth required />
                <TextField label="Nombre del Proyecto" value={wizardData.nombre_proyecto} onChange={(e) => setWizardData({...wizardData, nombre_proyecto: e.target.value})} fullWidth required />
                <TextField label="Objeto de la Contratación" value={wizardData.descripcion} onChange={(e) => setWizardData({...wizardData, descripcion: e.target.value})} fullWidth multiline rows={3} />
              </Box>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)} color="error">Cancelar</Button>
          <Box sx={{ flex: '1 1 auto' }} />
          <Button disabled={activeStep === 0} onClick={handleBack}>Atrás</Button>
          {activeStep === steps.length - 1 ? (
            <Button variant="contained" onClick={handleSubmit}>Guardar Expediente</Button>
          ) : (
            <Button variant="contained" onClick={handleNext}>Siguiente</Button>
          )}
        </DialogActions>
      </Dialog>
      
      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({...toast, open: false})} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
        <Alert severity={toast.severity as any} variant="filled">{toast.message}</Alert>
      </Snackbar>
    </MainCard>
  );
}
