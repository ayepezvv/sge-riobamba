import { useEffect, useState } from 'react';
import { Box, Chip, Typography } from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';
import { IconAddressBook, IconDeviceLaptop } from '@tabler/icons-react';

// project imports
import MainCard from 'ui-component/cards/MainCard';

// ==============================|| GESTOR DE PERSONAL ||============================== //

const PersonalManager = () => {
    const [rows, setRows] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // En un entorno real, aquí se harían dos llamadas paralelas:
        // 1. /api/administrativo/empleados
        // 2. /api/informatica/ips-asignadas
        // Y se cruzarían los datos por empleado_id.
        
        const mockData = [
            { 
                id: 1, 
                nombres: 'Juan Alberto', 
                apellidos: 'Pérez García', 
                cedula: '0601234567', 
                unidad: 'Dirección de TI', 
                puesto: 'Analista de Sistemas',
                ip_asignada: '192.168.10.45',
                equipo: 'LAPTOP-ADMIN-01',
                estado: 'ACTIVO'
            },
            { 
                id: 2, 
                nombres: 'María Elena', 
                apellidos: 'López Mora', 
                cedula: '0609876543', 
                unidad: 'Recursos Humanos', 
                puesto: 'Asistente Administrativo',
                ip_asignada: '192.168.10.82',
                equipo: 'DESKTOP-RRHH-02',
                estado: 'ACTIVO'
            }
        ];

        setRows(mockData);
        setLoading(false);
    }, []);

    const columns: GridColDef[] = [
        { field: 'cedula', headerName: 'Cédula', width: 120 },
        { field: 'apellidos', headerName: 'Apellidos', width: 200 },
        { field: 'nombres', headerName: 'Nombres', width: 200 },
        { field: 'unidad', headerName: 'Dirección/Unidad', width: 220 },
        { field: 'puesto', headerName: 'Puesto', width: 200 },
        { 
            field: 'ip_asignada', 
            headerName: 'IP Asignada', 
            width: 180,
            renderCell: (params) => (
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <IconDeviceLaptop size="1.2rem" style={{ marginRight: '8px', color: '#2196f3' }} />
                    <Typography variant="body2">{params.value || 'No asignada'}</Typography>
                </Box>
            )
        },
        { 
            field: 'estado', 
            headerName: 'Estado', 
            width: 120,
            renderCell: (params) => {
                const color = params.value === 'ACTIVO' ? 'success' : 'error';
                return <Chip label={params.value} color={color} size="small" variant="outlined" />;
            }
        }
    ];

    return (
        <MainCard 
            title="Gestión Integral de Personal" 
            secondary={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <IconAddressBook stroke={1.5} size="1.5rem" />
                </Box>
            }
        >
            <Box sx={{ height: 600, width: '100%' }}>
                <DataGrid
                    rows={rows}
                    columns={columns}
                    initialState={{ pagination: { paginationModel: { pageSize: 10 } } }}
                    pageSizeOptions={[10, 25, 50]}
                    loading={loading}
                    checkboxSelection
                    disableRowSelectionOnClick
                    slots={{ toolbar: GridToolbar }}
                    sx={{
                        '& .MuiDataGrid-columnHeaders': {
                            backgroundColor: '#f8fafc',
                            fontWeight: 'bold'
                        }
                    }}
                />
            </Box>
        </MainCard>
    );
};

export default PersonalManager;
