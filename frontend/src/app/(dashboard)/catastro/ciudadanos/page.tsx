'use client';

import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { 
  Chip, Box, Button, Dialog, DialogTitle, DialogContent, DialogContentText,
  DialogActions, TextField, FormControl, InputLabel, 
  Select, MenuItem, Snackbar, Alert, Typography,
  Tabs, Tab, Grid, Switch, FormControlLabel, IconButton, Tooltip
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import BlockIcon from '@mui/icons-material/Block';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import MainCard from 'ui-component/cards/MainCard';
import axios from 'utils/axios';

// Componente helper para las pestañas
interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}
function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

// Valores iniciales
const initialFormData = {
  tipo_persona: 'Natural',
  identificacion: '',
  nombres: '',
  apellidos: '',
  razon_social: '',
  tipo_empresa: '',
  naturaleza_juridica: '',
  fecha_nacimiento: '',
  genero: '',
  correo_principal: '',
  celular: '',
  telefono_fijo: '',
  preferencia_contacto: 'Correo',
  tiene_discapacidad: false,
  porcentaje_discapacidad: 0,
  aplica_tercera_edad: false,
  // Referencia
  ref_tipo: '',
  ref_nombres: '',
  ref_apellidos: '',
  ref_identificacion: ''
};

// ==============================|| PADRÓN DE CIUDADANOS ||============================== //

export default function CiudadanosPage() {
  const [ciudadanos, setCiudadanos] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // UI State
  const [open, setOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [tabValue, setTabValue] = useState(0);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });

  // Dialog State (Desactivar)
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [selectedUserForStatus, setSelectedUserForStatus] = useState<any>(null);

  // Form State
  const [formData, setFormData] = useState({ ...initialFormData });

  const fetchCiudadanos = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/ciudadanos/');
      setCiudadanos(response.data);
    } catch (error) {
      console.error("Error fetching citizens:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCiudadanos();
  }, []);

  const handleOpenNew = () => {
    setFormData({ ...initialFormData });
    setEditingId(null);
    setTabValue(0);
    setOpen(true);
  };

  const handleOpenEdit = (ciudadano: any) => {
    setEditingId(ciudadano.id);
    setFormData({
      ...initialFormData,
      ...ciudadano,
      tipo_persona: ciudadano.tipo_persona || 'Natural',
      porcentaje_discapacidad: ciudadano.porcentaje_discapacidad || 0,
      fecha_nacimiento: ciudadano.fecha_nacimiento || '',
    });
    setTabValue(0);
    setOpen(true);
  };
  
  const handleClose = () => {
    setOpen(false);
    setFormData({ ...initialFormData });
  };

  const handleChange = (e: any) => {
    const { name, value, checked, type } = e.target;
    setFormData({ 
      ...formData, 
      [name]: type === 'checkbox' ? checked : value 
    });
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleSubmit = async () => {
    try {
      const payload: any = {
        tipo_persona: formData.tipo_persona,
        identificacion: formData.identificacion,
        correo_principal: formData.correo_principal || null,
        celular: formData.celular || null,
        telefono_fijo: formData.telefono_fijo || null,
        preferencia_contacto: formData.preferencia_contacto || null,
        tiene_discapacidad: formData.tiene_discapacidad,
        porcentaje_discapacidad: formData.tiene_discapacidad ? Number(formData.porcentaje_discapacidad) : 0,
        aplica_tercera_edad: formData.aplica_tercera_edad
      };

      if (formData.tipo_persona === 'Natural') {
        payload.nombres = formData.nombres;
        payload.apellidos = formData.apellidos;
        payload.genero = formData.genero || null;
        payload.fecha_nacimiento = formData.fecha_nacimiento || null;
      } else {
        payload.razon_social = formData.razon_social;
        payload.tipo_empresa = formData.tipo_empresa || null;
        payload.naturaleza_juridica = formData.naturaleza_juridica || null;
      }

      if (editingId) {
        await axios.put(`/api/ciudadanos/${editingId}`, payload);
        setToast({ open: true, message: 'Ciudadano actualizado exitosamente', severity: 'success' });
      } else {
        payload.referencias = [];
        if (formData.ref_tipo && formData.ref_nombres && formData.ref_apellidos) {
          payload.referencias.push({
            tipo_referencia: formData.ref_tipo,
            nombres: formData.ref_nombres,
            apellidos: formData.ref_apellidos,
            identificacion: formData.ref_identificacion || null
          });
        }
        await axios.post('/api/ciudadanos/', payload);
        setToast({ open: true, message: 'Ciudadano registrado exitosamente', severity: 'success' });
      }
      
      handleClose();
      fetchCiudadanos();
    } catch (error: any) {
      console.error("Error saving citizen:", error);
      const errorMsg = error.response?.data?.detail || 'Error al guardar. Verifique los datos o cédula duplicada.';
      setToast({ open: true, message: typeof errorMsg === 'string' ? errorMsg : 'La identificación ya existe o es inválida.', severity: 'error' });
    }
  };

  const handleToggleStatusClick = (row: any) => {
    setSelectedUserForStatus(row);
    setConfirmOpen(true);
  };

  const handleConfirmStatusChange = async () => {
    if (!selectedUserForStatus) return;
    try {
      await axios.patch(`/api/ciudadanos/${selectedUserForStatus.id}/status`);
      setToast({ open: true, message: 'Estado modificado exitosamente', severity: 'success' });
      setConfirmOpen(false);
      fetchCiudadanos();
    } catch (error: any) {
      console.error("Error changing status:", error);
      setToast({ open: true, message: 'Error al cambiar estado.', severity: 'error' });
      setConfirmOpen(false);
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { 
      field: 'tipo_persona', 
      headerName: 'Tipo', 
      width: 120,
      renderCell: (params) => {
        return params.value === 'Natural' ? (
          <Chip label="Natural" color="primary" variant="outlined" size="small" />
        ) : (
          <Chip label="Jurídica" color="secondary" variant="outlined" size="small" />
        );
      }
    },
    { field: 'identificacion', headerName: 'Identificación', width: 140 },
    { 
      field: 'nombre_completo', 
      headerName: 'Nombre / Razón Social', 
      flex: 1, 
      minWidth: 250,
      valueGetter: (params, row) => {
        return row.tipo_persona === 'Natural' 
          ? `${row.nombres || ''} ${row.apellidos || ''}`
          : row.razon_social || '';
      }
    },
    { field: 'celular', headerName: 'Celular', width: 140 },
    { 
      field: 'is_active', 
      headerName: 'Estado', 
      width: 100,
      renderCell: (params) => {
        const isActive = params.value ?? true; // Default true if legacy records exist
        return isActive ? (
          <Chip label="Activo" color="success" size="small" />
        ) : (
          <Chip label="Inactivo" color="error" size="small" />
        );
      }
    },
    {
      field: 'acciones',
      headerName: 'Acciones',
      width: 120,
      sortable: false,
      renderCell: (params) => {
        const isActive = params.row.is_active ?? true;
        return (
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Tooltip title="Editar">
              <IconButton color="primary" onClick={() => handleOpenEdit(params.row)}>
                <EditIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title={isActive ? "Desactivar" : "Activar"}>
              <IconButton 
                color={isActive ? "error" : "success"} 
                onClick={() => handleToggleStatusClick(params.row)}
              >
                {isActive ? <BlockIcon /> : <CheckCircleOutlineIcon />}
              </IconButton>
            </Tooltip>
          </Box>
        );
      }
    }
  ];

  return (
    <MainCard 
      title="Padrón de Ciudadanos y Clientes"
      secondary={
        <Button variant="contained" color="primary" onClick={handleOpenNew}>
          + Nuevo Ciudadano
        </Button>
      }
    >
      <Box sx={{ height: 500, width: '100%', mt: 2 }}>
        <DataGrid
          rows={ciudadanos}
          columns={columns}
          loading={loading}
          initialState={{
            pagination: {
              paginationModel: { page: 0, pageSize: 10 },
            },
          }}
          pageSizeOptions={[10, 25, 50]}
          disableRowSelectionOnClick
        />
      </Box>

      {/* Modal UX Premium con Tabs */}
      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle sx={{ fontSize: '1.3rem', fontWeight: 600, borderBottom: 1, borderColor: 'divider', pb: 2 }}>
          {editingId ? 'Editar Ciudadano' : 'Registrar Nuevo Ciudadano'}
        </DialogTitle>
        <DialogContent sx={{ p: 3 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange} variant="fullWidth">
              <Tab label="1. Datos Generales" />
              <Tab label="2. Info de Contacto" />
              <Tab label="3. Beneficios y Referencias" />
            </Tabs>
          </Box>

          {/* TAB 1: GENERAL */}
          <TabPanel value={tabValue} index={0}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Tipo de Persona</InputLabel>
                  <Select name="tipo_persona" value={formData.tipo_persona} label="Tipo de Persona" onChange={handleChange} disabled={!!editingId}>
                    <MenuItem value="Natural">Persona Natural</MenuItem>
                    <MenuItem value="Juridica">Persona Jurídica</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField label="Identificación (Cédula/RUC)" name="identificacion" value={formData.identificacion} onChange={handleChange} fullWidth required />
              </Grid>

              {formData.tipo_persona === 'Natural' && (
                <>
                  <Grid item xs={12} sm={6}>
                    <TextField label="Nombres" name="nombres" value={formData.nombres} onChange={handleChange} fullWidth required />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField label="Apellidos" name="apellidos" value={formData.apellidos} onChange={handleChange} fullWidth required />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField label="Fecha de Nacimiento" name="fecha_nacimiento" type="date" value={formData.fecha_nacimiento} onChange={handleChange} fullWidth InputLabelProps={{ shrink: true }} />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth>
                      <InputLabel>Género</InputLabel>
                      <Select name="genero" value={formData.genero} label="Género" onChange={handleChange}>
                        <MenuItem value="Masculino">Masculino</MenuItem>
                        <MenuItem value="Femenino">Femenino</MenuItem>
                        <MenuItem value="Otro">Otro</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                </>
              )}

              {formData.tipo_persona === 'Juridica' && (
                <>
                  <Grid item xs={12}>
                    <TextField label="Razón Social" name="razon_social" value={formData.razon_social} onChange={handleChange} fullWidth required />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth>
                      <InputLabel>Tipo de Empresa</InputLabel>
                      <Select name="tipo_empresa" value={formData.tipo_empresa} label="Tipo de Empresa" onChange={handleChange}>
                        <MenuItem value="Publica">Pública</MenuItem>
                        <MenuItem value="Privada">Privada</MenuItem>
                        <MenuItem value="Mixta">Mixta</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth>
                      <InputLabel>Naturaleza Jurídica</InputLabel>
                      <Select name="naturaleza_juridica" value={formData.naturaleza_juridica} label="Naturaleza Jurídica" onChange={handleChange}>
                        <MenuItem value="Sociedad Anonima">Sociedad Anónima (S.A.)</MenuItem>
                        <MenuItem value="Compania Limitada">Compañía Limitada (Cía. Ltda.)</MenuItem>
                        <MenuItem value="Otra">Otra</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                </>
              )}
            </Grid>
          </TabPanel>

          {/* TAB 2: CONTACTO */}
          <TabPanel value={tabValue} index={1}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField label="Correo Electrónico" name="correo_principal" type="email" value={formData.correo_principal} onChange={handleChange} fullWidth />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField label="Celular" name="celular" value={formData.celular} onChange={handleChange} fullWidth />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField label="Teléfono Fijo" name="telefono_fijo" value={formData.telefono_fijo} onChange={handleChange} fullWidth />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Preferencia de Contacto</InputLabel>
                  <Select name="preferencia_contacto" value={formData.preferencia_contacto} label="Preferencia de Contacto" onChange={handleChange}>
                    <MenuItem value="Correo">Correo Electrónico</MenuItem>
                    <MenuItem value="WhatsApp">WhatsApp</MenuItem>
                    <MenuItem value="SMS">SMS</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </TabPanel>

          {/* TAB 3: BENEFICIOS Y REFERENCIAS */}
          <TabPanel value={tabValue} index={2}>
            {formData.tipo_persona === 'Natural' && (
              <>
                <Typography variant="h5" sx={{ mb: 2 }}>Beneficios de Ley</Typography>
                <Grid container spacing={2} sx={{ mb: 4, pl: 1 }}>
                  <Grid item xs={12} sm={6}>
                    <FormControlLabel
                      control={<Switch checked={formData.aplica_tercera_edad} onChange={handleChange} name="aplica_tercera_edad" color="primary" />}
                      label="Aplica Tercera Edad"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControlLabel
                      control={<Switch checked={formData.tiene_discapacidad} onChange={handleChange} name="tiene_discapacidad" color="primary" />}
                      label="Tiene Discapacidad"
                    />
                  </Grid>
                  {formData.tiene_discapacidad && (
                    <Grid item xs={12} sm={6}>
                      <TextField label="Porcentaje de Discapacidad (%)" name="porcentaje_discapacidad" type="number" value={formData.porcentaje_discapacidad} onChange={handleChange} fullWidth />
                    </Grid>
                  )}
                </Grid>
              </>
            )}

            <Typography variant="h5" sx={{ mb: 2 }}>Referencia ({formData.tipo_persona === 'Natural' ? 'Cónyuge / Familiar' : 'Representante Legal'})</Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Tipo de Referencia</InputLabel>
                  <Select name="ref_tipo" value={formData.ref_tipo} label="Tipo de Referencia" onChange={handleChange}>
                    {formData.tipo_persona === 'Natural' ? (
                      <>
                        <MenuItem value="Conyuge">Cónyuge</MenuItem>
                        <MenuItem value="Referencia Familiar">Familiar</MenuItem>
                        <MenuItem value="Referencia Personal">Personal</MenuItem>
                      </>
                    ) : (
                      <MenuItem value="Representante Legal">Representante Legal</MenuItem>
                    )}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField label="Identificación" name="ref_identificacion" value={formData.ref_identificacion} onChange={handleChange} fullWidth />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField label="Nombres" name="ref_nombres" value={formData.ref_nombres} onChange={handleChange} fullWidth />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField label="Apellidos" name="ref_apellidos" value={formData.ref_apellidos} onChange={handleChange} fullWidth />
              </Grid>
            </Grid>
          </TabPanel>

        </DialogContent>
        <DialogActions sx={{ p: 3, borderTop: 1, borderColor: 'divider' }}>
          <Button onClick={handleClose} color="error" variant="text" size="large">Cancelar</Button>
          <Button onClick={handleSubmit} variant="contained" color="primary" size="large">
            {editingId ? 'Actualizar Ciudadano' : 'Guardar Ciudadano'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Modal de Confirmación de Estado */}
      <Dialog open={confirmOpen} onClose={() => setConfirmOpen(false)}>
        <DialogTitle>Confirmar Acción</DialogTitle>
        <DialogContent>
          <DialogContentText>
            ¿Seguro que desea cambiar el estado de este ciudadano?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmOpen(false)} color="secondary">Cancelar</Button>
          <Button onClick={handleConfirmStatusChange} color="primary" autoFocus>
            Aceptar
          </Button>
        </DialogActions>
      </Dialog>

      {/* Feedback Visual */}
      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({ ...toast, open: false })} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
        <Alert onClose={() => setToast({ ...toast, open: false })} severity={toast.severity as any} variant="filled" sx={{ width: '100%' }}>
          {toast.message}
        </Alert>
      </Snackbar>
    </MainCard>
  );
}
