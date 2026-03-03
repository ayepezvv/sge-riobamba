'use client';

import { useEffect, useState, MouseEvent } from 'react';
import { useTheme } from '@mui/material/styles';
import { 
  Chip, Box, Button, Dialog, DialogTitle, DialogContent, DialogContentText,
  DialogActions, TextField, FormControl, InputLabel, 
  Select, MenuItem, Snackbar, Alert, Typography,
  Grid, Card, CardContent, Avatar, Menu, IconButton, Tooltip
} from '@mui/material';

// Icons
import EditIcon from '@mui/icons-material/Edit';
import BlockIcon from '@mui/icons-material/Block';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import MoreVertTwoToneIcon from '@mui/icons-material/MoreVertTwoTone';
import EmailTwoToneIcon from '@mui/icons-material/EmailTwoTone';
import ChatBubbleTwoToneIcon from '@mui/icons-material/ChatBubbleTwoTone';
import PhoneTwoToneIcon from '@mui/icons-material/PhoneTwoTone';
import AddIcon from '@mui/icons-material/Add';

import MainCard from 'ui-component/cards/MainCard';
import axios from 'utils/axios';

const initialFormData = {
  cedula: '',
  nombres: '',
  apellidos: '',
  correo: '',
  password: '',
  role_id: ''
};

// ==============================|| GESTIÓN DE USUARIOS (CARD VIEW) ||============================== //

export default function UsuariosPage() {
  const theme = useTheme();
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  
  // UI State
  const [open, setOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });

  // Dialog State (Desactivar)
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [selectedUserForStatus, setSelectedUserForStatus] = useState<any>(null);

  // Form State
  const [formData, setFormData] = useState({ ...initialFormData });

  // Menu State para las tarjetas
  const [anchorEl, setAnchorEl] = useState<{ [key: number]: HTMLElement | null }>({});

  const fetchUsers = async () => {
    try {
      const response = await axios.get('/api/users/');
      setUsers(response.data);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  const fetchRoles = async () => {
    try {
      const response = await axios.get('/api/roles/');
      setRoles(response.data);
    } catch (error) {
      console.error("Error fetching roles:", error);
    }
  };

  useEffect(() => {
    fetchUsers();
    fetchRoles();
  }, []);

  const handleOpenNew = () => {
    setEditingId(null);
    setFormData({ ...initialFormData });
    setOpen(true);
  };

  const handleOpenEdit = (user: any) => {
    handleMenuClose(user.id);
    setEditingId(user.id);
    setFormData({
      cedula: user.cedula,
      nombres: user.nombres,
      apellidos: user.apellidos,
      correo: user.correo,
      password: '', // Blank password on edit means it won't be updated
      role_id: user.role_id ? user.role_id.toString() : ''
    });
    setOpen(true);
  };
  
  const handleClose = () => {
    setOpen(false);
    setFormData({ ...initialFormData });
  };

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async () => {
    try {
      const payload: any = { 
        ...formData, 
        role_id: formData.role_id ? parseInt(formData.role_id) : null 
      };

      if (editingId) {
        if (!payload.password) {
          delete payload.password;
        }
        await axios.put(`/api/users/${editingId}`, payload);
        setToast({ open: true, message: 'Usuario actualizado exitosamente', severity: 'success' });
      } else {
        await axios.post('/api/users/', payload);
        setToast({ open: true, message: 'Usuario creado exitosamente', severity: 'success' });
      }
      
      handleClose();
      fetchUsers();
    } catch (error: any) {
      console.error("Error saving user:", error);
      const errorMsg = error.response?.data?.detail || 'Error al guardar usuario. Verifica los datos.';
      setToast({ open: true, message: errorMsg, severity: 'error' });
    }
  };

  const handleToggleStatusClick = (user: any) => {
    handleMenuClose(user.id);
    setSelectedUserForStatus(user);
    setConfirmOpen(true);
  };

  const handleConfirmStatusChange = async () => {
    if (!selectedUserForStatus) return;
    try {
      await axios.patch(`/api/users/${selectedUserForStatus.id}/status`);
      setToast({ open: true, message: 'Estado del usuario modificado exitosamente', severity: 'success' });
      setConfirmOpen(false);
      fetchUsers();
    } catch (error: any) {
      console.error("Error changing status:", error);
      setToast({ open: true, message: 'Error al cambiar estado.', severity: 'error' });
      setConfirmOpen(false);
    }
  };

  const handleMenuClick = (event: MouseEvent<HTMLElement>, userId: number) => {
    setAnchorEl({ ...anchorEl, [userId]: event.currentTarget });
  };

  const handleMenuClose = (userId: number) => {
    setAnchorEl({ ...anchorEl, [userId]: null });
  };

  return (
    <MainCard 
      title="Gestión de Personal"
      secondary={
        <Button variant="contained" color="secondary" startIcon={<AddIcon />} onClick={handleOpenNew}>
          Nuevo Usuario
        </Button>
      }
    >
      <Grid container spacing={3} sx={{ mt: 1 }}>
        {users.map((user: any) => {
          const isActive = user.is_active;
          const roleName = roles.find((r: any) => r.id === user.role_id)?.nombre_rol || 'Sin Rol';

          return (
            <Grid item xs={12} sm={6} md={4} lg={3} key={user.id}>
              <Card sx={{ 
                bgcolor: theme.palette.mode === 'dark' ? 'dark.main' : 'background.paper', 
                border: '1px solid', 
                borderColor: 'divider',
                textAlign: 'center',
                pt: 3,
                pb: 2,
                position: 'relative'
              }}>
                <IconButton
                  size="small"
                  sx={{ position: 'absolute', right: 8, top: 8 }}
                  onClick={(e) => handleMenuClick(e, user.id)}
                >
                  <MoreVertTwoToneIcon />
                </IconButton>
                <Menu
                  anchorEl={anchorEl[user.id]}
                  keepMounted
                  open={Boolean(anchorEl[user.id])}
                  onClose={() => handleMenuClose(user.id)}
                  anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                  transformOrigin={{ vertical: 'top', horizontal: 'right' }}
                >
                  <MenuItem onClick={() => handleOpenEdit(user)}>
                    <EditIcon sx={{ mr: 1.5, fontSize: '1.25rem' }} /> Editar
                  </MenuItem>
                  <MenuItem onClick={() => handleToggleStatusClick(user)} sx={{ color: isActive ? 'error.main' : 'success.main' }}>
                    {isActive ? <BlockIcon sx={{ mr: 1.5, fontSize: '1.25rem' }} /> : <CheckCircleOutlineIcon sx={{ mr: 1.5, fontSize: '1.25rem' }} />}
                    {isActive ? 'Bloquear' : 'Activar'}
                  </MenuItem>
                </Menu>

                <CardContent sx={{ p: 0, pb: '0 !important' }}>
                  <Avatar
                    sx={{
                      width: 72,
                      height: 72,
                      m: '0 auto',
                      bgcolor: isActive ? theme.palette.secondary.light : theme.palette.grey[300],
                      color: isActive ? theme.palette.secondary.dark : theme.palette.grey[600]
                    }}
                  >
                    {user.nombres.charAt(0)}{user.apellidos.charAt(0)}
                  </Avatar>
                  <Typography variant="h4" sx={{ mt: 2 }}>{user.nombres} {user.apellidos}</Typography>
                  <Typography variant="caption" color="textSecondary" sx={{ mb: 1, display: 'block' }}>{user.cedula}</Typography>
                  
                  <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, my: 1.5 }}>
                    <Chip label={roleName} size="small" variant="outlined" color="primary" />
                    <Chip label={isActive ? 'Activo' : 'Inactivo'} size="small" color={isActive ? 'success' : 'error'} />
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1, mt: 2, px: 2 }}>
                    <EmailTwoToneIcon color="secondary" fontSize="small" />
                    <Typography variant="body2" noWrap>{user.correo}</Typography>
                  </Box>

                  {/* Future Omnichannel Integration */}
                  <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mt: 3, pt: 2, borderTop: '1px solid', borderColor: 'divider' }}>
                    <Tooltip title="Mensaje Interno (Próximamente)">
                      <IconButton color="secondary" size="small">
                        <ChatBubbleTwoToneIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Llamada (Próximamente)">
                      <IconButton color="secondary" size="small">
                        <PhoneTwoToneIcon />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      {/* Modal de Creación / Edición */}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ fontSize: '1.25rem', fontWeight: 600 }}>
          {editingId ? 'Editar Usuario' : 'Crear Nuevo Usuario'}
        </DialogTitle>
        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 1 }}>
            <TextField label="Cédula" name="cedula" value={formData.cedula} onChange={handleChange} fullWidth required />
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField label="Nombres" name="nombres" value={formData.nombres} onChange={handleChange} fullWidth required />
              <TextField label="Apellidos" name="apellidos" value={formData.apellidos} onChange={handleChange} fullWidth required />
            </Box>
            <TextField label="Correo Electrónico" name="correo" type="email" value={formData.correo} onChange={handleChange} fullWidth required />
            
            <TextField 
              label="Contraseña" 
              name="password" 
              type="password" 
              value={formData.password} 
              onChange={handleChange} 
              fullWidth 
              required={!editingId} 
              helperText={editingId ? "Deja en blanco si no deseas cambiar la contraseña" : ""}
            />
            
            <FormControl fullWidth required>
              <InputLabel id="role-select-label">Rol del Usuario</InputLabel>
              <Select 
                labelId="role-select-label"
                name="role_id" 
                value={formData.role_id} 
                label="Rol del Usuario" 
                onChange={handleChange}
              >
                {roles.map((role: any) => (
                  <MenuItem key={role.id} value={role.id}>{role.nombre_rol}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={handleClose} color="error" variant="text">Cancelar</Button>
          <Button onClick={handleSubmit} variant="contained" color="secondary">
            {editingId ? 'Guardar Cambios' : 'Guardar Usuario'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Modal de Confirmación de Estado */}
      <Dialog open={confirmOpen} onClose={() => setConfirmOpen(false)}>
        <DialogTitle>Confirmar Acción</DialogTitle>
        <DialogContent>
          <DialogContentText>
            ¿Seguro que desea cambiar el estado de este usuario?
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
      <Snackbar 
        open={toast.open} 
        autoHideDuration={4000} 
        onClose={() => setToast({ ...toast, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={() => setToast({ ...toast, open: false })} severity={toast.severity as any} variant="filled" sx={{ width: '100%' }}>
          {toast.message}
        </Alert>
      </Snackbar>
    </MainCard>
  );
}
