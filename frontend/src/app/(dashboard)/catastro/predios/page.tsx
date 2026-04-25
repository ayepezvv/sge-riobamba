'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { useTheme } from '@mui/material/styles';
import { 
  Box, Button, Dialog, DialogTitle, DialogContent, 
  DialogActions, TextField, Snackbar, Alert, Typography,
  Grid, Card, CardContent, Divider, IconButton
} from '@mui/material';

// Icons
import AddIcon from '@mui/icons-material/Add';
import HouseIcon from '@mui/icons-material/House';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import MapIcon from '@mui/icons-material/Map';

import MainCard from 'ui-component/cards/MainCard';
import { listarPredios, crearPredio } from 'api/catastro';

// Dynamic imports para leaflet (evita el error 'window is not defined' en Next.js SSR)
import LeafletCSS from './leaflet-css';
const PrediosMap = dynamic(() => import('./MapComponent').then((mod) => mod.PrediosMap), { ssr: false, loading: () => <p>Cargando mapa...</p> });
const MiniMapPicker = dynamic(() => import('./MapComponent').then((mod) => mod.MiniMapPicker), { ssr: false, loading: () => <p>Cargando mapa...</p> });

// ==============================|| GESTIÓN DE PREDIOS Y MAPA ||============================== //

export default function PrediosPage() {
  const theme = useTheme();
  const [predios, setPredios] = useState([]);
  
  // UI State
  const [open, setOpen] = useState(false);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });

  // Form State
  const [formData, setFormData] = useState({
    clave_catastral: '',
    numero_casa: '',
    foto_fachada: '',
    croquis: ''
  });
  
  // Map Position State for new Predio [lat, lng]
  const [position, setPosition] = useState<[number, number] | null>(null);

  const fetchPredios = async () => {
    try {
      const data = await listarPredios();
      setPredios(data);
    } catch (error) {
      console.error("Error fetching predios:", error);
    }
  };

  useEffect(() => {
    fetchPredios();
  }, []);

  const handleOpenNew = () => {
    setFormData({ clave_catastral: '', numero_casa: '', foto_fachada: '', croquis: '' });
    setPosition(null);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async () => {
    try {
      const payload: any = { ...formData };
      
      // Construir GeoJSON (Point) si el usuario hizo clic en el mapa
      if (position) {
        payload.geometria_geojson = {
          type: "Point",
          coordinates: [position[1], position[0]] // GeoJSON es [lon, lat]
        };
      }

      await crearPredio(payload);
      setToast({ open: true, message: 'Predio registrado en el mapa exitosamente', severity: 'success' });
      
      handleClose();
      fetchPredios();
    } catch (error: any) {
      console.error("Error saving predio:", error);
      const errorMsg = error.response?.data?.detail || 'Error al guardar. La clave catastral podría estar duplicada.';
      setToast({ open: true, message: errorMsg, severity: 'error' });
    }
  };

  return (
    <>
      <LeafletCSS />
      <Grid container spacing={3}>
        {/* LADO IZQUIERDO: MAPA INTERACTIVO */}
        <Grid size={{ xs: 12, md: 7, lg: 8 }}>
          <MainCard title="Mapa Catastral (Visión General)" sx={{ height: 'calc(100vh - 170px)', display: 'flex', flexDirection: 'column' }} contentSX={{ flexGrow: 1, p: 0 }}>
            <Box sx={{ height: '100%', minHeight: 500, width: '100%' }}>
              <PrediosMap predios={predios} />
            </Box>
          </MainCard>
        </Grid>

        {/* LADO DERECHO: LISTADO Y GESTION */}
        <Grid size={{ xs: 12, md: 5, lg: 4 }}>
          <MainCard 
            title="Lista de Predios" 
            sx={{ height: 'calc(100vh - 170px)', overflowY: 'auto' }}
            secondary={
              <Button variant="contained" color="secondary" size="small" startIcon={<AddIcon />} onClick={handleOpenNew}>
                Nuevo
              </Button>
            }
          >
            <Grid container spacing={2}>
              {predios.map((p: any, idx: number) => (
                <Grid size={12} key={idx}>
                  <Card sx={{ border: '1px solid', borderColor: 'divider', '&:hover': { borderColor: 'secondary.main' } }}>
                    <CardContent sx={{ p: 2, pb: '16px !important' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Avatar sx={{ bgcolor: theme.palette.secondary.light, color: theme.palette.secondary.dark, mr: 2, width: 32, height: 32 }}>
                          <HouseIcon fontSize="small" />
                        </Avatar>
                        <Box>
                          <Typography variant="h5">C.C. {p.clave_catastral}</Typography>
                          <Typography variant="body2" color="textSecondary">Casa: {p.numero_casa || 'S/N'}</Typography>
                        </Box>
                      </Box>
                      <Divider sx={{ my: 1 }} />
                      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-start' }}>
                        <Tooltip title={p.foto_fachada ? "Ver Fachada" : "Sin foto"}>
                          <IconButton size="small" color={p.foto_fachada ? "primary" : "default"}>
                            <CameraAltIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title={p.geojson ? "Georreferenciado" : "Sin coordenadas"}>
                          <IconButton size="small" color={p.geojson ? "success" : "default"}>
                            <MapIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
              
              {predios.length === 0 && (
                <Grid size={12}>
                  <Typography align="center" color="textSecondary" sx={{ mt: 4 }}>No hay predios registrados.</Typography>
                </Grid>
              )}
            </Grid>
          </MainCard>
        </Grid>
      </Grid>

      {/* Modal de Creación UX */}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ fontSize: '1.25rem', fontWeight: 600 }}>Registrar Nuevo Predio</DialogTitle>
        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 1 }}>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField label="Clave Catastral" name="clave_catastral" value={formData.clave_catastral} onChange={handleChange} fullWidth required />
              <TextField label="Número de Casa" name="numero_casa" value={formData.numero_casa} onChange={handleChange} fullWidth />
            </Box>

            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField label="URL Foto Fachada" name="foto_fachada" value={formData.foto_fachada} onChange={handleChange} fullWidth placeholder="https://..." InputProps={{ startAdornment: <CameraAltIcon color="disabled" sx={{ mr: 1 }}/> }} />
              <TextField label="URL Croquis" name="croquis" value={formData.croquis} onChange={handleChange} fullWidth placeholder="https://..." InputProps={{ startAdornment: <MapIcon color="disabled" sx={{ mr: 1 }}/> }} />
            </Box>

            <Box sx={{ mt: 1 }}>
              <Typography variant="subtitle2" color="primary" sx={{ mb: 1 }}>Ubicación en el Mapa (Clic para capturar coordenada)</Typography>
              {/* Integración del Mini Mapa Reactivo */}
              <MiniMapPicker position={position} setPosition={setPosition} />
              
              {position && (
                <Typography variant="caption" color="success.main" sx={{ mt: 1, display: 'block' }}>
                  Coordenada capturada: {position[0].toFixed(5)}, {position[1].toFixed(5)}
                </Typography>
              )}
            </Box>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={handleClose} color="error" variant="text">Cancelar</Button>
          <Button onClick={handleSubmit} variant="contained" color="secondary">
            Guardar Predio
          </Button>
        </DialogActions>
      </Dialog>

      {/* Feedback Visual */}
      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({ ...toast, open: false })} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
        <Alert onClose={() => setToast({ ...toast, open: false })} severity={toast.severity as any} variant="filled" sx={{ width: '100%' }}>
          {toast.message}
        </Alert>
      </Snackbar>
    </>
  );
}
