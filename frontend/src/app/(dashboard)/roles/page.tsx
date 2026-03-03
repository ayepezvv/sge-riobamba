'use client';

import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { 
  Box, Button, Dialog, DialogTitle, DialogContent, 
  DialogActions, TextField, Snackbar, Alert, IconButton, Tooltip,
  FormGroup, FormControlLabel, Checkbox, Typography
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import MainCard from 'ui-component/cards/MainCard';
import axios from 'utils/axios';

// ==============================|| GESTIÓN DE ROLES ||============================== //

export default function RolesPage() {
  const [roles, setRoles] = useState([]);
  const [permissions, setPermissions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Modal state (Create / Edit)
  const [open, setOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    nombre_rol: '',
    descripcion: ''
  });
  const [selectedPermissions, setSelectedPermissions] = useState<number[]>([]);

  // Snackbar state
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });

  const fetchRoles = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/roles/');
      setRoles(response.data);
    } catch (error) {
      console.error("Error fetching roles:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPermissions = async () => {
    try {
      const response = await axios.get('/api/permissions/');
      setPermissions(response.data);
    } catch (error) {
      console.error("Error fetching permissions:", error);
    }
  };

  useEffect(() => {
    fetchRoles();
    fetchPermissions();
  }, []);

  const handleOpenNew = () => {
    setEditingId(null);
    setFormData({ nombre_rol: '', descripcion: '' });
    setSelectedPermissions([]);
    setOpen(true);
  };

  const handleOpenEdit = (role: any) => {
    setEditingId(role.id);
    setFormData({
      nombre_rol: role.nombre_rol,
      descripcion: role.descripcion || ''
    });
    const assignedPerms = role.permissions?.map((p: any) => p.id) || [];
    setSelectedPermissions(assignedPerms);
    setOpen(true);
  };
  
  const handleClose = () => {
    setOpen(false);
  };

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handlePermissionToggle = (permId: number) => {
    setSelectedPermissions((prev) => 
      prev.includes(permId) ? prev.filter(id => id !== permId) : [...prev, permId]
    );
  };

  const handleSubmit = async () => {
    try {
      const payload = { 
        ...formData, 
        permission_ids: selectedPermissions 
      };

      if (editingId) {
        await axios.put(`/api/roles/${editingId}`, payload);
        setToast({ open: true, message: 'Rol actualizado exitosamente', severity: 'success' });
      } else {
        await axios.post('/api/roles/', payload);
        setToast({ open: true, message: 'Rol creado exitosamente', severity: 'success' });
      }
      
      handleClose();
      fetchRoles();
    } catch (error: any) {
      console.error("Error saving role:", error);
      const errorMsg = error.response?.data?.detail || 'Error al guardar rol.';
      setToast({ open: true, message: errorMsg, severity: 'error' });
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'nombre_rol', headerName: 'Nombre del Rol', flex: 1, minWidth: 150 },
    { field: 'descripcion', headerName: 'Descripción', flex: 1, minWidth: 250 },
    {
      field: 'permissions',
      headerName: 'Permisos Asignados',
      flex: 1,
      minWidth: 200,
      renderCell: (params) => {
        const perms = params.row.permissions;
        if (!perms || perms.length === 0) return <Typography variant="body2" color="textSecondary">Ninguno</Typography>;
        return <Typography variant="body2">{perms.length} permiso(s)</Typography>;
      }
    },
    {
      field: 'acciones',
      headerName: 'Acciones',
      width: 100,
      sortable: false,
      renderCell: (params) => {
        // Bloquear edición del SuperAdmin por seguridad
        if (params.row.nombre_rol === 'SuperAdmin') return null;
        
        return (
          <Tooltip title="Editar">
            <IconButton color="primary" onClick={() => handleOpenEdit(params.row)}>
              <EditIcon />
            </IconButton>
          </Tooltip>
        );
      }
    }
  ];

  return (
    <MainCard 
      title="Gestión de Roles y Permisos"
      secondary={
        <Button variant="contained" color="secondary" onClick={handleOpenNew}>
          + Nuevo Rol
        </Button>
      }
    >
      <Box sx={{ height: 400, width: '100%', mt: 2 }}>
        <DataGrid
          rows={roles}
          columns={columns}
          loading={loading}
          initialState={{
            pagination: {
              paginationModel: { page: 0, pageSize: 5 },
            },
          }}
          pageSizeOptions={[5, 10, 25]}
          disableRowSelectionOnClick
        />
      </Box>

      {/* Modal de Creación / Edición */}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ fontSize: '1.25rem', fontWeight: 600 }}>
          {editingId ? 'Editar Rol' : 'Crear Nuevo Rol'}
        </DialogTitle>
        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 1 }}>
            <TextField label="Nombre del Rol" name="nombre_rol" value={formData.nombre_rol} onChange={handleChange} fullWidth required />
            <TextField label="Descripción" name="descripcion" value={formData.descripcion} onChange={handleChange} fullWidth multiline rows={2} />
            
            <Box sx={{ mt: 1 }}>
              <Typography variant="subtitle1" sx={{ mb: 1, fontWeight: 500 }}>Permisos del Sistema</Typography>
              <Box sx={{ maxHeight: 200, overflowY: 'auto', border: '1px solid', borderColor: 'divider', p: 1, borderRadius: 1 }}>
                <FormGroup>
                  {permissions.map((perm) => (
                    <FormControlLabel 
                      key={perm.id} 
                      control={
                        <Checkbox 
                          checked={selectedPermissions.includes(perm.id)} 
                          onChange={() => handlePermissionToggle(perm.id)} 
                        />
                      } 
                      label={perm.nombre_permiso} 
                    />
                  ))}
                </FormGroup>
              </Box>
            </Box>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={handleClose} color="error" variant="text">Cancelar</Button>
          <Button onClick={handleSubmit} variant="contained" color="secondary">
            {editingId ? 'Guardar Cambios' : 'Guardar Rol'}
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
