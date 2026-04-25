'use client';

import React, { useState, useCallback } from 'react';
import {
  Alert, Box, Button, CircularProgress, Divider, FormControl,
  Grid, InputLabel, MenuItem, Select, Table, TableBody,
  TableCell, TableHead, TableRow, TextField, Typography
} from '@mui/material';
import { IconSearch } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { listarCuentas, listarAsientos } from 'api/contabilidad';
import { CuentaContable, AsientoContable, LineaAsiento } from 'types/contabilidad';

interface MovimientoMayor {
  fecha: string;
  numeroAsiento: string;
  concepto: string;
  referencia?: string;
  debe: number;
  haber: number;
  saldo: number;
}

const MayorGeneralPage = () => {
  const [cuentas, setCuentas] = useState<CuentaContable[]>([]);
  const [cuentaSeleccionada, setCuentaSeleccionada] = useState<number | ''>('');
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');

  const [movimientos, setMovimientos] = useState<MovimientoMayor[]>([]);
  const [cuentaInfo, setCuentaInfo] = useState<CuentaContable | null>(null);
  const [cargandoCuentas, setCargandoCuentas] = useState(false);
  const [consultando, setConsultando] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [consultado, setConsultado] = useState(false);

  const buscarCuentas = useCallback(async () => {
    if (cuentas.length > 0) return;
    setCargandoCuentas(true);
    try {
      const res = await listarCuentas({ estado: 'ACTIVA' });
      setCuentas(res.filter(c => c.permite_movimientos));
    } catch {
      setError('Error al cargar la lista de cuentas');
    } finally {
      setCargandoCuentas(false);
    }
  }, [cuentas.length]);

  const consultarMayor = async () => {
    if (!cuentaSeleccionada) {
      setError('Debe seleccionar una cuenta contable');
      return;
    }
    setConsultando(true);
    setError(null);
    try {
      const params: any = { estado: 'PUBLICADO' };
      if (fechaInicio) params.fecha_inicio = fechaInicio;
      if (fechaFin) params.fecha_fin = fechaFin;

      const asientos = await listarAsientos(params);
      const cuenta = cuentas.find(c => c.id === cuentaSeleccionada)!;
      setCuentaInfo(cuenta);

      const lineaFiltradas: Array<{ asiento: AsientoContable; linea: LineaAsiento }> = [];
      for (const asiento of asientos) {
        for (const linea of asiento.lineas) {
          if (linea.cuenta_id === cuentaSeleccionada) {
            lineaFiltradas.push({ asiento, linea });
          }
        }
      }

      lineaFiltradas.sort((a, b) => a.asiento.fecha.localeCompare(b.asiento.fecha));

      let saldoAcumulado = 0;
      const movs: MovimientoMayor[] = lineaFiltradas.map(({ asiento, linea }) => {
        saldoAcumulado += Number(linea.debe) - Number(linea.haber);
        return {
          fecha: asiento.fecha,
          numeroAsiento: asiento.numero,
          concepto: linea.descripcion || asiento.concepto,
          referencia: asiento.referencia,
          debe: Number(linea.debe),
          haber: Number(linea.haber),
          saldo: saldoAcumulado,
        };
      });

      setMovimientos(movs);
      setConsultado(true);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al consultar el mayor general');
    } finally {
      setConsultando(false);
    }
  };

  const totalDebe = movimientos.reduce((s, m) => s + m.debe, 0);
  const totalHaber = movimientos.reduce((s, m) => s + m.haber, 0);
  const saldoFinal = movimientos.length > 0 ? movimientos[movimientos.length - 1].saldo : 0;

  return (
    <MainCard title="Mayor General">
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      {/* ── Filtros de consulta ── */}
      <Grid container spacing={2} alignItems="flex-end" sx={{ mb: 3 }}>
        <Grid size={{ xs: 12, md: 5 }}>
          <FormControl fullWidth>
            <InputLabel>Cuenta Contable *</InputLabel>
            <Select
              value={cuentaSeleccionada}
              label="Cuenta Contable *"
              onOpen={buscarCuentas}
              onChange={e => setCuentaSeleccionada(e.target.value as number)}
            >
              {cargandoCuentas
                ? <MenuItem disabled><CircularProgress size={16} sx={{ mr: 1 }} /> Cargando...</MenuItem>
                : cuentas.map(c => <MenuItem key={c.id} value={c.id}>{c.codigo} — {c.nombre}</MenuItem>)
              }
            </Select>
          </FormControl>
        </Grid>
        <Grid size={{ xs: 6, md: 2 }}>
          <TextField
            label="Fecha Inicio" type="date" fullWidth InputLabelProps={{ shrink: true }}
            value={fechaInicio}
            onChange={e => setFechaInicio(e.target.value)}
          />
        </Grid>
        <Grid size={{ xs: 6, md: 2 }}>
          <TextField
            label="Fecha Fin" type="date" fullWidth InputLabelProps={{ shrink: true }}
            value={fechaFin}
            onChange={e => setFechaFin(e.target.value)}
          />
        </Grid>
        <Grid size={{ xs: 12, md: 3 }}>
          <Button
            variant="contained" fullWidth startIcon={consultando ? <CircularProgress size={16} color="inherit" /> : <IconSearch size={18} />}
            onClick={consultarMayor} disabled={consultando || !cuentaSeleccionada}
          >
            {consultando ? 'Consultando...' : 'Consultar Mayor'}
          </Button>
        </Grid>
      </Grid>

      {/* ── Resultado ── */}
      {consultado && cuentaInfo && (
        <>
          <Box sx={{ bgcolor: '#e8f4fd', p: 2, borderRadius: 1, mb: 2 }}>
            <Typography variant="subtitle1" fontWeight={700}>
              {cuentaInfo.codigo} — {cuentaInfo.nombre}
            </Typography>
            <Typography variant="caption" color="textSecondary">
              Tipo: {cuentaInfo.tipo_cuenta_id} | Nivel: {cuentaInfo.nivel} | Estado: {cuentaInfo.estado}
            </Typography>
          </Box>

          <Table size="small">
            <TableHead>
              <TableRow sx={{ bgcolor: '#f8fafc' }}>
                <TableCell width={100}>Fecha</TableCell>
                <TableCell width={130}>N° Asiento</TableCell>
                <TableCell>Concepto</TableCell>
                <TableCell width={80}>Ref.</TableCell>
                <TableCell align="right" width={120}>Debe</TableCell>
                <TableCell align="right" width={120}>Haber</TableCell>
                <TableCell align="right" width={130}>Saldo</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {movimientos.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    <Typography color="textSecondary" sx={{ py: 3 }}>
                      No hay movimientos registrados para esta cuenta en el período seleccionado
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                movimientos.map((mov, idx) => (
                  <TableRow key={idx} hover>
                    <TableCell>{mov.fecha}</TableCell>
                    <TableCell>
                      <Typography variant="body2" fontFamily="monospace" fontWeight={600}>
                        {mov.numeroAsiento}
                      </Typography>
                    </TableCell>
                    <TableCell>{mov.concepto}</TableCell>
                    <TableCell>{mov.referencia ?? '—'}</TableCell>
                    <TableCell align="right" sx={{ color: mov.debe > 0 ? '#1565c0' : 'inherit' }}>
                      {mov.debe > 0 ? mov.debe.toFixed(2) : ''}
                    </TableCell>
                    <TableCell align="right" sx={{ color: mov.haber > 0 ? '#c62828' : 'inherit' }}>
                      {mov.haber > 0 ? mov.haber.toFixed(2) : ''}
                    </TableCell>
                    <TableCell align="right" sx={{ fontWeight: 600, color: mov.saldo >= 0 ? '#2e7d32' : '#c62828' }}>
                      {mov.saldo.toFixed(2)}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>

          <Divider sx={{ my: 1 }} />
          <Table size="small">
            <TableBody>
              <TableRow sx={{ bgcolor: '#e8f5e9' }}>
                <TableCell colSpan={4}><Typography fontWeight={700} align="right">TOTALES</Typography></TableCell>
                <TableCell align="right"><Typography fontWeight={700} color="#1565c0">{totalDebe.toFixed(2)}</Typography></TableCell>
                <TableCell align="right"><Typography fontWeight={700} color="#c62828">{totalHaber.toFixed(2)}</Typography></TableCell>
                <TableCell align="right">
                  <Typography fontWeight={700} color={saldoFinal >= 0 ? '#2e7d32' : '#c62828'}>
                    {saldoFinal.toFixed(2)}
                  </Typography>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </>
      )}
    </MainCard>
  );
};

export default MayorGeneralPage;
