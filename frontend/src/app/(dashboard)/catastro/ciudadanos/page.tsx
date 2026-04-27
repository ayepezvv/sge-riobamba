'use client';

import { useEffect, useState } from 'react';
// material-ui
import { useTheme } from '@mui/material/styles';
import { 
  Chip, Box, Button, Dialog, DialogTitle, DialogContent, DialogContentText,
  DialogActions, TextField, FormControl, InputLabel, 
  Select, MenuItem, Snackbar, Alert, Typography,
  Tabs, Tab, Grid, Switch, FormControlLabel, IconButton,
  Card, CardContent, Avatar, Divider, InputAdornment, OutlinedInput
} from '@mui/material';

// icons
import EditIcon from '@mui/icons-material/Edit';
import BlockIcon from '@mui/icons-material/Block';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import EmailTwoToneIcon from '@mui/icons-material/EmailTwoTone';
import PhoneTwoToneIcon from '@mui/icons-material/PhoneTwoTone';
import BusinessIcon from '@mui/icons-material/Business';
import PersonIcon from '@mui/icons-material/Person';
import SearchIcon from '@mui/icons-material/Search';
import AddIcon from '@mui/icons-material/Add';
import CloseIcon from '@mui/icons-material/Close';
import CakeIcon from '@mui/icons-material/Cake';
import AssignmentIndIcon from '@mui/icons-material/AssignmentInd';
import WcIcon from '@mui/icons-material/Wc';

import MainCard from 'ui-component/cards/MainCard';
import { listarCiudadanos, crearCiudadano, actualizarCiudadano, cambiarEstadoCiudadano } from 'api/catastro';

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

// ==============================|| PADRÓN DE CIUDADANOS (CONTACT LIST) ||============================== //

export default function CiudadanosPage() {
  const theme = useTheme();
  const [ciudadanos, setCiudadanos] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  
  // UI State
  const [open, setOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [tabValue, setTabValue] = useState(0);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });

  // Contact List State
  const [selectedUser, setSelectedUser] = useState<any>(null);

  // Dialog State (Desactivar)
  const [confirmOpen, setConfirmOpen] = useState(false);

  // Form State
  const [formData, setFormData] = useState({ ...initialFormData });

  const fetchCiudadanos = async () => {
    try {
      const data = await listarCiudadanos();
      setCiudadanos(data);
      
      // Update selected user if it was modified
      if (selectedUser) {
        const updatedUser = data.find((u: any) => u.id === selectedUser.id);
        if (updatedUser) setSelectedUser(updatedUser);
      }
    } catch (error) {
      console.error("Error fetching citizens:", error);
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
      fecha_nacimiento: ciudadano.fecha_nacimiento ? ciudadano.fecha_nacimiento.substring(0,10) : '',
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
        await actualizarCiudadano(editingId, payload);
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
        await crearCiudadano(payload);
        setToast({ open: true, message: 'Ciudadano registrado exitosamente', severity: 'success' });
      }
      
      handleClose();
      fetchCiudadanos();
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Error al guardar. Verifique los datos.';
      setToast({ open: true, message: typeof errorMsg === 'string' ? errorMsg : 'La identificación ya existe o es inválida.', severity: 'error' });
    }
  };

  const handleConfirmStatusChange = async () => {
    if (!selectedUser) return;
    try {
      await cambiarEstadoCiudadano(selectedUser.id);
      setToast({ open: true, message: 'Estado modificado exitosamente', severity: 'success' });
      setConfirmOpen(false);
      fetchCiudadanos();
    } catch (error: any) {
      setToast({ open: true, message: 'Error al cambiar estado.', severity: 'error' });
      setConfirmOpen(false);
    }
  };

  // Filtrado simple
  const filteredCiudadanos = ciudadanos.filter((c: any) => {
    const searchString = `${c.identificacion} ${c.nombres} ${c.apellidos} ${c.razon_social}`.toLowerCase();
    return searchString.includes(searchQuery.toLowerCase());
  });

  return (
    <MainCard title="Padrón de Ciudadanos y Clientes" content={false}>
      <CardContent>
        {/* HEADER BAR */}
        <Grid container spacing={2} justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
          <Grid size={{ xs: 12, sm: 8, md: 6 }}>
            <OutlinedInput
              id="input-search-contact"
              placeholder="Buscar por nombre, cédula o RUC..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              startAdornment={
                <InputAdornment position="start">
                  <SearchIcon color="secondary" />
                </InputAdornment>
              }
              size="small"
              fullWidth
            />
          </Grid>
          <Grid size={{ xs: 12, sm: 4, md: 6 }} sx={{ textAlign: 'right' }}>
            <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={handleOpenNew}>
              Nuevo Ciudadano
            </Button>
          </Grid>
        </Grid>

        {/* SPLIT VIEW (LIST vs DETAILS) */}
        <Grid container spacing={3}>
          {/* Left Column: List */}
          <Grid size={{ xs: 12, md: selectedUser ? 8 : 12 }}>
            {filteredCiudadanos.map((row: any, index) => {
              const isNatural = row.tipo_persona === 'Natural';
              const titleName = isNatural ? `${row.nombres || ''} ${row.apellidos || ''}` : row.razon_social;
              const isActive = row.is_active ?? true;
              const isSelected = selectedUser?.id === row.id;

              return (
                <Card 
                  key={index} 
                  sx={{ 
                    bgcolor: isSelected ? (theme.palette.mode === 'dark' ? 'dark.main' : 'primary.light') : (theme.palette.mode === 'dark' ? 'dark.main' : 'background.paper'),
                    mb: 1, 
                    border: '1px solid', 
                    borderColor: isSelected ? 'primary.main' : 'divider',
                    cursor: 'pointer',
                    '&:hover': { borderColor: 'primary.main', bgcolor: theme.palette.mode === 'dark' ? 'dark.800' : 'grey.50' }
                  }}
                  onClick={() => setSelectedUser(row)}
                >
                  <CardContent sx={{ p: 2, pb: '16px !important' }}>
                    <Grid container spacing={2} alignItems="center">
                      <Grid>
                        <Avatar
                          sx={{ 
                            width: 40, height: 40, 
                            bgcolor: isNatural ? theme.palette.primary.light : theme.palette.secondary.light,
                            color: isNatural ? theme.palette.primary.dark : theme.palette.secondary.dark
                          }}
                        >
                          {isNatural ? <PersonIcon /> : <BusinessIcon />}
                        </Avatar>
                      </Grid>
                      <Grid size="grow" sx={{ minWidth: 0 }}>
                        <Typography variant="h5" component="div">{titleName}</Typography>
                        <Typography variant="caption" color="textSecondary">{row.identificacion} • {row.tipo_persona}</Typography>
                      </Grid>
                      
                      {/* Mostrar iconos rapido en la lista si no esta seleccionado o si hay espacio */}
                      <Grid>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                           {isActive ? <Chip label="Activo" color="success" size="small" /> : <Chip label="Inactivo" color="error" size="small" />}
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              );
            })}
          </Grid>

          {/* Right Column: Details (Sliding Panel) */}
          {selectedUser && (
            <Grid size={{ xs: 12, md: 4 }}>
              <Card sx={{ border: '1px solid', borderColor: 'divider', height: '100%', position: 'relative' }}>
                <CardContent>
                  <IconButton 
                    sx={{ position: 'absolute', top: 8, right: 8 }} 
                    onClick={() => setSelectedUser(null)}
                  >
                    <CloseIcon />
                  </IconButton>
                  
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 2 }}>
                    <Avatar
                      sx={{ 
                        width: 80, height: 80, mb: 2,
                        bgcolor: selectedUser.tipo_persona === 'Natural' ? theme.palette.primary.light : theme.palette.secondary.light,
                        color: selectedUser.tipo_persona === 'Natural' ? theme.palette.primary.dark : theme.palette.secondary.dark
                      }}
                    >
                      {selectedUser.tipo_persona === 'Natural' ? <PersonIcon fontSize="large" /> : <BusinessIcon fontSize="large" />}
                    </Avatar>
                    <Typography variant="h4" textAlign="center">
                      {selectedUser.tipo_persona === 'Natural' ? `${selectedUser.nombres} ${selectedUser.apellidos}` : selectedUser.razon_social}
                    </Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                      {selectedUser.identificacion}
                    </Typography>
                    <Chip 
                      label={selectedUser.tipo_persona} 
                      color={selectedUser.tipo_persona === 'Natural' ? 'primary' : 'secondary'} 
                      size="small" 
                      variant="outlined" 
                    />
                  </Box>

                  <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mt: 3, mb: 3 }}>
                    <Button variant="outlined" startIcon={<EditIcon />} onClick={() => handleOpenEdit(selectedUser)}>
                      Editar
                    </Button>
                    <Button 
                      variant="outlined" 
                      color={(selectedUser.is_active ?? true) ? "error" : "success"}
                      startIcon={(selectedUser.is_active ?? true) ? <BlockIcon /> : <CheckCircleOutlineIcon />} 
                      onClick={() => setConfirmOpen(true)}
                    >
                      {(selectedUser.is_active ?? true) ? "Bloquear" : "Activar"}
                    </Button>
                  </Box>

                  <Divider />

                  <Box sx={{ mt: 3, display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <Typography variant="subtitle1" color="primary">Información de Contacto</Typography>
                    <Grid container spacing={2}>
                      <Grid size={{ xs: 12, sm: 6 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <EmailTwoToneIcon color="secondary" fontSize="small" />
                          <Box>
                            <Typography variant="caption" color="textSecondary" display="block">Correo</Typography>
                            <Typography variant="body2">{selectedUser.correo_principal || 'No registrado'}</Typography>
                          </Box>
                        </Box>
                      </Grid>
                      <Grid size={{ xs: 12, sm: 6 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <PhoneTwoToneIcon color="secondary" fontSize="small" />
                          <Box>
                            <Typography variant="caption" color="textSecondary" display="block">Teléfonos</Typography>
                            <Typography variant="body2">{selectedUser.celular} / {selectedUser.telefono_fijo || 'N/A'}</Typography>
                          </Box>
                        </Box>
                      </Grid>
                    </Grid>

                    <Divider sx={{ my: 1 }} />
                    <Typography variant="subtitle1" color="primary">Datos Demográficos / Comerciales</Typography>
                    
                    <Grid container spacing={2}>
                      {selectedUser.tipo_persona === 'Natural' && selectedUser.fecha_nacimiento && (
                        <Grid size={{ xs: 12, sm: 6 }}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <CakeIcon color="secondary" fontSize="small" />
                            <Box>
                              <Typography variant="caption" color="textSecondary" display="block">Nacimiento</Typography>
                              <Typography variant="body2">{selectedUser.fecha_nacimiento}</Typography>
                            </Box>
                          </Box>
                        </Grid>
                      )}
                      {selectedUser.tipo_persona === 'Natural' && selectedUser.genero && (
                        <Grid size={{ xs: 12, sm: 6 }}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <WcIcon color="secondary" fontSize="small" />
                            <Box>
                              <Typography variant="caption" color="textSecondary" display="block">Género</Typography>
                              <Typography variant="body2">{selectedUser.genero}</Typography>
                            </Box>
                          </Box>
                        </Grid>
                      )}
                      {selectedUser.tipo_persona === 'Juridica' && selectedUser.tipo_empresa && (
                        <Grid size={12}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <BusinessIcon color="secondary" fontSize="small" />
                            <Box>
                              <Typography variant="caption" color="textSecondary" display="block">Estructura</Typography>
                              <Typography variant="body2">{selectedUser.tipo_empresa} - {selectedUser.naturaleza_juridica}</Typography>
                            </Box>
                          </Box>
                        </Grid>
                      )}
                    </Grid>

                    {/* Beneficios (Si aplican) */}
                    {(selectedUser.tiene_discapacidad || selectedUser.aplica_tercera_edad) && (
                      <>
                        <Divider sx={{ my: 1 }} />
                        <Typography variant="subtitle1" color="primary">Beneficios de Ley</Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mt: 1 }}>
                          <AssignmentIndIcon color="secondary" />
                          <Box>
                            {selectedUser.aplica_tercera_edad && <Chip label="Tercera Edad" size="small" color="info" sx={{ mr: 1 }} />}
                            {selectedUser.tiene_discapacidad && <Chip label={`Discapacidad (${selectedUser.porcentaje_discapacidad}%)`} size="small" color="warning" />}
                          </Box>
                        </Box>
                      </>
                    )}
                    
                    {/* Referencias Anidadas */}
                    {selectedUser.referencias && selectedUser.referencias.length > 0 && (
                      <>
                        <Divider sx={{ my: 1 }} />
                        <Typography variant="subtitle1" color="primary">Referencias Registradas</Typography>
                        {selectedUser.referencias.map((ref: any, idx: number) => (
                           <Box key={idx} sx={{ p: 1.5, bgcolor: 'background.default', borderRadius: 1, border: '1px dashed', borderColor: 'divider' }}>
                             <Typography variant="body2" fontWeight="bold">{ref.tipo_referencia}</Typography>
                             <Typography variant="body2">{ref.nombres} {ref.apellidos}</Typography>
                             <Typography variant="caption" color="textSecondary">CI: {ref.identificacion || 'N/A'}</Typography>
                           </Box>
                        ))}
                      </>
                    )}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      </CardContent>

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
              <Grid size={12}>
                <FormControl fullWidth>
                  <InputLabel>Tipo de Persona</InputLabel>
                  <Select name="tipo_persona" value={formData.tipo_persona} label="Tipo de Persona" onChange={handleChange} disabled={!!editingId}>
                    <MenuItem value="Natural">Persona Natural</MenuItem>
                    <MenuItem value="Juridica">Persona Jurídica</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={{ xs: 12, sm: 6 }}>
                <TextField label="Identificación (Cédula/RUC)" name="identificacion" value={formData.identificacion} onChange={handleChange} fullWidth required />
              </Grid>

              {formData.tipo_persona === 'Natural' && (
                <>
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <TextField label="Nombres" name="nombres" value={formData.nombres} onChange={handleChange} fullWidth required />
                  </Grid>
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <TextField label="Apellidos" name="apellidos" value={formData.apellidos} onChange={handleChange} fullWidth required />
                  </Grid>
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <TextField label="Fecha de Nacimiento" name="fecha_nacimiento" type="date" value={formData.fecha_nacimiento} onChange={handleChange} fullWidth InputLabelProps={{ shrink: true }} />
                  </Grid>
                  <Grid size={{ xs: 12, sm: 6 }}>
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
                  <Grid size={12}>
                    <TextField label="Razón Social" name="razon_social" value={formData.razon_social} onChange={handleChange} fullWidth required />
                  </Grid>
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <FormControl fullWidth>
                      <InputLabel>Tipo de Empresa</InputLabel>
                      <Select name="tipo_empresa" value={formData.tipo_empresa} label="Tipo de Empresa" onChange={handleChange}>
                        <MenuItem value="Publica">Pública</MenuItem>
                        <MenuItem value="Privada">Privada</MenuItem>
                        <MenuItem value="Mixta">Mixta</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid size={{ xs: 12, sm: 6 }}>
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
              <Grid size={12}>
                <TextField label="Correo Electrónico" name="correo_principal" type="email" value={formData.correo_principal} onChange={handleChange} fullWidth />
              </Grid>
              <Grid size={{ xs: 12, sm: 6 }}>
                <TextField label="Celular" name="celular" value={formData.celular} onChange={handleChange} fullWidth />
              </Grid>
              <Grid size={{ xs: 12, sm: 6 }}>
                <TextField label="Teléfono Fijo" name="telefono_fijo" value={formData.telefono_fijo} onChange={handleChange} fullWidth />
              </Grid>
              <Grid size={12}>
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
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <FormControlLabel
                      control={<Switch checked={formData.aplica_tercera_edad} onChange={handleChange} name="aplica_tercera_edad" color="primary" />}
                      label="Aplica Tercera Edad"
                    />
                  </Grid>
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <FormControlLabel
                      control={<Switch checked={formData.tiene_discapacidad} onChange={handleChange} name="tiene_discapacidad" color="primary" />}
                      label="Tiene Discapacidad"
                    />
                  </Grid>
                  {formData.tiene_discapacidad && (
                    <Grid size={{ xs: 12, sm: 6 }}>
                      <TextField label="Porcentaje de Discapacidad (%)" name="porcentaje_discapacidad" type="number" value={formData.porcentaje_discapacidad} onChange={handleChange} fullWidth />
                    </Grid>
                  )}
                </Grid>
              </>
            )}

            <Typography variant="h5" sx={{ mb: 2 }}>Referencia ({formData.tipo_persona === 'Natural' ? 'Cónyuge / Familiar' : 'Representante Legal'})</Typography>
            <Grid container spacing={2}>
              <Grid size={{ xs: 12, sm: 6 }}>
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
              <Grid size={{ xs: 12, sm: 6 }}>
                <TextField label="Identificación" name="ref_identificacion" value={formData.ref_identificacion} onChange={handleChange} fullWidth />
              </Grid>
              <Grid size={{ xs: 12, sm: 6 }}>
                <TextField label="Nombres" name="ref_nombres" value={formData.ref_nombres} onChange={handleChange} fullWidth />
              </Grid>
              <Grid size={{ xs: 12, sm: 6 }}>
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
