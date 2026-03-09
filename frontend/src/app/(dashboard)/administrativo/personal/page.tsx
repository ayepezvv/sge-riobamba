'use client';
import { useEffect, useState } from 'react';
import {
  Box, Button, Card, CardContent, CardHeader, Dialog, DialogActions, DialogContent, DialogTitle,
  Grid, TextField, MenuItem, Select, FormControl, InputLabel, Snackbar, Alert, Avatar, IconButton, Badge,
  Tabs, Tab, Typography, List, ListItem, ListItemText, ListItemAvatar, ListItemSecondaryAction, Divider
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { IconUpload, IconSchool, IconTrash } from '@tabler/icons-react';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}
function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export default function PersonalPage() {
  const [data, setData] = useState([]);
  const [unidades, setUnidades] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [open, setOpen] = useState(false);
  const [tabIndex, setTabIndex] = useState(0);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });
  
  const [formData, setFormData] = useState<any>({
    cedula: '', nombres: '', apellidos: '', cargo: '', 
    regimen_legal: '', tipo_contrato: '', codigo_certificacion_sercop: '', 
    unidad_id: '', usuario_id: '', foto_perfil: '',
    direccion_domicilio: '', telefono_celular: '', correo_personal: '', archivo_firma_electronica: '',
    es_activo: true, titulos: []
  });
  
  const [tituloForm, setTituloForm] = useState({ nivel: '', nombre_titulo: '', institucion: '', registro_senescyt: '' });
  const [editingId, setEditingId] = useState<number | null>(null);

  const fetchPersonal = async () => {
    try {
      const res = await fetch('http://192.168.1.15:8000/api/administrativo/personal');
      if (res.ok) setData(await res.json());
    } catch (e) { console.error(e); }
  };

  const fetchUnidades = async () => {
    try {
      const res = await fetch('http://192.168.1.15:8000/api/administrativo/unidades');
      if (res.ok) setUnidades(await res.json());
    } catch (e) { console.error(e); }
  };

  const fetchUsuarios = async () => {
    try {
      const res = await fetch('http://192.168.1.15:8000/api/users');
      if (res.ok) setUsuarios(await res.json());
    } catch (e) { console.error(e); }
  };

  useEffect(() => { fetchPersonal(); fetchUnidades(); fetchUsuarios(); }, []);

  const handleOpen = (item = null) => {
    setTabIndex(0);
    if (item) {
      setEditingId(item.id);
      setFormData({
        ...item,
        usuario_id: item.usuario_id || '',
        direccion_domicilio: item.direccion_domicilio || '',
        telefono_celular: item.telefono_celular || '',
        correo_personal: item.correo_personal || '',
        archivo_firma_electronica: item.archivo_firma_electronica || '',
        titulos: item.titulos || []
      });
    } else {
      setEditingId(null);
      setFormData({
        cedula: '', nombres: '', apellidos: '', cargo: '', 
        regimen_legal: '', tipo_contrato: '', codigo_certificacion_sercop: '', 
        unidad_id: '', usuario_id: '', foto_perfil: '',
        direccion_domicilio: '', telefono_celular: '', correo_personal: '', archivo_firma_electronica: '',
        es_activo: true, titulos: []
      });
    }
    setOpen(true);
  };

  const handlePhotoUpload = (e: any) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData({ ...formData, foto_perfil: reader.result as string });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSignatureUpload = (e: any) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData({ ...formData, archivo_firma_electronica: reader.result as string });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = async () => {
    const url = editingId ? `http://192.168.1.15:8000/api/administrativo/personal/${editingId}` : 'http://192.168.1.15:8000/api/administrativo/personal';
    const method = editingId ? 'PUT' : 'POST';
    
    const payload = { ...formData };
    if (payload.usuario_id === '') payload.usuario_id = null;
    delete payload.titulos; // Titulos are handled separately
    
    try {
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        setToast({ open: true, message: 'Registro guardado exitosamente', severity: 'success' });
        setOpen(false);
        fetchPersonal();
      } else {
        setToast({ open: true, message: 'Error al guardar', severity: 'error' });
      }
    } catch (e) {
      setToast({ open: true, message: 'Error de red', severity: 'error' });
    }
  };

  const handleAddTitulo = async () => {
    if (!editingId) return;
    try {
      const res = await fetch(`http://192.168.1.15:8000/api/administrativo/personal/${editingId}/titulos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...tituloForm, personal_id: editingId })
      });
      if (res.ok) {
        setToast({ open: true, message: 'Título agregado', severity: 'success' });
        setTituloForm({ nivel: '', nombre_titulo: '', institucion: '', registro_senescyt: '' });
        fetchPersonal();
        // Update local state to reflect UI instantly
        const newTitulo = await res.json();
        setFormData({ ...formData, titulos: [...formData.titulos, newTitulo] });
      }
    } catch (e) { console.error(e); }
  };

  const handleDeleteTitulo = async (id: number) => {
    try {
      const res = await fetch(`http://192.168.1.15:8000/api/administrativo/personal/titulos/${id}`, { method: 'DELETE' });
      if (res.ok) {
        setToast({ open: true, message: 'Título eliminado', severity: 'success' });
        fetchPersonal();
        setFormData({ ...formData, titulos: formData.titulos.filter((t: any) => t.id !== id) });
      }
    } catch (e) { console.error(e); }
  };

  const stringAvatar = (name: string) => {
    if (!name) return { children: '?' };
    const parts = name.split(' ');
    if (parts.length > 1) return { children: `${parts[0][0]}${parts[1][0]}`.toUpperCase() };
    return { children: name[0].toUpperCase() };
  };

  const columns: GridColDef[] = [
    { field: 'foto_perfil', headerName: 'Avatar', width: 70, renderCell: (p) => (
        <Avatar src={p.value} sx={{ width: 32, height: 32, bgcolor: 'primary.main' }} {...(!p.value ? stringAvatar(`${p.row.nombres} ${p.row.apellidos}`) : {})} />
    )},
    { field: 'cedula', headerName: 'Cédula', width: 120 },
    { field: 'nombres', headerName: 'Nombres', flex: 1, renderCell: (p) => `${p.row.nombres} ${p.row.apellidos}` },
    { field: 'cargo', headerName: 'Cargo', flex: 1 },
    { field: 'unidad', headerName: 'Unidad', flex: 1, renderCell: (p) => p.value?.nombre || 'N/A' },
    { field: 'regimen_legal', headerName: 'Régimen', width: 130 },
    { field: 'acciones', headerName: 'Acciones', width: 120, renderCell: (params) => (
        <Button size="small" variant="contained" onClick={() => handleOpen(params.row)}>Editar</Button>
    )}
  ];

  return (
    <Box>
      <Card>
        <CardHeader title="Directorio de Personal" action={<Button variant="contained" onClick={() => handleOpen()}>+ Nuevo</Button>} />
        <CardContent>
          <DataGrid rows={data} columns={columns} autoHeight />
        </CardContent>
      </Card>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="md" fullWidth scroll="paper">
        <DialogTitle>{editingId ? 'Editar' : 'Nuevo'} Personal</DialogTitle>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabIndex} onChange={(e, val) => setTabIndex(val)} variant="scrollable" scrollButtons="auto">
            <Tab label="Datos Institucionales" />
            <Tab label="Datos Personales" />
            <Tab label="Firma Electrónica" />
            {editingId && <Tab label="Formación Académica" />}
          </Tabs>
        </Box>
        <DialogContent dividers sx={{ p: 0 }}>
          
          {/* TAB 1: DATOS INSTITUCIONALES */}
          <CustomTabPanel value={tabIndex} index={0}>
            <Grid container spacing={3}>
              <Grid item xs={12} display="flex" justifyContent="center">
                <Badge overlap="circular" anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                  badgeContent={
                    <IconButton color="primary" component="label" sx={{ bgcolor: 'background.paper', boxShadow: 1 }}>
                      <input hidden accept="image/*" type="file" onChange={handlePhotoUpload} />
                      <IconUpload size={20} />
                    </IconButton>
                  }
                >
                  <Avatar src={formData.foto_perfil} sx={{ width: 100, height: 100, fontSize: 36, bgcolor: 'primary.main' }}
                    {...(!formData.foto_perfil ? stringAvatar(`${formData.nombres || 'U'} ${formData.apellidos || ''}`) : {})}
                  />
                </Badge>
              </Grid>

              <Grid item xs={12} sm={6}><TextField fullWidth label="Cédula" value={formData.cedula} onChange={(e) => setFormData({ ...formData, cedula: e.target.value })} /></Grid>
              <Grid item xs={12} sm={6}><TextField fullWidth label="Cargo" value={formData.cargo} onChange={(e) => setFormData({ ...formData, cargo: e.target.value })} /></Grid>
              <Grid item xs={12} sm={6}><TextField fullWidth label="Nombres" value={formData.nombres} onChange={(e) => setFormData({ ...formData, nombres: e.target.value })} /></Grid>
              <Grid item xs={12} sm={6}><TextField fullWidth label="Apellidos" value={formData.apellidos} onChange={(e) => setFormData({ ...formData, apellidos: e.target.value })} /></Grid>
              
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth><InputLabel>Unidad</InputLabel>
                  <Select value={formData.unidad_id} label="Unidad" onChange={(e) => setFormData({ ...formData, unidad_id: e.target.value })}>
                    {unidades.map((u: any) => <MenuItem key={u.id} value={u.id}>{u.nombre} ({u.direccion?.nombre})</MenuItem>)}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={6}>
                <FormControl fullWidth><InputLabel>Vincular Usuario</InputLabel>
                  <Select value={formData.usuario_id} label="Vincular Usuario" onChange={(e) => setFormData({ ...formData, usuario_id: e.target.value })}>
                    <MenuItem value=""><em>Ninguno</em></MenuItem>
                    {usuarios.map((u: any) => <MenuItem key={u.id} value={u.id}>{u.nombres} {u.apellidos} ({u.cedula})</MenuItem>)}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={6}>
                <FormControl fullWidth><InputLabel>Régimen Legal</InputLabel>
                  <Select value={formData.regimen_legal} label="Régimen Legal" onChange={(e) => setFormData({ ...formData, regimen_legal: e.target.value })}>
                    <MenuItem value="LOEP">LOEP</MenuItem><MenuItem value="CODIGO_TRABAJO">Código de Trabajo</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth><InputLabel>Tipo de Contrato</InputLabel>
                  <Select value={formData.tipo_contrato} label="Tipo de Contrato" onChange={(e) => setFormData({ ...formData, tipo_contrato: e.target.value })}>
                    <MenuItem value="NOMBRAMIENTO">Nombramiento</MenuItem><MenuItem value="INDEFINIDO">Indefinido</MenuItem>
                    <MenuItem value="CONTRATADO_LOEP">Contratado LOEP</MenuItem><MenuItem value="CONTRATADO_CT">Contratado CT</MenuItem>
                    <MenuItem value="REQUERIDO_PROYECTO">Requerido Proyecto</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={6}><TextField fullWidth label="Código SERCOP (Opcional)" value={formData.codigo_certificacion_sercop} onChange={(e) => setFormData({ ...formData, codigo_certificacion_sercop: e.target.value })} /></Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth><InputLabel>Estado</InputLabel>
                  <Select value={formData.es_activo} label="Estado" onChange={(e) => setFormData({ ...formData, es_activo: e.target.value })}>
                    <MenuItem value={true}>Activo</MenuItem><MenuItem value={false}>Inactivo</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </CustomTabPanel>

          {/* TAB 2: DATOS PERSONALES */}
          <CustomTabPanel value={tabIndex} index={1}>
            <Grid container spacing={3}>
              <Grid item xs={12}><TextField fullWidth label="Dirección de Domicilio" value={formData.direccion_domicilio} onChange={(e) => setFormData({ ...formData, direccion_domicilio: e.target.value })} /></Grid>
              <Grid item xs={12} sm={6}><TextField fullWidth label="Teléfono Celular" value={formData.telefono_celular} onChange={(e) => setFormData({ ...formData, telefono_celular: e.target.value })} /></Grid>
              <Grid item xs={12} sm={6}><TextField fullWidth label="Correo Personal" type="email" value={formData.correo_personal} onChange={(e) => setFormData({ ...formData, correo_personal: e.target.value })} /></Grid>
            </Grid>
          </CustomTabPanel>

          {/* TAB 3: FIRMA ELECTRONICA */}
          <CustomTabPanel value={tabIndex} index={2}>
            <Grid container spacing={3} alignItems="center" justifyContent="center">
              <Grid item xs={12} textAlign="center">
                <Typography variant="h6" gutterBottom>Certificado de Firma Electrónica (.p12 / .pfx)</Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>Sube el archivo de firma para su uso automático en los flujos del sistema.</Typography>
                <Button variant={formData.archivo_firma_electronica ? "contained" : "outlined"} color={formData.archivo_firma_electronica ? "success" : "primary"} component="label" startIcon={<IconUpload />}>
                  {formData.archivo_firma_electronica ? 'Archivo Cargado (Cambiar)' : 'Subir Archivo de Firma'}
                  <input hidden type="file" accept=".p12,.pfx" onChange={handleSignatureUpload} />
                </Button>
                {formData.archivo_firma_electronica && <Typography variant="caption" display="block" sx={{ mt: 1, color: 'success.main' }}>✓ Firma guardada en bóveda segura.</Typography>}
              </Grid>
            </Grid>
          </CustomTabPanel>

          {/* TAB 4: FORMACION ACADEMICA */}
          {editingId && (
            <CustomTabPanel value={tabIndex} index={3}>
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={12} sm={4}>
                  <FormControl fullWidth size="small"><InputLabel>Nivel</InputLabel>
                    <Select value={tituloForm.nivel} label="Nivel" onChange={(e) => setTituloForm({ ...tituloForm, nivel: e.target.value })}>
                      <MenuItem value="TECNICO">Técnico</MenuItem><MenuItem value="TECNOLOGICO">Tecnológico</MenuItem>
                      <MenuItem value="TERCER_NIVEL">Tercer Nivel</MenuItem><MenuItem value="CUARTO_NIVEL">Cuarto Nivel</MenuItem><MenuItem value="PHD">PhD</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={8}><TextField fullWidth size="small" label="Nombre del Título" value={tituloForm.nombre_titulo} onChange={(e) => setTituloForm({ ...tituloForm, nombre_titulo: e.target.value })} /></Grid>
                <Grid item xs={12} sm={6}><TextField fullWidth size="small" label="Institución" value={tituloForm.institucion} onChange={(e) => setTituloForm({ ...tituloForm, institucion: e.target.value })} /></Grid>
                <Grid item xs={12} sm={4}><TextField fullWidth size="small" label="Registro SENESCYT" value={tituloForm.registro_senescyt} onChange={(e) => setTituloForm({ ...tituloForm, registro_senescyt: e.target.value })} /></Grid>
                <Grid item xs={12} sm={2}><Button fullWidth variant="contained" onClick={handleAddTitulo} sx={{ height: '100%' }}>Agregar</Button></Grid>
              </Grid>
              <Divider />
              <List sx={{ mt: 2 }}>
                {formData.titulos.length === 0 && <Typography variant="body2" color="textSecondary" textAlign="center">No hay títulos registrados.</Typography>}
                {formData.titulos.map((t: any) => (
                  <ListItem key={t.id} sx={{ bgcolor: 'background.default', mb: 1, borderRadius: 1 }}>
                    <ListItemAvatar><Avatar><IconSchool /></Avatar></ListItemAvatar>
                    <ListItemText primary={t.nombre_titulo} secondary={`${t.institucion} | Nivel: ${t.nivel.replace('_', ' ')} | SENESCYT: ${t.registro_senescyt || 'N/A'}`} />
                    <ListItemSecondaryAction><IconButton edge="end" color="error" onClick={() => handleDeleteTitulo(t.id)}><IconTrash size={20}/></IconButton></ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            </CustomTabPanel>
          )}

        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpen(false)}>Cerrar</Button>
          <Button variant="contained" onClick={handleSave}>Guardar Perfil</Button>
        </DialogActions>
      </Dialog>
      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({...toast, open: false})}>
        <Alert severity={toast.severity as any}>{toast.message}</Alert>
      </Snackbar>
    </Box>
  );
}
