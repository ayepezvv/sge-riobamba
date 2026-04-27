'use client';

import { useEffect, useState, useRef } from 'react';
import { 
  Box, Button, Dialog, DialogTitle, DialogContent, DialogActions, 
  TextField, Snackbar, Alert, Typography, Grid, Card, CardContent, 
  FormControl, InputLabel, Select, MenuItem, Chip, Accordion, AccordionSummary, AccordionDetails, IconButton, Tooltip
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import EditIcon from '@mui/icons-material/Edit';
import BlockIcon from '@mui/icons-material/Block';
import CreateNewFolderIcon from '@mui/icons-material/CreateNewFolder';
import MainCard from 'ui-component/cards/MainCard';
import { listarTiposProceso, crearTipoProceso, actualizarTipoProceso, listarPlantillas, subirPlantilla } from 'api/contratacion';

export default function AdminPlantillasPage() {
  const [tipos, setTipos] = useState<any[]>([]);
  const [plantillas, setPlantillas] = useState<any[]>([]);
  const [_loading, setLoading] = useState(true);
  
  // Modals state
  const [openUpload, setOpenUpload] = useState(false);
  const [openFolder, setOpenFolder] = useState(false);
  const [editingFolderId, setEditingFolderId] = useState<number | null>(null);
  
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [formUpload, setFormUpload] = useState({
    nombre: '',
    tipo_proceso_id: '',
    anio: new Date().getFullYear().toString(),
    file: null as File | null
  });

  const [formFolder, setFormFolder] = useState({
    nombre: '',
    categoria: 'Bienes y Servicios',
    condicion_monto: ''
  });

    const fetchData = async () => {
    setLoading(true);
    try {
      const [rawTipos, rawPlan] = await Promise.all([
        listarTiposProceso(),
        listarPlantillas()
      ]);
      setTipos(Array.isArray(rawTipos) ? rawTipos : []);
      setPlantillas(Array.isArray(rawPlan) ? rawPlan : []);
    } catch (error: any) {
      console.error(error);
      setToast({ open: true, message: error.message || 'Error cargando datos', severity: 'error' });
      setTipos([]);
      setPlantillas([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  // ------------------ CARPETAS (TIPO PROCESO) ------------------
  const handleOpenNewFolder = () => {
    setEditingFolderId(null);
    setFormFolder({ nombre: '', categoria: 'Bienes y Servicios', condicion_monto: '' });
    setOpenFolder(true);
  };

  const handleOpenEditFolder = (folder: any) => {
    setEditingFolderId(folder.id);
    setFormFolder({ 
      nombre: folder.nombre, 
      categoria: folder.categoria || 'Bienes y Servicios', 
      condicion_monto: folder.condicion_monto || '' 
    });
    setOpenFolder(true);
  };

  const handleSubmitFolder = async () => {
    try {
      if (editingFolderId) {
        await actualizarTipoProceso(editingFolderId, formFolder);
        setToast({ open: true, message: 'Carpeta actualizada', severity: 'success' });
      } else {
        await crearTipoProceso(formFolder);
        setToast({ open: true, message: 'Nueva carpeta creada', severity: 'success' });
      }
      setOpenFolder(false);
      fetchData();
    } catch (error: any) {
      setToast({ open: true, message: error.response?.data?.detail || 'Error', severity: 'error' });
    }
  };

  const handleToggleFolderStatus = async (folder: any) => {
    try {
      await actualizarTipoProceso(folder.id, { is_activo: !folder.is_activo });
      setToast({ open: true, message: 'Estado de carpeta modificado', severity: 'success' });
      fetchData();
    } catch (error) {
      setToast({ open: true, message: 'Error al cambiar estado', severity: 'error' });
    }
  };

  // ------------------ PLANTILLAS ------------------
  const handleFileChange = (e: any) => {
    if (e.target.files && e.target.files.length > 0) {
      setFormUpload({ ...formUpload, file: e.target.files[0] });
    }
  };

  const handleSubmitUpload = async () => {
    if (!formUpload.file) {
      setToast({ open: true, message: 'Debe seleccionar un archivo .docx', severity: 'warning' });
      return;
    }
    
    const payload = new FormData();
    payload.append('nombre', formUpload.nombre);
    payload.append('tipo_proceso_id', formUpload.tipo_proceso_id);
    payload.append('anio', formUpload.anio);
    payload.append('file', formUpload.file);

    try {
      await subirPlantilla(payload);
      setToast({ open: true, message: 'Nueva versión subida exitosamente', severity: 'success' });
      setOpenUpload(false);
      setFormUpload({ nombre: '', tipo_proceso_id: '', anio: new Date().getFullYear().toString(), file: null });
      fetchData();
    } catch (error: any) {
      setToast({ open: true, message: error.response?.data?.detail || 'Error al subir', severity: 'error' });
    }
  };

  // Agrupar carpetas por categoría para la UI
  const categories = ["Bienes y Servicios", "Obras", "Consultoría"];

  return (
    <MainCard 
      title="Administración del Flujograma SERCOP"
      secondary={
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="outlined" color="primary" startIcon={<CreateNewFolderIcon />} onClick={handleOpenNewFolder}>Nueva Carpeta</Button>
          <Button variant="contained" color="secondary" startIcon={<CloudUploadIcon />} onClick={() => setOpenUpload(true)}>Subir Plantilla</Button>
        </Box>
      }
    >
      <Box sx={{ mt: 1 }}>
        {categories.map(cat => {
          const tiposCat = tipos.filter(t => t.categoria === cat);
          if (tiposCat.length === 0) return null;
          
          return (
            <Box key={cat} sx={{ mb: 4 }}>
              <Typography variant="h4" color="primary" sx={{ mb: 2, borderBottom: '2px solid', borderColor: 'divider', pb: 1 }}>
                Rama: {cat}
              </Typography>
              
              {tiposCat.map((tipo) => {
                const templatesForType = plantillas.filter(p => p.tipo_proceso_id === tipo.id);
                const isFolderActive = tipo.is_activo ?? true;
                
                return (
                  <Accordion key={tipo.id} defaultExpanded={isFolderActive} sx={{ opacity: isFolderActive ? 1 : 0.6, bgcolor: isFolderActive ? 'inherit' : 'grey.100' }}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />} sx={{ bgcolor: isFolderActive ? 'grey.50' : 'grey.300' }}>
                      <Box sx={{ display: 'flex', width: '100%', justifyContent: 'space-between', alignItems: 'center', pr: 2 }}>
                        <Box>
                          <Typography variant="h5" sx={{ display: 'inline-block', mr: 2 }}>{tipo.nombre}</Typography>
                          {!isFolderActive && <Chip label="Inactiva" color="error" size="small" />}
                          <Typography variant="caption" color="textSecondary" display="block">Condición: {tipo.condicion_monto || 'N/A'}</Typography>
                        </Box>
                        <Box onClick={(e) => e.stopPropagation()}>
                          <Tooltip title="Editar Carpeta">
                            <IconButton size="small" color="primary" onClick={() => handleOpenEditFolder(tipo)}><EditIcon fontSize="small" /></IconButton>
                          </Tooltip>
                          <Tooltip title={isFolderActive ? "Desactivar Carpeta" : "Activar Carpeta"}>
                            <IconButton size="small" color={isFolderActive ? "error" : "success"} onClick={() => handleToggleFolderStatus(tipo)}><BlockIcon fontSize="small" /></IconButton>
                          </Tooltip>
                        </Box>
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      {templatesForType.length === 0 ? (
                        <Typography color="textSecondary" variant="body2">No hay plantillas registradas en esta carpeta.</Typography>
                      ) : (
                        <Grid container spacing={2}>
                          {templatesForType.map((tpl) => (
                            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={tpl.id}>
                              <Card sx={{ border: '1px solid', borderColor: tpl.is_activa ? 'success.main' : 'divider', bgcolor: tpl.is_activa ? 'success.light' : 'background.paper', opacity: tpl.is_activa ? 1 : 0.7 }}>
                                <CardContent>
                                  <Typography variant="h5">{tpl.nombre}</Typography>
                                  <Typography variant="body2" color="textSecondary" sx={{ mb: 1.5 }}>Año: {tpl.anio} | Versión: v{tpl.version}</Typography>
                                  {tpl.is_activa ? (
                                    <Chip label="Vigente / Activa" color="success" size="small" />
                                  ) : (
                                    <Chip label="Histórica / Inactiva" color="default" size="small" />
                                  )}
                                </CardContent>
                              </Card>
                            </Grid>
                          ))}
                        </Grid>
                      )}
                    </AccordionDetails>
                  </Accordion>
                );
              })}
            </Box>
          );
        })}
      </Box>

      {/* Modal Nueva Carpeta (Tipo Proceso) */}
      <Dialog open={openFolder} onClose={() => setOpenFolder(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingFolderId ? 'Editar Carpeta' : 'Nueva Carpeta de Proceso'}</DialogTitle>
        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 1 }}>
            <TextField label="Nombre (Ej. Licitación, Ínfima Cuantía)" value={formFolder.nombre} onChange={(e) => setFormFolder({...formFolder, nombre: e.target.value})} fullWidth required />
            <FormControl fullWidth required>
              <InputLabel>Rama / Categoría</InputLabel>
              <Select value={formFolder.categoria} label="Rama / Categoría" onChange={(e) => setFormFolder({...formFolder, categoria: e.target.value})}>
                <MenuItem value="Bienes y Servicios">Bienes y Servicios</MenuItem>
                <MenuItem value="Obras">Obras</MenuItem>
                <MenuItem value="Consultoría">Consultoría</MenuItem>
              </Select>
            </FormControl>
            <TextField label="Condición de Monto (Ej. > $10,000.00)" value={formFolder.condicion_monto} onChange={(e) => setFormFolder({...formFolder, condicion_monto: e.target.value})} fullWidth />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenFolder(false)} color="error">Cancelar</Button>
          <Button onClick={handleSubmitFolder} variant="contained" color="primary">Guardar Carpeta</Button>
        </DialogActions>
      </Dialog>

      {/* Modal Subir Plantilla */}
      <Dialog open={openUpload} onClose={() => setOpenUpload(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Subir Plantilla (Crear o Versionar)</DialogTitle>
        <DialogContent dividers>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            Si el nombre de la plantilla y la carpeta coinciden con una activa, el sistema automáticamente generará una nueva versión y dejará la anterior en el historial.
          </Typography>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 1 }}>
            <FormControl fullWidth required>
              <InputLabel>Carpeta de Destino</InputLabel>
              <Select value={formUpload.tipo_proceso_id} label="Carpeta de Destino" onChange={(e) => setFormUpload({...formUpload, tipo_proceso_id: e.target.value as string})}>
                {tipos.filter(t => t.is_activo !== false).map((t: any) => <MenuItem key={t.id} value={t.id}>{t.nombre} ({t.categoria})</MenuItem>)}
              </Select>
            </FormControl>
            <TextField label="Nombre del Documento (Ej. TDR Ínfima)" value={formUpload.nombre} onChange={(e) => setFormUpload({...formUpload, nombre: e.target.value})} fullWidth required />
            <TextField label="Año Fiscal" type="number" value={formUpload.anio} onChange={(e) => setFormUpload({...formUpload, anio: e.target.value})} fullWidth required />
            
            <Box sx={{ border: '1px dashed grey', p: 2, textAlign: 'center', borderRadius: 1 }}>
              <input type="file" accept=".docx" ref={fileInputRef} style={{ display: 'none' }} onChange={handleFileChange} />
              <Button variant="outlined" onClick={() => fileInputRef.current?.click()} startIcon={<CloudUploadIcon />}>
                Seleccionar archivo .docx
              </Button>
              {formUpload.file && <Typography variant="caption" display="block" sx={{ mt: 1 }}>{formUpload.file.name}</Typography>}
            </Box>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenUpload(false)} color="error">Cancelar</Button>
          <Button onClick={handleSubmitUpload} variant="contained" color="primary">Procesar Archivo</Button>
        </DialogActions>
      </Dialog>
      
      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({...toast, open: false})} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
        <Alert severity={toast.severity as any} variant="filled">{toast.message}</Alert>
      </Snackbar>
    </MainCard>
  );
}
