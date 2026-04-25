'use client';

import React, { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, FormControl, Grid, IconButton, InputLabel,
  MenuItem, Select, Table, TableBody, TableCell, TableHead, TableRow,
  TextField, Typography
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem, GridRowParams } from '@mui/x-data-grid';
import { IconPlus, IconEye, IconCheck, IconX, IconTrash } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { listarPagos, obtenerPago, crearPago, confirmarPago, anularPago, listarFacturas } from 'api/financiero';
import { listarCuentasBancarias } from 'api/tesoreria';
import {
  Pago, PagoCrear, TipoPago, MetodoPago, LineaPagoCrear, ResumenFactura,
} from 'types/financiero';
import { CuentaBancaria } from 'types/tesoreria';

const ESTADO_COLOR: Record<string, 'default' | 'warning' | 'success' | 'error'> = {
  BORRADOR: 'warning', CONFIRMADO: 'success', ANULADO: 'error',
};

const METODOS: MetodoPago[] = ['EFECTIVO', 'CHEQUE', 'TRANSFERENCIA', 'SPI', 'BCE', 'NOTA_CREDITO'];

const PagosPage = () => {
  const [pagos, setPagos] = useState<Pago[]>([]);
  const [facturas, setFacturas] = useState<ResumenFactura[]>([]);
  const [cuentasBancarias, setCuentasBancarias] = useState<CuentaBancaria[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [filtroTipo, setFiltroTipo] = useState('');
  const [filtroEstado, setFiltroEstado] = useState('');

  const [detallePago, setDetallePago] = useState<Pago | null>(null);
  const [abrirDetalle, setAbrirDetalle] = useState(false);

  const [abrirAnular, setAbrirAnular] = useState(false);
  const [idAnular, setIdAnular] = useState<number | null>(null);
  const [motivoAnulacion, setMotivoAnulacion] = useState('');
  const [anulando, setAnulando] = useState(false);

  const [abrirNuevo, setAbrirNuevo] = useState(false);
  const [formulario, setFormulario] = useState<PagoCrear>({
    tipo: 'CLIENTE', nombre_tercero: '', identificacion_tercero: '',
    fecha_pago: new Date().toISOString().split('T')[0], tipo_pago: 'TRANSFERENCIA', monto_total: 0, lineas: [],
  });
  const [guardando, setGuardando] = useState(false);
  const [errorFormulario, setErrorFormulario] = useState<string | null>(null);

  const sumaLineas = (formulario.lineas || []).reduce((s, l) => s + Number(l.monto_aplicado || 0), 0);

  const cargarDatos = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const params: any = {};
      if (filtroTipo) params.tipo = filtroTipo;
      if (filtroEstado) params.estado = filtroEstado;
      const [resPagos, resCuentas] = await Promise.all([
        listarPagos(params),
        listarCuentasBancarias({ solo_activas: true }),
      ]);
      setPagos(resPagos);
      setCuentasBancarias(resCuentas);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar');
    } finally {
      setCargando(false);
    }
  }, [filtroTipo, filtroEstado]);

  useEffect(() => { cargarDatos(); }, [cargarDatos]);

  const cargarFacturas = useCallback(async (tipo: TipoPago) => {
    try {
      const res = await listarFacturas({ tipo, estado: 'APROBADA' });
      setFacturas(res.filter(f => f.saldo_pendiente > 0));
    } catch {
      setFacturas([]);
    }
  }, []);

  const verDetalle = async (id: number) => {
    try {
      const p = await obtenerPago(id);
      setDetallePago(p);
      setAbrirDetalle(true);
    } catch {
      setError('Error al obtener el detalle del pago');
    }
  };

  const handleConfirmar = async (id: number) => {
    if (!confirm('¿Confirmar este pago?')) return;
    try {
      await confirmarPago(id);
      await cargarDatos();
    } catch (err: any) {
      setError(err?.detail || 'Error al confirmar');
    }
  };

  const handleAnular = async () => {
    if (!idAnular || motivoAnulacion.length < 5) {
      setError('El motivo debe tener al menos 5 caracteres.');
      return;
    }
    setAnulando(true);
    try {
      await anularPago(idAnular, motivoAnulacion);
      setAbrirAnular(false);
      await cargarDatos();
    } catch (err: any) {
      setError(err?.detail || 'Error al anular');
    } finally {
      setAnulando(false);
    }
  };

  const agregarLinea = () => {
    setFormulario(f => ({ ...f, lineas: [...(f.lineas || []), { factura_id: 0, monto_aplicado: 0 }] }));
  };

  const quitarLinea = (idx: number) => {
    setFormulario(f => ({ ...f, lineas: (f.lineas || []).filter((_, i) => i !== idx) }));
  };

  const actualizarLinea = (idx: number, campo: keyof LineaPagoCrear, valor: any) => {
    setFormulario(f => {
      const lineas = [...(f.lineas || [])];
      lineas[idx] = { ...lineas[idx], [campo]: valor };
      return { ...f, lineas };
    });
  };

  const handleGuardar = async () => {
    if (!formulario.nombre_tercero || !formulario.identificacion_tercero || !formulario.monto_total) {
      setErrorFormulario('Tercero, identificación y monto son obligatorios.');
      return;
    }
    if ((formulario.lineas || []).length > 0 && Math.abs(sumaLineas - Number(formulario.monto_total)) > 0.01) {
      setErrorFormulario(`La suma de líneas (${sumaLineas.toFixed(2)}) no coincide con el monto total (${formulario.monto_total}).`);
      return;
    }
    setGuardando(true);
    setErrorFormulario(null);
    try {
      await crearPago(formulario);
      setAbrirNuevo(false);
      setFormulario({
        tipo: 'CLIENTE', nombre_tercero: '', identificacion_tercero: '',
        fecha_pago: new Date().toISOString().split('T')[0], tipo_pago: 'TRANSFERENCIA', monto_total: 0, lineas: [],
      });
      await cargarDatos();
    } catch (err: any) {
      setErrorFormulario(err?.detail || err?.message || 'Error al crear el pago');
    } finally {
      setGuardando(false);
    }
  };

  const columnas: GridColDef[] = [
    { field: 'numero', headerName: 'N° Pago', width: 130, renderCell: p => <Typography variant="body2" fontFamily="monospace" fontWeight={700}>{p.value}</Typography> },
    { field: 'tipo', headerName: 'Tipo', width: 100, renderCell: p => <Chip label={p.value} size="small" color={p.value === 'CLIENTE' ? 'primary' : 'secondary'} variant="outlined" /> },
    { field: 'nombre_tercero', headerName: 'Tercero', flex: 1, minWidth: 180 },
    { field: 'fecha_pago', headerName: 'Fecha', width: 110 },
    { field: 'tipo_pago', headerName: 'Método', width: 130, renderCell: p => <Chip label={p.value} size="small" /> },
    { field: 'monto_total', headerName: 'Monto', width: 110, type: 'number', valueFormatter: (p: any) => Number(p.value).toFixed(2) },
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
            <GridActionsCellItem key="anular" icon={<IconX size={18} />} label="Anular" onClick={() => { setIdAnular(params.row.id); setMotivoAnulacion(''); setAbrirAnular(true); }} showInMenu />,
          );
        }
        return actions;
      },
    },
  ];

  return (
    <MainCard
      title="Pagos y Cobros"
      secondary={
        <Button variant="contained" startIcon={<IconPlus size={18} />} onClick={() => { cargarFacturas(formulario.tipo); setAbrirNuevo(true); }}>
          Nuevo Pago
        </Button>
      }
    >
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid size={{ xs: 12, md: 3 }}>
          <FormControl fullWidth size="small">
            <InputLabel>Tipo</InputLabel>
            <Select value={filtroTipo} label="Tipo" onChange={e => setFiltroTipo(e.target.value)}>
              <MenuItem value="">Todos</MenuItem>
              <MenuItem value="CLIENTE">CLIENTE</MenuItem>
              <MenuItem value="PROVEEDOR">PROVEEDOR</MenuItem>
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
              <MenuItem value="ANULADO">ANULADO</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      <Box sx={{ height: 540, width: '100%' }}>
        <DataGrid rows={pagos} columns={columnas} loading={cargando}
          pageSizeOptions={[25, 50]} slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { showQuickFilter: true } }}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          disableRowSelectionOnClick
          sx={{ border: 'none', '& .MuiDataGrid-columnHeaders': { backgroundColor: '#f8fafc', fontWeight: 700 } }}
        />
      </Box>

      {/* Modal Detalle */}
      <Dialog open={abrirDetalle} onClose={() => setAbrirDetalle(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Pago N° {detallePago?.numero}
          <Chip label={detallePago?.estado} color={ESTADO_COLOR[detallePago?.estado ?? ''] ?? 'default'} size="small" sx={{ ml: 2 }} />
        </DialogTitle>
        <DialogContent dividers>
          {detallePago && (
            <Grid container spacing={1}>
              <Grid size={6}><Typography variant="caption" color="textSecondary">Tipo</Typography><Typography>{detallePago.tipo}</Typography></Grid>
              <Grid size={6}><Typography variant="caption" color="textSecondary">Fecha</Typography><Typography>{detallePago.fecha_pago}</Typography></Grid>
              <Grid size={12}><Typography variant="caption" color="textSecondary">Tercero</Typography><Typography>{detallePago.nombre_tercero} ({detallePago.identificacion_tercero})</Typography></Grid>
              <Grid size={6}><Typography variant="caption" color="textSecondary">Método</Typography><Typography>{detallePago.tipo_pago}</Typography></Grid>
              <Grid size={6}><Typography variant="caption" color="textSecondary">Monto Total</Typography><Typography fontWeight={700} color="primary">{Number(detallePago.monto_total).toFixed(2)}</Typography></Grid>
              {detallePago.referencia_bancaria && <Grid size={12}><Typography variant="caption" color="textSecondary">Referencia Bancaria</Typography><Typography>{detallePago.referencia_bancaria}</Typography></Grid>}
              {detallePago.lineas.length > 0 && (
                <Grid size={12}>
                  <Typography variant="subtitle2" sx={{ mt: 1 }}>Facturas Aplicadas</Typography>
                  <Table size="small">
                    <TableHead><TableRow sx={{ bgcolor: '#f8fafc' }}>
                      <TableCell>Factura ID</TableCell>
                      <TableCell align="right">Monto Aplicado</TableCell>
                    </TableRow></TableHead>
                    <TableBody>
                      {detallePago.lineas.map(l => (
                        <TableRow key={l.id}>
                          <TableCell>{l.factura_id}</TableCell>
                          <TableCell align="right">{Number(l.monto_aplicado).toFixed(2)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </Grid>
              )}
            </Grid>
          )}
        </DialogContent>
        <DialogActions><Button onClick={() => setAbrirDetalle(false)} color="inherit">Cerrar</Button></DialogActions>
      </Dialog>

      {/* Modal Anular */}
      <Dialog open={abrirAnular} onClose={() => setAbrirAnular(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Anular Pago</DialogTitle>
        <DialogContent dividers>
          <TextField label="Motivo de anulación *" fullWidth multiline rows={3}
            value={motivoAnulacion} onChange={e => setMotivoAnulacion(e.target.value)} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirAnular(false)} color="inherit">Cancelar</Button>
          <Button onClick={handleAnular} color="error" variant="contained" disabled={anulando || motivoAnulacion.length < 5}
            startIcon={anulando ? <CircularProgress size={16} /> : undefined}>
            {anulando ? 'Anulando...' : 'Confirmar Anulación'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Modal Nuevo Pago */}
      <Dialog open={abrirNuevo} onClose={() => setAbrirNuevo(false)} maxWidth="md" fullWidth>
        <DialogTitle>Nuevo Pago / Cobro</DialogTitle>
        <DialogContent dividers>
          {errorFormulario && <Alert severity="error" sx={{ mb: 2 }}>{errorFormulario}</Alert>}
          <Grid container spacing={2} sx={{ pt: 1, mb: 2 }}>
            <Grid size={{ xs: 6, md: 2 }}>
              <FormControl fullWidth>
                <InputLabel>Tipo *</InputLabel>
                <Select value={formulario.tipo} label="Tipo *"
                  onChange={e => { const t = e.target.value as TipoPago; setFormulario({ ...formulario, tipo: t }); cargarFacturas(t); }}>
                  <MenuItem value="CLIENTE">CLIENTE</MenuItem>
                  <MenuItem value="PROVEEDOR">PROVEEDOR</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 6, md: 2 }}>
              <TextField label="Fecha *" type="date" fullWidth InputLabelProps={{ shrink: true }}
                value={formulario.fecha_pago} onChange={e => setFormulario({ ...formulario, fecha_pago: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 12, md: 3 }}>
              <TextField label="Nombre Tercero *" fullWidth value={formulario.nombre_tercero}
                onChange={e => setFormulario({ ...formulario, nombre_tercero: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 6, md: 2 }}>
              <TextField label="Identificación *" fullWidth value={formulario.identificacion_tercero}
                onChange={e => setFormulario({ ...formulario, identificacion_tercero: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 6, md: 3 }}>
              <FormControl fullWidth>
                <InputLabel>Método de Pago *</InputLabel>
                <Select value={formulario.tipo_pago} label="Método de Pago *"
                  onChange={e => setFormulario({ ...formulario, tipo_pago: e.target.value as MetodoPago })}>
                  {METODOS.map(m => <MenuItem key={m} value={m}>{m}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 6, md: 2 }}>
              <TextField label="Monto Total *" type="number" fullWidth value={formulario.monto_total}
                onChange={e => setFormulario({ ...formulario, monto_total: parseFloat(e.target.value) || 0 })} />
            </Grid>
            <Grid size={{ xs: 6, md: 2 }}>
              <FormControl fullWidth>
                <InputLabel>Cuenta Bancaria</InputLabel>
                <Select value={formulario.cuenta_bancaria_id || ''} label="Cuenta Bancaria"
                  onChange={e => setFormulario({ ...formulario, cuenta_bancaria_id: Number(e.target.value) || undefined })}>
                  <MenuItem value="">Sin cuenta</MenuItem>
                  {cuentasBancarias.map(c => <MenuItem key={c.id} value={c.id}>{c.nombre}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, md: 4 }}>
              <TextField label="Referencia Bancaria" fullWidth value={formulario.referencia_bancaria || ''}
                onChange={e => setFormulario({ ...formulario, referencia_bancaria: e.target.value })} />
            </Grid>
          </Grid>

          {facturas.length > 0 && (
            <>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="subtitle2">Aplicar a Facturas (opcional)</Typography>
                <Box>
                  {(formulario.lineas || []).length > 0 && (
                    <Chip label={`Suma líneas: ${sumaLineas.toFixed(2)} / Total: ${formulario.monto_total}`}
                      color={Math.abs(sumaLineas - Number(formulario.monto_total)) < 0.01 ? 'success' : 'warning'} size="small" sx={{ mr: 1 }} />
                  )}
                  <Button size="small" startIcon={<IconPlus size={16} />} onClick={agregarLinea}>Agregar factura</Button>
                </Box>
              </Box>
              <Table size="small">
                <TableHead>
                  <TableRow sx={{ bgcolor: '#f8fafc' }}>
                    <TableCell>Factura</TableCell>
                    <TableCell align="right" width="130">Monto a Aplicar</TableCell>
                    <TableCell width="50" />
                  </TableRow>
                </TableHead>
                <TableBody>
                  {(formulario.lineas || []).map((linea, idx) => (
                    <TableRow key={idx}>
                      <TableCell>
                        <FormControl fullWidth size="small">
                          <Select value={linea.factura_id || ''} onChange={e => actualizarLinea(idx, 'factura_id', Number(e.target.value))}>
                            <MenuItem value=""><em>Seleccionar factura...</em></MenuItem>
                            {facturas.map(f => <MenuItem key={f.id} value={f.id}>{f.numero} — {f.nombre_tercero} (Saldo: {Number(f.saldo_pendiente).toFixed(2)})</MenuItem>)}
                          </Select>
                        </FormControl>
                      </TableCell>
                      <TableCell>
                        <TextField size="small" type="number" inputProps={{ min: 0, step: '0.01', style: { textAlign: 'right' } }}
                          value={linea.monto_aplicado} onChange={e => actualizarLinea(idx, 'monto_aplicado', parseFloat(e.target.value) || 0)} />
                      </TableCell>
                      <TableCell>
                        <IconButton size="small" color="error" onClick={() => quitarLinea(idx)}><IconTrash size={16} /></IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevo(false)} color="inherit">Cancelar</Button>
          <Button onClick={handleGuardar} variant="contained" disabled={guardando}
            startIcon={guardando ? <CircularProgress size={16} /> : undefined}>
            {guardando ? 'Guardando...' : 'Crear Pago (Borrador)'}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default PagosPage;
