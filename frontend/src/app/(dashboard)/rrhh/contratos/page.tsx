'use client';

import { useState, useEffect, useCallback } from 'react';
import {
    Grid, Button, Dialog, DialogTitle, DialogContent, DialogActions,
    TextField, MenuItem, Chip, Box, Alert, CircularProgress,
    Stack, Tooltip, IconButton, Typography
} from '@mui/material';
import {
    DataGrid, GridColDef, GridToolbar,
    GridActionsCellItem, GridRowParams
} from '@mui/x-data-grid';
import {
    IconPlus, IconRefresh, IconUser,
    IconContract, IconMoneybag, IconCheck
} from '@tabler/icons-react';
import MainCard from 'ui-component/cards/MainCard';
import { listarContratos, crearContrato, actualizarContrato, listarEmpleados, listarCargos, listarEscalasSalariales } from 'api/rrhh';

// ─────────────────────────────────────────────────────────────────────────────
// TIPOS
// ─────────────────────────────────────────────────────────────────────────────
interface Empleado {
    id_empleado: number;
    identificacion: string;
    nombres: string;
    apellidos: string;
}

interface EscalaSalarial {
    id_escala: number;
    grado: string;
    salario_base: string;
}

interface Cargo {
    id_cargo: number;
    nombre_cargo: string;
}

interface Contrato {
    id_contrato: number;
    id_empleado: number;
    id_escala_salarial: number | null;
    id_cargo: number;
    tipo_contrato: string;
    fecha_inicio: string;
    fecha_fin: string | null;
    sueldo_pactado: string;
    estado_contrato: string;
    observaciones: string | null;
    empleado: Empleado | null;
    cargo: Cargo | null;
    escala: EscalaSalarial | null;
}

const TIPO_CONTRATO_OPT = [
    { value: 'NOMBRAMIENTO',         label: 'Nombramiento Permanente'  },
    { value: 'NOMBRAMIENTO_PROV',    label: 'Nombramiento Provisional' },
    { value: 'OCASIONAL',            label: 'Contrato Ocasional'       },
    { value: 'INDEFINIDO',           label: 'Indefinido'               },
    { value: 'CONTRATADO_LOSEP',     label: 'Contrato LOSEP'           },
    { value: 'CONTRATADO_CT',        label: 'Contrato Código Trabajo'  },
    { value: 'REQUERIDO_PROYECTO',   label: 'Requerido por Proyecto'   },
];

const ESTADO_COLOR: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
    ACTIVO: 'success', VENCIDO: 'warning', TERMINADO: 'error',
};

const FORM_INIT = {
    id_empleado:        '',
    id_cargo:           '',
    id_escala_salarial: '',
    tipo_contrato:      'NOMBRAMIENTO',
    fecha_inicio:       new Date().toISOString().split('T')[0],
    fecha_fin:          '',
    sueldo_pactado:     '',
    observaciones:      '',
};

// ─────────────────────────────────────────────────────────────────────────────
// COMPONENTE PRINCIPAL
// ─────────────────────────────────────────────────────────────────────────────
export default function GestionContratos() {
    const [contratos, setContratos] = useState<Contrato[]>([]);
    const [empleados, setEmpleados] = useState<Empleado[]>([]);
    const [cargos,    setCargos]    = useState<Cargo[]>([]);
    const [escalas,   setEscalas]   = useState<EscalaSalarial[]>([]);
    
    const [loading,   setLoading]   = useState(true);
    const [error,     setError]     = useState<string | null>(null);

    const [openModal, setOpenModal] = useState(false);
    const [form,      setForm]      = useState(FORM_INIT);
    const [saving,    setSaving]    = useState(false);
    const [formError, setFormError] = useState<string | null>(null);

    // ── Fetch ──────────────────────────────────────────────────────────────
    const cargarDatos = useCallback(async () => {
        setLoading(true); setError(null);
        try {
            const [rawContratos, rawEmpleados, rawCargos, rawEscalas] = await Promise.all([
                listarContratos(),
                listarEmpleados(),
                listarCargos(),
                listarEscalasSalariales(),
            ]);

            const toArray = (d: any) => Array.isArray(d) ? d : (d?.items ?? d?.data ?? []);

            setContratos(toArray(rawContratos));
            setEmpleados(toArray(rawEmpleados));
            setCargos(toArray(rawCargos));
            setEscalas(toArray(rawEscalas));
        } catch (e: any) {
            setError(e.response?.data?.detail ?? 'Error al cargar los datos');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => { cargarDatos(); }, [cargarDatos]);

    // ── Actions ────────────────────────────────────────────────────────────
    const abrirModal = () => {
        setForm(FORM_INIT);
        setFormError(null);
        setOpenModal(true);
    };

    const handleGuardar = async () => {
        if (!form.id_empleado) return setFormError('El empleado es obligatorio.');
        if (!form.id_cargo) return setFormError('El cargo es obligatorio.');
        if (!form.tipo_contrato) return setFormError('El tipo de contrato es obligatorio.');
        if (!form.fecha_inicio) return setFormError('La fecha de inicio es obligatoria.');
        if (!form.sueldo_pactado || isNaN(Number(form.sueldo_pactado)) || Number(form.sueldo_pactado) <= 0) {
            return setFormError('Sueldo pactado inválido.');
        }

        setSaving(true); setFormError(null);
        try {
            await crearContrato({
                id_empleado:        Number(form.id_empleado),
                id_cargo:           Number(form.id_cargo),
                id_escala_salarial: form.id_escala_salarial ? Number(form.id_escala_salarial) : null,
                tipo_contrato:      form.tipo_contrato,
                fecha_inicio:       form.fecha_inicio,
                fecha_fin:          form.fecha_fin || null,
                sueldo_pactado:     Number(form.sueldo_pactado),
                estado_contrato:    'ACTIVO',
                observaciones:      form.observaciones || null,
            });
            setOpenModal(false);
            await cargarDatos();
        } catch (e: any) {
            setFormError(e.response?.data?.detail ?? 'Error al guardar el contrato');
        } finally {
            setSaving(false);
        }
    };

    const handleFinalizar = async (contrato: Contrato) => {
        if (!confirm('¿Confirma que desea finalizar este contrato?')) return;
        try {
            await actualizarContrato(contrato.id_contrato, {
                estado_contrato: 'TERMINADO',
                fecha_fin: new Date().toISOString().split('T')[0]
            });
            await cargarDatos();
        } catch (e: any) {
            alert(e.response?.data?.detail ?? 'Error al finalizar contrato');
        }
    };

    // ── Cambio de Escala -> Autofill Salario ───────────────────────────────
    const handleEscalaChange = (idEscala: string) => {
        setForm({ ...form, id_escala_salarial: idEscala });
        if (idEscala) {
            const es = escalas.find(e => e.id_escala === Number(idEscala));
            if (es) setForm(prev => ({ ...prev, sueldo_pactado: es.salario_base }));
        }
    };

    // ── Columnas ───────────────────────────────────────────────────────────
    const columns: GridColDef[] = [
        {
            field: 'empleado', headerName: 'Empleado / ID', flex: 1, minWidth: 200,
            valueGetter: (_v: any, row: Contrato) => row.empleado 
                ? `${row.empleado.apellidos} ${row.empleado.nombres}` : '—',
            renderCell: (p) => (
                <Stack direction="row" spacing={1} alignItems="center" height="100%">
                    <IconUser size={16} style={{ flexShrink: 0, opacity: 0.6 }} />
                    <Box>
                        <Typography variant="body2" fontWeight={600}>{p.value}</Typography>
                        <Typography variant="caption" color="text.secondary">
                            {p.row.empleado?.identificacion}
                        </Typography>
                    </Box>
                </Stack>
            ),
        },
        {
            field: 'cargo', headerName: 'Cargo Asignado', flex: 1, minWidth: 150,
            valueGetter: (_v: any, row: Contrato) => row.cargo?.nombre_cargo ?? '—',
            renderCell: (p) => (
                <Typography variant="body2">{p.value}</Typography>
            ),
        },
        {
            field: 'tipo_contrato', headerName: 'Tipo Contrato', width: 170,
            renderCell: (p) => (
                <Chip
                    label={TIPO_CONTRATO_OPT.find(t => t.value === p.value)?.label ?? p.value}
                    size="small" variant="outlined"
                />
            )
        },
        {
            field: 'sueldo_pactado', headerName: 'Sueldo (USD)', width: 130,
            renderCell: (p) => (
                <Stack direction="row" spacing={0.5} alignItems="center" height="100%">
                    <IconMoneybag size={15} style={{ opacity: 0.6 }} color="green" />
                    <Typography variant="body2" fontWeight={600}>
                        ${Number(p.value).toFixed(2)}
                    </Typography>
                </Stack>
            ),
        },
        {
            field: 'fecha_inicio', headerName: 'Fecha Inicio', width: 120,
        },
        {
            field: 'fecha_fin', headerName: 'Fecha Fin', width: 120,
            renderCell: (p) => (
                <Typography variant="body2" color={p.value ? 'text.primary' : 'text.disabled'}>
                    {p.value || 'Vigente'}
                </Typography>
            )
        },
        {
            field: 'estado_contrato', headerName: 'Estado', width: 110,
            renderCell: (p) => (
                <Chip
                    label={p.value} size="small" variant="filled"
                    color={ESTADO_COLOR[p.value as string] ?? 'default'}
                />
            ),
        },
        {
            field: 'acciones', type: 'actions', headerName: '', width: 70,
            getActions: (p: GridRowParams<Contrato>) => [
                <GridActionsCellItem
                    key="fin"
                    icon={<IconCheck size={17} />}
                    label="Finalizar Contrato"
                    onClick={() => handleFinalizar(p.row)}
                    disabled={p.row.estado_contrato !== 'ACTIVO'}
                    showInMenu
                />,
            ],
        },
    ];

    // ── Render ─────────────────────────────────────────────────────────────
    return (
        <>
            <MainCard
                title="Gestión de Contratos"
                secondary={
                    <Stack direction="row" spacing={1}>
                        <Tooltip title="Recargar">
                            <IconButton onClick={cargarDatos} size="small">
                                <IconRefresh size={18} />
                            </IconButton>
                        </Tooltip>
                        <Button
                            variant="contained"
                            startIcon={<IconPlus size={18} />}
                            onClick={abrirModal}
                        >
                            Nuevo Contrato
                        </Button>
                    </Stack>
                }
            >
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                <Box sx={{ height: 620, width: '100%' }}>
                    <DataGrid
                        rows={contratos.filter(c => c !== null)}
                        getRowId={(row) => row.id_contrato}
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

            {/* ══════════════════ MODAL CREAR CONTRATO ═══════════════════════ */}
            <Dialog open={openModal} onClose={() => setOpenModal(false)} maxWidth="md" fullWidth>
                <DialogTitle>
                    <Stack direction="row" spacing={1} alignItems="center">
                        <IconContract size={22} />
                        <Box>
                            <Typography variant="h5">Nuevo Contrato</Typography>
                            <Typography variant="caption" color="text.secondary">
                                Vincula un Empleado con un Cargo y Escala Salarial
                            </Typography>
                        </Box>
                    </Stack>
                </DialogTitle>

                <DialogContent dividers>
                    {formError && (
                        <Alert severity="error" sx={{ mb: 2 }}>{formError}</Alert>
                    )}

                    <Grid container spacing={2}>
                        {/* Empleado */}
                        <Grid size={12}>
                            <TextField
                                select
                                label="Empleado *"
                                fullWidth
                                value={form.id_empleado}
                                onChange={e => setForm({ ...form, id_empleado: e.target.value })}
                            >
                                {empleados.length === 0 && <MenuItem disabled value="">Cargando empleados...</MenuItem>}
                                {empleados.map(e => (
                                    <MenuItem key={e.id_empleado} value={e.id_empleado}>
                                        {e.apellidos} {e.nombres} — {e.identificacion}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </Grid>

                        {/* Rango 2: Cargo + Escala */}
                        <Grid size={6}>
                            <TextField
                                select
                                label="Cargo *"
                                fullWidth
                                value={form.id_cargo}
                                onChange={e => setForm({ ...form, id_cargo: e.target.value })}
                            >
                                {cargos.length === 0 && <MenuItem disabled value="">Cargando cargos...</MenuItem>}
                                {cargos.map(c => (
                                    <MenuItem key={c.id_cargo} value={c.id_cargo}>
                                        {c.nombre_cargo}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </Grid>

                        <Grid size={6}>
                            <TextField
                                select
                                label="Escala Salarial"
                                fullWidth
                                value={form.id_escala_salarial}
                                onChange={e => handleEscalaChange(e.target.value)}
                            >
                                <MenuItem value="">— Manual / Sin Escala —</MenuItem>
                                {escalas.map(e => (
                                    <MenuItem key={e.id_escala} value={e.id_escala}>
                                        [{e.grado}] ${Number(e.salario_base).toFixed(2)}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </Grid>

                        <Grid size={4}>
                            <TextField
                                select
                                label="Tipo de Contrato *"
                                fullWidth
                                value={form.tipo_contrato}
                                onChange={e => setForm({ ...form, tipo_contrato: e.target.value })}
                            >
                                {TIPO_CONTRATO_OPT.map(t => (
                                    <MenuItem key={t.value} value={t.value}>{t.label}</MenuItem>
                                ))}
                            </TextField>
                        </Grid>

                        <Grid size={4}>
                            <TextField
                                label="Sueldo Pactado (USD) *"
                                type="number"
                                fullWidth
                                inputProps={{ min: 0, step: '0.01' }}
                                value={form.sueldo_pactado}
                                onChange={e => setForm({ ...form, sueldo_pactado: e.target.value })}
                                helperText="Se autocompleta si eliges escala"
                            />
                        </Grid>

                        <Grid size={4}></Grid>

                        {/* Fechas */}
                        <Grid size={6}>
                            <TextField
                                label="Fecha de Inicio *"
                                type="date"
                                fullWidth
                                InputLabelProps={{ shrink: true }}
                                value={form.fecha_inicio}
                                onChange={e => setForm({ ...form, fecha_inicio: e.target.value })}
                            />
                        </Grid>

                        <Grid size={6}>
                            <TextField
                                label="Fecha de Fin"
                                type="date"
                                fullWidth
                                InputLabelProps={{ shrink: true }}
                                value={form.fecha_fin}
                                onChange={e => setForm({ ...form, fecha_fin: e.target.value })}
                                helperText="Dejar vacío si es indefinido o provisional abierto"
                            />
                        </Grid>

                        {/* Observaciones */}
                        <Grid size={12}>
                            <TextField
                                label="Observaciones"
                                fullWidth
                                multiline
                                rows={2}
                                value={form.observaciones}
                                onChange={e => setForm({ ...form, observaciones: e.target.value })}
                            />
                        </Grid>
                    </Grid>
                </DialogContent>

                <DialogActions>
                    <Button onClick={() => setOpenModal(false)} color="inherit">Cancelar</Button>
                    <Button
                        onClick={handleGuardar}
                        variant="contained"
                        disabled={saving}
                        startIcon={saving ? <CircularProgress size={16} /> : undefined}
                    >
                        {saving ? 'Guardando...' : 'Crear Contrato'}
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}
