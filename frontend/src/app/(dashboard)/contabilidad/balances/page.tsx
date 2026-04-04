'use client';

import React, { useState } from 'react';
import {
  Alert, Box, Button, CircularProgress, Grid, Tab, Table, TableBody,
  TableCell, TableHead, TableRow, Tabs, TextField, Typography
} from '@mui/material';
import { IconCalculator, IconReport } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { listarCuentas, listarTiposCuenta, obtenerSaldoCuenta } from 'api/contabilidad';
import { CuentaContable, SaldoCuenta, TipoCuenta } from 'types/contabilidad';

interface FilaBalance {
  codigo: string;
  nombre: string;
  nivel: number;
  tipo: string;
  totalDebe: number;
  totalHaber: number;
  saldo: number;
}

interface FilaComprobacion {
  codigo: string;
  nombre: string;
  totalDebe: number;
  totalHaber: number;
}

const BalancesPage = () => {
  const [tabActiva, setTabActiva] = useState(0);
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Balance de comprobación
  const [filasComprobacion, setFilasComprobacion] = useState<FilaComprobacion[]>([]);
  const [generadoComprobacion, setGeneradoComprobacion] = useState(false);

  // Balance general
  const [filasBalance, setFilasBalance] = useState<FilaBalance[]>([]);
  const [tipos, setTipos] = useState<TipoCuenta[]>([]);
  const [generadoBalance, setGeneradoBalance] = useState(false);

  const generarBalanceComprobacion = async () => {
    setCargando(true);
    setError(null);
    try {
      const cuentas = await listarCuentas({ estado: 'ACTIVA' });
      const cuentasConMovimientos = cuentas.filter(c => c.permite_movimientos && c.es_hoja);

      const params: any = {};
      if (fechaInicio) params.fecha_inicio = fechaInicio;
      if (fechaFin) params.fecha_fin = fechaFin;

      const saldosPromises = cuentasConMovimientos.map(c => obtenerSaldoCuenta(c.id, params));
      const saldos = await Promise.all(saldosPromises);

      const filas: FilaComprobacion[] = saldos
        .filter(s => s.total_debe > 0 || s.total_haber > 0)
        .sort((a, b) => a.codigo.localeCompare(b.codigo))
        .map(s => ({
          codigo: s.codigo,
          nombre: s.nombre,
          totalDebe: Number(s.total_debe),
          totalHaber: Number(s.total_haber),
        }));

      setFilasComprobacion(filas);
      setGeneradoComprobacion(true);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al generar el balance de comprobación');
    } finally {
      setCargando(false);
    }
  };

  const generarBalanceGeneral = async () => {
    setCargando(true);
    setError(null);
    try {
      const [cuentas, tiposResp] = await Promise.all([
        listarCuentas({ estado: 'ACTIVA' }),
        listarTiposCuenta(),
      ]);
      setTipos(tiposResp);

      const cuentasHoja = cuentas.filter(c => c.permite_movimientos && c.es_hoja);
      const params: any = {};
      if (fechaInicio) params.fecha_inicio = fechaInicio;
      if (fechaFin) params.fecha_fin = fechaFin;

      const saldosPromises = cuentasHoja.map(c => obtenerSaldoCuenta(c.id, params));
      const saldos = await Promise.all(saldosPromises);

      const saldoMap = new Map<number, SaldoCuenta>(saldos.map(s => [s.cuenta_id, s]));

      const filas: FilaBalance[] = cuentasHoja
        .filter(c => {
          const s = saldoMap.get(c.id);
          return s && (s.total_debe > 0 || s.total_haber > 0);
        })
        .sort((a, b) => a.codigo.localeCompare(b.codigo))
        .map(c => {
          const s = saldoMap.get(c.id)!;
          const tipo = tiposResp.find(t => t.id === c.tipo_cuenta_id);
          return {
            codigo: c.codigo,
            nombre: c.nombre,
            nivel: c.nivel,
            tipo: tipo?.nombre ?? '—',
            totalDebe: Number(s.total_debe),
            totalHaber: Number(s.total_haber),
            saldo: Number(s.saldo),
          };
        });

      setFilasBalance(filas);
      setGeneradoBalance(true);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al generar el balance general');
    } finally {
      setCargando(false);
    }
  };

  const totalDebeComp = filasComprobacion.reduce((s, f) => s + f.totalDebe, 0);
  const totalHaberComp = filasComprobacion.reduce((s, f) => s + f.totalHaber, 0);

  const totalSaldoDeudor = filasBalance.filter(f => f.saldo > 0).reduce((s, f) => s + f.saldo, 0);
  const totalSaldoAcreedor = filasBalance.filter(f => f.saldo < 0).reduce((s, f) => s + Math.abs(f.saldo), 0);

  // Agrupar balance general por tipo
  const tiposUnicos = [...new Set(filasBalance.map(f => f.tipo))];

  return (
    <MainCard title="Balances Financieros">
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      {/* ── Selector de período ── */}
      <Grid container spacing={2} alignItems="flex-end" sx={{ mb: 3 }}>
        <Grid item xs={6} md={3}>
          <TextField
            label="Fecha Inicio" type="date" fullWidth InputLabelProps={{ shrink: true }}
            value={fechaInicio} onChange={e => setFechaInicio(e.target.value)}
          />
        </Grid>
        <Grid item xs={6} md={3}>
          <TextField
            label="Fecha Fin" type="date" fullWidth InputLabelProps={{ shrink: true }}
            value={fechaFin} onChange={e => setFechaFin(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <Typography variant="caption" color="textSecondary">
            Sin fechas = todos los movimientos publicados
          </Typography>
        </Grid>
      </Grid>

      <Tabs value={tabActiva} onChange={(_, v) => setTabActiva(v)} sx={{ mb: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Tab label="Balance de Comprobación" icon={<IconCalculator size={18} />} iconPosition="start" />
        <Tab label="Balance General" icon={<IconReport size={18} />} iconPosition="start" />
      </Tabs>

      {/* ── TAB 1: Balance de Comprobación ── */}
      {tabActiva === 0 && (
        <Box>
          <Button
            variant="contained" startIcon={cargando ? <CircularProgress size={16} color="inherit" /> : <IconCalculator size={18} />}
            onClick={generarBalanceComprobacion} disabled={cargando}
            sx={{ mb: 2 }}
          >
            {cargando ? 'Generando...' : 'Generar Balance de Comprobación'}
          </Button>

          {generadoComprobacion && (
            <Table size="small">
              <TableHead>
                <TableRow sx={{ bgcolor: '#e8f4fd' }}>
                  <TableCell width={140}><Typography fontWeight={700}>Código</Typography></TableCell>
                  <TableCell><Typography fontWeight={700}>Nombre de la Cuenta</Typography></TableCell>
                  <TableCell align="right" width={140}><Typography fontWeight={700}>Débitos</Typography></TableCell>
                  <TableCell align="right" width={140}><Typography fontWeight={700}>Créditos</Typography></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filasComprobacion.map((fila, idx) => (
                  <TableRow key={idx} hover>
                    <TableCell><Typography variant="body2" fontFamily="monospace">{fila.codigo}</Typography></TableCell>
                    <TableCell>{fila.nombre}</TableCell>
                    <TableCell align="right" sx={{ color: '#1565c0' }}>{fila.totalDebe.toFixed(2)}</TableCell>
                    <TableCell align="right" sx={{ color: '#c62828' }}>{fila.totalHaber.toFixed(2)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}

          {generadoComprobacion && (
            <Table size="small">
              <TableBody>
                <TableRow sx={{ bgcolor: '#e8f5e9' }}>
                  <TableCell width={140} />
                  <TableCell><Typography fontWeight={700}>TOTALES</Typography></TableCell>
                  <TableCell align="right" width={140}><Typography fontWeight={700} color="#1565c0">{totalDebeComp.toFixed(2)}</Typography></TableCell>
                  <TableCell align="right" width={140}><Typography fontWeight={700} color="#c62828">{totalHaberComp.toFixed(2)}</Typography></TableCell>
                </TableRow>
                <TableRow>
                  <TableCell colSpan={4} align="center">
                    {Math.abs(totalDebeComp - totalHaberComp) < 0.01
                      ? <Typography color="success.main" fontWeight={700}>✓ Balance cuadrado (Débitos = Créditos)</Typography>
                      : <Typography color="error.main" fontWeight={700}>⚠ Balance no cuadrado — diferencia: {(totalDebeComp - totalHaberComp).toFixed(2)}</Typography>
                    }
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          )}
        </Box>
      )}

      {/* ── TAB 2: Balance General ── */}
      {tabActiva === 1 && (
        <Box>
          <Button
            variant="contained" startIcon={cargando ? <CircularProgress size={16} color="inherit" /> : <IconReport size={18} />}
            onClick={generarBalanceGeneral} disabled={cargando}
            sx={{ mb: 2 }}
          >
            {cargando ? 'Generando...' : 'Generar Balance General'}
          </Button>

          {generadoBalance && (
            <>
              {tiposUnicos.map(tipo => {
                const filasTipo = filasBalance.filter(f => f.tipo === tipo);
                const totalTipo = filasTipo.reduce((s, f) => s + f.saldo, 0);
                return (
                  <Box key={tipo} sx={{ mb: 3 }}>
                    <Typography variant="subtitle1" fontWeight={700} sx={{ bgcolor: '#e8f4fd', px: 2, py: 1, borderRadius: 1, mb: 1 }}>
                      {tipo}
                    </Typography>
                    <Table size="small">
                      <TableHead>
                        <TableRow sx={{ bgcolor: '#f8fafc' }}>
                          <TableCell width={150}>Código</TableCell>
                          <TableCell>Nombre</TableCell>
                          <TableCell align="right" width={140}>Saldo Deudor</TableCell>
                          <TableCell align="right" width={140}>Saldo Acreedor</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {filasTipo.map((fila, idx) => (
                          <TableRow key={idx} hover>
                            <TableCell><Typography variant="body2" fontFamily="monospace">{fila.codigo}</Typography></TableCell>
                            <TableCell>{'  '.repeat((fila.nivel - 1))}{fila.nombre}</TableCell>
                            <TableCell align="right" sx={{ color: fila.saldo > 0 ? '#1565c0' : 'inherit' }}>
                              {fila.saldo > 0 ? fila.saldo.toFixed(2) : ''}
                            </TableCell>
                            <TableCell align="right" sx={{ color: fila.saldo < 0 ? '#c62828' : 'inherit' }}>
                              {fila.saldo < 0 ? Math.abs(fila.saldo).toFixed(2) : ''}
                            </TableCell>
                          </TableRow>
                        ))}
                        <TableRow sx={{ bgcolor: '#f0f4ff' }}>
                          <TableCell colSpan={2}><Typography fontWeight={700} align="right">Subtotal {tipo}</Typography></TableCell>
                          <TableCell align="right"><Typography fontWeight={700} color="#1565c0">{totalTipo > 0 ? totalTipo.toFixed(2) : ''}</Typography></TableCell>
                          <TableCell align="right"><Typography fontWeight={700} color="#c62828">{totalTipo < 0 ? Math.abs(totalTipo).toFixed(2) : ''}</Typography></TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </Box>
                );
              })}

              <Table size="small">
                <TableBody>
                  <TableRow sx={{ bgcolor: '#e8f5e9' }}>
                    <TableCell colSpan={2}><Typography fontWeight={700} align="right" sx={{ fontSize: '1rem' }}>TOTALES GENERALES</Typography></TableCell>
                    <TableCell align="right" width={140}><Typography fontWeight={700} color="#1565c0" sx={{ fontSize: '1rem' }}>{totalSaldoDeudor.toFixed(2)}</Typography></TableCell>
                    <TableCell align="right" width={140}><Typography fontWeight={700} color="#c62828" sx={{ fontSize: '1rem' }}>{totalSaldoAcreedor.toFixed(2)}</Typography></TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </>
          )}
        </Box>
      )}
    </MainCard>
  );
};

export default BalancesPage;
