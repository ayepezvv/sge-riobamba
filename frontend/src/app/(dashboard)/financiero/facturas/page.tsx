'use client';

import React, { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, Divider, FormControl, Grid, IconButton,
  InputLabel, MenuItem, Select, Table, TableBody, TableCell, TableHead,
  TableRow, TextField, Typography
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem, GridRowParams } from '@mui/x-data-grid';
import { IconPlus, IconEye, IconCheck, IconX, IconTrash } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { listarTiposDocumento, listarFacturas, obtenerFactura, crearFactura, aprobarFactura, anularFactura } from 'api/financiero';
import {
  ResumenFactura, Factura, FacturaCrear, TipoDocumento, TipoFactura,
  LineaFacturaCrear, TipoImpuesto,
} from 'types/financiero';

const ESTADO_COLOR: Record<string, 'default' | 'warning' | 'success' | 'error'> = {
  BORRADOR: 'warning', APROBADA: 'success', ANULADA: 'error',
};

const LINEA_VACIA: LineaFacturaCrear = {
  descripcion: '', precio_unitario: 0, cantidad: 1, descuento_linea: 0,
  tipo_impuesto: 'IVA_15', porcentaje_impuesto: 15,
};

const TIPOS_IVA: { valor: TipoImpuesto; pct: number }[] = [
  { valor: 'IVA_15', pct: 15 }, { valor: 'IVA_12', pct: 12 },
  { valor: 'IVA_5', pct: 5 }, { valor: 'IVA_0', pct: 0 }, { valor: 'EXENTO', pct: 0 },
];

const FacturasPage = () => {
  const [facturas, setFacturas] = useState<ResumenFactura[]>([]);
  const [tiposDocumento, setTiposDocumento] = useState<TipoDocumento[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [filtroTipo, setFiltroTipo] = useState('');
  const [filtroEstado, setFiltroEstado] = useState('');

  const [detalleFactura, setDetalleFactura] = useState<Factura | null>(null);
  const [abrirDetalle, setAbrirDetalle] = useState(false);

  const [abrirAnular, setAbrirAnular] = useState(false);
  const [idAnular, setIdAnular] = useState<number | null>(null);
  const [motivoAnulacion, setMotivoAnulacion] = useState('');
  const [anulando, setAnulando] = useState(false);

  const [abrirNuevo, setAbrirNuevo] = useState(false);
  const [formulario, setFormulario] = useState<FacturaCrear>({
    tipo_documento_id: 0, tipo: 'CLIENTE', nombre_tercero: '', identificacion_tercero: '',
    fecha_emision: new Date().toISOString().split('T')[0], lineas: [{ ...LINEA_VACIA }],
  });
  const [guardando, setGuardando] = useState(false);
  const [errorFormulario, setErrorFormulario] = useState<string | null>(null);

  const calcularLinea = (l: LineaFacturaCrear) => {
    const subtotal = Number(l.cantidad || 1) * Number(l.precio_unitario || 0) - Number(l.descuento_linea || 0);
    const iva = subtotal * Number(l.porcentaje_impuesto || 0) / 100;
    return { subtotal, iva, total: subtotal + iva };
  };

  const totales = formulario.lineas.reduce((acc, l) => {
    const { subtotal, iva, total } = calcularLinea(l);
    return { subtotal: acc.subtotal + subtotal, iva: acc.iva + iva, total: acc.total + total };
  }, { subtotal: 0, iva: 0, total: 0 });

  const cargarDatos = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const params: any = {};
      if (filtroTipo) params.tipo = filtroTipo;
      if (filtroEstado) params.estado = filtroEstado;
      const [resFacturas, resTipos] = await Promise.all([
        listarFacturas(params),
        listarTiposDocumento(),
      ]);
      setFacturas(resFacturas);
      setTiposDocumento(resTipos);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar datos');
    } finally {
      setCargando(false);
    }
  }, [filtroTipo, filtroEstado]);

  useEffect(() => { cargarDatos(); }, [cargarDatos]);

  const verDetalle = async (id: number) => {
    try {
      const f = await obtenerFactura(id);
      setDetalleFactura(f);
      setAbrirDetalle(true);
    } catch {
      setError('Error al obtener el detalle de la factura');
    }
  };

  const handleAprobar = async (id: number) => {
    if (!confirm('¿Aprobar esta factura?')) return;
    try {
      await aprobarFactura(id);
      await cargarDatos();
    } catch (err: any) {
      setError(err?.detail || 'Error al aprobar');
    }
  };

  const handleAnular = async () => {
    if (!idAnular || motivoAnulacion.length < 5) {
      setError('El motivo debe tener al menos 5 caracteres.');
      return;
    }
    setAnulando(true);
    try {
      await anularFactura(idAnular, motivoAnulacion);
      setAbrirAnular(false);
      await cargarDatos();
    } catch (err: any) {
      setError(err?.detail || 'Error al anular');
    } finally {
      setAnulando(false);
    }
  };

  const actualizarLinea = (idx: number, campo: keyof LineaFacturaCrear, valor: any) => {
    setFormulario(f => {
      const lineas = [...f.lineas];
      lineas[idx] = { ...lineas[idx], [campo]: valor };
      if (campo === 'tipo_impuesto') {
        const found = TIPOS_IVA.find(t => t.valor === valor);
        if (found) lineas[idx].porcentaje_impuesto = found.pct;
      }
      return { ...f, lineas };
    });
  };

  const handleGuardar = async () => {
    if (!formulario.tipo_documento_id || !formulario.nombre_tercero || !formulario.identificacion_tercero || !formulario.fecha_emision) {
      setErrorFormulario('Tipo de documento, tercero, identificación y fecha son obligatorios.');
      return;
    }
    if (formulario.lineas.some(l => !l.descripcion)) {
      setErrorFormulario('Todas las líneas deben tener descripción.');
      return;
    }
    setGuardando(true);
    setErrorFormulario(null);
    try {
      await crearFactura(formulario);
      setAbrirNuevo(false);
      setFormulario({
        tipo_documento_id: 0, tipo: 'CLIENTE', nombre_tercero: '', identificacion_tercero: '',
        fecha_emision: new Date().toISOString().split('T')[0], lineas: [{ ...LINEA_VACIA }],
      });
      await cargarDatos();
    } catch (err: any) {
      setErrorFormulario(err?.detail || err?.message || 'Error al crear la factura');
    } finally {
      setGuardando(false);
    }
  };

  const columnas: GridColDef[] = [
    { field: 'numero', headerName: 'N° Factura', width: 140, renderCell: p => <Typography variant="body2" fontFamily="monospace" fontWeight={700}>{p.value}</Typography> },
    { field: 'tipo', headerName: 'Tipo', width: 100, renderCell: p => <Chip label={p.value} size="small" color={p.value === 'CLIENTE' ? 'primary' : 'secondary'} variant="outlined" /> },
    { field: 'nombre_tercero', headerName: 'Tercero', flex: 1, minWidth: 180 },
    { field: 'identificacion_tercero', headerName: 'Identificación', width: 130 },
    { field: 'fecha_emision', headerName: 'Emisión', width: 110 },
    { field: 'total', headerName: 'Total', width: 110, type: 'number', valueFormatter: (p: any) => Number(p.value).toFixed(2) },
    { field: 'saldo_pendiente', headerName: 'Saldo', width: 110, type: 'number', valueFormatter: (p: any) => Number(p.value).toFixed(2) },
    {
      field: 'estado', headerName: 'Estado', width: 100,
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
            <GridActionsCellItem key="aprobar" icon={<IconCheck size={18} />} label="Aprobar" onClick={() => handleAprobar(params.row.id)} showInMenu />,
            <GridActionsCellItem key="anular" icon={<IconX size={18} />} label="Anular" onClick={() => { setIdAnular(params.row.id); setMotivoAnulacion(''); setAbrirAnular(true); }} showInMenu />,
          );
        }
        return actions;
      },
    },
  ];

  return (
    <MainCard
      title="Facturas (AR/AP)"
      secondary={
        <Button variant="contained" startIcon={<IconPlus size={18} />} onClick={() => setAbrirNuevo(true)}>
          Nueva Factura
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
              <MenuItem value="APROBADA">APROBADA</MenuItem>
              <MenuItem value="ANULADA">ANULADA</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      <Box sx={{ height: 560, width: '100%' }}>
        <DataGrid
          rows={facturas} columns={columnas} loading={cargando}
          pageSizeOptions={[25, 50]} slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { showQuickFilter: true } }}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          disableRowSelectionOnClick
          sx={{ border: 'none', '& .MuiDataGrid-columnHeaders': { backgroundColor: '#f8fafc', fontWeight: 700 } }}
        />
      </Box>

      {/* Modal Detalle */}
      <Dialog open={abrirDetalle} onClose={() => setAbrirDetalle(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Factura N° {detalleFactura?.numero}
          <Chip label={detalleFactura?.estado} color={ESTADO_COLOR[detalleFactura?.estado ?? ''] ?? 'default'} size="small" sx={{ ml: 2 }} />
        </DialogTitle>
        <DialogContent dividers>
          {detalleFactura && (
            <>
              <Grid container spacing={1} sx={{ mb: 2 }}>
                <Grid size={{ xs: 6, md: 3 }}><Typography variant="caption" color="textSecondary">Tipo</Typography><Typography>{detalleFactura.tipo}</Typography></Grid>
                <Grid size={{ xs: 6, md: 3 }}><Typography variant="caption" color="textSecondary">Fecha Emisión</Typography><Typography>{detalleFactura.fecha_emision}</Typography></Grid>
                <Grid size={{ xs: 12, md: 6 }}><Typography variant="caption" color="textSecondary">Tercero</Typography><Typography>{detalleFactura.nombre_tercero} ({detalleFactura.identificacion_tercero})</Typography></Grid>
                {detalleFactura.observaciones && <Grid size={12}><Typography variant="caption" color="textSecondary">Observaciones</Typography><Typography>{detalleFactura.observaciones}</Typography></Grid>}
              </Grid>
              <Table size="small">
                <TableHead>
                  <TableRow sx={{ bgcolor: '#f8fafc' }}>
                    <TableCell>Descripción</TableCell>
                    <TableCell align="right">Cant.</TableCell>
                    <TableCell align="right">Precio Unit.</TableCell>
                    <TableCell align="right">IVA</TableCell>
                    <TableCell align="right">Total Línea</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {detalleFactura.lineas.map(l => (
                    <TableRow key={l.id}>
                      <TableCell>{l.descripcion}</TableCell>
                      <TableCell align="right">{l.cantidad}</TableCell>
                      <TableCell align="right">{Number(l.precio_unitario).toFixed(2)}</TableCell>
                      <TableCell align="right"><Chip label={l.tipo_impuesto} size="small" /></TableCell>
                      <TableCell align="right"><Typography fontWeight={700}>{Number(l.total_linea).toFixed(2)}</Typography></TableCell>
                    </TableRow>
                  ))}
                  <TableRow sx={{ bgcolor: '#f0f4ff' }}>
                    <TableCell colSpan={3} align="right"><Typography fontWeight={700}>SUBTOTAL / IVA / TOTAL</Typography></TableCell>
                    <TableCell align="right"><Typography>{Number(detalleFactura.total_iva).toFixed(2)}</Typography></TableCell>
                    <TableCell align="right"><Typography fontWeight={700} color="primary">{Number(detalleFactura.total).toFixed(2)}</Typography></TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </>
          )}
        </DialogContent>
        <DialogActions><Button onClick={() => setAbrirDetalle(false)} color="inherit">Cerrar</Button></DialogActions>
      </Dialog>

      {/* Modal Anular */}
      <Dialog open={abrirAnular} onClose={() => setAbrirAnular(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Anular Factura</DialogTitle>
        <DialogContent dividers>
          <TextField label="Motivo de anulación (mínimo 5 caracteres) *" fullWidth multiline rows={3}
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

      {/* Modal Nueva Factura */}
      <Dialog open={abrirNuevo} onClose={() => setAbrirNuevo(false)} maxWidth="lg" fullWidth>
        <DialogTitle>Nueva Factura</DialogTitle>
        <DialogContent dividers>
          {errorFormulario && <Alert severity="error" sx={{ mb: 2 }}>{errorFormulario}</Alert>}
          <Grid container spacing={2} sx={{ pt: 1, mb: 2 }}>
            <Grid size={{ xs: 12, md: 3 }}>
              <FormControl fullWidth>
                <InputLabel>Tipo Documento *</InputLabel>
                <Select value={formulario.tipo_documento_id || ''} label="Tipo Documento *"
                  onChange={e => setFormulario({ ...formulario, tipo_documento_id: Number(e.target.value) })}>
                  {tiposDocumento.map(t => <MenuItem key={t.id} value={t.id}>{t.nombre}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 6, md: 2 }}>
              <FormControl fullWidth>
                <InputLabel>Tipo *</InputLabel>
                <Select value={formulario.tipo} label="Tipo *"
                  onChange={e => setFormulario({ ...formulario, tipo: e.target.value as TipoFactura })}>
                  <MenuItem value="CLIENTE">CLIENTE</MenuItem>
                  <MenuItem value="PROVEEDOR">PROVEEDOR</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 6, md: 2 }}>
              <TextField label="Fecha Emisión *" type="date" fullWidth InputLabelProps={{ shrink: true }}
                value={formulario.fecha_emision} onChange={e => setFormulario({ ...formulario, fecha_emision: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 12, md: 3 }}>
              <TextField label="Nombre Tercero *" fullWidth value={formulario.nombre_tercero}
                onChange={e => setFormulario({ ...formulario, nombre_tercero: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 12, md: 2 }}>
              <TextField label="Identificación *" fullWidth value={formulario.identificacion_tercero}
                onChange={e => setFormulario({ ...formulario, identificacion_tercero: e.target.value })} />
            </Grid>
            <Grid size={12}>
              <TextField label="Observaciones" fullWidth value={formulario.observaciones || ''}
                onChange={e => setFormulario({ ...formulario, observaciones: e.target.value })} />
            </Grid>
          </Grid>
          <Divider sx={{ mb: 2 }} />
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="subtitle2">Líneas de Factura</Typography>
            <Box>
              <Chip label={`Total: ${totales.total.toFixed(2)} | IVA: ${totales.iva.toFixed(2)}`} color="primary" size="small" sx={{ mr: 1 }} />
              <Button size="small" startIcon={<IconPlus size={16} />} onClick={() => setFormulario(f => ({ ...f, lineas: [...f.lineas, { ...LINEA_VACIA }] }))}>
                Agregar línea
              </Button>
            </Box>
          </Box>
          <Table size="small">
            <TableHead>
              <TableRow sx={{ bgcolor: '#f8fafc' }}>
                <TableCell>Descripción *</TableCell>
                <TableCell align="right" width="80">Cant.</TableCell>
                <TableCell align="right" width="120">Precio Unit.</TableCell>
                <TableCell width="120">IVA</TableCell>
                <TableCell align="right" width="100">Total</TableCell>
                <TableCell width="50" />
              </TableRow>
            </TableHead>
            <TableBody>
              {formulario.lineas.map((linea, idx) => {
                const { total } = calcularLinea(linea);
                return (
                  <TableRow key={idx}>
                    <TableCell>
                      <TextField size="small" fullWidth value={linea.descripcion}
                        onChange={e => actualizarLinea(idx, 'descripcion', e.target.value)} />
                    </TableCell>
                    <TableCell>
                      <TextField size="small" type="number" inputProps={{ min: 1, step: '0.001', style: { textAlign: 'right' } }}
                        value={linea.cantidad} onChange={e => actualizarLinea(idx, 'cantidad', parseFloat(e.target.value) || 1)} />
                    </TableCell>
                    <TableCell>
                      <TextField size="small" type="number" inputProps={{ min: 0, step: '0.01', style: { textAlign: 'right' } }}
                        value={linea.precio_unitario} onChange={e => actualizarLinea(idx, 'precio_unitario', parseFloat(e.target.value) || 0)} />
                    </TableCell>
                    <TableCell>
                      <FormControl fullWidth size="small">
                        <Select value={linea.tipo_impuesto} onChange={e => actualizarLinea(idx, 'tipo_impuesto', e.target.value)}>
                          {TIPOS_IVA.map(t => <MenuItem key={t.valor} value={t.valor}>{t.valor}</MenuItem>)}
                        </Select>
                      </FormControl>
                    </TableCell>
                    <TableCell align="right"><Typography fontWeight={700}>{total.toFixed(2)}</Typography></TableCell>
                    <TableCell>
                      {formulario.lineas.length > 1 && (
                        <IconButton size="small" color="error" onClick={() => setFormulario(f => ({ ...f, lineas: f.lineas.filter((_, i) => i !== idx) }))}>
                          <IconTrash size={16} />
                        </IconButton>
                      )}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirNuevo(false)} color="inherit">Cancelar</Button>
          <Button onClick={handleGuardar} variant="contained" disabled={guardando}
            startIcon={guardando ? <CircularProgress size={16} /> : undefined}>
            {guardando ? 'Guardando...' : 'Crear Factura (Borrador)'}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default FacturasPage;
