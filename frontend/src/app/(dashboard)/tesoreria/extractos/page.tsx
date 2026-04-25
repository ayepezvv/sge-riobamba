'use client';

import React, { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, FormControl, Grid, IconButton, InputLabel,
  MenuItem, Select, Table, TableBody, TableCell, TableHead, TableRow, TextField, Typography
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem, GridRowParams } from '@mui/x-data-grid';
import { IconPlus, IconEye, IconCheck, IconTrash } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { listarCuentasBancarias, listarExtractos, obtenerExtracto, crearExtracto, confirmarExtracto } from 'api/tesoreria';
import { CuentaBancaria, ExtractoBancario, ExtractoBancarioCrear, LineaExtractoCrear } from 'types/tesoreria';

const ESTADO_COLOR: Record<string, 'default' | 'warning' | 'success'> = {
  BORRADOR: 'warning', CONFIRMADO: 'success',
};

const LINEA_VACIA: LineaExtractoCrear = {
  fecha: '', tipo_transaccion: 'TRANSFERENCIA', referencia: '', descripcion: '', valor: 0,
};

const ExtractosPage = () => {
  const [extractos, setExtractos] = useState<ExtractoBancario[]>([]);
  const [cuentas, setCuentas] = useState<CuentaBancaria[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [filtroCuenta, setFiltroCuenta] = useState<number | ''>('');
  const [filtroEstado, setFiltroEstado] = useState('');

  const [detalleExtracto, setDetalleExtracto] = useState<ExtractoBancario | null>(null);
  const [abrirDetalle, setAbrirDetalle] = useState(false);

  const [abrirNuevo, setAbrirNuevo] = useState(false);
  const [formulario, setFormulario] = useState<ExtractoBancarioCrear>({
    cuenta_bancaria_id: 0, fecha_inicio: '', fecha_fin: '', saldo_inicial: 0, saldo_final: 0, lineas: [],
  });
  const [guardando, setGuardando] = useState(false);
  const [errorFormulario, setErrorFormulario] = useState<string | null>(null);

  const cargarDatos = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const params: any = {};
      if (filtroCuenta) params.cuenta_bancaria_id = filtroCuenta;
      if (filtroEstado) params.estado = filtroEstado;
      const [resExtractos, resCuentas] = await Promise.all([
        listarExtractos(params),
        listarCuentasBancarias({ solo_activas: false }),
      ]);
      setExtractos(resExtractos);
      setCuentas(resCuentas);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar los datos');
    } finally {
      setCargando(false);
    }
  }, [filtroCuenta, filtroEstado]);

  useEffect(() => { cargarDatos(); }, [cargarDatos]);

  const verDetalle = async (id: number) => {
    try {
      const ext = await obtenerExtracto(id);
      setDetalleExtracto(ext);
      setAbrirDetalle(true);
    } catch {
      setError('Error al obtener el detalle del extracto');
    }
  };

  const handleConfirmar = async (id: number) => {
    if (!confirm('¿Confirmar este extracto? No podrá modificarse.')) return;
    try {
      await confirmarExtracto(id);
      await cargarDatos();
    } catch (err: any) {
      setError(err?.detail || 'Error al confirmar el extracto');
    }
  };

  const agregarLinea = () => {
    setFormulario(f => ({ ...f, lineas: [...(f.lineas || []), { ...LINEA_VACIA }] }));
  };

  const quitarLinea = (idx: number) => {
    setFormulario(f => ({ ...f, lineas: (f.lineas || []).filter((_, i) => i !== idx) }));
  };

  const actualizarLinea = (idx: number, campo: keyof LineaExtractoCrear, valor: any) => {
    setFormulario(f => {
      const lineas = [...(f.lineas || [])];
      lineas[idx] = { ...lineas[idx], [campo]: valor };
      return { ...f, lineas };
    });
  };

  const handleGuardar = async () => {
    if (!formulario.cuenta_bancaria_id || !formulario.fecha_inicio || !formulario.fecha_fin) {
      setErrorFormulario('Cuenta bancaria, fecha inicio y fecha fin son obligatorios.');
      return;
    }
    setGuardando(true);
    setErrorFormulario(null);
    try {
      await crearExtracto(formulario);
      setAbrirNuevo(false);
      setFormulario({ cuenta_bancaria_id: 0, fecha_inicio: '', fecha_fin: '', saldo_inicial: 0, saldo_final: 0, lineas: [] });
      await cargarDatos();
    } catch (err: any) {
      setErrorFormulario(err?.detail || err?.message || 'Error al crear el extracto');
    } finally {
      setGuardando(false);
    }
  };

  const columnas: GridColDef[] = [
    {
      field: 'cuenta_bancaria_id', headerName: 'Cuenta Bancaria', flex: 1, minWidth: 180,
      valueGetter: (p: any) => cuentas.find(c => c.id === p.row.cuenta_bancaria_id)?.nombre ?? '—',
    },
    { field: 'referencia', headerName: 'Referencia', width: 130 },
    { field: 'fecha_inicio', headerName: 'Desde', width: 110 },
    { field: 'fecha_fin', headerName: 'Hasta', width: 110 },
    { field: 'saldo_inicial', headerName: 'Saldo Inicial', width: 120, type: 'number', valueFormatter: (p: any) => Number(p.value).toFixed(2) },
    { field: 'saldo_final', headerName: 'Saldo Final', width: 120, type: 'number', valueFormatter: (p: any) => Number(p.value).toFixed(2) },
    {
      field: 'estado', headerName: 'Estado', width: 110,
      renderCell: p => <Chip label={p.value} color={ESTADO_COLOR[p.value] ?? 'default'} size="small" variant="outlined" />,
    },
    {
      field: 'acciones', type: 'actions', headerName: '', width: 80,
      getActions: (params: GridRowParams) => {
        const actions = [
          <GridActionsCellItem key="ver" icon={<IconEye size={18} />} label="Ver detalle" onClick={() => verDetalle(params.row.id)} />,
        ];
        if (params.row.estado === 'BORRADOR') {
          actions.push(
            <GridActionsCellItem key="confirmar" icon={<IconCheck size={18} />} label="Confirmar" onClick={() => handleConfirmar(params.row.id)} showInMenu />,
          );
        }
        return actions;
      },
    },
  ];

  const TIPOS_TRANSACCION = ['IESS', 'SRI', 'BCE', 'SPI', 'TRANSFERENCIA', 'CHEQUE', 'NOTA_DEBITO', 'NOTA_CREDITO', 'OTRO'];

  return (
    <MainCard
      title="Extractos Bancarios"
      secondary={
        <Button variant="contained" startIcon={<IconPlus size={18} />} onClick={() => setAbrirNuevo(true)}>
          Nuevo Extracto
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
        <Grid size={{ xs: 12, md: 3 }}>
          <FormControl fullWidth size="small">
            <InputLabel>Estado</InputLabel>
            <Select value={filtroEstado} label="Estado" onChange={e => setFiltroEstado(e.target.value)}>
              <MenuItem value="">Todos</MenuItem>
              <MenuItem value="BORRADOR">BORRADOR</MenuItem>
              <MenuItem value="CONFIRMADO">CONFIRMADO</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      <Box sx={{ height: 520, width: '100%' }}>
        <DataGrid
          rows={extractos} columns={columnas} loading={cargando}
          pageSizeOptions={[25, 50]} slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { showQuickFilter: true } }}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          disableRowSelectionOnClick
          sx={{ border: 'none', '& .MuiDataGrid-columnHeaders': { backgroundColor: '#f8fafc', fontWeight: 700 } }}
        />
      </Box>

      {/* Modal Detalle */}
      <Dialog open={abrirDetalle} onClose={() => setAbrirDetalle(false)} maxWidth="md" fullWidth>
        <DialogTitle>Detalle Extracto — {cuentas.find(c => c.id === detalleExtracto?.cuenta_bancaria_id)?.nombre}</DialogTitle>
        <DialogContent dividers>
          {detalleExtracto && (
            <>
              <Grid container spacing={1} sx={{ mb: 2 }}>
                <Grid size={{ xs: 6, md: 3 }}><Typography variant="caption" color="textSecondary">Desde</Typography><Typography>{detalleExtracto.fecha_inicio}</Typography></Grid>
                <Grid size={{ xs: 6, md: 3 }}><Typography variant="caption" color="textSecondary">Hasta</Typography><Typography>{detalleExtracto.fecha_fin}</Typography></Grid>
                <Grid size={{ xs: 6, md: 3 }}><Typography variant="caption" color="textSecondary">Saldo Inicial</Typography><Typography>{Number(detalleExtracto.saldo_inicial).toFixed(2)}</Typography></Grid>
                <Grid size={{ xs: 6, md: 3 }}><Typography variant="caption" color="textSecondary">Saldo Final</Typography><Typography fontWeight={700}>{Number(detalleExtracto.saldo_final).toFixed(2)}</Typography></Grid>
              </Grid>
              <Table size="small">
                <TableHead>
                  <TableRow sx={{ bgcolor: '#f8fafc' }}>
                    <TableCell>Fecha</TableCell>
                    <TableCell>Tipo</TableCell>
                    <TableCell>Referencia</TableCell>
                    <TableCell>Descripción</TableCell>
                    <TableCell align="right">Valor</TableCell>
                    <TableCell>Conciliada</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {(detalleExtracto.lineas || []).map(l => (
                    <TableRow key={l.id}>
                      <TableCell>{l.fecha}</TableCell>
                      <TableCell><Chip label={l.tipo_transaccion} size="small" /></TableCell>
                      <TableCell>{l.referencia || '—'}</TableCell>
                      <TableCell>{l.descripcion || '—'}</TableCell>
                      <TableCell align="right" sx={{ color: Number(l.valor) >= 0 ? 'success.main' : 'error.main', fontWeight: 700 }}>
                        {Number(l.valor).toFixed(2)}
                      </TableCell>
                      <TableCell><Chip label={l.esta_conciliada ? 'Sí' : 'No'} color={l.esta_conciliada ? 'success' : 'default'} size="small" /></TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </>
          )}
        </DialogContent>
        <DialogActions><Button onClick={() => setAbrirDetalle(false)} color="inherit">Cerrar</Button></DialogActions>
      </Dialog>

      {/* Modal Nuevo Extracto */}
      <Dialog open={abrirNuevo} onClose={() => setAbrirNuevo(false)} maxWidth="lg" fullWidth>
        <DialogTitle>Nuevo Extracto Bancario</DialogTitle>
        <DialogContent dividers>
          {errorFormulario && <Alert severity="error" sx={{ mb: 2 }}>{errorFormulario}</Alert>}
          <Grid container spacing={2} sx={{ pt: 1, mb: 2 }}>
            <Grid size={{ xs: 12, md: 4 }}>
              <FormControl fullWidth>
                <InputLabel>Cuenta Bancaria *</InputLabel>
                <Select value={formulario.cuenta_bancaria_id || ''} label="Cuenta Bancaria *"
                  onChange={e => setFormulario({ ...formulario, cuenta_bancaria_id: Number(e.target.value) })}>
                  {cuentas.filter(c => c.es_activa).map(c => <MenuItem key={c.id} value={c.id}>{c.nombre}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 6, md: 2 }}>
              <TextField label="Fecha Inicio *" type="date" fullWidth InputLabelProps={{ shrink: true }}
                value={formulario.fecha_inicio} onChange={e => setFormulario({ ...formulario, fecha_inicio: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 6, md: 2 }}>
              <TextField label="Fecha Fin *" type="date" fullWidth InputLabelProps={{ shrink: true }}
                value={formulario.fecha_fin} onChange={e => setFormulario({ ...formulario, fecha_fin: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 6, md: 2 }}>
              <TextField label="Saldo Inicial" type="number" fullWidth value={formulario.saldo_inicial}
                onChange={e => setFormulario({ ...formulario, saldo_inicial: parseFloat(e.target.value) || 0 })} />
            </Grid>
            <Grid size={{ xs: 6, md: 2 }}>
              <TextField label="Saldo Final" type="number" fullWidth value={formulario.saldo_final}
                onChange={e => setFormulario({ ...formulario, saldo_final: parseFloat(e.target.value) || 0 })} />
            </Grid>
          </Grid>

          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="subtitle2">Líneas del Extracto</Typography>
            <Button size="small" startIcon={<IconPlus size={16} />} onClick={agregarLinea}>Agregar línea</Button>
          </Box>
          <Table size="small">
            <TableHead>
              <TableRow sx={{ bgcolor: '#f8fafc' }}>
                <TableCell width="110">Fecha</TableCell>
                <TableCell width="140">Tipo</TableCell>
                <TableCell width="120">Referencia</TableCell>
                <TableCell>Descripción</TableCell>
                <TableCell align="right" width="120">Valor (±)</TableCell>
                <TableCell width="50" />
              </TableRow>
            </TableHead>
            <TableBody>
              {(formulario.lineas || []).map((linea, idx) => (
                <TableRow key={idx}>
                  <TableCell>
                    <TextField size="small" type="date" InputLabelProps={{ shrink: true }} value={linea.fecha}
                      onChange={e => actualizarLinea(idx, 'fecha', e.target.value)} />
                  </TableCell>
                  <TableCell>
                    <FormControl fullWidth size="small">
                      <Select value={linea.tipo_transaccion} onChange={e => actualizarLinea(idx, 'tipo_transaccion', e.target.value)}>
                        {TIPOS_TRANSACCION.map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
                      </Select>
                    </FormControl>
                  </TableCell>
                  <TableCell>
                    <TextField size="small" fullWidth value={linea.referencia || ''}
                      onChange={e => actualizarLinea(idx, 'referencia', e.target.value)} />
                  </TableCell>
                  <TableCell>
                    <TextField size="small" fullWidth value={linea.descripcion || ''}
                      onChange={e => actualizarLinea(idx, 'descripcion', e.target.value)} />
                  </TableCell>
                  <TableCell>
                    <TextField size="small" type="number" inputProps={{ step: '0.01', style: { textAlign: 'right' } }}
                      value={linea.valor} onChange={e => actualizarLinea(idx, 'valor', parseFloat(e.target.value) || 0)} />
                  </TableCell>
                  <TableCell>
                    <IconButton size="small" color="error" onClick={() => quitarLinea(idx)}><IconTrash size={16} /></IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevo(false)} color="inherit">Cancelar</Button>
          <Button onClick={handleGuardar} variant="contained" disabled={guardando}
            startIcon={guardando ? <CircularProgress size={16} /> : undefined}>
            {guardando ? 'Guardando...' : 'Crear Extracto (Borrador)'}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default ExtractosPage;
