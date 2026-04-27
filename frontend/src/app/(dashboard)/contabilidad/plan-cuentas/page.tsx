'use client';

import { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, FormControl, Grid, InputLabel, MenuItem,
  Select, TextField, Typography
} from '@mui/material';
import { DataGrid, GridActionsCellItem, GridColDef, GridRowParams, GridToolbar } from '@mui/x-data-grid';
import { IconPlus, IconEdit } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { listarCuentas, listarTiposCuenta, crearCuenta, actualizarCuenta } from 'api/contabilidad';
import { CuentaContable, CuentaContableCrear, TipoCuenta } from 'types/contabilidad';

// ── Colores por nivel de cuenta ──────────────────────────────
const COLOR_NIVEL: Record<number, string> = {
  1: '#1565c0', 2: '#2e7d32', 3: '#6a1b9a',
  4: '#e65100', 5: '#00838f',
};

const ESTADO_COLOR: Record<string, 'success' | 'error'> = {
  ACTIVA: 'success', INACTIVA: 'error',
};

const FORM_DEFAULT: CuentaContableCrear = {
  codigo: '', nombre: '', descripcion: '', tipo_cuenta_id: 0,
  cuenta_padre_id: undefined, nivel: 1, es_hoja: true,
  permite_movimientos: true, partida_presupuestaria: '', estado: 'ACTIVA',
};

// ── Componente principal ─────────────────────────────────────
const PlanDeCuentasPage = () => {
  const [cuentas, setCuentas] = useState<CuentaContable[]>([]);
  const [tipos, setTipos] = useState<TipoCuenta[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [abrirModal, setAbrirModal] = useState(false);
  const [modoEdicion, setModoEdicion] = useState<number | null>(null);
  const [formulario, setFormulario] = useState<CuentaContableCrear>(FORM_DEFAULT);
  const [guardando, setGuardando] = useState(false);
  const [errorFormulario, setErrorFormulario] = useState<string | null>(null);

  const cargarDatos = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const [resCuentas, resTipos] = await Promise.all([
        listarCuentas(),
        listarTiposCuenta(),
      ]);
      setCuentas(resCuentas);
      setTipos(resTipos);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar el plan de cuentas');
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => { cargarDatos(); }, [cargarDatos]);

  const abrirNueva = () => {
    setModoEdicion(null);
    setFormulario(FORM_DEFAULT);
    setErrorFormulario(null);
    setAbrirModal(true);
  };

  const abrirEdicion = (cuenta: CuentaContable) => {
    setModoEdicion(cuenta.id);
    setFormulario({
      codigo: cuenta.codigo,
      nombre: cuenta.nombre,
      descripcion: cuenta.descripcion ?? '',
      tipo_cuenta_id: cuenta.tipo_cuenta_id,
      cuenta_padre_id: cuenta.cuenta_padre_id,
      nivel: cuenta.nivel,
      es_hoja: cuenta.es_hoja,
      permite_movimientos: cuenta.permite_movimientos,
      partida_presupuestaria: cuenta.partida_presupuestaria ?? '',
      estado: cuenta.estado,
    });
    setErrorFormulario(null);
    setAbrirModal(true);
  };

  const handleGuardar = async () => {
    if (!formulario.codigo || !formulario.nombre || !formulario.tipo_cuenta_id) {
      setErrorFormulario('Código, Nombre y Tipo de Cuenta son obligatorios.');
      return;
    }
    setGuardando(true);
    setErrorFormulario(null);
    try {
      if (modoEdicion) {
        await actualizarCuenta(modoEdicion, {
          nombre: formulario.nombre,
          descripcion: formulario.descripcion,
          partida_presupuestaria: formulario.partida_presupuestaria,
          estado: formulario.estado,
          permite_movimientos: formulario.permite_movimientos,
        });
      } else {
        await crearCuenta(formulario);
      }
      setAbrirModal(false);
      await cargarDatos();
    } catch (err: any) {
      setErrorFormulario(err?.detail || err?.message || 'Error al guardar la cuenta');
    } finally {
      setGuardando(false);
    }
  };

  const columnas: GridColDef[] = [
    {
      field: 'codigo', headerName: 'Código', width: 150,
      renderCell: (p) => (
        <Typography
          variant="body2" fontFamily="monospace" fontWeight={700}
          sx={{ color: COLOR_NIVEL[p.row.nivel] ?? '#333' }}
        >
          {'  '.repeat((p.row.nivel - 1) * 2)}{p.value}
        </Typography>
      ),
    },
    { field: 'nombre', headerName: 'Nombre', flex: 1, minWidth: 200 },
    {
      field: 'tipo_cuenta_id', headerName: 'Tipo', width: 140,
      valueGetter: (params: any) => tipos.find(t => t.id === params.row.tipo_cuenta_id)?.nombre ?? '—',
    },
    { field: 'nivel', headerName: 'Nivel', width: 70, type: 'number' },
    {
      field: 'estado', headerName: 'Estado', width: 100,
      renderCell: (p) => (
        <Chip label={p.value} color={ESTADO_COLOR[p.value] ?? 'default'} size="small" variant="outlined" />
      ),
    },
    { field: 'permite_movimientos', headerName: 'Mov.', width: 80, type: 'boolean' },
    {
      field: 'partida_presupuestaria', headerName: 'Partida Presup.', width: 160,
      valueGetter: (p: any) => p.row.partida_presupuestaria || '—',
    },
    {
      field: 'acciones', type: 'actions', headerName: '', width: 60,
      getActions: (params: GridRowParams) => [
        <GridActionsCellItem
          key="editar"
          icon={<IconEdit size={18} />}
          label="Editar"
          onClick={() => abrirEdicion(params.row as CuentaContable)}
        />,
      ],
    },
  ];

  return (
    <MainCard
      title="Plan de Cuentas — SIGEF"
      secondary={
        <Button variant="contained" startIcon={<IconPlus size={18} />} onClick={abrirNueva}>
          Nueva Cuenta
        </Button>
      }
    >
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Box sx={{ height: 650, width: '100%' }}>
        <DataGrid
          rows={cuentas}
          columns={columnas}
          loading={cargando}
          pageSizeOptions={[25, 50, 100]}
          slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { showQuickFilter: true } }}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          disableRowSelectionOnClick
          sx={{
            border: 'none',
            '& .MuiDataGrid-columnHeaders': { backgroundColor: '#f8fafc', fontWeight: 700 },
            '& .MuiDataGrid-row:hover': { backgroundColor: '#f0f4ff' },
          }}
        />
      </Box>

      {/* ── Modal: Nueva / Editar Cuenta ── */}
      <Dialog open={abrirModal} onClose={() => setAbrirModal(false)} maxWidth="md" fullWidth>
        <DialogTitle>{modoEdicion ? 'Editar Cuenta Contable' : 'Nueva Cuenta Contable'}</DialogTitle>
        <DialogContent dividers>
          {errorFormulario && <Alert severity="error" sx={{ mb: 2 }}>{errorFormulario}</Alert>}
          <Grid container spacing={2} sx={{ pt: 1 }}>
            <Grid size={{ xs: 12, md: 4 }}>
              <TextField
                label="Código SIGEF *" fullWidth value={formulario.codigo} disabled={!!modoEdicion}
                onChange={e => setFormulario({ ...formulario, codigo: e.target.value })}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 8 }}>
              <TextField
                label="Nombre *" fullWidth value={formulario.nombre}
                onChange={e => setFormulario({ ...formulario, nombre: e.target.value })}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 4 }}>
              <FormControl fullWidth>
                <InputLabel>Tipo de Cuenta *</InputLabel>
                <Select
                  value={formulario.tipo_cuenta_id || ''}
                  label="Tipo de Cuenta *"
                  disabled={!!modoEdicion}
                  onChange={e => setFormulario({ ...formulario, tipo_cuenta_id: Number(e.target.value) })}
                >
                  {tipos.map(t => <MenuItem key={t.id} value={t.id}>{t.nombre}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, md: 4 }}>
              <TextField
                label="Nivel (1-10)" type="number" fullWidth value={formulario.nivel} disabled={!!modoEdicion}
                inputProps={{ min: 1, max: 10 }}
                onChange={e => setFormulario({ ...formulario, nivel: Number(e.target.value) })}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 4 }}>
              <FormControl fullWidth>
                <InputLabel>Estado</InputLabel>
                <Select
                  value={formulario.estado || 'ACTIVA'}
                  label="Estado"
                  onChange={e => setFormulario({ ...formulario, estado: e.target.value })}
                >
                  <MenuItem value="ACTIVA">ACTIVA</MenuItem>
                  <MenuItem value="INACTIVA">INACTIVA</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={12}>
              <TextField
                label="Partida Presupuestaria" fullWidth value={formulario.partida_presupuestaria}
                onChange={e => setFormulario({ ...formulario, partida_presupuestaria: e.target.value })}
              />
            </Grid>
            <Grid size={12}>
              <TextField
                label="Descripción" fullWidth multiline rows={2} value={formulario.descripcion}
                onChange={e => setFormulario({ ...formulario, descripcion: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirModal(false)} color="inherit">Cancelar</Button>
          <Button
            onClick={handleGuardar} variant="contained" disabled={guardando}
            startIcon={guardando ? <CircularProgress size={16} /> : undefined}
          >
            {guardando ? 'Guardando...' : (modoEdicion ? 'Actualizar' : 'Crear Cuenta')}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default PlanDeCuentasPage;
