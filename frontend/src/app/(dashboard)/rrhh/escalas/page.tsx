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
    IconPlus, IconRefresh, IconEdit, IconCurrencyDollar
} from '@tabler/icons-react';
import MainCard from 'ui-component/cards/MainCard';
import axios from 'utils/axios';

// ─────────────────────────────────────────────────────────────────────────────
// TIPOS
// ─────────────────────────────────────────────────────────────────────────────
interface EscalaSalarial {
    id_escala: number;
    grado: string;
    salario_base: string;
    regimen_laboral: string;
}

const REGIMEN_OPT = ['LOEP', 'CODIGO_TRABAJO'];

const REGIMEN_LABEL: Record<string, string> = {
    LOEP:           'LOEP',
    CODIGO_TRABAJO: 'Código de Trabajo',
};

const FORM_INIT = {
    grado: '',
    salario_base: '',
    regimen_laboral: 'LOEP',
};

// ─────────────────────────────────────────────────────────────────────────────
// COMPONENTE
// ─────────────────────────────────────────────────────────────────────────────
export default function EscalasSalariales() {
    const [escalas,   setEscalas]   = useState<EscalaSalarial[]>([]);
    const [loading,   setLoading]   = useState(true);
    const [error,     setError]     = useState<string | null>(null);
    const [openModal, setOpenModal] = useState(false);
    const [editTarget, setEditTarget] = useState<EscalaSalarial | null>(null);
    const [form,      setForm]      = useState(FORM_INIT);
    const [saving,    setSaving]    = useState(false);
    const [formError, setFormError] = useState<string | null>(null);

    // ── Fetch ──────────────────────────────────────────────────────────────
    const cargar = useCallback(async () => {
        setLoading(true); setError(null);
        try {
            const res = await axios.get('/api/rrhh/escalas-salariales');
            const raw: EscalaSalarial[] = Array.isArray(res.data) ? res.data
                : (res.data?.items ?? res.data?.data ?? []);
            setEscalas(
                raw
                    .filter((e): e is EscalaSalarial => e !== null && e !== undefined)
                    .map(e => ({ ...e, id: e.id_escala }))
            );
        } catch (e: any) {
            setError(e.response?.data?.detail ?? 'Error al cargar escalas salariales');
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

    const abrirEditar = (escala: EscalaSalarial) => {
        setEditTarget(escala);
        setForm({
            grado:           escala.grado,
            salario_base:    escala.salario_base,
            regimen_laboral: escala.regimen_laboral,
        });
        setFormError(null);
        setOpenModal(true);
    };

    // ── Guardar ────────────────────────────────────────────────────────────
    const handleGuardar = async () => {
        if (!form.grado.trim() || !form.salario_base || !form.regimen_laboral) {
            setFormError('Grado, salario base y régimen laboral son obligatorios.');
            return;
        }
        const salario = parseFloat(form.salario_base);
        if (isNaN(salario) || salario <= 0) {
            setFormError('El salario base debe ser un número positivo.');
            return;
        }
        setSaving(true); setFormError(null);
        try {
            const payload = {
                grado:           form.grado.trim().toUpperCase(),
                salario_base:    salario,
                regimen_laboral: form.regimen_laboral,
            };

            if (editTarget) {
                await axios.put(`/api/rrhh/escalas-salariales/${editTarget.id_escala}`, payload);
            } else {
                await axios.post('/api/rrhh/escalas-salariales', payload);
            }

            setOpenModal(false);
            await cargar();
        } catch (e: any) {
            setFormError(e.response?.data?.detail ?? 'Error al guardar la escala');
        } finally {
            setSaving(false);
        }
    };

    // ── Columnas ───────────────────────────────────────────────────────────
    const columns: GridColDef[] = [
        {
            field: 'grado', headerName: 'Grado', width: 120,
            renderCell: (p) => (
                <Chip label={p.value} size="small" color="primary" variant="outlined" />
            ),
        },
        {
            field: 'salario_base', headerName: 'Salario Base (USD)', width: 180,
            renderCell: (p) => (
                <Stack direction="row" spacing={0.5} alignItems="center" height="100%">
                    <IconCurrencyDollar size={15} style={{ opacity: 0.6 }} />
                    <Typography variant="body2" fontWeight={600}>
                        {Number(p.value).toLocaleString('es-EC', { minimumFractionDigits: 2 })}
                    </Typography>
                </Stack>
            ),
        },
        {
            field: 'regimen_laboral', headerName: 'Régimen Laboral', flex: 1, minWidth: 160,
            renderCell: (p) => (
                <Chip
                    label={REGIMEN_LABEL[p.value as string] ?? p.value}
                    size="small"
                    color={p.value === 'LOEP' ? 'info' : 'secondary'}
                    variant="outlined"
                />
            ),
        },
        {
            field: 'acciones', type: 'actions', headerName: '', width: 70,
            getActions: (p: GridRowParams<EscalaSalarial>) => [
                <GridActionsCellItem
                    key="editar"
                    icon={<IconEdit size={17} />}
                    label="Editar"
                    onClick={() => abrirEditar(p.row)}
                />,
            ],
        },
    ];

    // ── Render ─────────────────────────────────────────────────────────────
    return (
        <>
            <MainCard
                title="Escalas Salariales"
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
                            Nueva Escala
                        </Button>
                    </Stack>
                }
            >
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                <Box sx={{ height: 520, width: '100%' }}>
                    <DataGrid
                        rows={escalas}
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
            <Dialog open={openModal} onClose={() => setOpenModal(false)} maxWidth="xs" fullWidth>
                <DialogTitle>
                    {editTarget
                        ? `Editar Escala: ${editTarget.grado}`
                        : 'Nueva Escala Salarial'}
                </DialogTitle>

                <DialogContent dividers>
                    {formError && (
                        <Alert severity="error" sx={{ mb: 2 }}>{formError}</Alert>
                    )}

                    <Stack spacing={2} sx={{ pt: 0.5 }}>
                        <TextField
                            label="Grado *"
                            fullWidth
                            placeholder="Ej: SP1, CT3, G2..."
                            value={form.grado}
                            onChange={e => setForm({ ...form, grado: e.target.value })}
                            helperText="Se guardará en mayúsculas"
                        />

                        <TextField
                            label="Salario Base (USD) *"
                            fullWidth
                            type="number"
                            inputProps={{ min: 0, step: '0.01' }}
                            value={form.salario_base}
                            onChange={e => setForm({ ...form, salario_base: e.target.value })}
                        />

                        <TextField
                            select
                            label="Régimen Laboral *"
                            fullWidth
                            value={form.regimen_laboral}
                            onChange={e => setForm({ ...form, regimen_laboral: e.target.value })}
                        >
                            {REGIMEN_OPT.map(r => (
                                <MenuItem key={r} value={r}>
                                    {REGIMEN_LABEL[r] ?? r}
                                </MenuItem>
                            ))}
                        </TextField>
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
                        {saving ? 'Guardando...' : editTarget ? 'Guardar Cambios' : 'Crear Escala'}
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}
