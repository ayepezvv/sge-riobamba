'use client';

import { useState, useEffect, useCallback } from 'react';
import {
    Button, Dialog, DialogTitle, DialogContent, DialogActions,
    TextField, MenuItem, Chip, Box, Alert, CircularProgress,
    Stack, Tooltip, IconButton, Typography
} from '@mui/material';
import {
    DataGrid, GridColDef, GridToolbar,
    GridActionsCellItem, GridRowParams
} from '@mui/x-data-grid';
import {
    IconPlus, IconRefresh, IconEdit, IconBriefcase, IconToggleLeft
} from '@tabler/icons-react';
import MainCard from 'ui-component/cards/MainCard';
import { listarCargos, crearCargo, actualizarCargo, listarEscalasSalariales } from 'api/rrhh';

// ─────────────────────────────────────────────────────────────────────────────
// TIPOS
// ─────────────────────────────────────────────────────────────────────────────
interface EscalaSalarial {
    id_escala: number;
    grado: string;
    salario_base: string;
    regimen_laboral: string;
}

interface Cargo {
    id_cargo: number;
    nombre_cargo: string;
    id_escala_salarial: number | null;
    partida_presupuestaria: string | null;
    estado: string;
    escala: EscalaSalarial | null;
}

const ESTADO_OPT = ['ACTIVO', 'INACTIVO'];

const ESTADO_COLOR: Record<string, 'success' | 'error' | 'default'> = {
    ACTIVO:   'success',
    INACTIVO: 'error',
};

const FORM_INIT = {
    nombre_cargo: '',
    id_escala_salarial: null as number | null,
    partida_presupuestaria: '',
    estado: 'ACTIVO',
};

// ─────────────────────────────────────────────────────────────────────────────
// COMPONENTE
// ─────────────────────────────────────────────────────────────────────────────
export default function Cargos() {
    const [cargos,    setCargos]    = useState<Cargo[]>([]);
    const [escalas,   setEscalas]   = useState<EscalaSalarial[]>([]);
    const [loading,   setLoading]   = useState(true);
    const [error,     setError]     = useState<string | null>(null);
    const [openModal, setOpenModal] = useState(false);
    const [editTarget, setEditTarget] = useState<Cargo | null>(null);
    const [form,      setForm]      = useState(FORM_INIT);
    const [saving,    setSaving]    = useState(false);
    const [formError, setFormError] = useState<string | null>(null);

    // ── Fetch ──────────────────────────────────────────────────────────────
    const cargar = useCallback(async () => {
        setLoading(true); setError(null);
        try {
            const [rawCargos, rawEscalas] = await Promise.all([
                listarCargos(),
                listarEscalasSalariales(),
            ]);

            const toCargos: Cargo[] = Array.isArray(rawCargos) ? rawCargos
                : (rawCargos?.items ?? rawCargos?.data ?? []);
            setCargos(
                toCargos
                    .filter((c): c is Cargo => c !== null && c !== undefined)
                    .map(c => ({ ...c, id: c.id_cargo }))
            );

            const toEscalas: EscalaSalarial[] = Array.isArray(rawEscalas) ? rawEscalas
                : (rawEscalas?.items ?? rawEscalas?.data ?? []);
            setEscalas(toEscalas.filter((e): e is EscalaSalarial => e !== null && e !== undefined));
        } catch (e: any) {
            setError(e.response?.data?.detail ?? 'Error al cargar cargos');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => { cargar(); }, [cargar]);

    // ── Abrir modal ────────────────────────────────────────────────────────
    const abrirCrear = () => {
        setEditTarget(null);
        setForm(FORM_INIT);
        setFormError(null);
        setOpenModal(true);
    };

    const abrirEditar = (cargo: Cargo) => {
        setEditTarget(cargo);
        setForm({
            nombre_cargo:           cargo.nombre_cargo,
            id_escala_salarial:    cargo.id_escala_salarial ?? null,
            partida_presupuestaria: cargo.partida_presupuestaria ?? '',
            estado:                 cargo.estado,
        });
        setFormError(null);
        setOpenModal(true);
    };

    // ── Guardar ────────────────────────────────────────────────────────────
    const handleGuardar = async () => {
        if (!form.nombre_cargo.trim()) {
            setFormError('El nombre del cargo es obligatorio.');
            return;
        }
        setSaving(true); setFormError(null);
        try {
            const payload = {
                nombre_cargo:           form.nombre_cargo.trim(),
                id_escala_salarial:    form.id_escala_salarial,
                partida_presupuestaria: form.partida_presupuestaria.trim() || null,
                estado:                 form.estado,
            };

            if (editTarget) {
                await actualizarCargo(editTarget.id_cargo, payload);
            } else {
                await crearCargo(payload);
            }

            setOpenModal(false);
            await cargar();
        } catch (e: any) {
            setFormError(e.response?.data?.detail ?? 'Error al guardar el cargo');
        } finally {
            setSaving(false);
        }
    };

    // ── Toggle estado ──────────────────────────────────────────────────────
    const handleToggleEstado = async (cargo: Cargo) => {
        const nuevoEstado = cargo.estado === 'ACTIVO' ? 'INACTIVO' : 'ACTIVO';
        try {
            await actualizarCargo(cargo.id_cargo, { estado: nuevoEstado });
            await cargar();
        } catch (e: any) {
            alert(e.response?.data?.detail ?? 'Error al cambiar estado');
        }
    };

    // ── Columnas ───────────────────────────────────────────────────────────
    const columns: GridColDef[] = [
        {
            field: 'nombre_cargo', headerName: 'Nombre del Cargo', flex: 1, minWidth: 220,
            renderCell: (p) => (
                <Stack direction="row" spacing={1} alignItems="center" height="100%">
                    <IconBriefcase size={16} style={{ flexShrink: 0, opacity: 0.6 }} />
                    <Typography variant="body2" fontWeight={600}>{p.value}</Typography>
                </Stack>
            ),
        },
        {
            field: 'escala', headerName: 'Escala Salarial', width: 180,
            valueGetter: (_v: any, row: Cargo) => {
                if (!row?.escala) return '—';
                return `${row.escala.grado} — $${Number(row.escala.salario_base).toFixed(2)}`;
            },
        },
        {
            field: 'partida_presupuestaria', headerName: 'Partida Presup.', width: 170,
            renderCell: (p) => (
                <Typography variant="body2" color={p.value ? 'text.primary' : 'text.disabled'}>
                    {p.value || '—'}
                </Typography>
            ),
        },
        {
            field: 'estado', headerName: 'Estado', width: 110,
            renderCell: (p) => (
                <Chip
                    label={p.value}
                    size="small"
                    color={ESTADO_COLOR[p.value as string] ?? 'default'}
                    variant="filled"
                />
            ),
        },
        {
            field: 'acciones', type: 'actions', headerName: '', width: 80,
            getActions: (p: GridRowParams<Cargo>) => [
                <GridActionsCellItem
                    key="editar"
                    icon={<IconEdit size={17} />}
                    label="Editar"
                    onClick={() => abrirEditar(p.row)}
                />,
                <GridActionsCellItem
                    key="toggle"
                    icon={<IconToggleLeft size={17} />}
                    label={p.row.estado === 'ACTIVO' ? 'Desactivar' : 'Activar'}
                    onClick={() => handleToggleEstado(p.row)}
                    showInMenu
                />,
            ],
        },
    ];

    // ── Render ─────────────────────────────────────────────────────────────
    return (
        <>
            <MainCard
                title="Catálogo de Cargos"
                secondary={
                    <Stack direction="row" spacing={1}>
                        <Tooltip title="Recargar">
                            <IconButton onClick={cargar} size="small">
                                <IconRefresh size={18} />
                            </IconButton>
                        </Tooltip>
                        <Button
                            variant="contained"
                            startIcon={<IconPlus size={18} />}
                            onClick={abrirCrear}
                        >
                            Nuevo Cargo
                        </Button>
                    </Stack>
                }
            >
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                <Box sx={{ height: 560, width: '100%' }}>
                    <DataGrid
                        rows={cargos}
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

            {/* ══════════════════ MODAL CREAR / EDITAR ═══════════════════════ */}
            <Dialog open={openModal} onClose={() => setOpenModal(false)} maxWidth="sm" fullWidth>
                <DialogTitle>
                    {editTarget
                        ? `Editar: ${editTarget.nombre_cargo}`
                        : 'Nuevo Cargo'}
                </DialogTitle>

                <DialogContent dividers>
                    {formError && (
                        <Alert severity="error" sx={{ mb: 2 }}>{formError}</Alert>
                    )}

                    <Stack spacing={2} sx={{ pt: 0.5 }}>
                        {/* Nombre */}
                        <TextField
                            label="Nombre del Cargo *"
                            fullWidth
                            value={form.nombre_cargo}
                            onChange={e => setForm({ ...form, nombre_cargo: e.target.value })}
                        />

                        {/* Escala Salarial */}
                        <TextField
                            select
                            label="Escala Salarial (opcional)"
                            fullWidth
                            value={form.id_escala_salarial ?? -1}
                            onChange={e => {
                                const v = Number(e.target.value);
                                setForm({ ...form, id_escala_salarial: v > 0 ? v : null });
                            }}
                            helperText={
                                escalas.length === 0
                                    ? 'No hay escalas registradas — crea una primera en Escalas Salariales'
                                    : 'Asigna la banda salarial del cargo'
                            }
                        >
                            <MenuItem value={-1}>— Sin escala asignada —</MenuItem>
                            {escalas.map(e => (
                                <MenuItem key={e.id_escala} value={e.id_escala}>
                                    [{e.grado}] ${Number(e.salario_base).toFixed(2)} — {
                                        e.regimen_laboral === 'LOEP' ? 'LOEP' : 'Cód. Trabajo'
                                    }
                                </MenuItem>
                            ))}
                        </TextField>

                        {/* Partida presupuestaria */}
                        <TextField
                            label="Partida Presupuestaria"
                            fullWidth
                            placeholder="Ej: 710105-001"
                            value={form.partida_presupuestaria}
                            onChange={e => setForm({ ...form, partida_presupuestaria: e.target.value })}
                        />

                        {/* Estado — solo visible al editar */}
                        {editTarget && (
                            <TextField
                                select
                                label="Estado"
                                fullWidth
                                value={form.estado}
                                onChange={e => setForm({ ...form, estado: e.target.value })}
                            >
                                {ESTADO_OPT.map(s => (
                                    <MenuItem key={s} value={s}>{s}</MenuItem>
                                ))}
                            </TextField>
                        )}
                    </Stack>
                </DialogContent>

                <DialogActions>
                    <Button onClick={() => setOpenModal(false)} color="inherit">Cancelar</Button>
                    <Button
                        onClick={handleGuardar}
                        variant="contained"
                        disabled={saving}
                        startIcon={saving ? <CircularProgress size={16} /> : undefined}
                    >
                        {saving ? 'Guardando...' : editTarget ? 'Guardar Cambios' : 'Crear Cargo'}
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}
