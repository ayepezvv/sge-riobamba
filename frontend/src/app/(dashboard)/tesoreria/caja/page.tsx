'use client';

import React, { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, FormControl, Grid, InputLabel, MenuItem,
  Select, TextField, Typography
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem, GridRowParams } from '@mui/x-data-grid';
import { IconPlus, IconListDetails } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { listarCajas, crearCaja, registrarMovimientoCaja, listarMovimientosCaja } from 'api/tesoreria';
import { CajaChica, CajaChicaCrear, MovimientoCaja, MovimientoCajaCrear, TipoMovimientoCaja } from 'types/tesoreria';

const ESTADO_COLOR: Record<string, 'default' | 'success' | 'error'> = {
  ABIERTA: 'success', CERRADA: 'error',
};

const TIPOS_MOVIMIENTO: TipoMovimientoCaja[] = ['APERTURA', 'EGRESO', 'REPOSICION', 'CIERRE'];

const CajaPage = () => {
  const [cajas, setCajas] = useState<CajaChica[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [abrirNuevaCaja, setAbrirNuevaCaja] = useState(false);
  const [formularioCaja, setFormularioCaja] = useState<CajaChicaCrear>({
    nombre: '', monto_autorizado: 0, responsable: '',
  });
  const [guardandoCaja, setGuardandoCaja] = useState(false);
  const [errorCaja, setErrorCaja] = useState<string | null>(null);

  const [cajaSeleccionada, setCajaSeleccionada] = useState<CajaChica | null>(null);
  const [movimientos, setMovimientos] = useState<MovimientoCaja[]>([]);
  const [abrirMovimientos, setAbrirMovimientos] = useState(false);

  const [abrirNuevoMovimiento, setAbrirNuevoMovimiento] = useState(false);
  const [formularioMovimiento, setFormularioMovimiento] = useState<MovimientoCajaCrear>({
    tipo: 'EGRESO', fecha: new Date().toISOString().split('T')[0], descripcion: '', valor: 0,
  });
  const [guardandoMovimiento, setGuardandoMovimiento] = useState(false);
  const [errorMovimiento, setErrorMovimiento] = useState<string | null>(null);

  const cargarCajas = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const res = await listarCajas();
      setCajas(res);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar cajas');
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => { cargarCajas(); }, [cargarCajas]);

  const verMovimientos = async (caja: CajaChica) => {
    setCajaSeleccionada(caja);
    try {
      const res = await listarMovimientosCaja(caja.id);
      setMovimientos(res);
    } catch {
      setMovimientos([]);
    }
    setAbrirMovimientos(true);
  };

  const handleCrearCaja = async () => {
    if (!formularioCaja.nombre || !formularioCaja.monto_autorizado) {
      setErrorCaja('Nombre y monto autorizado son obligatorios.');
      return;
    }
    setGuardandoCaja(true);
    setErrorCaja(null);
    try {
      await crearCaja(formularioCaja);
      setAbrirNuevaCaja(false);
      setFormularioCaja({ nombre: '', monto_autorizado: 0, responsable: '' });
      await cargarCajas();
    } catch (err: any) {
      setErrorCaja(err?.detail || err?.message || 'Error al crear la caja');
    } finally {
      setGuardandoCaja(false);
    }
  };

  const handleRegistrarMovimiento = async () => {
    if (!cajaSeleccionada || !formularioMovimiento.descripcion || !formularioMovimiento.valor) {
      setErrorMovimiento('Descripción y valor son obligatorios.');
      return;
    }
    setGuardandoMovimiento(true);
    setErrorMovimiento(null);
    try {
      await registrarMovimientoCaja(cajaSeleccionada.id, formularioMovimiento);
      const res = await listarMovimientosCaja(cajaSeleccionada.id);
      setMovimientos(res);
      setAbrirNuevoMovimiento(false);
      setFormularioMovimiento({ tipo: 'EGRESO', fecha: new Date().toISOString().split('T')[0], descripcion: '', valor: 0 });
      await cargarCajas();
    } catch (err: any) {
      setErrorMovimiento(err?.detail || err?.message || 'Error al registrar movimiento');
    } finally {
      setGuardandoMovimiento(false);
    }
  };

  const columnas: GridColDef[] = [
    { field: 'nombre', headerName: 'Nombre', flex: 1, minWidth: 180 },
    { field: 'responsable', headerName: 'Responsable', width: 180 },
    { field: 'monto_autorizado', headerName: 'Monto Autorizado', width: 150, type: 'number', valueFormatter: (p: any) => Number(p.value).toFixed(2) },
    { field: 'saldo_actual', headerName: 'Saldo Actual', width: 130, type: 'number', valueFormatter: (p: any) => Number(p.value).toFixed(2) },
    {
      field: 'estado', headerName: 'Estado', width: 100,
      renderCell: p => <Chip label={p.value} color={ESTADO_COLOR[p.value] ?? 'default'} size="small" />,
    },
    {
      field: 'acciones', type: 'actions', headerName: '', width: 60,
      getActions: (params: GridRowParams) => [
        <GridActionsCellItem key="movimientos" icon={<IconListDetails size={18} />} label="Ver Movimientos" onClick={() => verMovimientos(params.row as CajaChica)} />,
      ],
    },
  ];

  const columnasMovimientos: GridColDef[] = [
    { field: 'fecha', headerName: 'Fecha', width: 110 },
    { field: 'tipo', headerName: 'Tipo', width: 120, renderCell: p => <Chip label={p.value} size="small" variant="outlined" /> },
    { field: 'descripcion', headerName: 'Descripción', flex: 1, minWidth: 200 },
    { field: 'referencia', headerName: 'Referencia', width: 120 },
    {
      field: 'valor', headerName: 'Valor', width: 110, type: 'number',
      valueFormatter: (p: any) => Number(p.value).toFixed(2),
      cellClassName: (p: any) => {
        const tipo = (p.row as MovimientoCaja).tipo;
        return tipo === 'EGRESO' || tipo === 'CIERRE' ? 'egreso-cell' : 'ingreso-cell';
      },
    },
  ];

  return (
    <MainCard
      title="Caja Chica"
      secondary={
        <Button variant="contained" startIcon={<IconPlus size={18} />} onClick={() => setAbrirNuevaCaja(true)}>
          Nueva Caja
        </Button>
      }
    >
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Box sx={{ height: 460, width: '100%' }}>
        <DataGrid
          rows={cajas} columns={columnas} loading={cargando}
          pageSizeOptions={[25, 50]} slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { showQuickFilter: true } }}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          disableRowSelectionOnClick
          sx={{ border: 'none', '& .MuiDataGrid-columnHeaders': { backgroundColor: '#f8fafc', fontWeight: 700 } }}
        />
      </Box>

      {/* Modal Nueva Caja */}
      <Dialog open={abrirNuevaCaja} onClose={() => setAbrirNuevaCaja(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Nueva Caja Chica</DialogTitle>
        <DialogContent dividers>
          {errorCaja && <Alert severity="error" sx={{ mb: 2 }}>{errorCaja}</Alert>}
          <Grid container spacing={2} sx={{ pt: 1 }}>
            <Grid item xs={12}>
              <TextField label="Nombre *" fullWidth value={formularioCaja.nombre}
                onChange={e => setFormularioCaja({ ...formularioCaja, nombre: e.target.value })} />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField label="Responsable" fullWidth value={formularioCaja.responsable || ''}
                onChange={e => setFormularioCaja({ ...formularioCaja, responsable: e.target.value })} />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField label="Monto Autorizado *" type="number" fullWidth value={formularioCaja.monto_autorizado}
                onChange={e => setFormularioCaja({ ...formularioCaja, monto_autorizado: parseFloat(e.target.value) || 0 })} />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevaCaja(false)} color="inherit">Cancelar</Button>
          <Button onClick={handleCrearCaja} variant="contained" disabled={guardandoCaja}
            startIcon={guardandoCaja ? <CircularProgress size={16} /> : undefined}>
            {guardandoCaja ? 'Creando...' : 'Crear Caja'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Modal Movimientos */}
      <Dialog open={abrirMovimientos} onClose={() => setAbrirMovimientos(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Movimientos — {cajaSeleccionada?.nombre}
          <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
            Saldo actual: <strong>{Number(cajaSeleccionada?.saldo_actual).toFixed(2)} USD</strong>
          </Typography>
        </DialogTitle>
        <DialogContent dividers>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 1 }}>
            <Button size="small" variant="outlined" startIcon={<IconPlus size={16} />}
              onClick={() => setAbrirNuevoMovimiento(true)} disabled={cajaSeleccionada?.estado === 'CERRADA'}>
              Registrar Movimiento
            </Button>
          </Box>
          <Box sx={{ height: 380 }}>
            <DataGrid
              rows={movimientos} columns={columnasMovimientos}
              pageSizeOptions={[25]} disableRowSelectionOnClick
              sx={{
                border: 'none',
                '& .egreso-cell': { color: 'error.main', fontWeight: 700 },
                '& .ingreso-cell': { color: 'success.main', fontWeight: 700 },
              }}
            />
          </Box>
        </DialogContent>
        <DialogActions><Button onClick={() => setAbrirMovimientos(false)} color="inherit">Cerrar</Button></DialogActions>
      </Dialog>

      {/* Modal Nuevo Movimiento */}
      <Dialog open={abrirNuevoMovimiento} onClose={() => setAbrirNuevoMovimiento(false)} maxWidth="xs" fullWidth>
        <DialogTitle>Registrar Movimiento — {cajaSeleccionada?.nombre}</DialogTitle>
        <DialogContent dividers>
          {errorMovimiento && <Alert severity="error" sx={{ mb: 2 }}>{errorMovimiento}</Alert>}
          <Grid container spacing={2} sx={{ pt: 1 }}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Tipo *</InputLabel>
                <Select value={formularioMovimiento.tipo} label="Tipo *"
                  onChange={e => setFormularioMovimiento({ ...formularioMovimiento, tipo: e.target.value as TipoMovimientoCaja })}>
                  {TIPOS_MOVIMIENTO.map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField label="Fecha *" type="date" fullWidth InputLabelProps={{ shrink: true }}
                value={formularioMovimiento.fecha}
                onChange={e => setFormularioMovimiento({ ...formularioMovimiento, fecha: e.target.value })} />
            </Grid>
            <Grid item xs={12}>
              <TextField label="Descripción *" fullWidth value={formularioMovimiento.descripcion}
                onChange={e => setFormularioMovimiento({ ...formularioMovimiento, descripcion: e.target.value })} />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField label="Valor *" type="number" fullWidth value={formularioMovimiento.valor}
                onChange={e => setFormularioMovimiento({ ...formularioMovimiento, valor: parseFloat(e.target.value) || 0 })} />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField label="Referencia" fullWidth value={formularioMovimiento.referencia || ''}
                onChange={e => setFormularioMovimiento({ ...formularioMovimiento, referencia: e.target.value })} />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevoMovimiento(false)} color="inherit">Cancelar</Button>
          <Button onClick={handleRegistrarMovimiento} variant="contained" disabled={guardandoMovimiento}
            startIcon={guardandoMovimiento ? <CircularProgress size={16} /> : undefined}>
            {guardandoMovimiento ? 'Guardando...' : 'Registrar'}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default CajaPage;
