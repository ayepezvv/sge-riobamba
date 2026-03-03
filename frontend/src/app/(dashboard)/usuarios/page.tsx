'use client';

import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { 
  Chip, Box, Button, Dialog, DialogTitle, DialogContent, DialogContentText,
  DialogActions, TextField, FormControl, InputLabel, 
  Select, MenuItem, Snackbar, Alert, IconButton, Tooltip 
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import BlockIcon from '@mui/icons-material/Block';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import MainCard from 'ui-component/cards/MainCard';
import axios from 'utils/axios';

// ==============================|| GESTIÓN DE USUARIOS ||============================== //

export default function UsuariosPage() {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Modal state (Create / Edit)
  const [open, setOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    cedula: '',
    nombres: '',
    apellidos: '',
    correo: '',
    password: '',
    role_id: ''
  });

  // Modal confirmación (Status Toggle)
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [selectedUserForStatus, setSelectedUserForStatus] = useState<any>(null);

  // Snackbar state
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/users/');
      setUsers(response.data);
    } catch (error) {
      console.error("Error fetching users:", error);
    } finally {
      setLoading(false);
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
    setFormData({ cedula: '', nombres: '', apellidos: '', correo: '', password: '', role_id: '' });
    setOpen(true);
  };

  const handleOpenEdit = (user: any) => {
    setEditingId(user.id);
    setFormData({
      cedula: user.cedula,
      nombres: user.nombres,
      apellidos: user.apellidos,
      correo: user.correo,
      password: '', // Blank password on edit means it won't be updated unless typed
      role_id: user.role_id ? user.role_id.toString() : ''
    });
    setOpen(true);
  };
  
  const handleClose = () => {
    setOpen(false);
    setFormData({ cedula: '', nombres: '', apellidos: '', correo: '', password: '', role_id: '' });
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
        // Edit Mode: remove password if empty to avoid overriding with blank
        if (!payload.password) {
          delete payload.password;
        }
        await axios.put(`/api/users/${editingId}`, payload);
        setToast({ open: true, message: 'Usuario actualizado exitosamente', severity: 'success' });
      } else {
        // Create Mode
        await axios.post('/api/users/', payload);
        setToast({ open: true, message: 'Usuario creado exitosamente', severity: 'success' });
      }
      
      handleClose();
      fetchUsers(); // Refresh grid reactively
    } catch (error: any) {
      console.error("Error saving user:", error);
      const errorMsg = error.response?.data?.detail || 'Error al guardar usuario. Verifica los datos.';
      setToast({ open: true, message: errorMsg, severity: 'error' });
    }
  };

  const handleToggleStatusClick = (user: any) => {
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

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'cedula', headerName: 'Cédula', width: 130 },
    { field: 'nombres', headerName: 'Nombres', flex: 1, minWidth: 150 },
    { field: 'apellidos', headerName: 'Apellidos', flex: 1, minWidth: 150 },
    { field: 'correo', headerName: 'Correo', flex: 1, minWidth: 200 },
    { 
      field: 'is_active', 
      headerName: 'Estado', 
      width: 130,
      renderCell: (params) => {
        return params.value ? (
          <Chip label="Activo" color="success" size="small" />
        ) : (
          <Chip label="Inactivo" color="error" size="small" />
        );
      }
    },
    {
      field: 'acciones',
      headerName: 'Acciones',
      width: 150,
      sortable: false,
      renderCell: (params) => {
        const isActive = params.row.is_active;
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
      title="Gestión de Personal"
      secondary={
        <Button variant="contained" color="secondary" onClick={handleOpenNew}>
          + Nuevo Usuario
        </Button>
      }
    >
      <Box sx={{ height: 400, width: '100%', mt: 2 }}>
        <DataGrid
          rows={users}
          columns={columns}
          loading={loading}
          initialState={{
            pagination: {
              paginationModel: { page: 0, pageSize: 5 },
            },
          }}
          pageSizeOptions={[5, 10, 25]}
          checkboxSelection
          disableRowSelectionOnClick
        />
      </Box>

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
        <Alert 
          onClose={() => setToast({ ...toast, open: false })} 
          severity={toast.severity as any} 
          variant="filled"
          sx={{ width: '100%' }}
        >
          {toast.message}
        </Alert>
      </Snackbar>
    </MainCard>
  );
}
