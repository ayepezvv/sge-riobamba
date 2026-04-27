'use client';

import { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, Divider, FormControl, Grid, IconButton,
  InputLabel, MenuItem, Select, Table, TableBody, TableCell, TableHead,
  TableRow, TextField, Typography
} from '@mui/material';
import { DataGrid, GridActionsCellItem, GridColDef, GridRowParams, GridToolbar } from '@mui/x-data-grid';
import { IconPlus, IconEye, IconCheck, IconX, IconTrash } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import {
  listarAsientos, obtenerAsiento, crearAsiento, publicarAsiento, anularAsiento,
  listarDiarios, listarPeriodos, listarCuentas,
} from 'api/contabilidad';
import {
  AsientoContable, AsientoContableCrear, Diario, PeriodoContable,
  CuentaContable, LineaAsientoCrear,
} from 'types/contabilidad';

const ESTADO_COLOR: Record<string, 'default' | 'warning' | 'success' | 'error'> = {
  BORRADOR: 'warning', PUBLICADO: 'success', ANULADO: 'error',
};

const LINEA_VACIA: LineaAsientoCrear = { cuenta_id: 0, descripcion: '', debe: 0, haber: 0, orden: 1 };

const AsientosContablesPage = () => {
  const [asientos, setAsientos] = useState<AsientoContable[]>([]);
  const [diarios, setDiarios] = useState<Diario[]>([]);
  const [periodos, setPeriodos] = useState<PeriodoContable[]>([]);
  const [cuentas, setCuentas] = useState<CuentaContable[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filtros
  const [filtroPeriodo, setFiltroPeriodo] = useState<number | ''>('');
  const [filtroEstado, setFiltroEstado] = useState('');

  // Modal detalle
  const [asientoDetalle, setAsientoDetalle] = useState<AsientoContable | null>(null);
  const [abrirDetalle, setAbrirDetalle] = useState(false);

  // Modal anular
  const [abrirAnular, setAbrirAnular] = useState(false);
  const [idAnular, setIdAnular] = useState<number | null>(null);
  const [motivoAnulacion, setMotivoAnulacion] = useState('');
  const [anulando, setAnulando] = useState(false);

  // Modal nuevo asiento
  const [abrirNuevo, setAbrirNuevo] = useState(false);
  const [formulario, setFormulario] = useState<AsientoContableCrear>({
    diario_id: 0, periodo_id: 0, fecha: '', referencia: '', concepto: '', lineas: [
      { ...LINEA_VACIA, orden: 1 },
      { ...LINEA_VACIA, orden: 2 },
    ],
  });
  const [guardando, setGuardando] = useState(false);
  const [errorFormulario, setErrorFormulario] = useState<string | null>(null);

  const totalDebe = formulario.lineas.reduce((s, l) => s + Number(l.debe || 0), 0);
  const totalHaber = formulario.lineas.reduce((s, l) => s + Number(l.haber || 0), 0);
  const asientoCuadrado = totalDebe > 0 && totalDebe === totalHaber;

  const cargarDatos = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const params: any = {};
      if (filtroPeriodo) params.periodo_id = filtroPeriodo;
      if (filtroEstado) params.estado = filtroEstado;

      const [resAsientos, resDiarios, resPeriodos, resCuentas] = await Promise.all([
        listarAsientos(params),
        listarDiarios(),
        listarPeriodos(),
        listarCuentas({ estado: 'ACTIVA' }),
      ]);
      setAsientos(resAsientos);
      setDiarios(resDiarios);
      setPeriodos(resPeriodos);
      setCuentas(resCuentas.filter(c => c.permite_movimientos));
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar los asientos');
    } finally {
      setCargando(false);
    }
  }, [filtroPeriodo, filtroEstado]);

  useEffect(() => { cargarDatos(); }, [cargarDatos]);

  const verDetalle = async (id: number) => {
    try {
      const asiento = await obtenerAsiento(id);
      setAsientoDetalle(asiento);
      setAbrirDetalle(true);
    } catch {
      setError('Error al obtener el detalle del asiento');
    }
  };

  const handlePublicar = async (id: number) => {
    if (!confirm('¿Publicar este asiento? Esta acción es irreversible.')) return;
    try {
      await publicarAsiento(id);
      await cargarDatos();
    } catch (err: any) {
      setError(err?.detail || 'Error al publicar el asiento');
    }
  };

  const confirmarAnular = (id: number) => {
    setIdAnular(id);
    setMotivoAnulacion('');
    setAbrirAnular(true);
  };

  const handleAnular = async () => {
    if (!idAnular || motivoAnulacion.length < 10) {
      setError('El motivo de anulación debe tener al menos 10 caracteres.');
      return;
    }
    setAnulando(true);
    try {
      await anularAsiento(idAnular, motivoAnulacion);
      setAbrirAnular(false);
      await cargarDatos();
    } catch (err: any) {
      setError(err?.detail || 'Error al anular el asiento');
    } finally {
      setAnulando(false);
    }
  };

  const agregarLinea = () => {
    setFormulario(f => ({
      ...f,
      lineas: [...f.lineas, { ...LINEA_VACIA, orden: f.lineas.length + 1 }],
    }));
  };

  const quitarLinea = (idx: number) => {
    setFormulario(f => ({
      ...f,
      lineas: f.lineas.filter((_, i) => i !== idx).map((l, i) => ({ ...l, orden: i + 1 })),
    }));
  };

  const actualizarLinea = (idx: number, campo: keyof LineaAsientoCrear, valor: any) => {
    setFormulario(f => {
      const lineas = [...f.lineas];
      lineas[idx] = { ...lineas[idx], [campo]: valor };
      // Si se pone debe, limpiar haber y viceversa
      if (campo === 'debe' && Number(valor) > 0) lineas[idx].haber = 0;
      if (campo === 'haber' && Number(valor) > 0) lineas[idx].debe = 0;
      return { ...f, lineas };
    });
  };

  const handleGuardar = async () => {
    if (!formulario.diario_id || !formulario.periodo_id || !formulario.fecha || !formulario.concepto) {
      setErrorFormulario('Diario, Período, Fecha y Concepto son obligatorios.');
      return;
    }
    if (!asientoCuadrado) {
      setErrorFormulario(`El asiento no cuadra: Debe ${totalDebe.toFixed(2)} ≠ Haber ${totalHaber.toFixed(2)}`);
      return;
    }
    const lineasInvalidas = formulario.lineas.filter(l => !l.cuenta_id);
    if (lineasInvalidas.length > 0) {
      setErrorFormulario('Todas las líneas deben tener una cuenta asignada.');
      return;
    }
    setGuardando(true);
    setErrorFormulario(null);
    try {
      await crearAsiento(formulario);
      setAbrirNuevo(false);
      setFormulario({
        diario_id: 0, periodo_id: 0, fecha: '', referencia: '', concepto: '',
        lineas: [{ ...LINEA_VACIA, orden: 1 }, { ...LINEA_VACIA, orden: 2 }],
      });
      await cargarDatos();
    } catch (err: any) {
      setErrorFormulario(err?.detail || err?.message || 'Error al crear el asiento');
    } finally {
      setGuardando(false);
    }
  };

  const columnas: GridColDef[] = [
    { field: 'numero', headerName: 'N° Asiento', width: 130, renderCell: p => <Typography variant="body2" fontFamily="monospace" fontWeight={700}>{p.value}</Typography> },
    { field: 'fecha', headerName: 'Fecha', width: 110 },
    {
      field: 'diario_id', headerName: 'Diario', width: 130,
      valueGetter: (p: any) => diarios.find(d => d.id === p.row.diario_id)?.nombre ?? '—',
    },
    { field: 'concepto', headerName: 'Concepto', flex: 1, minWidth: 200 },
    {
      field: 'total_debe', headerName: 'Debe', width: 120, type: 'number',
      valueFormatter: (p: any) => Number(p.value).toFixed(2),
    },
    {
      field: 'total_haber', headerName: 'Haber', width: 120, type: 'number',
      valueFormatter: (p: any) => Number(p.value).toFixed(2),
    },
    {
      field: 'estado', headerName: 'Estado', width: 110,
      renderCell: p => <Chip label={p.value} color={ESTADO_COLOR[p.value] ?? 'default'} size="small" variant="outlined" />,
    },
    {
      field: 'acciones', type: 'actions', headerName: '', width: 100,
      getActions: (params: GridRowParams) => {
        const actions = [
          <GridActionsCellItem key="ver" icon={<IconEye size={18} />} label="Ver detalle" onClick={() => verDetalle(params.row.id)} />,
        ];
        if (params.row.estado === 'BORRADOR') {
          actions.push(
            <GridActionsCellItem key="publicar" icon={<IconCheck size={18} />} label="Publicar" onClick={() => handlePublicar(params.row.id)} showInMenu />,
            <GridActionsCellItem key="anular" icon={<IconX size={18} />} label="Anular" onClick={() => confirmarAnular(params.row.id)} showInMenu />,
          );
        }
        return actions;
      },
    },
  ];

  return (
    <MainCard
      title="Asientos Contables"
      secondary={
        <Button variant="contained" startIcon={<IconPlus size={18} />} onClick={() => setAbrirNuevo(true)}>
          Nuevo Asiento
        </Button>
      }
    >
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      {/* ── Filtros ── */}
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid size={{ xs: 12, md: 4 }}>
          <FormControl fullWidth size="small">
            <InputLabel>Filtrar por Período</InputLabel>
            <Select value={filtroPeriodo} label="Filtrar por Período" onChange={e => setFiltroPeriodo(e.target.value as number | '')}>
              <MenuItem value="">Todos</MenuItem>
              {periodos.map(p => <MenuItem key={p.id} value={p.id}>{p.nombre}</MenuItem>)}
            </Select>
          </FormControl>
        </Grid>
        <Grid size={{ xs: 12, md: 3 }}>
          <FormControl fullWidth size="small">
            <InputLabel>Estado</InputLabel>
            <Select value={filtroEstado} label="Estado" onChange={e => setFiltroEstado(e.target.value)}>
              <MenuItem value="">Todos</MenuItem>
              <MenuItem value="BORRADOR">BORRADOR</MenuItem>
              <MenuItem value="PUBLICADO">PUBLICADO</MenuItem>
              <MenuItem value="ANULADO">ANULADO</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={asientos}
          columns={columnas}
          loading={cargando}
          pageSizeOptions={[25, 50]}
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

      {/* ── Modal: Detalle Asiento ── */}
      <Dialog open={abrirDetalle} onClose={() => setAbrirDetalle(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Asiento N° {asientoDetalle?.numero}
          <Chip label={asientoDetalle?.estado} color={ESTADO_COLOR[asientoDetalle?.estado ?? ''] ?? 'default'} size="small" sx={{ ml: 2 }} />
        </DialogTitle>
        <DialogContent dividers>
          {asientoDetalle && (
            <>
              <Grid container spacing={1} sx={{ mb: 2 }}>
                <Grid size={{ xs: 6, md: 3 }}><Typography variant="caption" color="textSecondary">Fecha</Typography><Typography>{asientoDetalle.fecha}</Typography></Grid>
                <Grid size={{ xs: 6, md: 3 }}><Typography variant="caption" color="textSecondary">Diario</Typography><Typography>{diarios.find(d => d.id === asientoDetalle.diario_id)?.nombre ?? '—'}</Typography></Grid>
                <Grid size={{ xs: 12, md: 6 }}><Typography variant="caption" color="textSecondary">Concepto</Typography><Typography>{asientoDetalle.concepto}</Typography></Grid>
                {asientoDetalle.referencia && <Grid size={12}><Typography variant="caption" color="textSecondary">Referencia</Typography><Typography>{asientoDetalle.referencia}</Typography></Grid>}
                {asientoDetalle.motivo_anulacion && <Grid size={12}><Alert severity="error">Motivo de anulación: {asientoDetalle.motivo_anulacion}</Alert></Grid>}
              </Grid>
              <Table size="small">
                <TableHead>
                  <TableRow sx={{ bgcolor: '#f8fafc' }}>
                    <TableCell>Cuenta</TableCell>
                    <TableCell>Descripción</TableCell>
                    <TableCell align="right">Debe</TableCell>
                    <TableCell align="right">Haber</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {asientoDetalle.lineas.map(l => (
                    <TableRow key={l.id}>
                      <TableCell><Typography variant="body2" fontFamily="monospace">{cuentas.find(c => c.id === l.cuenta_id)?.codigo ?? l.cuenta_id} — {cuentas.find(c => c.id === l.cuenta_id)?.nombre ?? ''}</Typography></TableCell>
                      <TableCell>{l.descripcion}</TableCell>
                      <TableCell align="right">{l.debe > 0 ? Number(l.debe).toFixed(2) : ''}</TableCell>
                      <TableCell align="right">{l.haber > 0 ? Number(l.haber).toFixed(2) : ''}</TableCell>
                    </TableRow>
                  ))}
                  <TableRow sx={{ bgcolor: '#f0f4ff' }}>
                    <TableCell colSpan={2}><Typography fontWeight={700}>TOTALES</Typography></TableCell>
                    <TableCell align="right"><Typography fontWeight={700}>{Number(asientoDetalle.total_debe).toFixed(2)}</Typography></TableCell>
                    <TableCell align="right"><Typography fontWeight={700}>{Number(asientoDetalle.total_haber).toFixed(2)}</Typography></TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirDetalle(false)} color="inherit">Cerrar</Button>
        </DialogActions>
      </Dialog>

      {/* ── Modal: Anular Asiento ── */}
      <Dialog open={abrirAnular} onClose={() => setAbrirAnular(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Anular Asiento</DialogTitle>
        <DialogContent dividers>
          <TextField
            label="Motivo de anulación (mínimo 10 caracteres) *"
            fullWidth multiline rows={3}
            value={motivoAnulacion}
            onChange={e => setMotivoAnulacion(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirAnular(false)} color="inherit">Cancelar</Button>
          <Button onClick={handleAnular} color="error" variant="contained" disabled={anulando || motivoAnulacion.length < 10}
            startIcon={anulando ? <CircularProgress size={16} /> : undefined}>
            {anulando ? 'Anulando...' : 'Confirmar Anulación'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* ── Modal: Nuevo Asiento ── */}
      <Dialog open={abrirNuevo} onClose={() => setAbrirNuevo(false)} maxWidth="lg" fullWidth>
        <DialogTitle>Nuevo Asiento Contable</DialogTitle>
        <DialogContent dividers>
          {errorFormulario && <Alert severity="error" sx={{ mb: 2 }}>{errorFormulario}</Alert>}
          <Grid container spacing={2} sx={{ pt: 1, mb: 2 }}>
            <Grid size={{ xs: 12, md: 3 }}>
              <FormControl fullWidth>
                <InputLabel>Diario *</InputLabel>
                <Select value={formulario.diario_id || ''} label="Diario *"
                  onChange={e => setFormulario({ ...formulario, diario_id: Number(e.target.value) })}>
                  {diarios.filter(d => d.es_activo).map(d => <MenuItem key={d.id} value={d.id}>{d.nombre}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, md: 3 }}>
              <FormControl fullWidth>
                <InputLabel>Período *</InputLabel>
                <Select value={formulario.periodo_id || ''} label="Período *"
                  onChange={e => setFormulario({ ...formulario, periodo_id: Number(e.target.value) })}>
                  {periodos.filter(p => p.estado === 'ABIERTO').map(p => <MenuItem key={p.id} value={p.id}>{p.nombre}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, md: 3 }}>
              <TextField label="Fecha *" type="date" fullWidth InputLabelProps={{ shrink: true }}
                value={formulario.fecha}
                onChange={e => setFormulario({ ...formulario, fecha: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 12, md: 3 }}>
              <TextField label="Referencia" fullWidth value={formulario.referencia}
                onChange={e => setFormulario({ ...formulario, referencia: e.target.value })} />
            </Grid>
            <Grid size={12}>
              <TextField label="Concepto *" fullWidth value={formulario.concepto}
                onChange={e => setFormulario({ ...formulario, concepto: e.target.value })} />
            </Grid>
          </Grid>
          <Divider sx={{ mb: 2 }} />
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
            <Typography variant="subtitle2">Líneas del Asiento</Typography>
            <Box>
              <Chip
                label={asientoCuadrado ? `✓ CUADRADO (${totalDebe.toFixed(2)})` : `Debe: ${totalDebe.toFixed(2)} | Haber: ${totalHaber.toFixed(2)}`}
                color={asientoCuadrado ? 'success' : 'warning'}
                size="small"
                sx={{ mr: 1 }}
              />
              <Button size="small" startIcon={<IconPlus size={16} />} onClick={agregarLinea}>Agregar línea</Button>
            </Box>
          </Box>
          <Table size="small">
            <TableHead>
              <TableRow sx={{ bgcolor: '#f8fafc' }}>
                <TableCell width="40%">Cuenta</TableCell>
                <TableCell>Descripción</TableCell>
                <TableCell align="right" width="130">Debe</TableCell>
                <TableCell align="right" width="130">Haber</TableCell>
                <TableCell width="50" />
              </TableRow>
            </TableHead>
            <TableBody>
              {formulario.lineas.map((linea, idx) => (
                <TableRow key={idx}>
                  <TableCell>
                    <FormControl fullWidth size="small">
                      <Select value={linea.cuenta_id || ''}
                        onChange={e => actualizarLinea(idx, 'cuenta_id', Number(e.target.value))}>
                        <MenuItem value=""><em>Seleccionar cuenta...</em></MenuItem>
                        {cuentas.map(c => <MenuItem key={c.id} value={c.id}>{c.codigo} — {c.nombre}</MenuItem>)}
                      </Select>
                    </FormControl>
                  </TableCell>
                  <TableCell>
                    <TextField size="small" fullWidth value={linea.descripcion}
                      onChange={e => actualizarLinea(idx, 'descripcion', e.target.value)} />
                  </TableCell>
                  <TableCell align="right">
                    <TextField size="small" type="number" inputProps={{ min: 0, step: '0.01', style: { textAlign: 'right' } }}
                      value={linea.debe || ''}
                      onChange={e => actualizarLinea(idx, 'debe', parseFloat(e.target.value) || 0)} />
                  </TableCell>
                  <TableCell align="right">
                    <TextField size="small" type="number" inputProps={{ min: 0, step: '0.01', style: { textAlign: 'right' } }}
                      value={linea.haber || ''}
                      onChange={e => actualizarLinea(idx, 'haber', parseFloat(e.target.value) || 0)} />
                  </TableCell>
                  <TableCell>
                    {formulario.lineas.length > 2 && (
                      <IconButton size="small" color="error" onClick={() => quitarLinea(idx)}>
                        <IconTrash size={16} />
                      </IconButton>
                    )}
                  </TableCell>
                </TableRow>
              ))}
              <TableRow sx={{ bgcolor: '#f8fafc' }}>
                <TableCell colSpan={2}><Typography variant="subtitle2" align="right">TOTALES</Typography></TableCell>
                <TableCell align="right"><Typography fontWeight={700}>{totalDebe.toFixed(2)}</Typography></TableCell>
                <TableCell align="right"><Typography fontWeight={700}>{totalHaber.toFixed(2)}</Typography></TableCell>
                <TableCell />
              </TableRow>
            </TableBody>
          </Table>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevo(false)} color="inherit">Cancelar</Button>
          <Button onClick={handleGuardar} variant="contained" disabled={guardando || !asientoCuadrado}
            startIcon={guardando ? <CircularProgress size={16} /> : undefined}>
            {guardando ? 'Guardando...' : 'Crear Asiento (Borrador)'}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default AsientosContablesPage;
