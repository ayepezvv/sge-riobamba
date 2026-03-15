'use client';

import { useState, useEffect, useCallback } from 'react';
import {
    Grid, Button, Dialog, DialogTitle, DialogContent, DialogActions,
    TextField, MenuItem, Chip, Box, Alert, CircularProgress,
    Stack, Divider, Typography, Stepper, Step, StepLabel,
    FormControlLabel, Switch, Tooltip, IconButton
} from '@mui/material';
import {
    DataGrid, GridColDef, GridToolbar,
    GridActionsCellItem, GridRowParams
} from '@mui/x-data-grid';
import {
    IconUserPlus, IconEye, IconUserX, IconBriefcase,
    IconId, IconRefresh, IconCertificate,
    IconPhone, IconMail
} from '@tabler/icons-react';
import MainCard from 'ui-component/cards/MainCard';
import axios from 'utils/axios';

// ──────────────────────────────────────────────────────────────────────────────
// TIPOS
// ──────────────────────────────────────────────────────────────────────────────
interface Area { id_area: number; nombre: string; tipo_area: string; }
interface Cargo { id_cargo: number; nombre_cargo: string; }
interface Historial {
    id_historial: number; fecha_inicio: string; fecha_fin: string | null;
    salario_acordado: string; tipo_contrato: string;
    area: Area | null; cargo: Cargo | null;
}
interface Empleado {
    id_empleado: number; identificacion: string; tipo_identificacion: string;
    nombres: string; apellidos: string; estado_empleado: string;
    genero?: string; regimen_legal?: string; tipo_contrato_actual?: string;
    codigo_sercop?: string; telefono_celular?: string; correo_personal?: string;
    aplica_iess: boolean; acumula_fondos_reserva: boolean; acumula_decimos: boolean;
    porcentaje_discapacidad: string; historial: Historial[];
}

const ESTADO_COLOR: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
    ACTIVO: 'success', VACACIONES: 'warning', PERMISO: 'warning', DESVINCULADO: 'error'
};
const TIPO_CONTRATO = ['NOMBRAMIENTO', 'INDEFINIDO', 'CONTRATADO_LOSEP', 'CONTRATADO_CT', 'REQUERIDO_PROYECTO'];
const REGIMEN_LEGAL = ['LOEP', 'CODIGO_TRABAJO'];
const GENERO_OPT = ['MASCULINO', 'FEMENINO', 'OTRO'];
const TIPO_ID_OPT = ['CEDULA', 'PASAPORTE', 'RUC'];
const PASOS = ['Datos Personales', 'Posición Inicial'];

// ──────────────────────────────────────────────────────────────────────────────
// HELPERS
// ──────────────────────────────────────────────────────────────────────────────
const historialActivo = (emp: Empleado | null | undefined) =>
    emp?.historial?.find((h: Historial) => !h.fecha_fin) ?? null;

// ──────────────────────────────────────────────────────────────────────────────
// COLUMNAS DATAGRID
// ──────────────────────────────────────────────────────────────────────────────
const buildColumns = (
    onVer: (emp: Empleado) => void,
    onDesvincular: (id: number) => void
): GridColDef[] => [
        { field: 'identificacion', headerName: 'Identificación', width: 130 },
        { field: 'apellidos', headerName: 'Apellidos', flex: 1, minWidth: 140 },
        { field: 'nombres', headerName: 'Nombres', flex: 1, minWidth: 130 },
        {
            field: 'cargo_actual', headerName: 'Cargo', width: 190,
            valueGetter: (_v: any, row: Empleado) => row ? (historialActivo(row)?.cargo?.nombre_cargo ?? '—') : '—',
        },
        {
            field: 'area_actual', headerName: 'Área / Unidad', width: 190,
            valueGetter: (_v: any, row: Empleado) => row ? (historialActivo(row)?.area?.nombre ?? '—') : '—',
        },
        {
            field: 'salario_actual', headerName: 'Salario', width: 110,
            valueGetter: (_v: any, row: Empleado) => {
                if (!row) return '—';
                const h = historialActivo(row);
                return h ? `$${Number(h.salario_acordado).toFixed(2)}` : '—';
            },
        },
        {
            field: 'regimen_legal', headerName: 'Régimen', width: 120,
            renderCell: (p) => p.value
                ? <Chip label={p.value} size="small" variant="outlined" color="info" />
                : <span>—</span>,
        },
        {
            field: 'estado_empleado', headerName: 'Estado', width: 120,
            renderCell: (p) => (
                <Chip
                    label={p.value} size="small" variant="outlined"
                    color={ESTADO_COLOR[p.value] ?? 'default'}
                />
            ),
        },
        {
            field: 'acciones', type: 'actions', headerName: '', width: 70,
            getActions: (p: GridRowParams<Empleado>) => [
                <GridActionsCellItem key="ver" icon={<IconEye size={18} />}
                    label="Ver perfil" onClick={() => onVer(p.row)} />,
                <GridActionsCellItem key="desv" icon={<IconUserX size={18} />}
                    label="Desvincular" onClick={() => onDesvincular(p.row.id_empleado)}
                    showInMenu />,
            ]
        }
    ];

// ──────────────────────────────────────────────────────────────────────────────
// ESTADO INICIAL DEL FORMULARIO (2 pasos)
// ──────────────────────────────────────────────────────────────────────────────
const FORM_INIT = {
    tipo_identificacion: 'CEDULA', identificacion: '', nombres: '', apellidos: '',
    fecha_nacimiento: '', genero: '', regimen_legal: '', tipo_contrato_actual: '',
    codigo_sercop: '', telefono_celular: '', correo_personal: '',
    porcentaje_discapacidad: '0', aplica_iess: true,
    acumula_fondos_reserva: true, acumula_decimos: false,
    // Paso 2
    id_area: '', id_cargo: '', tipo_contrato: 'NOMBRAMIENTO',
    fecha_inicio: new Date().toISOString().split('T')[0],
    salario_acordado: '',
};

// ──────────────────────────────────────────────────────────────────────────────
// COMPONENTE PRINCIPAL
// ──────────────────────────────────────────────────────────────────────────────
export default function DirectorioPersonalRRHH() {
    const [empleados, setEmpleados] = useState<Empleado[]>([]);
    const [areas, setAreas] = useState<Area[]>([]);
    const [cargos, setCargos] = useState<Cargo[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Modal formulario
    const [openModal, setOpenModal] = useState(false);
    const [paso, setPaso] = useState(0);
    const [form, setForm] = useState(FORM_INIT);
    const [saving, setSaving] = useState(false);
    const [formError, setFormError] = useState<string | null>(null);

    // Modal detalle
    const [detalle, setDetalle] = useState<Empleado | null>(null);

    // ── Fetch ──────────────────────────────────────────────────────────────
    const cargarDatos = useCallback(async () => {
        setLoading(true); setError(null);
        try {
            const [r1, r2, r3] = await Promise.all([
                axios.get('/api/rrhh/empleados'),
                axios.get('/api/rrhh/areas'),
                axios.get('/api/rrhh/cargos'),
            ]);
            // Extraer array correctamente (la API puede envolver en { items: [...] } o retornar array directo)
            const rawEmpleados: Empleado[] = Array.isArray(r1.data) ? r1.data
                : (r1.data?.items ?? r1.data?.data ?? []);
            setEmpleados(
                rawEmpleados
                    .filter((e): e is Empleado => e !== null && e !== undefined)
                    .map((e: Empleado) => ({ ...e, historial: e.historial ?? [], id: e.id_empleado }))
            );
            setAreas(r2.data);
            setCargos(r3.data);
        } catch (e: any) {
            setError(e.response?.data?.detail ?? 'Error al cargar datos');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => { cargarDatos(); }, [cargarDatos]);

    // ── Desvincular ────────────────────────────────────────────────────────
    const handleDesvincular = async (id: number) => {
        if (!confirm('¿Confirma la desvinculación (borrado lógico)?')) return;
        try {
            await axios.delete(`/api/rrhh/empleados/${id}`);
            await cargarDatos();
        } catch (e: any) {
            alert(e.response?.data?.detail ?? 'Error al desvincular');
        }
    };

    // ── Navegación Stepper ─────────────────────────────────────────────────
    const handleSiguiente = () => {
        if (!form.identificacion || !form.nombres || !form.apellidos || !form.fecha_nacimiento) {
            setFormError('Identificación, nombres, apellidos y fecha de nacimiento son obligatorios.');
            return;
        }
        setFormError(null);
        setPaso(1);
    };

    // ── Guardar (2 llamadas API: empleado + historial) ─────────────────────
    const handleGuardar = async () => {
        if (!form.id_area || !form.id_cargo || !form.salario_acordado) {
            setFormError('Área, cargo y salario acordado son obligatorios.');
            return;
        }
        setSaving(true); setFormError(null);
        try {
            const empRes = await axios.post('/api/rrhh/empleados', {
                tipo_identificacion: form.tipo_identificacion,
                identificacion: form.identificacion,
                nombres: form.nombres,
                apellidos: form.apellidos,
                fecha_nacimiento: form.fecha_nacimiento,
                genero: form.genero || null,
                regimen_legal: form.regimen_legal || null,
                tipo_contrato_actual: form.tipo_contrato_actual || null,
                codigo_sercop: form.codigo_sercop || null,
                telefono_celular: form.telefono_celular || null,
                correo_personal: form.correo_personal || null,
                porcentaje_discapacidad: Number(form.porcentaje_discapacidad),
                aplica_iess: form.aplica_iess,
                acumula_fondos_reserva: form.acumula_fondos_reserva,
                acumula_decimos: form.acumula_decimos,
            });
            const nuevoId = empRes.data.id_empleado;

            await axios.post(`/api/rrhh/empleados/${nuevoId}/historial`, {
                id_empleado: nuevoId,
                id_area: Number(form.id_area),
                id_cargo: Number(form.id_cargo),
                tipo_contrato: form.tipo_contrato,
                fecha_inicio: form.fecha_inicio,
                salario_acordado: Number(form.salario_acordado),
            });

            setOpenModal(false);
            setForm(FORM_INIT);
            setPaso(0);
            await cargarDatos();
        } catch (e: any) {
            setFormError(e.response?.data?.detail ?? 'Error al registrar empleado');
        } finally {
            setSaving(false);
        }
    };

    const cerrarModal = () => {
        setOpenModal(false); setForm(FORM_INIT); setPaso(0); setFormError(null);
    };

    const columns = buildColumns(setDetalle, handleDesvincular);

    // ──────────────────────────────────────────────────────────────────────────
    // RENDER
    // ──────────────────────────────────────────────────────────────────────────
    return (
        <>
            {/* ════════════════════════════════ TABLA PRINCIPAL ═══════════ */}
            <MainCard
                title="Directorio de Personal"
                secondary={
                    <Stack direction="row" spacing={1}>
                        <Tooltip title="Recargar">
                            <IconButton onClick={cargarDatos} size="small">
                                <IconRefresh size={18} />
                            </IconButton>
                        </Tooltip>
                        <Button variant="contained" startIcon={<IconUserPlus size={18} />}
                            onClick={() => setOpenModal(true)}>
                            Nuevo Empleado
                        </Button>
                    </Stack>
                }
            >
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                <Box sx={{ height: 620, width: '100%' }}>
                    <DataGrid
                        rows={empleados.filter(e => e !== null && e !== undefined)}
                        columns={columns}
                        loading={loading}
                        pageSizeOptions={[10, 25, 50]}
                        slots={{ toolbar: GridToolbar }}
                        slotProps={{ toolbar: { showQuickFilter: true } }}
                        initialState={{ pagination: { paginationModel: { pageSize: 10 } } }}
                        disableRowSelectionOnClick
                        sx={{
                            border: 'none',
                            '& .MuiDataGrid-columnHeaders': { bgcolor: '#f8fafc', fontWeight: 700 },
                            '& .MuiDataGrid-row:hover': { bgcolor: '#f0f4ff' },
                        }}
                    />
                </Box>
            </MainCard>

            {/* ═══════════════════ MODAL — NUEVO EMPLEADO (STEPPER) ════════ */}
            <Dialog open={openModal} onClose={cerrarModal} maxWidth="md" fullWidth>
                <DialogTitle>
                    Registrar Nuevo Empleado
                    <Stepper activeStep={paso} sx={{ mt: 1 }}>
                        {PASOS.map(l => <Step key={l}><StepLabel>{l}</StepLabel></Step>)}
                    </Stepper>
                </DialogTitle>

                <DialogContent dividers>
                    {formError && <Alert severity="error" sx={{ mb: 2 }}>{formError}</Alert>}

                    {/* ── Paso 0: Datos Personales ── */}
                    {paso === 0 && (
                        <Grid container spacing={2} sx={{ pt: 1 }}>
                            <Grid size={4}>
                                <TextField select label="Tipo Identificación" fullWidth
                                    value={form.tipo_identificacion}
                                    onChange={e => setForm({ ...form, tipo_identificacion: e.target.value })}>
                                    {TIPO_ID_OPT.map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid size={4}>
                                <TextField label="Identificación *" fullWidth value={form.identificacion}
                                    onChange={e => setForm({ ...form, identificacion: e.target.value })} />
                            </Grid>
                            <Grid size={4}>
                                <TextField select label="Género" fullWidth value={form.genero}
                                    onChange={e => setForm({ ...form, genero: e.target.value })}>
                                    <MenuItem value="">Sin especificar</MenuItem>
                                    {GENERO_OPT.map(g => <MenuItem key={g} value={g}>{g}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid size={6}>
                                <TextField label="Nombres *" fullWidth value={form.nombres}
                                    onChange={e => setForm({ ...form, nombres: e.target.value })} />
                            </Grid>
                            <Grid size={6}>
                                <TextField label="Apellidos *" fullWidth value={form.apellidos}
                                    onChange={e => setForm({ ...form, apellidos: e.target.value })} />
                            </Grid>
                            <Grid size={4}>
                                <TextField label="Fecha Nacimiento *" type="date" fullWidth
                                    InputLabelProps={{ shrink: true }} value={form.fecha_nacimiento}
                                    onChange={e => setForm({ ...form, fecha_nacimiento: e.target.value })} />
                            </Grid>
                            <Grid size={4}>
                                <TextField select label="Régimen Legal" fullWidth value={form.regimen_legal}
                                    onChange={e => setForm({ ...form, regimen_legal: e.target.value })}>
                                    <MenuItem value="">Sin especificar</MenuItem>
                                    {REGIMEN_LEGAL.map(r => <MenuItem key={r} value={r}>{r}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid size={4}>
                                <TextField select label="Tipo Contrato Actual" fullWidth
                                    value={form.tipo_contrato_actual}
                                    onChange={e => setForm({ ...form, tipo_contrato_actual: e.target.value })}>
                                    <MenuItem value="">Sin especificar</MenuItem>
                                    {TIPO_CONTRATO.map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid size={4}>
                                <TextField label="Código SERCOP" fullWidth value={form.codigo_sercop}
                                    onChange={e => setForm({ ...form, codigo_sercop: e.target.value })} />
                            </Grid>
                            <Grid size={4}>
                                <TextField label="Teléfono" fullWidth value={form.telefono_celular}
                                    onChange={e => setForm({ ...form, telefono_celular: e.target.value })} />
                            </Grid>
                            <Grid size={4}>
                                <TextField label="Correo Personal" fullWidth value={form.correo_personal}
                                    onChange={e => setForm({ ...form, correo_personal: e.target.value })} />
                            </Grid>
                            <Grid size={3}>
                                <TextField label="% Discapacidad" type="number" fullWidth
                                    value={form.porcentaje_discapacidad}
                                    onChange={e => setForm({ ...form, porcentaje_discapacidad: e.target.value })} />
                            </Grid>
                            <Grid size={3}>
                                <FormControlLabel label="Aplica IESS"
                                    control={<Switch checked={form.aplica_iess}
                                        onChange={e => setForm({ ...form, aplica_iess: e.target.checked })} />} />
                            </Grid>
                            <Grid size={3}>
                                <FormControlLabel label="Fondos Reserva"
                                    control={<Switch checked={form.acumula_fondos_reserva}
                                        onChange={e => setForm({ ...form, acumula_fondos_reserva: e.target.checked })} />} />
                            </Grid>
                            <Grid size={3}>
                                <FormControlLabel label="Décimos"
                                    control={<Switch checked={form.acumula_decimos}
                                        onChange={e => setForm({ ...form, acumula_decimos: e.target.checked })} />} />
                            </Grid>
                        </Grid>
                    )}

                    {/* ── Paso 1: Posición Inicial ── */}
                    {paso === 1 && (
                        <Grid container spacing={2} sx={{ pt: 1 }}>
                            <Grid size={12}>
                                <Alert severity="info" sx={{ mb: 1 }}>
                                    Esta posición quedará registrada como historial laboral activo.
                                </Alert>
                            </Grid>
                            <Grid size={6}>
                                <TextField select label="Área / Unidad *" fullWidth value={form.id_area}
                                    onChange={e => setForm({ ...form, id_area: e.target.value })}>
                                    {areas.map(a => <MenuItem key={a.id_area} value={a.id_area}>{a.nombre}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid size={6}>
                                <TextField select label="Cargo *" fullWidth value={form.id_cargo}
                                    onChange={e => setForm({ ...form, id_cargo: e.target.value })}>
                                    {cargos.map(c => <MenuItem key={c.id_cargo} value={c.id_cargo}>{c.nombre_cargo}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid size={4}>
                                <TextField select label="Tipo de Contrato *" fullWidth value={form.tipo_contrato}
                                    onChange={e => setForm({ ...form, tipo_contrato: e.target.value })}>
                                    {TIPO_CONTRATO.map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid size={4}>
                                <TextField label="Fecha Inicio *" type="date" fullWidth
                                    InputLabelProps={{ shrink: true }} value={form.fecha_inicio}
                                    onChange={e => setForm({ ...form, fecha_inicio: e.target.value })} />
                            </Grid>
                            <Grid size={4}>
                                <TextField label="Salario Acordado *" type="number" fullWidth
                                    value={form.salario_acordado}
                                    onChange={e => setForm({ ...form, salario_acordado: e.target.value })} />
                            </Grid>
                        </Grid>
                    )}
                </DialogContent>

                <DialogActions>
                    <Button onClick={cerrarModal} color="inherit">Cancelar</Button>
                    {paso === 0 && (
                        <Button onClick={handleSiguiente} variant="outlined">
                            Siguiente →
                        </Button>
                    )}
                    {paso === 1 && (
                        <>
                            <Button onClick={() => { setPaso(0); setFormError(null); }}>
                                ← Atrás
                            </Button>
                            <Button onClick={handleGuardar} variant="contained" disabled={saving}
                                startIcon={saving ? <CircularProgress size={16} /> : undefined}>
                                {saving ? 'Guardando...' : 'Registrar Empleado'}
                            </Button>
                        </>
                    )}
                </DialogActions>
            </Dialog>

            {/* ═════════════════════ MODAL — DETALLE EMPLEADO ════════════ */}
            <Dialog open={!!detalle} onClose={() => setDetalle(null)} maxWidth="sm" fullWidth>
                <DialogTitle>
                    <Stack direction="row" spacing={1} alignItems="center">
                        <IconId size={22} />
                        <Box>
                            <Typography variant="h5" component="span">
                                {detalle?.apellidos}, {detalle?.nombres}
                            </Typography>
                            <Typography variant="caption" display="block" color="text.secondary">
                                {detalle?.tipo_identificacion}: {detalle?.identificacion}
                            </Typography>
                        </Box>
                        <Chip
                            label={detalle?.estado_empleado}
                            color={ESTADO_COLOR[detalle?.estado_empleado ?? ''] ?? 'default'}
                            size="small" sx={{ ml: 'auto' }}
                        />
                    </Stack>
                </DialogTitle>
                <DialogContent dividers>
                    <Stack spacing={1.5}>
                        {/* Posición actual */}
                        <Box display="flex" gap={1} alignItems="flex-start">
                            <IconBriefcase size={18} style={{ marginTop: 2, flexShrink: 0 }} />
                            <Box>
                                <Typography variant="body2" fontWeight={600}>
                                    {historialActivo(detalle)?.cargo?.nombre_cargo ?? 'Sin cargo asignado'}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                    {historialActivo(detalle)?.area?.nombre ?? '—'}
                                </Typography>
                            </Box>
                        </Box>

                        {/* Datos de régimen */}
                        <Box display="flex" gap={1}>
                            <IconCertificate size={18} style={{ flexShrink: 0, marginTop: 2 }} />
                            <Stack direction="row" spacing={1} flexWrap="wrap">
                                {detalle?.regimen_legal && (
                                    <Chip label={detalle.regimen_legal} size="small" color="info" variant="outlined" />
                                )}
                                {detalle?.tipo_contrato_actual && (
                                    <Chip label={detalle.tipo_contrato_actual} size="small" variant="outlined" />
                                )}
                                {detalle?.codigo_sercop && (
                                    <Chip label={`SERCOP: ${detalle.codigo_sercop}`} size="small" variant="outlined" />
                                )}
                            </Stack>
                        </Box>

                        {/* Contacto */}
                        {detalle?.telefono_celular && (
                            <Box display="flex" gap={1} alignItems="center">
                                <IconPhone size={16} />
                                <Typography variant="body2">{detalle.telefono_celular}</Typography>
                            </Box>
                        )}
                        {detalle?.correo_personal && (
                            <Box display="flex" gap={1} alignItems="center">
                                <IconMail size={16} />
                                <Typography variant="body2">{detalle.correo_personal}</Typography>
                            </Box>
                        )}

                        <Divider />

                        {/* Timeline historial */}
                        <Typography variant="caption" color="text.secondary" fontWeight={700}>
                            HISTORIAL LABORAL ({detalle?.historial?.length ?? 0} registros)
                        </Typography>
                        {detalle?.historial?.map(h => (
                            <Box key={h.id_historial}
                                sx={{ pl: 1.5, borderLeft: '3px solid', borderColor: h.fecha_fin ? 'grey.300' : 'primary.main' }}>
                                <Typography variant="body2" fontWeight={600}>
                                    {h.cargo?.nombre_cargo ?? '—'}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                    {h.area?.nombre ?? '—'} | {h.tipo_contrato}<br />
                                    {h.fecha_inicio} → {h.fecha_fin ?? <b>Vigente</b>} | ${Number(h.salario_acordado).toFixed(2)}
                                </Typography>
                            </Box>
                        ))}
                    </Stack>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setDetalle(null)}>Cerrar</Button>
                </DialogActions>
            </Dialog>
        </>
    );
}
