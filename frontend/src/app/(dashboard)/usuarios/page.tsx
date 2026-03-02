'use client';

import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Chip, Box } from '@mui/material';
import MainCard from 'ui-component/cards/MainCard';
import axios from 'utils/axios';

// ==============================|| GESTIÓN DE USUARIOS ||============================== //

export default function UsuariosPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get('/api/users/');
        setUsers(response.data);
      } catch (error) {
        console.error("Error fetching users:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchUsers();
  }, []);

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
  ];

  return (
    <MainCard title="Gestión de Personal">
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
    </MainCard>
  );
}
