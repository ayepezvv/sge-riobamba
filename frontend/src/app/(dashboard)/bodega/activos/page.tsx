'use client';

import { useEffect, useState } from 'react';
import {
    Grid, Typography, Button, Dialog, DialogTitle, DialogContent, DialogActions,
    TextField, Stack, IconButton, Box, Chip
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import MainCard from 'ui-component/cards/MainCard';
import { gridSpacing } from 'store/constant';
import { IconDeviceDesktop, IconPrinter, IconRouter, IconPlus, IconEdit, IconTrash } from '@tabler/icons-react';
import { listarActivos, crearActivo, listarCategorias } from 'api/bodega';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { useSnackbar } from 'notistack';

// Interfaces
interface Categoria {
    id: number;
    nombre: string;
}

interface ActivoFijo {
    id: number;
    codigo_inventario: string;
    nombre: string;
    descripcion?: string;
    marca?: string;
    modelo?: string;
    numero_serie?: string;
    costo_inicial?: number;
    valor_depreciado?: number;
    estado_fisico: 'BUENO' | 'REGULAR' | 'MALO' | 'DE_BAJA';
    categoria: Categoria;
    is_active: boolean;
}

const ActivosFijosPage = () => {
    const { enqueueSnackbar } = useSnackbar();
    const [activos, setActivos] = useState<ActivoFijo[]>([]);
    const [categorias, setCategorias] = useState<Categoria[]>([]);
    const [openModal, setOpenModal] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const fetchActivos = async () => {
        setIsLoading(true);
        try {
            const data = await listarActivos();
            setActivos(data);
        } catch (error) {
            enqueueSnackbar('Error al cargar activos fijos', { variant: 'error' });
        } finally {
            setIsLoading(false);
        }
    };

    const fetchCategorias = async () => {
        try {
            const data = await listarCategorias();
            setCategorias(data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchActivos();
        fetchCategorias();
    }, []);

    const formik = useFormik({
        initialValues: {
            codigo_inventario: '',
            nombre: '',
            descripcion: '',
            marca: '',
            modelo: '',
            numero_serie: '',
            costo_inicial: '',
            estado_fisico: 'BUENO',
            categoria_id: '' as number | ''
        },
        validationSchema: yup.object().shape({
            codigo_inventario: yup.string().required('Requerido'),
            nombre: yup.string().required('Requerido'),
            categoria_id: yup.number().required('Debe seleccionar una categoría')
        }),
        onSubmit: async (values, { resetForm }) => {
            try {
                await crearActivo({
                    ...values,
                    costo_inicial: values.costo_inicial ? parseFloat(values.costo_inicial as string) : null,
                    is_active: true
                });
                enqueueSnackbar('Activo registrado exitosamente', { variant: 'success' });
                setOpenModal(false);
                resetForm();
                fetchActivos();
            } catch (error: any) {
                enqueueSnackbar(error.response?.data?.detail || 'Error al guardar el activo', { variant: 'error' });
            }
        }
    });

    const getEstadoColor = (estado: string) => {
        switch (estado) {
            case 'BUENO': return 'success';
            case 'REGULAR': return 'warning';
            case 'MALO': return 'error';
            case 'DE_BAJA': return 'default';
            default: return 'primary';
        }
    };

    const columns: GridColDef[] = [
        { field: 'codigo_inventario', headerName: 'Cód. Inventario', width: 140 },
        { field: 'nombre', headerName: 'Nombre del Bien', width: 220 },
        {
            field: 'categoria',
            headerName: 'Categoría',
            width: 180,
            renderCell: (params) => (
                <Chip label={params.value?.nombre} variant="outlined" size="small" />
            )
        },
        { field: 'marca', headerName: 'Marca', width: 130 },
        { field: 'modelo', headerName: 'Modelo', width: 130 },
        { field: 'numero_serie', headerName: 'S/N', width: 150 },
        {
            field: 'estado_fisico',
            headerName: 'Estado Físico',
            width: 130,
            renderCell: (params) => (
                <Chip size="small" color={getEstadoColor(params.value)} label={params.value} />
            )
        },
        {
            field: 'actions',
            headerName: 'Acciones',
            width: 120,
            renderCell: () => (
                <Box>
                    <IconButton color="primary" size="small"><IconEdit size={18} /></IconButton>
                    <IconButton color="error" size="small"><IconTrash size={18} /></IconButton>
                </Box>
            )
        }
    ];

    return (
        <Grid container spacing={gridSpacing}>
            <Grid item xs={12}>
                <MainCard
                    title="Catálogo de Activos Fijos y Bienes"
                    secondary={
                        <Button variant="contained" startIcon={<IconPlus />} color="secondary" onClick={() => setOpenModal(true)}>
                            Registrar Nuevo Activo
                        </Button>
                    }
                >
                    <Box sx={{ height: 600, width: '100%' }}>
                        <DataGrid
                            rows={activos}
                            columns={columns}
                            loading={isLoading}
                            initialState={{
                                pagination: { paginationModel: { pageSize: 10 } },
                            }}
                            pageSizeOptions={[10, 25, 50]}
                            disableRowSelectionOnClick
                            density="comfortable"
                        />
                    </Box>
                </MainCard>
            </Grid>

            {/* Modal de Creación */}
            <Dialog open={openModal} onClose={() => setOpenModal(false)} maxWidth="md" fullWidth>
                <DialogTitle>Registrar Nuevo Activo Fijo</DialogTitle>
                <DialogContent>
                    <form onSubmit={formik.handleSubmit} id="activo-form">
                        <Grid container spacing={2} sx={{ mt: 1 }}>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    fullWidth label="Código de Inventario" name="codigo_inventario"
                                    value={formik.values.codigo_inventario} onChange={formik.handleChange}
                                    error={formik.touched.codigo_inventario && Boolean(formik.errors.codigo_inventario)}
                                    helperText={formik.touched.codigo_inventario && formik.errors.codigo_inventario}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    select fullWidth label="Categoría" name="categoria_id"
                                    SelectProps={{ native: true }}
                                    value={formik.values.categoria_id} onChange={formik.handleChange}
                                    error={formik.touched.categoria_id && Boolean(formik.errors.categoria_id)}
                                    helperText={formik.touched.categoria_id && formik.errors.categoria_id}
                                >
                                    <option value="">Seleccione...</option>
                                    {categorias.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
                                </TextField>
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    fullWidth label="Nombre del Bien" name="nombre"
                                    value={formik.values.nombre} onChange={formik.handleChange}
                                    error={formik.touched.nombre && Boolean(formik.errors.nombre)}
                                    helperText={formik.touched.nombre && formik.errors.nombre}
                                />
                            </Grid>
                            <Grid item xs={12} sm={4}>
                                <TextField
                                    fullWidth label="Marca" name="marca"
                                    value={formik.values.marca} onChange={formik.handleChange}
                                />
                            </Grid>
                            <Grid item xs={12} sm={4}>
                                <TextField
                                    fullWidth label="Modelo" name="modelo"
                                    value={formik.values.modelo} onChange={formik.handleChange}
                                />
                            </Grid>
                            <Grid item xs={12} sm={4}>
                                <TextField
                                    fullWidth label="Número de Serie (S/N)" name="numero_serie"
                                    value={formik.values.numero_serie} onChange={formik.handleChange}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    fullWidth label="Costo Inicial ($)" name="costo_inicial" type="number"
                                    value={formik.values.costo_inicial} onChange={formik.handleChange}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    select fullWidth label="Estado Físico" name="estado_fisico"
                                    SelectProps={{ native: true }}
                                    value={formik.values.estado_fisico} onChange={formik.handleChange}
                                >
                                    <option value="BUENO">Bueno</option>
                                    <option value="REGULAR">Regular</option>
                                    <option value="MALO">Malo</option>
                                    <option value="DE_BAJA">De Baja</option>
                                </TextField>
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    fullWidth label="Descripción / Observaciones" name="descripcion"
                                    multiline rows={3}
                                    value={formik.values.descripcion} onChange={formik.handleChange}
                                />
                            </Grid>
                        </Grid>
                    </form>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenModal(false)} color="error">Cancelar</Button>
                    <Button type="submit" form="activo-form" variant="contained" color="primary">Guardar Activo</Button>
                </DialogActions>
            </Dialog>
        </Grid>
    );
};

export default ActivosFijosPage;
