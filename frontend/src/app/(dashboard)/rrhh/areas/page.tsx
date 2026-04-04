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
    IconPlus, IconRefresh, IconSitemap, IconEdit, IconToggleLeft
} from '@tabler/icons-react';
import MainCard from 'ui-component/cards/MainCard';
import { listarAreas, crearArea, actualizarArea } from 'api/rrhh';

// ─────────────────────────────────────────────────────────────────────────────
// TIPOS
// ─────────────────────────────────────────────────────────────────────────────
interface Area {
    id_area: number;
    id_area_padre: number | null;
    tipo_area: string;
    nombre: string;
    estado: string;
}

const TIPO_AREA_OPT = ['GERENCIA', 'DIRECCION', 'COORDINACION', 'UNIDAD'];
const ESTADO_OPT = ['ACTIVO', 'INACTIVO'];

const TIPO_COLOR: Record<string, 'primary' | 'secondary' | 'info' | 'warning'> = {
    GERENCIA: 'primary',
    DIRECCION: 'secondary',
    COORDINACION: 'warning',
    UNIDAD: 'info',
};

const ESTADO_COLOR: Record<string, 'success' | 'error' | 'default'> = {
    ACTIVO: 'success',
    INACTIVO: 'error',
};

// ─────────────────────────────────────────────────────────────────────────────
// FORMULARIO INICIAL
// ─────────────────────────────────────────────────────────────────────────────
const FORM_INIT = {
    nombre: '',
    tipo_area: 'UNIDAD',
    id_area_padre: null as number | null,  // null = nivel raíz
    estado: 'ACTIVO',
};

// ─────────────────────────────────────────────────────────────────────────────
// COMPONENTE
// ─────────────────────────────────────────────────────────────────────────────
export default function AreasOrganizacionales() {
    const [areas, setAreas] = useState<Area[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    /* Modal crear / editar */
    const [openModal, setOpenModal] = useState(false);
    const [editTarget, setEditTarget] = useState<Area | null>(null);
    const [form, setForm] = useState(FORM_INIT);
    const [saving, setSaving] = useState(false);
    const [formError, setFormError] = useState<string | null>(null);

    // ── Fetch ──────────────────────────────────────────────────────────────
    const cargar = useCallback(async () => {
        setLoading(true); setError(null);
        try {
            const res = await listarAreas();
            const raw: Area[] = Array.isArray(res) ? res
                : (res?.items ?? res?.data ?? []);
            setAreas(
                raw
                    .filter((a): a is Area => a !== null && a !== undefined)
                    .map(a => ({ ...a, id: a.id_area }))   // DataGrid requiere campo 'id'
            );
        } catch (e: any) {
            setError(e.response?.data?.detail ?? 'Error al cargar áreas organizacionales');
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

    const abrirEditar = (area: Area) => {
        setEditTarget(area);
        setForm({
            nombre: area.nombre,
            tipo_area: area.tipo_area,
            id_area_padre: area.id_area_padre ?? null,
            estado: area.estado,
        });
        setFormError(null);
        setOpenModal(true);
    };

    // ── Guardar ────────────────────────────────────────────────────────────
    const handleGuardar = async () => {
        if (!form.nombre.trim() || !form.tipo_area) {
            setFormError('El nombre y el tipo de área son obligatorios.');
            return;
        }
        setSaving(true); setFormError(null);
        try {
            const payload = {
                nombre: form.nombre.trim(),
                tipo_area: form.tipo_area,
                estado: form.estado,
                // null explícito cuando no tiene padre — FastAPI valida Optional[int] = None
                id_area_padre: (form.id_area_padre !== null && form.id_area_padre > 0)
                    ? form.id_area_padre
                    : null,
            };

            if (editTarget) {
                await actualizarArea(editTarget.id_area, payload);
            } else {
                await crearArea(payload);
            }

            setOpenModal(false);
            await cargar();
        } catch (e: any) {
            setFormError(e.response?.data?.detail ?? 'Error al guardar el área');
        } finally {
            setSaving(false);
        }
    };

    // ── Toggle estado ──────────────────────────────────────────────────────
    const handleToggleEstado = async (area: Area) => {
        const nuevoEstado = area.estado === 'ACTIVO' ? 'INACTIVO' : 'ACTIVO';
        try {
            await actualizarArea(area.id_area, { estado: nuevoEstado });
            await cargar();
        } catch (e: any) {
            alert(e.response?.data?.detail ?? 'Error al cambiar estado');
        }
    };

    // ── Columnas ───────────────────────────────────────────────────────────
    const columns: GridColDef[] = [
        {
            field: 'nombre', headerName: 'Nombre del Área', flex: 1, minWidth: 200,
            renderCell: (p) => (
                <Stack direction="row" spacing={1} alignItems="center" height="100%">
                    <IconSitemap size={16} style={{ flexShrink: 0, opacity: 0.6 }} />
                    <Typography variant="body2" fontWeight={600}>{p.value}</Typography>
                </Stack>
            ),
        },
        {
            field: 'tipo_area', headerName: 'Tipo de Área', width: 160,
            renderCell: (p) => (
                <Chip
                    label={p.value}
                    size="small"
                    color={TIPO_COLOR[p.value as string] ?? 'default'}
                    variant="outlined"
                />
            ),
        },
        {
            field: 'id_area_padre', headerName: 'Área Padre', width: 170,
            valueGetter: (_v: any, row: Area) => {
                if (!row || !row.id_area_padre) return '—';
                const padre = areas.find(a => a.id_area === row.id_area_padre);
                return padre ? padre.nombre : `#${row.id_area_padre}`;
            },
        },
        {
            field: 'estado', headerName: 'Estado', width: 120,
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
            getActions: (p: GridRowParams<Area>) => [
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
                title="Estructura Organizacional (Áreas)"
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
                            Nueva Área
                        </Button>
                    </Stack>
                }
            >
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                <Box sx={{ height: 560, width: '100%' }}>
                    <DataGrid
                        rows={areas}
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

            {/* ══════════════════════ MODAL CREAR / EDITAR ══════════════════ */}
            <Dialog open={openModal} onClose={() => setOpenModal(false)} maxWidth="sm" fullWidth>
                <DialogTitle>
                    {editTarget ? `Editar: ${editTarget.nombre}` : 'Nueva Área Organizacional'}
                </DialogTitle>

                <DialogContent dividers>
                    {formError && (
                        <Alert severity="error" sx={{ mb: 2 }}>{formError}</Alert>
                    )}

                    <Stack spacing={2} sx={{ pt: 0.5 }}>
                        {/* Nombre */}
                        <TextField
                            label="Nombre del Área *"
                            fullWidth
                            value={form.nombre}
                            onChange={e => setForm({ ...form, nombre: e.target.value })}
                        />

                        {/* Tipo */}
                        <TextField
                            select
                            label="Tipo de Área *"
                            fullWidth
                            value={form.tipo_area}
                            onChange={e => setForm({ ...form, tipo_area: e.target.value })}
                        >
                            {TIPO_AREA_OPT.map(t => (
                                <MenuItem key={t} value={t}>{t}</MenuItem>
                            ))}
                        </TextField>

                        {/* Área padre (opcional) */}
                        <TextField
                            select
                            label="Área Padre (opcional)"
                            fullWidth
                            value={form.id_area_padre ?? -1}
                            onChange={e => {
                                const v = Number(e.target.value);
                                setForm({ ...form, id_area_padre: v > 0 ? v : null });
                            }}
                        >
                            {/* -1 es centinela de "sin padre" — se convierte a null en el payload */}
                            <MenuItem value={-1}>— Sin área padre (nivel raíz) —</MenuItem>
                            {areas
                                .filter(a => !editTarget || a.id_area !== editTarget.id_area)
                                .map(a => (
                                    <MenuItem key={a.id_area} value={a.id_area}>
                                        [{a.tipo_area}] {a.nombre}
                                    </MenuItem>
                                ))
                            }
                        </TextField>

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
                        {saving ? 'Guardando...' : editTarget ? 'Guardar Cambios' : 'Crear Área'}
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}
