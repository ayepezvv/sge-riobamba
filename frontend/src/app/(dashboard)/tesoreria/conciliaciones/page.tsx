'use client';

import { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, FormControl, Grid, InputLabel, MenuItem,
  Select, TextField
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem, GridRowParams } from '@mui/x-data-grid';
import { IconPlus, IconLock } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import {
  listarCuentasBancarias, listarExtractos, listarConciliaciones,
  crearConciliacion, cerrarConciliacion,
} from 'api/tesoreria';
import { CuentaBancaria, ExtractoBancario, ConciliacionBancaria, ConciliacionBancariaCrear } from 'types/tesoreria';

const ESTADO_COLOR: Record<string, 'default' | 'warning' | 'success'> = {
  ABIERTA: 'warning', CERRADA: 'success',
};

const ConciliacionesPage = () => {
  const [conciliaciones, setConciliaciones] = useState<ConciliacionBancaria[]>([]);
  const [cuentas, setCuentas] = useState<CuentaBancaria[]>([]);
  const [extractos, setExtractos] = useState<ExtractoBancario[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [filtroCuenta, setFiltroCuenta] = useState<number | ''>('');

  const [abrirNuevo, setAbrirNuevo] = useState(false);
  const [formulario, setFormulario] = useState<ConciliacionBancariaCrear>({
    cuenta_bancaria_id: 0, extracto_id: 0, fecha_inicio: '', fecha_fin: '',
    saldo_libro: 0, saldo_extracto: 0, notas: '',
  });
  const [guardando, setGuardando] = useState(false);
  const [errorFormulario, setErrorFormulario] = useState<string | null>(null);

  const cargarDatos = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const params: any = {};
      if (filtroCuenta) params.cuenta_bancaria_id = filtroCuenta;
      const [resConciliaciones, resCuentas, resExtractos] = await Promise.all([
        listarConciliaciones(params),
        listarCuentasBancarias({ solo_activas: false }),
        listarExtractos({ estado: 'CONFIRMADO' }),
      ]);
      setConciliaciones(resConciliaciones);
      setCuentas(resCuentas);
      setExtractos(resExtractos);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar');
    } finally {
      setCargando(false);
    }
  }, [filtroCuenta]);

  useEffect(() => { cargarDatos(); }, [cargarDatos]);

  const handleCerrar = async (id: number) => {
    if (!confirm('¿Cerrar esta conciliación? Esta acción es definitiva.')) return;
    try {
      await cerrarConciliacion(id);
      await cargarDatos();
    } catch (err: any) {
      setError(err?.detail || 'Error al cerrar la conciliación');
    }
  };

  const handleGuardar = async () => {
    if (!formulario.cuenta_bancaria_id || !formulario.extracto_id || !formulario.fecha_inicio || !formulario.fecha_fin) {
      setErrorFormulario('Cuenta bancaria, extracto, fechas son obligatorios.');
      return;
    }
    setGuardando(true);
    setErrorFormulario(null);
    try {
      await crearConciliacion(formulario);
      setAbrirNuevo(false);
      setFormulario({ cuenta_bancaria_id: 0, extracto_id: 0, fecha_inicio: '', fecha_fin: '', saldo_libro: 0, saldo_extracto: 0, notas: '' });
      await cargarDatos();
    } catch (err: any) {
      setErrorFormulario(err?.detail || err?.message || 'Error al crear');
    } finally {
      setGuardando(false);
    }
  };

  const extractosFiltrados = formulario.cuenta_bancaria_id
    ? extractos.filter(e => e.cuenta_bancaria_id === formulario.cuenta_bancaria_id)
    : extractos;

  const columnas: GridColDef[] = [
    {
      field: 'cuenta_bancaria_id', headerName: 'Cuenta Bancaria', flex: 1, minWidth: 160,
      valueGetter: (p: any) => cuentas.find(c => c.id === p.row.cuenta_bancaria_id)?.nombre ?? '—',
    },
    { field: 'fecha_inicio', headerName: 'Desde', width: 110 },
    { field: 'fecha_fin', headerName: 'Hasta', width: 110 },
    { field: 'saldo_libro', headerName: 'Saldo Libro', width: 120, type: 'number', valueFormatter: (p: any) => Number(p.value).toFixed(2) },
    { field: 'saldo_extracto', headerName: 'Saldo Extracto', width: 130, type: 'number', valueFormatter: (p: any) => Number(p.value).toFixed(2) },
    {
      field: 'diferencia', headerName: 'Diferencia', width: 110, type: 'number',
      valueGetter: (p: any) => Number(p.row.saldo_libro) - Number(p.row.saldo_extracto),
      valueFormatter: (p: any) => Number(p.value).toFixed(2),
      cellClassName: (p: any) => Math.abs(Number(p.value)) < 0.01 ? '' : 'error-cell',
    },
    {
      field: 'estado', headerName: 'Estado', width: 100,
      renderCell: p => <Chip label={p.value} color={ESTADO_COLOR[p.value] ?? 'default'} size="small" variant="outlined" />,
    },
    {
      field: 'acciones', type: 'actions', headerName: '', width: 60,
      getActions: (params: GridRowParams) => {
        if (params.row.estado === 'ABIERTA') {
          return [
            <GridActionsCellItem key="cerrar" icon={<IconLock size={18} />} label="Cerrar Conciliación" onClick={() => handleCerrar(params.row.id)} showInMenu />,
          ];
        }
        return [];
      },
    },
  ];

  return (
    <MainCard
      title="Conciliación Bancaria"
      secondary={
        <Button variant="contained" startIcon={<IconPlus size={18} />} onClick={() => setAbrirNuevo(true)}>
          Nueva Conciliación
        </Button>
      }
    >
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid size={{ xs: 12, md: 4 }}>
          <FormControl fullWidth size="small">
            <InputLabel>Cuenta Bancaria</InputLabel>
            <Select value={filtroCuenta} label="Cuenta Bancaria" onChange={e => setFiltroCuenta(e.target.value as number | '')}>
              <MenuItem value="">Todas</MenuItem>
              {cuentas.map(c => <MenuItem key={c.id} value={c.id}>{c.nombre}</MenuItem>)}
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      <Box sx={{ height: 520, width: '100%' }}>
        <DataGrid
          rows={conciliaciones} columns={columnas} loading={cargando}
          pageSizeOptions={[25, 50]} slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { showQuickFilter: true } }}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          disableRowSelectionOnClick
          sx={{
            border: 'none',
            '& .MuiDataGrid-columnHeaders': { backgroundColor: '#f8fafc', fontWeight: 700 },
            '& .error-cell': { color: 'error.main', fontWeight: 700 },
          }}
        />
      </Box>

      <Dialog open={abrirNuevo} onClose={() => setAbrirNuevo(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Nueva Conciliación Bancaria</DialogTitle>
        <DialogContent dividers>
          {errorFormulario && <Alert severity="error" sx={{ mb: 2 }}>{errorFormulario}</Alert>}
          <Grid container spacing={2} sx={{ pt: 1 }}>
            <Grid size={12}>
              <FormControl fullWidth>
                <InputLabel>Cuenta Bancaria *</InputLabel>
                <Select value={formulario.cuenta_bancaria_id || ''} label="Cuenta Bancaria *"
                  onChange={e => setFormulario({ ...formulario, cuenta_bancaria_id: Number(e.target.value), extracto_id: 0 })}>
                  {cuentas.filter(c => c.es_activa).map(c => <MenuItem key={c.id} value={c.id}>{c.nombre}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={12}>
              <FormControl fullWidth disabled={!formulario.cuenta_bancaria_id}>
                <InputLabel>Extracto Bancario (Confirmado) *</InputLabel>
                <Select value={formulario.extracto_id || ''} label="Extracto Bancario (Confirmado) *"
                  onChange={e => setFormulario({ ...formulario, extracto_id: Number(e.target.value) })}>
                  {extractosFiltrados.map(e => <MenuItem key={e.id} value={e.id}>{e.fecha_inicio} → {e.fecha_fin} | {e.referencia || 'Sin ref.'}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={6}>
              <TextField label="Fecha Inicio *" type="date" fullWidth InputLabelProps={{ shrink: true }}
                value={formulario.fecha_inicio} onChange={e => setFormulario({ ...formulario, fecha_inicio: e.target.value })} />
            </Grid>
            <Grid size={6}>
              <TextField label="Fecha Fin *" type="date" fullWidth InputLabelProps={{ shrink: true }}
                value={formulario.fecha_fin} onChange={e => setFormulario({ ...formulario, fecha_fin: e.target.value })} />
            </Grid>
            <Grid size={6}>
              <TextField label="Saldo según Libros" type="number" fullWidth value={formulario.saldo_libro}
                onChange={e => setFormulario({ ...formulario, saldo_libro: parseFloat(e.target.value) || 0 })} />
            </Grid>
            <Grid size={6}>
              <TextField label="Saldo según Extracto" type="number" fullWidth value={formulario.saldo_extracto}
                onChange={e => setFormulario({ ...formulario, saldo_extracto: parseFloat(e.target.value) || 0 })} />
            </Grid>
            <Grid size={12}>
              <TextField label="Notas" multiline rows={2} fullWidth value={formulario.notas || ''}
                onChange={e => setFormulario({ ...formulario, notas: e.target.value })} />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevo(false)} color="inherit">Cancelar</Button>
          <Button onClick={handleGuardar} variant="contained" disabled={guardando}
            startIcon={guardando ? <CircularProgress size={16} /> : undefined}>
            {guardando ? 'Creando...' : 'Crear Conciliación'}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default ConciliacionesPage;
