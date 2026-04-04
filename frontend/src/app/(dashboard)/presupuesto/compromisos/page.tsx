'use client';

import React, { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, Grid, Tab, Tabs, TextField, Typography
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem } from '@mui/x-data-grid';
import { IconPlus, IconBan } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { listarCompromisos, crearCompromiso, anularCompromiso, listarDevengados, crearDevengado } from 'api/presupuesto';
import { Compromiso, CompromisoCrear, Devengado, DevengadoCrear } from 'types/presupuesto';

const formatMonto = (v: number) =>
  new Intl.NumberFormat('es-EC', { style: 'currency', currency: 'USD' }).format(v);

const COLOR_ESTADO: Record<string, 'default' | 'warning' | 'success' | 'error' | 'info'> = {
  ACTIVO: 'success', ANULADO: 'error', DEVENGADO: 'info',
};

const CompromisosPage = () => {
  const [pestana, setPestana] = useState(0);

  // Compromisos
  const [compromisos, setCompromisos] = useState<Compromiso[]>([]);
  const [cargandoComp, setCargandoComp] = useState(true);
  const [errorComp, setErrorComp] = useState<string | null>(null);
  const [abrirNuevoComp, setAbrirNuevoComp] = useState(false);
  const [formularioComp, setFormularioComp] = useState<CompromisoCrear>({
    id_certificado: 0, numero_compromiso: '', monto_comprometido: 0,
    concepto: '', fecha_compromiso: new Date().toISOString().split('T')[0],
  });
  const [guardandoComp, setGuardandoComp] = useState(false);
  const [errorFormComp, setErrorFormComp] = useState<string | null>(null);
  const [abrirAnular, setAbrirAnular] = useState(false);
  const [compAnular, setCompAnular] = useState<Compromiso | null>(null);
  const [motivoAnulacion, setMotivoAnulacion] = useState('');
  const [guardandoAnular, setGuardandoAnular] = useState(false);
  const [errorAnular, setErrorAnular] = useState<string | null>(null);

  // Devengados
  const [devengados, setDevengados] = useState<Devengado[]>([]);
  const [cargandoDev, setCargandoDev] = useState(true);
  const [errorDev, setErrorDev] = useState<string | null>(null);
  const [abrirNuevoDev, setAbrirNuevoDev] = useState(false);
  const [formularioDev, setFormularioDev] = useState<DevengadoCrear>({
    id_compromiso: 0, numero_devengado: '', monto_devengado: 0,
    concepto: '', fecha_devengado: new Date().toISOString().split('T')[0],
  });
  const [guardandoDev, setGuardandoDev] = useState(false);
  const [errorFormDev, setErrorFormDev] = useState<string | null>(null);

  const cargarCompromisos = useCallback(async () => {
    setCargandoComp(true);
    setErrorComp(null);
    try {
      setCompromisos(await listarCompromisos());
    } catch (err: any) {
      setErrorComp(err?.message || 'Error');
    } finally {
      setCargandoComp(false);
    }
  }, []);

  const cargarDevengados = useCallback(async () => {
    setCargandoDev(true);
    setErrorDev(null);
    try {
      setDevengados(await listarDevengados());
    } catch (err: any) {
      setErrorDev(err?.message || 'Error');
    } finally {
      setCargandoDev(false);
    }
  }, []);

  useEffect(() => { cargarCompromisos(); cargarDevengados(); }, [cargarCompromisos, cargarDevengados]);

  const handleCrearCompromiso = async () => {
    if (!formularioComp.id_certificado || !formularioComp.numero_compromiso || !formularioComp.monto_comprometido) {
      setErrorFormComp('ID certificado, número y monto son obligatorios.');
      return;
    }
    setGuardandoComp(true);
    setErrorFormComp(null);
    try {
      await crearCompromiso(formularioComp);
      setAbrirNuevoComp(false);
      cargarCompromisos();
    } catch (err: any) {
      setErrorFormComp(err?.response?.data?.detail || err?.message || 'Error');
    } finally {
      setGuardandoComp(false);
    }
  };

  const handleAnularCompromiso = async () => {
    if (!motivoAnulacion) { setErrorAnular('El motivo es obligatorio.'); return; }
    setGuardandoAnular(true);
    setErrorAnular(null);
    try {
      await anularCompromiso(compAnular!.id_compromiso, motivoAnulacion);
      setAbrirAnular(false);
      cargarCompromisos();
    } catch (err: any) {
      setErrorAnular(err?.response?.data?.detail || err?.message || 'Error');
    } finally {
      setGuardandoAnular(false);
    }
  };

  const handleCrearDevengado = async () => {
    if (!formularioDev.id_compromiso || !formularioDev.numero_devengado || !formularioDev.monto_devengado) {
      setErrorFormDev('ID compromiso, número y monto son obligatorios.');
      return;
    }
    setGuardandoDev(true);
    setErrorFormDev(null);
    try {
      await crearDevengado(formularioDev);
      setAbrirNuevoDev(false);
      cargarDevengados();
      cargarCompromisos();
    } catch (err: any) {
      setErrorFormDev(err?.response?.data?.detail || err?.message || 'Error');
    } finally {
      setGuardandoDev(false);
    }
  };

  const columnasCompromiso: GridColDef[] = [
    { field: 'numero_compromiso', headerName: 'Número', width: 160 },
    { field: 'id_certificado', headerName: 'Certificado', width: 100 },
    { field: 'concepto', headerName: 'Concepto', flex: 1 },
    { field: 'monto_comprometido', headerName: 'Monto', width: 140, renderCell: ({ value }) => formatMonto(value) },
    { field: 'fecha_compromiso', headerName: 'Fecha', width: 120 },
    {
      field: 'estado', headerName: 'Estado', width: 110,
      renderCell: ({ value }) => <Chip label={value} size="small" color={COLOR_ESTADO[value] || 'default'} />,
    },
    {
      field: 'acciones', type: 'actions', headerName: 'Anular', width: 80,
      getActions: ({ row }) => {
        const comp = row as Compromiso;
        if (comp.estado !== 'ACTIVO') return [];
        return [
          <GridActionsCellItem key="anular" icon={<IconBan size={18} />} label="Anular"
            onClick={() => { setCompAnular(comp); setMotivoAnulacion(''); setErrorAnular(null); setAbrirAnular(true); }} />,
        ];
      },
    },
  ];

  const columnasDevengado: GridColDef[] = [
    { field: 'numero_devengado', headerName: 'Número', width: 160 },
    { field: 'id_compromiso', headerName: 'Compromiso', width: 110 },
    { field: 'concepto', headerName: 'Concepto', flex: 1 },
    { field: 'monto_devengado', headerName: 'Monto', width: 140, renderCell: ({ value }) => formatMonto(value) },
    { field: 'fecha_devengado', headerName: 'Fecha', width: 120 },
    {
      field: 'estado', headerName: 'Estado', width: 110,
      renderCell: ({ value }) => <Chip label={value} size="small" color={COLOR_ESTADO[value] || 'default'} />,
    },
  ];

  return (
    <MainCard title="Compromisos y Devengados">
      <Tabs value={pestana} onChange={(_, v) => setPestana(v)} sx={{ mb: 2 }}>
        <Tab label="Compromisos" />
        <Tab label="Devengados" />
      </Tabs>

      {pestana === 0 && (
        <>
          <Box sx={{ mb: 2 }}>
            <Button variant="contained" startIcon={<IconPlus />}
              onClick={() => { setErrorFormComp(null); setAbrirNuevoComp(true); }}>
              Nuevo Compromiso
            </Button>
          </Box>
          {errorComp && <Alert severity="error" sx={{ mb: 2 }}>{errorComp}</Alert>}
          {cargandoComp ? (
            <Box display="flex" justifyContent="center" p={4}><CircularProgress /></Box>
          ) : (
            <DataGrid rows={compromisos} columns={columnasCompromiso}
              getRowId={r => r.id_compromiso}
              slots={{ toolbar: GridToolbar }} slotProps={{ toolbar: { showQuickFilter: true } }}
              autoHeight density="compact"
              initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
              pageSizeOptions={[25, 50]} />
          )}
        </>
      )}

      {pestana === 1 && (
        <>
          <Box sx={{ mb: 2 }}>
            <Button variant="contained" startIcon={<IconPlus />}
              onClick={() => { setErrorFormDev(null); setAbrirNuevoDev(true); }}>
              Nuevo Devengado
            </Button>
          </Box>
          {errorDev && <Alert severity="error" sx={{ mb: 2 }}>{errorDev}</Alert>}
          {cargandoDev ? (
            <Box display="flex" justifyContent="center" p={4}><CircularProgress /></Box>
          ) : (
            <DataGrid rows={devengados} columns={columnasDevengado}
              getRowId={r => r.id_devengado}
              slots={{ toolbar: GridToolbar }} slotProps={{ toolbar: { showQuickFilter: true } }}
              autoHeight density="compact"
              initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
              pageSizeOptions={[25, 50]} />
          )}
        </>
      )}

      {/* Dialog Nuevo Compromiso */}
      <Dialog open={abrirNuevoComp} onClose={() => setAbrirNuevoComp(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Nuevo Compromiso</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid item xs={6}>
              <TextField fullWidth label="ID Certificado" type="number" size="small" required
                value={formularioComp.id_certificado || ''}
                onChange={e => setFormularioComp(f => ({ ...f, id_certificado: Number(e.target.value) }))} />
            </Grid>
            <Grid item xs={6}>
              <TextField fullWidth label="Número Compromiso" size="small" required
                value={formularioComp.numero_compromiso}
                onChange={e => setFormularioComp(f => ({ ...f, numero_compromiso: e.target.value }))} />
            </Grid>
            <Grid item xs={6}>
              <TextField fullWidth label="Monto Comprometido" type="number" size="small" required
                value={formularioComp.monto_comprometido || ''}
                onChange={e => setFormularioComp(f => ({ ...f, monto_comprometido: Number(e.target.value) }))} />
            </Grid>
            <Grid item xs={6}>
              <TextField fullWidth label="Fecha Compromiso" type="date" size="small"
                value={formularioComp.fecha_compromiso}
                onChange={e => setFormularioComp(f => ({ ...f, fecha_compromiso: e.target.value }))}
                InputLabelProps={{ shrink: true }} />
            </Grid>
            <Grid item xs={12}>
              <TextField fullWidth label="Concepto" size="small" required multiline rows={2}
                value={formularioComp.concepto}
                onChange={e => setFormularioComp(f => ({ ...f, concepto: e.target.value }))} />
            </Grid>
          </Grid>
          {errorFormComp && <Alert severity="error" sx={{ mt: 2 }}>{errorFormComp}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevoComp(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleCrearCompromiso} disabled={guardandoComp}>
            {guardandoComp ? <CircularProgress size={20} /> : 'Crear'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog Anular Compromiso */}
      <Dialog open={abrirAnular} onClose={() => setAbrirAnular(false)} maxWidth="xs" fullWidth>
        <DialogTitle>Anular Compromiso</DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Compromiso: <strong>{compAnular?.numero_compromiso}</strong>
          </Typography>
          <TextField fullWidth label="Motivo de Anulación" multiline rows={3} size="small" required
            value={motivoAnulacion} onChange={e => setMotivoAnulacion(e.target.value)} />
          {errorAnular && <Alert severity="error" sx={{ mt: 2 }}>{errorAnular}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirAnular(false)}>Cancelar</Button>
          <Button variant="contained" color="error" onClick={handleAnularCompromiso} disabled={guardandoAnular}>
            {guardandoAnular ? <CircularProgress size={20} /> : 'Anular'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog Nuevo Devengado */}
      <Dialog open={abrirNuevoDev} onClose={() => setAbrirNuevoDev(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Nuevo Devengado</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid item xs={6}>
              <TextField fullWidth label="ID Compromiso" type="number" size="small" required
                value={formularioDev.id_compromiso || ''}
                onChange={e => setFormularioDev(f => ({ ...f, id_compromiso: Number(e.target.value) }))} />
            </Grid>
            <Grid item xs={6}>
              <TextField fullWidth label="Número Devengado" size="small" required
                value={formularioDev.numero_devengado}
                onChange={e => setFormularioDev(f => ({ ...f, numero_devengado: e.target.value }))} />
            </Grid>
            <Grid item xs={6}>
              <TextField fullWidth label="Monto Devengado" type="number" size="small" required
                value={formularioDev.monto_devengado || ''}
                onChange={e => setFormularioDev(f => ({ ...f, monto_devengado: Number(e.target.value) }))} />
            </Grid>
            <Grid item xs={6}>
              <TextField fullWidth label="Fecha Devengado" type="date" size="small"
                value={formularioDev.fecha_devengado}
                onChange={e => setFormularioDev(f => ({ ...f, fecha_devengado: e.target.value }))}
                InputLabelProps={{ shrink: true }} />
            </Grid>
            <Grid item xs={12}>
              <TextField fullWidth label="Concepto" size="small" required multiline rows={2}
                value={formularioDev.concepto}
                onChange={e => setFormularioDev(f => ({ ...f, concepto: e.target.value }))} />
            </Grid>
          </Grid>
          {errorFormDev && <Alert severity="error" sx={{ mt: 2 }}>{errorFormDev}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevoDev(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleCrearDevengado} disabled={guardandoDev}>
            {guardandoDev ? <CircularProgress size={20} /> : 'Crear'}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default CompromisosPage;
