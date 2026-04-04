'use client';

import React, { useState, useEffect, useCallback } from 'react';
import {
    Grid, Button, Dialog, DialogTitle, DialogContent, DialogActions,
    TextField, MenuItem, Chip, Box, Typography, Alert, CircularProgress,
    FormControl, InputLabel, Select, Autocomplete
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem, GridRowParams } from '@mui/x-data-grid';
import { IconUserPlus, IconEye, IconUserX } from '@tabler/icons-react';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import { listarEmpleadosAdministrativo, listarUnidades, listarPuestos, crearEmpleadoAdministrativo, eliminarEmpleadoAdministrativo } from 'api/administrativo';

// ──────────────────────────────────────────────────────────────────────────────
// TIPOS
// ──────────────────────────────────────────────────────────────────────────────
interface Unidad { id: number; nombre: string; nombre_dir?: string; }
interface Puesto { id: number; denominacion: string; }
interface Empleado {
    id: number; cedula: string; nombres: string; apellidos: string;
    estado_empleado: string; unidad: Unidad | null; puesto: Puesto | null;
    telefono_celular?: string; correo_personal?: string; regimen_legal?: string;
}

const ESTADO_COLOR: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
    ACTIVO: 'success', VACACIONES: 'warning', PERMISO: 'warning', DESVINCULADO: 'error'
};

const REGIMEN_OPCIONES = ['LOEP', 'CODIGO_TRABAJO'];
const CONTRATO_OPCIONES = ['NOMBRAMIENTO', 'INDEFINIDO', 'CONTRATADO_LOEP', 'CONTRATADO_CT', 'REQUERIDO_PROYECTO'];
const GENERO_OPCIONES = ['MASCULINO', 'FEMENINO', 'OTRO'];

// ──────────────────────────────────────────────────────────────────────────────
// COLUMNAS DEL DATAGRID
// ──────────────────────────────────────────────────────────────────────────────
const buildColumns = (onVer: (id: number) => void, onDesvincular: (id: number) => void): GridColDef[] => [
    { field: 'cedula', headerName: 'Cédula', width: 120 },
    { field: 'apellidos', headerName: 'Apellidos', width: 180, flex: 1 },
    { field: 'nombres', headerName: 'Nombres', width: 160, flex: 1 },
    {
        field: 'unidad_nombre', headerName: 'Unidad / Dirección', width: 220,
        valueGetter: (params: any) => params.row.unidad?.nombre ?? '—',
    },
    {
        field: 'puesto_nombre', headerName: 'Puesto', width: 200,
        valueGetter: (params: any) => params.row.puesto?.denominacion ?? '—',
    },
    {
        field: 'estado_empleado', headerName: 'Estado', width: 130,
        renderCell: (params) => (
            <Chip
                label={params.value}
                color={ESTADO_COLOR[params.value] ?? 'default'}
                size="small"
                variant="outlined"
            />
        ),
    },
    {
        field: 'acciones', type: 'actions', headerName: '', width: 80,
        getActions: (params: GridRowParams) => [
            <GridActionsCellItem icon={<IconEye size={18} />} label="Ver perfil" onClick={() => onVer(params.row.id)} />,
            <GridActionsCellItem icon={<IconUserX size={18} />} label="Desvincular" onClick={() => onDesvincular(params.row.id)} showInMenu />,
        ],
    },
];

// ──────────────────────────────────────────────────────────────────────────────
// FORMULARIO NUEVO EMPLEADO
// ──────────────────────────────────────────────────────────────────────────────
const FORM_DEFAULT = {
    cedula: '', nombres: '', apellidos: '', fecha_nacimiento: '',
    genero: '', regimen_legal: '', tipo_contrato_actual: '',
    telefono_celular: '', correo_personal: '', unidad_id: '', puesto_id: '',
};

// ──────────────────────────────────────────────────────────────────────────────
// COMPONENTE PRINCIPAL
// ──────────────────────────────────────────────────────────────────────────────
const DirectorioPersonalPage = () => {
    const [empleados, setEmpleados] = useState<Empleado[]>([]);
    const [unidades, setUnidades] = useState<Unidad[]>([]);
    const [puestos, setPuestos] = useState<Puesto[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Modal Nuevo Empleado
    const [openModal, setOpenModal] = useState(false);
    const [form, setForm] = useState(FORM_DEFAULT);
    const [savingForm, setSavingForm] = useState(false);
    const [formError, setFormError] = useState<string | null>(null);

    // ── Fetch datos ──
    const cargarDatos = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const [rawEmp, rawUnid, rawPuest] = await Promise.all([
                listarEmpleadosAdministrativo(),
                listarUnidades(),
                listarPuestos(),
            ]);
            setEmpleados(rawEmp);
            setUnidades(rawUnid);
            setPuestos(rawPuest);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Error al cargar datos del servidor');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => { cargarDatos(); }, [cargarDatos]);

    // ── Acciones ──
    const handleVer = (id: number) => {
        // En Fase 2 se abrirá el perfil completo del empleado
        console.info('Ver empleado ID:', id);
    };

    const handleDesvincular = async (id: number) => {
        if (!confirm('¿Confirma la desvinculación de este empleado? La acción es reversible desde administración.')) return;
        try {
            await eliminarEmpleadoAdministrativo(id);
            await cargarDatos();
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Error al desvincular empleado');
        }
    };

    const handleGuardar = async () => {
        if (!form.cedula || !form.nombres || !form.apellidos || !form.fecha_nacimiento || !form.unidad_id) {
            setFormError('Los campos Cédula, Nombres, Apellidos, Fecha de Nacimiento y Unidad son obligatorios.');
            return;
        }
        setSavingForm(true);
        setFormError(null);
        try {
            await crearEmpleadoAdministrativo({
                ...form,
                unidad_id: Number(form.unidad_id),
                puesto_id: form.puesto_id ? Number(form.puesto_id) : null,
                porcentaje_discapacidad: 0,
                genero: form.genero || null,
                regimen_legal: form.regimen_legal || null,
                tipo_contrato_actual: form.tipo_contrato_actual || null,
            });
            setOpenModal(false);
            setForm(FORM_DEFAULT);
            await cargarDatos();
        } catch (err: any) {
            setFormError(err.response?.data?.detail || 'Error al registrar empleado');
        } finally {
            setSavingForm(false);
        }
    };

    const columns = buildColumns(handleVer, handleDesvincular);

    return (
        <MainCard
            title="Directorio de Personal"
            secondary={
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<IconUserPlus size={18} />}
                    onClick={() => setOpenModal(true)}
                >
                    Nuevo Empleado
                </Button>
            }
        >
            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

            <Box sx={{ height: 600, width: '100%' }}>
                <DataGrid
                    rows={empleados}
                    columns={columns}
                    loading={loading}
                    pageSizeOptions={[10, 25, 50]}
                    slots={{ toolbar: GridToolbar }}
                    slotProps={{ toolbar: { showQuickFilter: true } }}
                    initialState={{ pagination: { paginationModel: { pageSize: 10 } } }}
                    disableRowSelectionOnClick
                    sx={{
                        border: 'none',
                        '& .MuiDataGrid-columnHeaders': { backgroundColor: '#f8fafc', fontWeight: 700 },
                        '& .MuiDataGrid-row:hover': { backgroundColor: '#f0f4ff' },
                    }}
                />
            </Box>

            {/* ── Modal: Nuevo Empleado ── */}
            <Dialog open={openModal} onClose={() => setOpenModal(false)} maxWidth="md" fullWidth>
                <DialogTitle>Registrar Nuevo Empleado</DialogTitle>
                <DialogContent dividers>
                    {formError && <Alert severity="error" sx={{ mb: 2 }}>{formError}</Alert>}
                    <Grid container spacing={2} sx={{ pt: 1 }}>
                        <Grid item xs={12} md={4}>
                            <TextField label="Cédula *" fullWidth value={form.cedula}
                                onChange={e => setForm({ ...form, cedula: e.target.value })} />
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField label="Nombres *" fullWidth value={form.nombres}
                                onChange={e => setForm({ ...form, nombres: e.target.value })} />
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField label="Apellidos *" fullWidth value={form.apellidos}
                                onChange={e => setForm({ ...form, apellidos: e.target.value })} />
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField label="Fecha de Nacimiento *" type="date" fullWidth
                                InputLabelProps={{ shrink: true }} value={form.fecha_nacimiento}
                                onChange={e => setForm({ ...form, fecha_nacimiento: e.target.value })} />
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField select label="Género" fullWidth value={form.genero}
                                onChange={e => setForm({ ...form, genero: e.target.value })}>
                                <MenuItem value="">Sin especificar</MenuItem>
                                {GENERO_OPCIONES.map(g => <MenuItem key={g} value={g}>{g}</MenuItem>)}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField select label="Unidad *" fullWidth value={form.unidad_id}
                                onChange={e => setForm({ ...form, unidad_id: e.target.value })}>
                                {unidades.map(u => <MenuItem key={u.id} value={u.id}>{u.nombre}</MenuItem>)}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField select label="Puesto" fullWidth value={form.puesto_id}
                                onChange={e => setForm({ ...form, puesto_id: e.target.value })}>
                                <MenuItem value="">Ninguno</MenuItem>
                                {puestos.map(p => <MenuItem key={p.id} value={p.id}>{p.denominacion}</MenuItem>)}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField select label="Régimen Legal" fullWidth value={form.regimen_legal}
                                onChange={e => setForm({ ...form, regimen_legal: e.target.value })}>
                                <MenuItem value="">Sin especificar</MenuItem>
                                {REGIMEN_OPCIONES.map(r => <MenuItem key={r} value={r}>{r}</MenuItem>)}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField select label="Tipo de Contrato" fullWidth value={form.tipo_contrato_actual}
                                onChange={e => setForm({ ...form, tipo_contrato_actual: e.target.value })}>
                                <MenuItem value="">Sin especificar</MenuItem>
                                {CONTRATO_OPCIONES.map(c => <MenuItem key={c} value={c}>{c}</MenuItem>)}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Teléfono Celular" fullWidth value={form.telefono_celular}
                                onChange={e => setForm({ ...form, telefono_celular: e.target.value })} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Correo Personal" fullWidth value={form.correo_personal}
                                onChange={e => setForm({ ...form, correo_personal: e.target.value })} />
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => { setOpenModal(false); setFormError(null); }} color="inherit">
                        Cancelar
                    </Button>
                    <Button onClick={handleGuardar} variant="contained" disabled={savingForm}
                        startIcon={savingForm ? <CircularProgress size={16} /> : undefined}>
                        {savingForm ? 'Guardando...' : 'Registrar Empleado'}
                    </Button>
                </DialogActions>
            </Dialog>
        </MainCard>
    );
};

export default DirectorioPersonalPage;
