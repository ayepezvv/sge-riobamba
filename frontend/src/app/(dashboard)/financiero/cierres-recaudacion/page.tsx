'use client';

import { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, Grid, TextField, Typography
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem, GridRowParams } from '@mui/x-data-grid';
import { IconPlus, IconEye } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { listarCierresRecaudacion, obtenerCierreRecaudacion, crearCierreRecaudacion } from 'api/financiero';
import { CierreRecaudacion, CierreRecaudacionCrear } from 'types/financiero';

const CierresRecaudacionPage = () => {
  const [cierres, setCierres] = useState<CierreRecaudacion[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [detalleId, setDetalleId] = useState<CierreRecaudacion | null>(null);
  const [abrirDetalle, setAbrirDetalle] = useState(false);

  const [abrirNuevo, setAbrirNuevo] = useState(false);
  const [formulario, setFormulario] = useState<CierreRecaudacionCrear>({
    fecha: new Date().toISOString().split('T')[0],
    total_recaudado: 0,
    numero_transacciones: 0,
    observaciones: '',
  });
  const [guardando, setGuardando] = useState(false);
  const [errorFormulario, setErrorFormulario] = useState<string | null>(null);

  const cargarDatos = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const res = await listarCierresRecaudacion();
      setCierres(res);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar datos');
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => { cargarDatos(); }, [cargarDatos]);

  const verDetalle = async (id: number) => {
    try {
      const c = await obtenerCierreRecaudacion(id);
      setDetalleId(c);
      setAbrirDetalle(true);
    } catch {
      setError('Error al obtener el detalle del cierre');
    }
  };

  const handleGuardar = async () => {
    if (!formulario.fecha || !formulario.total_recaudado) {
      setErrorFormulario('Fecha y total recaudado son obligatorios.');
      return;
    }
    setGuardando(true);
    setErrorFormulario(null);
    try {
      await crearCierreRecaudacion(formulario);
      setAbrirNuevo(false);
      setFormulario({ fecha: new Date().toISOString().split('T')[0], total_recaudado: 0, numero_transacciones: 0, observaciones: '' });
      await cargarDatos();
    } catch (err: any) {
      setErrorFormulario(err?.detail || err?.message || 'Error al crear el cierre');
    } finally {
      setGuardando(false);
    }
  };

  const columnas: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'fecha', headerName: 'Fecha', width: 120 },
    {
      field: 'total_recaudado', headerName: 'Total Recaudado', width: 150, type: 'number',
      valueFormatter: (p: any) => Number(p.value).toFixed(2),
      renderCell: p => <Typography fontWeight={700} color="success.main">{Number(p.value).toFixed(2)}</Typography>,
    },
    { field: 'numero_transacciones', headerName: 'N° Transacciones', width: 150, type: 'number' },
    { field: 'observaciones', headerName: 'Observaciones', flex: 1, minWidth: 200 },
    {
      field: 'asiento_recaudacion_id', headerName: 'Asiento Rec.', width: 120,
      renderCell: p => p.value ? <Typography variant="body2" color="success.main">#{p.value}</Typography> : '—',
    },
    {
      field: 'asiento_traslado_bce_id', headerName: 'Asiento BCE', width: 120,
      renderCell: p => p.value ? <Typography variant="body2" color="success.main">#{p.value}</Typography> : '—',
    },
    {
      field: 'acciones', type: 'actions', headerName: '', width: 60,
      getActions: (params: GridRowParams) => [
        <GridActionsCellItem key="ver" icon={<IconEye size={18} />} label="Ver detalle" onClick={() => verDetalle(params.row.id)} />,
      ],
    },
  ];

  return (
    <MainCard
      title="Cierres de Recaudación"
      secondary={
        <Button variant="contained" startIcon={<IconPlus size={18} />} onClick={() => setAbrirNuevo(true)}>
          Nuevo Cierre
        </Button>
      }
    >
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Box sx={{ height: 500, width: '100%' }}>
        <DataGrid rows={cierres} columns={columnas} loading={cargando}
          pageSizeOptions={[25, 50]} slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { showQuickFilter: true } }}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          disableRowSelectionOnClick
          sx={{ border: 'none', '& .MuiDataGrid-columnHeaders': { backgroundColor: '#f8fafc', fontWeight: 700 } }}
        />
      </Box>

      {/* Modal Detalle */}
      <Dialog open={abrirDetalle} onClose={() => setAbrirDetalle(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Cierre de Recaudación — {detalleId?.fecha}</DialogTitle>
        <DialogContent dividers>
          {detalleId && (
            <Grid container spacing={2}>
              <Grid size={6}><Typography variant="caption" color="textSecondary">Fecha</Typography><Typography fontWeight={700}>{detalleId.fecha}</Typography></Grid>
              <Grid size={6}><Typography variant="caption" color="textSecondary">N° Transacciones</Typography><Typography fontWeight={700}>{detalleId.numero_transacciones}</Typography></Grid>
              <Grid size={12}><Typography variant="caption" color="textSecondary">Total Recaudado</Typography><Typography variant="h4" color="success.main">{Number(detalleId.total_recaudado).toFixed(2)} USD</Typography></Grid>
              {detalleId.observaciones && <Grid size={12}><Typography variant="caption" color="textSecondary">Observaciones</Typography><Typography>{detalleId.observaciones}</Typography></Grid>}
              <Grid size={6}><Typography variant="caption" color="textSecondary">Asiento Recaudación</Typography><Typography>{detalleId.asiento_recaudacion_id ? `#${detalleId.asiento_recaudacion_id}` : 'Pendiente'}</Typography></Grid>
              <Grid size={6}><Typography variant="caption" color="textSecondary">Asiento Traslado BCE</Typography><Typography>{detalleId.asiento_traslado_bce_id ? `#${detalleId.asiento_traslado_bce_id}` : 'Pendiente'}</Typography></Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions><Button onClick={() => setAbrirDetalle(false)} color="inherit">Cerrar</Button></DialogActions>
      </Dialog>

      {/* Modal Nuevo Cierre */}
      <Dialog open={abrirNuevo} onClose={() => setAbrirNuevo(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Nuevo Cierre de Recaudación</DialogTitle>
        <DialogContent dividers>
          {errorFormulario && <Alert severity="error" sx={{ mb: 2 }}>{errorFormulario}</Alert>}
          <Grid container spacing={2} sx={{ pt: 1 }}>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField label="Fecha *" type="date" fullWidth InputLabelProps={{ shrink: true }}
                value={formulario.fecha} onChange={e => setFormulario({ ...formulario, fecha: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField label="Total Recaudado *" type="number" fullWidth value={formulario.total_recaudado}
                onChange={e => setFormulario({ ...formulario, total_recaudado: parseFloat(e.target.value) || 0 })} />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField label="N° Transacciones" type="number" fullWidth value={formulario.numero_transacciones}
                onChange={e => setFormulario({ ...formulario, numero_transacciones: parseInt(e.target.value) || 0 })} />
            </Grid>
            <Grid size={12}>
              <TextField label="Observaciones" multiline rows={2} fullWidth value={formulario.observaciones || ''}
                onChange={e => setFormulario({ ...formulario, observaciones: e.target.value })} />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevo(false)} color="inherit">Cancelar</Button>
          <Button onClick={handleGuardar} variant="contained" disabled={guardando}
            startIcon={guardando ? <CircularProgress size={16} /> : undefined}>
            {guardando ? 'Procesando...' : 'Registrar Cierre'}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default CierresRecaudacionPage;
