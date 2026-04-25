'use client';

import { useEffect, useState } from 'react';
import {
    Grid, Typography, Button, Dialog, DialogTitle, DialogContent, DialogActions,
    TextField, Stack, IconButton, Box
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import MainCard from 'ui-component/cards/MainCard';
import { gridSpacing } from 'store/constant';
import { IconPlus, IconEdit, IconTrash } from '@tabler/icons-react';
import { listarCategorias, crearCategoria, actualizarCategoria, eliminarCategoria } from 'api/bodega';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { useSnackbar } from 'notistack';

interface Categoria {
    id: number;
    nombre: string;
    descripcion: string;
    is_active: boolean;
}

const CategoriasBodegaPage = () => {
    const { enqueueSnackbar } = useSnackbar();
    const [categorias, setCategorias] = useState<Categoria[]>([]);
    const [openModal, setOpenModal] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [editId, setEditId] = useState<number | null>(null);

    const fetchCategorias = async () => {
        setIsLoading(true);
        try {
            const data = await listarCategorias();
            setCategorias(data);
        } catch (error) {
            enqueueSnackbar('Error al cargar categorías', { variant: 'error' });
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchCategorias();
    }, []);

    const formik = useFormik({
        initialValues: {
            nombre: '',
            descripcion: ''
        },
        validationSchema: yup.object().shape({
            nombre: yup.string().required('El nombre de la categoría es obligatorio')
        }),
        onSubmit: async (values, { resetForm }) => {
            try {
                if (editId) {
                    await actualizarCategoria(editId, values);
                    enqueueSnackbar('Categoría actualizada exitosamente', { variant: 'success' });
                } else {
                    await crearCategoria({ ...values, is_active: true });
                    enqueueSnackbar('Categoría creada exitosamente', { variant: 'success' });
                }
                setOpenModal(false);
                resetForm();
                fetchCategorias();
            } catch (error: any) {
                enqueueSnackbar(error.response?.data?.detail || 'Error al procesar la categoría', { variant: 'error' });
            }
        }
    });

    const handleEdit = (cat: Categoria) => {
        setEditId(cat.id);
        formik.setValues({
            nombre: cat.nombre,
            descripcion: cat.descripcion || ''
        });
        setOpenModal(true);
    };

    const handleCreate = () => {
        setEditId(null);
        formik.resetForm();
        setOpenModal(true);
    };

    const handleDelete = async (id: number) => {
        if (!window.confirm("¿Seguro que desea eliminar esta categoría? Si tiene activos asignados, esta acción podría fallar.")) return;
        try {
            await eliminarCategoria(id);
            enqueueSnackbar('Categoría eliminada', { variant: 'success' });
            fetchCategorias();
        } catch (error) {
            enqueueSnackbar('Error al eliminar categoría. Verifique que no esté en uso.', { variant: 'error' });
        }
    };

    const columns: GridColDef[] = [
        { field: 'id', headerName: 'ID', width: 90 },
        { field: 'nombre', headerName: 'Categoría', width: 250, renderCell: (params) => <Typography fontWeight={500}>{params.value}</Typography> },
        { field: 'descripcion', headerName: 'Descripción', width: 400 },
        {
            field: 'actions',
            headerName: 'Acciones',
            width: 150,
            renderCell: (params) => (
                <Box>
                    <IconButton color="primary" size="small" onClick={() => handleEdit(params.row)}><IconEdit size={18} /></IconButton>
                    <IconButton color="error" size="small" onClick={() => handleDelete(params.row.id)}><IconTrash size={18} /></IconButton>
                </Box>
            )
        }
    ];

    return (
        <Grid container spacing={gridSpacing}>
            <Grid size={12}>
                <MainCard
                    title="Diccionario de Categorías"
                    secondary={
                        <Button variant="contained" startIcon={<IconPlus />} color="secondary" onClick={handleCreate}>
                            Nueva Categoría
                        </Button>
                    }
                >
                    <Box sx={{ height: 500, width: '100%' }}>
                        <DataGrid
                            rows={categorias}
                            columns={columns}
                            loading={isLoading}
                            initialState={{
                                pagination: { paginationModel: { pageSize: 10 } },
                            }}
                            pageSizeOptions={[10, 25]}
                            disableRowSelectionOnClick
                            density="comfortable"
                        />
                    </Box>
                </MainCard>
            </Grid>

            {/* Modal de Creación / Edición */}
            <Dialog open={openModal} onClose={() => setOpenModal(false)} maxWidth="sm" fullWidth>
                <DialogTitle>{editId ? "Editar Categoría" : "Nueva Categoría"}</DialogTitle>
                <DialogContent>
                    <form onSubmit={formik.handleSubmit} id="categoria-form">
                        <Stack spacing={2} sx={{ mt: 1 }}>
                            <TextField
                                fullWidth label="Nombre de Categoría" name="nombre"
                                value={formik.values.nombre} onChange={formik.handleChange}
                                error={formik.touched.nombre && Boolean(formik.errors.nombre)}
                                helperText={formik.touched.nombre && formik.errors.nombre}
                                placeholder="Ej. Computación, Muebles"
                            />
                            <TextField
                                fullWidth label="Descripción" name="descripcion"
                                multiline rows={3}
                                value={formik.values.descripcion} onChange={formik.handleChange}
                            />
                        </Stack>
                    </form>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenModal(false)} color="error">Cancelar</Button>
                    <Button type="submit" form="categoria-form" variant="contained" color="primary">Guardar</Button>
                </DialogActions>
            </Dialog>
        </Grid>
    );
};

export default CategoriasBodegaPage;
