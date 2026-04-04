// ============================================================
// Servicio API — Módulo Contabilidad
// Base URL: /api/contabilidad/
// ============================================================
import axios from 'utils/axios';
import {
  TipoCuenta, TipoCuentaCrear,
  CuentaContable, CuentaContableArbol, CuentaContableCrear, SaldoCuenta,
  Diario, DiarioCrear,
  PeriodoContable, PeriodoContableCrear,
  AsientoContable, AsientoContableCrear,
} from 'types/contabilidad';

const BASE = '/api/contabilidad';

// ── Tipos de Cuenta ──────────────────────────────────────────
export const listarTiposCuenta = (): Promise<TipoCuenta[]> =>
  axios.get(`${BASE}/tipos-cuenta`).then(r => r.data);

export const crearTipoCuenta = (datos: TipoCuentaCrear): Promise<TipoCuenta> =>
  axios.post(`${BASE}/tipos-cuenta`, datos).then(r => r.data);

export const actualizarTipoCuenta = (id: number, datos: Partial<TipoCuentaCrear>): Promise<TipoCuenta> =>
  axios.put(`${BASE}/tipos-cuenta/${id}`, datos).then(r => r.data);

// ── Cuentas Contables ────────────────────────────────────────
export const listarCuentas = (params?: { estado?: string; tipo_cuenta_id?: number }): Promise<CuentaContable[]> =>
  axios.get(`${BASE}/cuentas`, { params }).then(r => r.data);

export const obtenerArbolCuentas = (): Promise<CuentaContableArbol[]> =>
  axios.get(`${BASE}/cuentas/arbol`).then(r => r.data);

export const obtenerCuenta = (id: number): Promise<CuentaContable> =>
  axios.get(`${BASE}/cuentas/${id}`).then(r => r.data);

export const crearCuenta = (datos: CuentaContableCrear): Promise<CuentaContable> =>
  axios.post(`${BASE}/cuentas`, datos).then(r => r.data);

export const actualizarCuenta = (id: number, datos: Partial<CuentaContableCrear>): Promise<CuentaContable> =>
  axios.put(`${BASE}/cuentas/${id}`, datos).then(r => r.data);

export const obtenerSaldoCuenta = (id: number, params?: { fecha_inicio?: string; fecha_fin?: string }): Promise<SaldoCuenta> =>
  axios.get(`${BASE}/cuentas/${id}/saldo`, { params }).then(r => r.data);

// ── Diarios ──────────────────────────────────────────────────
export const listarDiarios = (): Promise<Diario[]> =>
  axios.get(`${BASE}/diarios`).then(r => r.data);

export const crearDiario = (datos: DiarioCrear): Promise<Diario> =>
  axios.post(`${BASE}/diarios`, datos).then(r => r.data);

export const actualizarDiario = (id: number, datos: Partial<DiarioCrear>): Promise<Diario> =>
  axios.put(`${BASE}/diarios/${id}`, datos).then(r => r.data);

// ── Períodos Contables ────────────────────────────────────────
export const listarPeriodos = (): Promise<PeriodoContable[]> =>
  axios.get(`${BASE}/periodos`).then(r => r.data);

export const crearPeriodo = (datos: PeriodoContableCrear): Promise<PeriodoContable> =>
  axios.post(`${BASE}/periodos`, datos).then(r => r.data);

export const cambiarEstadoPeriodo = (id: number, estado: string): Promise<PeriodoContable> =>
  axios.patch(`${BASE}/periodos/${id}/estado`, { estado }).then(r => r.data);

// ── Asientos Contables ────────────────────────────────────────
export const listarAsientos = (params?: {
  periodo_id?: number;
  diario_id?: number;
  estado?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}): Promise<AsientoContable[]> =>
  axios.get(`${BASE}/asientos`, { params }).then(r => r.data);

export const obtenerAsiento = (id: number): Promise<AsientoContable> =>
  axios.get(`${BASE}/asientos/${id}`).then(r => r.data);

export const crearAsiento = (datos: AsientoContableCrear): Promise<AsientoContable> =>
  axios.post(`${BASE}/asientos`, datos).then(r => r.data);

export const publicarAsiento = (id: number): Promise<AsientoContable> =>
  axios.patch(`${BASE}/asientos/${id}/publicar`, {}).then(r => r.data);

export const anularAsiento = (id: number, motivo_anulacion: string): Promise<AsientoContable> =>
  axios.patch(`${BASE}/asientos/${id}/anular`, { motivo_anulacion }).then(r => r.data);
