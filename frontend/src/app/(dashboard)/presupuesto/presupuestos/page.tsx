'use client';

import React, { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, Grid, Tab, Tabs, TextField, Typography
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem } from '@mui/x-data-grid';
import { IconPlus, IconListDetails } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import {
  listarPresupuestos, crearPresupuesto,
  listarAsignaciones, crearAsignacion,
  listarPartidas,
} from 'api/presupuesto';
import {
  PresupuestoAnual, PresupuestoAnualCrear,
  AsignacionPresupuestaria, AsignacionPresupuestariaCrear,
  PartidaPresupuestaria,
} from 'types/presupuesto';

const formatMonto = (v: number) =>
  new Intl.NumberFormat('es-EC', { style: 'currency', currency: 'USD' }).format(v);

const PresupuestosPage = () => {
  const [presupuestos, setPresupuestos] = useState<PresupuestoAnual[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [abrirNuevo, setAbrirNuevo] = useState(false);
  const [formulario, setFormulario] = useState<PresupuestoAnualCrear>({
    anio_fiscal: new Date().getFullYear(), denominacion: '', monto_inicial: 0,
  });
  const [guardando, setGuardando] = useState(false);
  const [errorForm, setErrorForm] = useState<string | null>(null);

  // Asignaciones
  const [presupuestoSeleccionado, setPresupuestoSeleccionado] = useState<PresupuestoAnual | null>(null);
  const [asignaciones, setAsignaciones] = useState<AsignacionPresupuestaria[]>([]);
  const [cargandoAsig, setCargandoAsig] = useState(false);
  const [abrirAsignaciones, setAbrirAsignaciones] = useState(false);
  const [partidas, setPartidas] = useState<PartidaPresupuestaria[]>([]);
  const [abrirNuevaAsig, setAbrirNuevaAsig] = useState(false);
  const [formularioAsig, setFormularioAsig] = useState<AsignacionPresupuestariaCrear>({
    id_presupuesto: 0, id_partida: 0, monto_inicial: 0,
  });
  const [guardandoAsig, setGuardandoAsig] = useState(false);
  const [errorAsig, setErrorAsig] = useState<string | null>(null);

  const cargarPresupuestos = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const res = await listarPresupuestos();
      setPresupuestos(res);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar presupuestos');
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => { cargarPresupuestos(); }, [cargarPresupuestos]);

  const verAsignaciones = async (pres: PresupuestoAnual) => {
    setPresupuestoSeleccionado(pres);
    setCargandoAsig(true);
    try {
      const [asigs, parts] = await Promise.all([
        listarAsignaciones({ id_presupuesto: pres.id_presupuesto }),
        listarPartidas({ solo_hojas: true }),
      ]);
      setAsignaciones(asigs);
      setPartidas(parts);
    } catch {
      setAsignaciones([]);
    } finally {
      setCargandoAsig(false);
    }
    setAbrirAsignaciones(true);
  };

  const handleCrearPresupuesto = async () => {
    if (!formulario.denominacion) {
      setErrorForm('Denominación es obligatoria.');
      return;
    }
    setGuardando(true);
    setErrorForm(null);
    try {
      await crearPresupuesto(formulario);
      setAbrirNuevo(false);
      cargarPresupuestos();
    } catch (err: any) {
      setErrorForm(err?.response?.data?.detail || err?.message || 'Error al crear presupuesto');
    } finally {
      setGuardando(false);
    }
  };

  const handleCrearAsignacion = async () => {
    if (!formularioAsig.id_partida) {
      setErrorAsig('Seleccione una partida.');
      return;
    }
    setGuardandoAsig(true);
    setErrorAsig(null);
    try {
      await crearAsignacion({ ...formularioAsig, id_presupuesto: presupuestoSeleccionado!.id_presupuesto });
      setAbrirNuevaAsig(false);
      const asigs = await listarAsignaciones({ id_presupuesto: presupuestoSeleccionado!.id_presupuesto });
      setAsignaciones(asigs);
    } catch (err: any) {
      setErrorAsig(err?.response?.data?.detail || err?.message || 'Error al crear asignación');
    } finally {
      setGuardandoAsig(false);
    }
  };

  const columnasPresupuesto: GridColDef[] = [
    { field: 'anio_fiscal', headerName: 'Año Fiscal', width: 100, type: 'number' },
    { field: 'denominacion', headerName: 'Denominación', flex: 1 },
    {
      field: 'monto_inicial', headerName: 'Monto Inicial', width: 160,
      renderCell: ({ value }) => formatMonto(value),
    },
    {
      field: 'monto_codificado', headerName: 'Monto Codificado', width: 160,
      renderCell: ({ value }) => formatMonto(value),
    },
    {
      field: 'estado', headerName: 'Estado', width: 120,
      renderCell: ({ value }) => <Chip label={value} size="small"
        color={value === 'APROBADO' ? 'success' : value === 'CERRADO' ? 'error' : 'warning'} />,
    },
    {
      field: 'acciones', type: 'actions', headerName: 'Asignaciones', width: 120,
      getActions: ({ row }) => [
        <GridActionsCellItem key="ver" icon={<IconListDetails size={18} />} label="Ver Asignaciones"
          onClick={() => verAsignaciones(row as PresupuestoAnual)} />,
      ],
    },
  ];

  const columnasAsignacion: GridColDef[] = [
    { field: 'id_partida', headerName: 'ID Partida', width: 100 },
    { field: 'monto_inicial', headerName: 'Inicial', width: 130, renderCell: ({ value }) => formatMonto(value) },
    { field: 'monto_codificado', headerName: 'Codificado', width: 130, renderCell: ({ value }) => formatMonto(value) },
    { field: 'monto_comprometido', headerName: 'Comprometido', width: 130, renderCell: ({ value }) => formatMonto(value) },
    { field: 'monto_devengado', headerName: 'Devengado', width: 130, renderCell: ({ value }) => formatMonto(value) },
    { field: 'saldo_disponible', headerName: 'Saldo', width: 130, renderCell: ({ value }) => formatMonto(value ?? 0) },
    {
      field: 'estado', headerName: 'Estado', width: 100,
      renderCell: ({ value }) => <Chip label={value} size="small" color={value === 'ACTIVO' ? 'success' : 'default'} />,
    },
  ];

  return (
    <MainCard title="Presupuestos Anuales">
      <Box sx={{ mb: 2 }}>
        <Button variant="contained" startIcon={<IconPlus />} onClick={() => { setErrorForm(null); setAbrirNuevo(true); }}>
          Nuevo Presupuesto
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {cargando ? (
        <Box display="flex" justifyContent="center" p={4}><CircularProgress /></Box>
      ) : (
        <DataGrid
          rows={presupuestos}
          columns={columnasPresupuesto}
          getRowId={r => r.id_presupuesto}
          slots={{ toolbar: GridToolbar }}
          autoHeight density="compact"
          initialState={{ pagination: { paginationModel: { pageSize: 10 } } }}
          pageSizeOptions={[10, 25]}
        />
      )}

      {/* Dialog Nuevo Presupuesto */}
      <Dialog open={abrirNuevo} onClose={() => setAbrirNuevo(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Nuevo Presupuesto Anual</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid size={4}>
              <TextField fullWidth label="Año Fiscal" type="number" size="small"
                value={formulario.anio_fiscal}
                onChange={e => setFormulario(f => ({ ...f, anio_fiscal: Number(e.target.value) }))} />
            </Grid>
            <Grid size={8}>
              <TextField fullWidth label="Denominación" size="small" required
                value={formulario.denominacion}
                onChange={e => setFormulario(f => ({ ...f, denominacion: e.target.value }))} />
            </Grid>
            <Grid size={6}>
              <TextField fullWidth label="Monto Inicial" type="number" size="small"
                value={formulario.monto_inicial || 0}
                onChange={e => setFormulario(f => ({ ...f, monto_inicial: Number(e.target.value) }))} />
            </Grid>
          </Grid>
          {errorForm && <Alert severity="error" sx={{ mt: 2 }}>{errorForm}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevo(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleCrearPresupuesto} disabled={guardando}>
            {guardando ? <CircularProgress size={20} /> : 'Crear'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog Asignaciones */}
      <Dialog open={abrirAsignaciones} onClose={() => setAbrirAsignaciones(false)} maxWidth="lg" fullWidth>
        <DialogTitle>
          Asignaciones — Presupuesto {presupuestoSeleccionado?.anio_fiscal}: {presupuestoSeleccionado?.denominacion}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mb: 2 }}>
            <Button variant="outlined" startIcon={<IconPlus />} onClick={() => { setErrorAsig(null); setFormularioAsig({ id_presupuesto: 0, id_partida: 0, monto_inicial: 0 }); setAbrirNuevaAsig(true); }}>
              Agregar Asignación
            </Button>
          </Box>
          {cargandoAsig ? (
            <Box display="flex" justifyContent="center" p={4}><CircularProgress /></Box>
          ) : (
            <DataGrid
              rows={asignaciones}
              columns={columnasAsignacion}
              getRowId={r => r.id_asignacion}
              autoHeight density="compact"
              initialState={{ pagination: { paginationModel: { pageSize: 15 } } }}
              pageSizeOptions={[15, 30]}
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirAsignaciones(false)}>Cerrar</Button>
        </DialogActions>
      </Dialog>

      {/* Dialog Nueva Asignación */}
      <Dialog open={abrirNuevaAsig} onClose={() => setAbrirNuevaAsig(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Nueva Asignación Presupuestaria</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid size={12}>
              <TextField fullWidth label="Buscar Partida (ID)" type="number" size="small"
                value={formularioAsig.id_partida || ''}
                onChange={e => setFormularioAsig(f => ({ ...f, id_partida: Number(e.target.value) }))}
                helperText="Ingrese el ID de la partida presupuestaria hoja"
              />
            </Grid>
            <Grid size={6}>
              <TextField fullWidth label="Monto Inicial" type="number" size="small"
                value={formularioAsig.monto_inicial || 0}
                onChange={e => setFormularioAsig(f => ({ ...f, monto_inicial: Number(e.target.value) }))} />
            </Grid>
          </Grid>
          {errorAsig && <Alert severity="error" sx={{ mt: 2 }}>{errorAsig}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevaAsig(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleCrearAsignacion} disabled={guardandoAsig}>
            {guardandoAsig ? <CircularProgress size={20} /> : 'Crear'}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default PresupuestosPage;
