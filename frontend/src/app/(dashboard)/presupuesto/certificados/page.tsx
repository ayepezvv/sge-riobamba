'use client';

import React, { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, FormControl, Grid, InputLabel, MenuItem,
  Select, TextField, Typography
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem } from '@mui/x-data-grid';
import { IconPlus, IconCheck, IconX } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { listarCertificados, crearCertificado, cambiarEstadoCertificado } from 'api/presupuesto';
import {
  CertificadoPresupuestario, CertificadoPresupuestarioCrear,
  CertificadoPresupuestarioEstado, EstadoCertificado
} from 'types/presupuesto';

const formatMonto = (v: number) =>
  new Intl.NumberFormat('es-EC', { style: 'currency', currency: 'USD' }).format(v);

const COLOR_ESTADO: Record<string, 'default' | 'warning' | 'success' | 'error' | 'info'> = {
  PENDIENTE: 'warning', APROBADO: 'success', ANULADO: 'error', LIQUIDADO: 'info',
};

const CertificadosPage = () => {
  const [certificados, setCertificados] = useState<CertificadoPresupuestario[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filtroEstado, setFiltroEstado] = useState<string>('');

  const [abrirFormulario, setAbrirFormulario] = useState(false);
  const [formulario, setFormulario] = useState<CertificadoPresupuestarioCrear>({
    id_asignacion: 0,
    monto_certificado: 0,
    concepto: '',
    fecha_solicitud: new Date().toISOString().split('T')[0],
  });
  const [guardando, setGuardando] = useState(false);
  const [errorForm, setErrorForm] = useState<string | null>(null);

  // Cambio estado
  const [abrirCambioEstado, setAbrirCambioEstado] = useState(false);
  const [certSeleccionado, setCertSeleccionado] = useState<CertificadoPresupuestario | null>(null);
  const [nuevoEstado, setNuevoEstado] = useState<'APROBADO' | 'ANULADO'>('APROBADO');
  const [motivoAnulacion, setMotivoAnulacion] = useState('');
  const [guardandoEstado, setGuardandoEstado] = useState(false);
  const [errorEstado, setErrorEstado] = useState<string | null>(null);

  const cargarCertificados = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const res = await listarCertificados(filtroEstado ? { estado: filtroEstado } : {});
      setCertificados(res);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar certificados');
    } finally {
      setCargando(false);
    }
  }, [filtroEstado]);

  useEffect(() => { cargarCertificados(); }, [cargarCertificados]);

  const handleCrearCertificado = async () => {
    if (!formulario.id_asignacion || !formulario.monto_certificado || !formulario.concepto) {
      setErrorForm('Asignación, monto y concepto son obligatorios.');
      return;
    }
    setGuardando(true);
    setErrorForm(null);
    try {
      await crearCertificado(formulario);
      setAbrirFormulario(false);
      cargarCertificados();
    } catch (err: any) {
      setErrorForm(err?.response?.data?.detail || err?.message || 'Error al crear certificado');
    } finally {
      setGuardando(false);
    }
  };

  const abrirCambio = (cert: CertificadoPresupuestario, estado: 'APROBADO' | 'ANULADO') => {
    setCertSeleccionado(cert);
    setNuevoEstado(estado);
    setMotivoAnulacion('');
    setErrorEstado(null);
    setAbrirCambioEstado(true);
  };

  const handleCambiarEstado = async () => {
    if (nuevoEstado === 'ANULADO' && !motivoAnulacion) {
      setErrorEstado('El motivo de anulación es obligatorio.');
      return;
    }
    setGuardandoEstado(true);
    setErrorEstado(null);
    try {
      const payload: CertificadoPresupuestarioEstado = {
        estado: nuevoEstado,
        motivo_anulacion: nuevoEstado === 'ANULADO' ? motivoAnulacion : undefined,
      };
      await cambiarEstadoCertificado(certSeleccionado!.id_certificado, payload);
      setAbrirCambioEstado(false);
      cargarCertificados();
    } catch (err: any) {
      setErrorEstado(err?.response?.data?.detail || err?.message || 'Error al cambiar estado');
    } finally {
      setGuardandoEstado(false);
    }
  };

  const columnas: GridColDef[] = [
    { field: 'numero_certificado', headerName: 'Número', width: 160 },
    { field: 'id_asignacion', headerName: 'Asignación', width: 100 },
    { field: 'concepto', headerName: 'Concepto', flex: 1 },
    {
      field: 'monto_certificado', headerName: 'Monto', width: 140,
      renderCell: ({ value }) => formatMonto(value),
    },
    { field: 'fecha_solicitud', headerName: 'Fecha Solicitud', width: 130 },
    { field: 'fecha_certificacion', headerName: 'Fecha Cert.', width: 120 },
    {
      field: 'estado', headerName: 'Estado', width: 110,
      renderCell: ({ value }) => <Chip label={value} size="small" color={COLOR_ESTADO[value] || 'default'} />,
    },
    {
      field: 'acciones', type: 'actions', headerName: 'Acciones', width: 100,
      getActions: ({ row }) => {
        const cert = row as CertificadoPresupuestario;
        if (cert.estado !== 'PENDIENTE') return [];
        return [
          <GridActionsCellItem key="aprobar" icon={<IconCheck size={18} />} label="Aprobar"
            onClick={() => abrirCambio(cert, 'APROBADO')} />,
          <GridActionsCellItem key="anular" icon={<IconX size={18} />} label="Anular"
            onClick={() => abrirCambio(cert, 'ANULADO')} />,
        ];
      },
    },
  ];

  return (
    <MainCard title="Certificados Presupuestarios">
      <Box sx={{ mb: 2, display: 'flex', gap: 2, alignItems: 'center' }}>
        <FormControl size="small" sx={{ minWidth: 160 }}>
          <InputLabel>Estado</InputLabel>
          <Select value={filtroEstado} label="Estado" onChange={e => setFiltroEstado(e.target.value)}>
            <MenuItem value="">Todos</MenuItem>
            {['PENDIENTE', 'APROBADO', 'ANULADO', 'LIQUIDADO'].map(e => (
              <MenuItem key={e} value={e}>{e}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button variant="contained" startIcon={<IconPlus />}
          onClick={() => { setErrorForm(null); setAbrirFormulario(true); }}>
          Nuevo Certificado
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {cargando ? (
        <Box display="flex" justifyContent="center" p={4}><CircularProgress /></Box>
      ) : (
        <DataGrid
          rows={certificados}
          columns={columnas}
          getRowId={r => r.id_certificado}
          slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { showQuickFilter: true } }}
          autoHeight density="compact"
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          pageSizeOptions={[25, 50]}
        />
      )}

      {/* Dialog Nuevo Certificado */}
      <Dialog open={abrirFormulario} onClose={() => setAbrirFormulario(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Nuevo Certificado Presupuestario</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid size={6}>
              <TextField fullWidth label="ID Asignación" type="number" size="small" required
                value={formulario.id_asignacion || ''}
                onChange={e => setFormulario(f => ({ ...f, id_asignacion: Number(e.target.value) }))} />
            </Grid>
            <Grid size={6}>
              <TextField fullWidth label="Monto a Certificar" type="number" size="small" required
                value={formulario.monto_certificado || ''}
                onChange={e => setFormulario(f => ({ ...f, monto_certificado: Number(e.target.value) }))} />
            </Grid>
            <Grid size={12}>
              <TextField fullWidth label="Concepto" size="small" required
                value={formulario.concepto}
                onChange={e => setFormulario(f => ({ ...f, concepto: e.target.value }))}
                multiline rows={2} />
            </Grid>
            <Grid size={6}>
              <TextField fullWidth label="Fecha Solicitud" type="date" size="small"
                value={formulario.fecha_solicitud}
                onChange={e => setFormulario(f => ({ ...f, fecha_solicitud: e.target.value }))}
                InputLabelProps={{ shrink: true }} />
            </Grid>
            <Grid size={6}>
              <TextField fullWidth label="Fecha Vencimiento" type="date" size="small"
                value={formulario.fecha_vencimiento || ''}
                onChange={e => setFormulario(f => ({ ...f, fecha_vencimiento: e.target.value }))}
                InputLabelProps={{ shrink: true }} />
            </Grid>
          </Grid>
          {errorForm && <Alert severity="error" sx={{ mt: 2 }}>{errorForm}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirFormulario(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleCrearCertificado} disabled={guardando}>
            {guardando ? <CircularProgress size={20} /> : 'Crear'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog Cambiar Estado */}
      <Dialog open={abrirCambioEstado} onClose={() => setAbrirCambioEstado(false)} maxWidth="xs" fullWidth>
        <DialogTitle>{nuevoEstado === 'APROBADO' ? 'Aprobar Certificado' : 'Anular Certificado'}</DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Certificado: <strong>{certSeleccionado?.numero_certificado}</strong>
          </Typography>
          {nuevoEstado === 'ANULADO' && (
            <TextField fullWidth label="Motivo de Anulación" multiline rows={3} size="small" required
              value={motivoAnulacion}
              onChange={e => setMotivoAnulacion(e.target.value)} />
          )}
          {errorEstado && <Alert severity="error" sx={{ mt: 2 }}>{errorEstado}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirCambioEstado(false)}>Cancelar</Button>
          <Button variant="contained"
            color={nuevoEstado === 'APROBADO' ? 'success' : 'error'}
            onClick={handleCambiarEstado} disabled={guardandoEstado}>
            {guardandoEstado ? <CircularProgress size={20} /> : nuevoEstado}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default CertificadosPage;
