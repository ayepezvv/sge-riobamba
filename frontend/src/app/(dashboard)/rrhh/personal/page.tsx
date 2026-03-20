'use client';

import { useState, useEffect, useCallback } from 'react';
import {
    Grid, Button, Dialog, DialogTitle, DialogContent, DialogActions,
    TextField, MenuItem, Chip, Box, Alert, CircularProgress,
    Stack, Divider, Typography, Tabs, Tab,
    FormControlLabel, Switch, Tooltip, IconButton
} from '@mui/material';
import {
    DataGrid, GridColDef, GridToolbar,
    GridActionsCellItem, GridRowParams
} from '@mui/x-data-grid';
import {
    IconUserPlus, IconEye, IconUserX, IconBriefcase,
    IconId, IconRefresh, IconCertificate,
    IconPhone, IconMail, IconUser, IconClipboardList
} from '@tabler/icons-react';
import MainCard from 'ui-component/cards/MainCard';
import axios from 'utils/axios';

// ─────────────────────────────────────────────────────────────────────────────
// TIPOS
// ─────────────────────────────────────────────────────────────────────────────
interface Area    { id_area: number;  nombre: string; tipo_area: string; }
interface Cargo   { id_cargo: number; nombre_cargo: string; }
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

// ─────────────────────────────────────────────────────────────────────────────
// CATÁLOGOS
// ─────────────────────────────────────────────────────────────────────────────
const ESTADO_COLOR: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
    ACTIVO: 'success', VACACIONES: 'warning', PERMISO: 'warning', DESVINCULADO: 'error',
};
const TIPO_CONTRATO_OPT = [
    { value: 'NOMBRAMIENTO',         label: 'Nombramiento Permanente'  },
    { value: 'NOMBRAMIENTO_PROV',    label: 'Nombramiento Provisional' },
    { value: 'OCASIONAL',            label: 'Contrato Ocasional'       },
    { value: 'INDEFINIDO',           label: 'Indefinido'               },
    { value: 'CONTRATADO_LOSEP',     label: 'Contrato LOSEP'           },
    { value: 'CONTRATADO_CT',        label: 'Contrato Código Trabajo'  },
    { value: 'REQUERIDO_PROYECTO',   label: 'Requerido por Proyecto'   },
];
const REGIMEN_OPT = [
    { value: 'LOEP',          label: 'LOEP'              },
    { value: 'CODIGO_TRABAJO', label: 'Código de Trabajo' },
    { value: 'LOSEP',         label: 'LOSEP'             },
];
const GENERO_OPT  = ['MASCULINO', 'FEMENINO', 'OTRO'];
const TIPO_ID_OPT = ['CEDULA', 'PASAPORTE', 'RUC'];

// ─────────────────────────────────────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────────────────────────────────────
const historialActivo = (emp: Empleado | null | undefined) =>
    emp?.historial?.find((h: Historial) => !h.fecha_fin) ?? null;

/** Valida cédula ecuatoriana (10 dígitos, algoritmo módulo 10) */
function validarCedula(cedula: string): boolean {
    if (!/^\d{10}$/.test(cedula)) return false;
    const digitos = cedula.split('').map(Number);
    const prov = digitos[0] * 10 + digitos[1];
    if (prov < 1 || prov > 24) return false;
    let suma = 0;
    for (let i = 0; i < 9; i++) {
        let v = digitos[i] * (i % 2 === 0 ? 2 : 1);
        if (v > 9) v -= 9;
        suma += v;
    }
    return (10 - (suma % 10)) % 10 === digitos[9];
}

// ─────────────────────────────────────────────────────────────────────────────
// ESTADO INICIAL DEL FORMULARIO
// ─────────────────────────────────────────────────────────────────────────────
const FORM_INIT = {
    // Pestaña 1 — Datos Personales
    tipo_identificacion:  'CEDULA',
    identificacion:       '',
    nombres:              '',
    apellidos:            '',
    fecha_nacimiento:     '',
    genero:               '',
    correo_personal:      '',
    telefono_celular:     '',
    // Pestaña 2 — Datos Laborales
    regimen_legal:           '',
    tipo_contrato_actual:    '',
    codigo_sercop:           '',
    porcentaje_discapacidad: '0',
    aplica_iess:             true,
    acumula_fondos_reserva:  true,
    acumula_decimos:         false,
    // Posición inicial (historial)
    id_area:          '',
    id_cargo:         '',
    tipo_contrato:    'NOMBRAMIENTO',
    fecha_inicio:     new Date().toISOString().split('T')[0],
    salario_acordado: '',
};

// ─────────────────────────────────────────────────────────────────────────────
// COLUMNAS DATAGRID
// ─────────────────────────────────────────────────────────────────────────────
const buildColumns = (
    onVer:          (emp: Empleado)  => void,
    onDesvincular:  (id: number)     => void
): GridColDef[] => [
    { field: 'identificacion',  headerName: 'Cédula / ID', width: 125 },
    { field: 'apellidos',       headerName: 'Apellidos',   flex: 1,   minWidth: 140 },
    { field: 'nombres',         headerName: 'Nombres',     flex: 1,   minWidth: 130 },
    {
        field: 'cargo_actual', headerName: 'Cargo', width: 200,
        valueGetter: (_v: any, row: Empleado) =>
            row ? (historialActivo(row)?.cargo?.nombre_cargo ?? '—') : '—',
    },
    {
        field: 'area_actual', headerName: 'Área / Unidad', width: 200,
        valueGetter: (_v: any, row: Empleado) =>
            row ? (historialActivo(row)?.area?.nombre ?? '—') : '—',
    },
    {
        field: 'regimen_legal', headerName: 'Régimen', width: 120,
        renderCell: (p) => p.value
            ? <Chip label={p.value} size="small" variant="outlined" color="info" />
            : <Typography variant="body2" color="text.disabled">—</Typography>,
    },
    {
        field: 'estado_empleado', headerName: 'Estado', width: 115,
        renderCell: (p) => (
            <Chip label={p.value} size="small" variant="filled"
                color={ESTADO_COLOR[p.value] ?? 'default'} />
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
        ],
    },
];

// ─────────────────────────────────────────────────────────────────────────────
// COMPONENTE PRINCIPAL
// ─────────────────────────────────────────────────────────────────────────────
export default function DirectorioPersonalRRHH() {
    const [empleados, setEmpleados] = useState<Empleado[]>([]);
    const [areas,     setAreas]     = useState<Area[]>([]);
    const [cargos,    setCargos]    = useState<Cargo[]>([]);
    const [loading,   setLoading]   = useState(true);
    const [error,     setError]     = useState<string | null>(null);

    // Modal registro
    const [openModal, setOpenModal] = useState(false);
    const [tabActual, setTabActual] = useState(0);
    const [form,      setForm]      = useState(FORM_INIT);
    const [saving,    setSaving]    = useState(false);
    const [formError, setFormError] = useState<string | null>(null);

    // Modal detalle
    const [detalle, setDetalle] = useState<Empleado | null>(null);

    // ── Fetch principal ───────────────────────────────────────────────────
    const cargarDatos = useCallback(async () => {
        setLoading(true); setError(null);
        try {
            const [r1, r2, r3] = await Promise.all([
                axios.get('/api/rrhh/empleados'),
                axios.get('/api/rrhh/areas'),
                axios.get('/api/rrhh/cargos'),
            ]);

            const toArray = (d: any) =>
                Array.isArray(d) ? d : (d?.items ?? d?.data ?? []);

            const rawEmpleados: Empleado[] = toArray(r1.data);
            setEmpleados(
                rawEmpleados
                    .filter((e): e is Empleado => e !== null && e !== undefined)
                    .map(e => ({ ...e, historial: e.historial ?? [], id: e.id_empleado }))
            );
            setAreas(toArray(r2.data).filter((a: any) => a !== null));
            setCargos(toArray(r3.data).filter((c: any) => c !== null));
        } catch (e: any) {
            setError(e.response?.data?.detail ?? 'Error al cargar datos del directorio');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => { cargarDatos(); }, [cargarDatos]);

    // ── Abrir / cerrar modal ──────────────────────────────────────────────
    const abrirModal = () => {
        setForm(FORM_INIT);
        setFormError(null);
        setTabActual(0);
        setOpenModal(true);
    };

    // ── Validación por pestaña ────────────────────────────────────────────
    const validarTab1 = (): string | null => {
        if (!form.nombres.trim())   return 'El nombre es obligatorio.';
        if (!form.apellidos.trim()) return 'Los apellidos son obligatorios.';
        if (!form.identificacion.trim()) return 'La identificación es obligatoria.';
        if (form.tipo_identificacion === 'CEDULA' && !validarCedula(form.identificacion)) {
            return 'La cédula no es válida (10 dígitos, algoritmo módulo 10).';
        }
        if (!form.fecha_nacimiento) return 'La fecha de nacimiento es obligatoria.';
        return null;
    };

    const validarTab2 = (): string | null => {
        if (!form.id_area)          return 'Selecciona un Área Organizacional.';
        if (!form.id_cargo)         return 'Selecciona un Cargo.';
        if (!form.tipo_contrato)    return 'Selecciona el tipo de contrato para el historial.';
        if (!form.fecha_inicio)     return 'La fecha de ingreso es obligatoria.';
        if (!form.salario_acordado || Number(form.salario_acordado) <= 0)
            return 'El salario acordado debe ser mayor a 0.';
        return null;
    };

    // ── Avanzar / retroceder tab ──────────────────────────────────────────
    const handleSiguiente = () => {
        const err = validarTab1();
        if (err) { setFormError(err); return; }
        setFormError(null);
        setTabActual(1);
    };

    // ── Guardar ───────────────────────────────────────────────────────────
    const handleGuardar = async () => {
        const errT2 = validarTab2();
        if (errT2) { setFormError(errT2); return; }

        setSaving(true); setFormError(null);
        try {
            // Limpieza de nulos para evitar 422 de Pydantic
            const nullIfEmpty = (v: string) => v.trim() || null;

            const empRes = await axios.post('/api/rrhh/empleados', {
                tipo_identificacion:     form.tipo_identificacion,
                identificacion:          form.identificacion.trim(),
                nombres:                 form.nombres.trim(),
                apellidos:               form.apellidos.trim(),
                fecha_nacimiento:        form.fecha_nacimiento,
                genero:                  nullIfEmpty(form.genero),
                regimen_legal:           nullIfEmpty(form.regimen_legal),
                tipo_contrato_actual:    nullIfEmpty(form.tipo_contrato_actual),
                codigo_sercop:           nullIfEmpty(form.codigo_sercop),
                telefono_celular:        nullIfEmpty(form.telefono_celular),
                correo_personal:         nullIfEmpty(form.correo_personal),
                porcentaje_discapacidad: Number(form.porcentaje_discapacidad) || 0,
                aplica_iess:             form.aplica_iess,
                acumula_fondos_reserva:  form.acumula_fondos_reserva,
                acumula_decimos:         form.acumula_decimos,
            });

            const nuevoId: number = empRes.data.id_empleado;

            await axios.post(`/api/rrhh/empleados/${nuevoId}/historial`, {
                id_empleado:     nuevoId,
                id_area:         Number(form.id_area),
                id_cargo:        Number(form.id_cargo),
                tipo_contrato:   form.tipo_contrato,
                fecha_inicio:    form.fecha_inicio,
                salario_acordado: Number(form.salario_acordado),
            });

            setOpenModal(false);
            await cargarDatos();
        } catch (e: any) {
            const detail = e.response?.data?.detail;
            if (Array.isArray(detail)) {
                setFormError(detail.map((d: any) => d.msg).join(' | '));
            } else {
                setFormError(detail ?? 'Error al registrar el empleado');
            }
        } finally {
            setSaving(false);
        }
    };

    const handleDesvincular = async (id: number) => {
        if (!confirm('¿Confirma la desvinculación (borrado lógico)?')) return;
        try {
            await axios.delete(`/api/rrhh/empleados/${id}`);
            await cargarDatos();
        } catch (e: any) {
            alert(e.response?.data?.detail ?? 'Error al desvincular');
        }
    };

    const columns = buildColumns(setDetalle, handleDesvincular);

    // ─────────────────────────────────────────────────────────────────────
    // RENDER
    // ─────────────────────────────────────────────────────────────────────
    return (
        <>
            {/* ══════════════════════ TABLA PRINCIPAL ══════════════════════ */}
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
                            onClick={abrirModal}>
                            Nuevo Empleado
                        </Button>
                    </Stack>
                }
            >
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                <Box sx={{ height: 600, width: '100%' }}>
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

            {/* ══════════════════ MODAL REGISTRO EMPLEADO ══════════════════ */}
            <Dialog open={openModal} onClose={() => setOpenModal(false)}
                maxWidth="md" fullWidth>
                <DialogTitle>
                    <Stack direction="row" spacing={1} alignItems="center">
                        <IconUserPlus size={22} />
                        <Box>
                            <Typography variant="h5">Registro de Nuevo Empleado</Typography>
                            <Typography variant="caption" color="text.secondary">
                                Súper Modelo V3 — Complete ambas secciones
                            </Typography>
                        </Box>
                    </Stack>
                </DialogTitle>

                <DialogContent dividers sx={{ p: 0 }}>
                    {/* ── Tabs ─────────────────────────────────────────── */}
                    <Tabs
                        value={tabActual}
                        onChange={(_e, v) => { if (v === 1 && tabActual === 0) { handleSiguiente(); } else { setTabActual(v); setFormError(null); } }}
                        sx={{ borderBottom: 1, borderColor: 'divider', px: 2 }}
                    >
                        <Tab icon={<IconUser size={16} />} iconPosition="start"
                            label="Información Personal" />
                        <Tab icon={<IconClipboardList size={16} />} iconPosition="start"
                            label="Información Laboral" />
                    </Tabs>

                    <Box sx={{ p: 3 }}>
                        {formError && (
                            <Alert severity="error" sx={{ mb: 2 }} onClose={() => setFormError(null)}>
                                {formError}
                            </Alert>
                        )}

                        {/* ─── TAB 1: Datos Personales ─────────────────── */}
                        {tabActual === 0 && (
                            <Grid container spacing={2}>
                                {/* Tipo + Identificación */}
                                <Grid size={4}>
                                    <TextField select label="Tipo ID *" fullWidth
                                        value={form.tipo_identificacion}
                                        onChange={e => setForm({ ...form, tipo_identificacion: e.target.value })}>
                                        {TIPO_ID_OPT.map(t => (
                                            <MenuItem key={t} value={t}>{t}</MenuItem>
                                        ))}
                                    </TextField>
                                </Grid>
                                <Grid size={8}>
                                    <TextField label="Número de Identificación *" fullWidth
                                        value={form.identificacion}
                                        error={form.tipo_identificacion === 'CEDULA' && form.identificacion.length === 10 && !validarCedula(form.identificacion)}
                                        helperText={
                                            form.tipo_identificacion === 'CEDULA' && form.identificacion.length === 10 && !validarCedula(form.identificacion)
                                                ? 'Cédula inválida (verificar dígito)' : ''
                                        }
                                        onChange={e => setForm({ ...form, identificacion: e.target.value })} />
                                </Grid>

                                {/* Nombres y Apellidos */}
                                <Grid size={6}>
                                    <TextField label="Nombres *" fullWidth value={form.nombres}
                                        onChange={e => setForm({ ...form, nombres: e.target.value })} />
                                </Grid>
                                <Grid size={6}>
                                    <TextField label="Apellidos *" fullWidth value={form.apellidos}
                                        onChange={e => setForm({ ...form, apellidos: e.target.value })} />
                                </Grid>

                                {/* Nacimiento + Género */}
                                <Grid size={4}>
                                    <TextField label="Fecha de Nacimiento *" type="date" fullWidth
                                        InputLabelProps={{ shrink: true }} value={form.fecha_nacimiento}
                                        onChange={e => setForm({ ...form, fecha_nacimiento: e.target.value })} />
                                </Grid>
                                <Grid size={4}>
                                    <TextField select label="Género" fullWidth value={form.genero}
                                        onChange={e => setForm({ ...form, genero: e.target.value })}>
                                        <MenuItem value="">Sin especificar</MenuItem>
                                        {GENERO_OPT.map(g => <MenuItem key={g} value={g}>{g}</MenuItem>)}
                                    </TextField>
                                </Grid>
                                <Grid size={4}>
                                    <TextField label="% Discapacidad" type="number" fullWidth
                                        inputProps={{ min: 0, max: 100, step: 1 }}
                                        value={form.porcentaje_discapacidad}
                                        onChange={e => setForm({ ...form, porcentaje_discapacidad: e.target.value })} />
                                </Grid>

                                {/* Contacto */}
                                <Grid size={6}>
                                    <TextField label="Correo Institucional / Personal" fullWidth
                                        type="email" value={form.correo_personal}
                                        onChange={e => setForm({ ...form, correo_personal: e.target.value })} />
                                </Grid>
                                <Grid size={6}>
                                    <TextField label="Teléfono Celular" fullWidth
                                        value={form.telefono_celular}
                                        onChange={e => setForm({ ...form, telefono_celular: e.target.value })} />
                                </Grid>

                                {/* Previsional */}
                                <Grid size={12}>
                                    <Stack direction="row" spacing={2} flexWrap="wrap">
                                        <FormControlLabel label="Aplica IESS"
                                            control={<Switch checked={form.aplica_iess}
                                                onChange={e => setForm({ ...form, aplica_iess: e.target.checked })} />} />
                                        <FormControlLabel label="Fondos de Reserva"
                                            control={<Switch checked={form.acumula_fondos_reserva}
                                                onChange={e => setForm({ ...form, acumula_fondos_reserva: e.target.checked })} />} />
                                        <FormControlLabel label="Décimos"
                                            control={<Switch checked={form.acumula_decimos}
                                                onChange={e => setForm({ ...form, acumula_decimos: e.target.checked })} />} />
                                    </Stack>
                                </Grid>
                            </Grid>
                        )}

                        {/* ─── TAB 2: Información Laboral ──────────────── */}
                        {tabActual === 1 && (
                            <Grid container spacing={2}>
                                {/* Sección: Régimen y Contrato */}
                                <Grid size={12}>
                                    <Typography variant="overline" color="primary" fontWeight={700}>
                                        Régimen Legal y Contratación
                                    </Typography>
                                </Grid>

                                <Grid size={4}>
                                    <TextField select label="Régimen Legal" fullWidth
                                        value={form.regimen_legal}
                                        onChange={e => setForm({ ...form, regimen_legal: e.target.value })}>
                                        <MenuItem value="">Sin especificar</MenuItem>
                                        {REGIMEN_OPT.map(r => (
                                            <MenuItem key={r.value} value={r.value}>{r.label}</MenuItem>
                                        ))}
                                    </TextField>
                                </Grid>
                                <Grid size={4}>
                                    <TextField select label="Tipo Contrato Actual" fullWidth
                                        value={form.tipo_contrato_actual}
                                        onChange={e => setForm({ ...form, tipo_contrato_actual: e.target.value })}>
                                        <MenuItem value="">Sin especificar</MenuItem>
                                        {TIPO_CONTRATO_OPT.map(t => (
                                            <MenuItem key={t.value} value={t.value}>{t.label}</MenuItem>
                                        ))}
                                    </TextField>
                                </Grid>
                                <Grid size={4}>
                                    <TextField label="Código SERCOP" fullWidth
                                        placeholder="Ej: 1234-FUNC"
                                        value={form.codigo_sercop}
                                        onChange={e => setForm({ ...form, codigo_sercop: e.target.value })} />
                                </Grid>

                                {/* Sección: Posición inicial */}
                                <Grid size={12}>
                                    <Divider />
                                    <Typography variant="overline" color="primary" fontWeight={700} sx={{ mt: 1, display: 'block' }}>
                                        Posición Inicial (Historial Laboral)
                                    </Typography>
                                </Grid>

                                <Grid size={6}>
                                    <TextField select label="Área Organizacional *" fullWidth
                                        value={form.id_area}
                                        onChange={e => setForm({ ...form, id_area: e.target.value })}>
                                        {areas.length === 0 && (
                                            <MenuItem disabled value="">Cargando áreas...</MenuItem>
                                        )}
                                        {areas.map(a => (
                                            <MenuItem key={a.id_area} value={a.id_area}>
                                                [{a.tipo_area}] {a.nombre}
                                            </MenuItem>
                                        ))}
                                    </TextField>
                                </Grid>
                                <Grid size={6}>
                                    <TextField select label="Cargo *" fullWidth
                                        value={form.id_cargo}
                                        onChange={e => setForm({ ...form, id_cargo: e.target.value })}>
                                        {cargos.length === 0 && (
                                            <MenuItem disabled value="">Cargando cargos...</MenuItem>
                                        )}
                                        {cargos.map(c => (
                                            <MenuItem key={c.id_cargo} value={c.id_cargo}>
                                                {c.nombre_cargo}
                                            </MenuItem>
                                        ))}
                                    </TextField>
                                </Grid>

                                <Grid size={4}>
                                    <TextField select label="Tipo Contrato (Historial) *" fullWidth
                                        value={form.tipo_contrato}
                                        onChange={e => setForm({ ...form, tipo_contrato: e.target.value })}>
                                        {TIPO_CONTRATO_OPT.map(t => (
                                            <MenuItem key={t.value} value={t.value}>{t.label}</MenuItem>
                                        ))}
                                    </TextField>
                                </Grid>
                                <Grid size={4}>
                                    <TextField label="Fecha de Ingreso *" type="date" fullWidth
                                        InputLabelProps={{ shrink: true }} value={form.fecha_inicio}
                                        onChange={e => setForm({ ...form, fecha_inicio: e.target.value })} />
                                </Grid>
                                <Grid size={4}>
                                    <TextField label="Salario Acordado (USD) *" type="number" fullWidth
                                        inputProps={{ min: 0, step: '0.01' }} value={form.salario_acordado}
                                        onChange={e => setForm({ ...form, salario_acordado: e.target.value })} />
                                </Grid>
                            </Grid>
                        )}
                    </Box>
                </DialogContent>

                <DialogActions>
                    <Button onClick={() => setOpenModal(false)} color="inherit">Cancelar</Button>
                    {tabActual === 0 ? (
                        <Button variant="contained" onClick={handleSiguiente}>
                            Siguiente → Datos Laborales
                        </Button>
                    ) : (
                        <>
                            <Button onClick={() => { setTabActual(0); setFormError(null); }}>
                                ← Volver
                            </Button>
                            <Button onClick={handleGuardar} variant="contained" disabled={saving}
                                startIcon={saving ? <CircularProgress size={16} /> : undefined}>
                                {saving ? 'Registrando...' : 'Registrar Empleado'}
                            </Button>
                        </>
                    )}
                </DialogActions>
            </Dialog>

            {/* ══════════════════════ MODAL DETALLE ════════════════════════ */}
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
                        <Box sx={{ ml: 'auto' }}>
                            <Chip
                                label={detalle?.estado_empleado ?? ''}
                                size="small"
                                color={ESTADO_COLOR[detalle?.estado_empleado ?? ''] ?? 'default'}
                            />
                        </Box>
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

                        {/* Régimen */}
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

                        {/* Historial */}
                        <Typography variant="caption" color="text.secondary" fontWeight={700}>
                            HISTORIAL LABORAL
                        </Typography>

                        {detalle?.historial && detalle.historial.length > 0 ? (
                            detalle.historial.map((h: Historial) => (
                                <Box key={h.id_historial} display="flex" gap={1.5}
                                    sx={{ pl: 1, borderLeft: '3px solid', borderColor: h.fecha_fin ? 'grey.300' : 'primary.main' }}>
                                    <Box>
                                        <Typography variant="body2" fontWeight={600}>
                                            {h.cargo?.nombre_cargo ?? '—'}
                                        </Typography>
                                        <Typography variant="caption" color="text.secondary">
                                            {h.area?.nombre ?? '—'} | {h.tipo_contrato}<br />
                                            {h.fecha_inicio} → {h.fecha_fin ?? <b>Vigente</b>} | ${Number(h.salario_acordado).toFixed(2)}
                                        </Typography>
                                    </Box>
                                </Box>
                            ))
                        ) : (
                            <Typography variant="body2" color="text.disabled">
                                Sin historial registrado
                            </Typography>
                        )}
                    </Stack>
                </DialogContent>

                <DialogActions>
                    <Button onClick={() => setDetalle(null)}>Cerrar</Button>
                </DialogActions>
            </Dialog>
        </>
    );
}
