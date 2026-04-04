// ============================================================
// Servicio API — Módulo Tesorería
// Base URL: /api/tesoreria/
// ============================================================
import axios from 'utils/axios';
import {
  EntidadBancaria, EntidadBancariaCrear,
  CuentaBancaria, CuentaBancariaCrear,
  ExtractoBancario, ExtractoBancarioCrear,
  ConciliacionBancaria, ConciliacionBancariaCrear, MarcaConciliacionCrear, MarcaConciliacion,
  CajaChica, CajaChicaCrear, MovimientoCaja, MovimientoCajaCrear,
} from 'types/tesoreria';

const BASE = '/api/tesoreria';

// ── Entidades Bancarias ──────────────────────────────────────
export const listarEntidadesBancarias = (soloActivas = true): Promise<EntidadBancaria[]> =>
  axios.get(`${BASE}/entidades-bancarias`, { params: { solo_activas: soloActivas } }).then(r => r.data);

export const crearEntidadBancaria = (datos: EntidadBancariaCrear): Promise<EntidadBancaria> =>
  axios.post(`${BASE}/entidades-bancarias`, datos).then(r => r.data);

export const actualizarEntidadBancaria = (id: number, datos: Partial<EntidadBancariaCrear>): Promise<EntidadBancaria> =>
  axios.put(`${BASE}/entidades-bancarias/${id}`, datos).then(r => r.data);

// ── Cuentas Bancarias ────────────────────────────────────────
export const listarCuentasBancarias = (params?: { entidad_bancaria_id?: number; solo_activas?: boolean }): Promise<CuentaBancaria[]> =>
  axios.get(`${BASE}/cuentas-bancarias`, { params }).then(r => r.data);

export const obtenerCuentaBancaria = (id: number): Promise<CuentaBancaria> =>
  axios.get(`${BASE}/cuentas-bancarias/${id}`).then(r => r.data);

export const crearCuentaBancaria = (datos: CuentaBancariaCrear): Promise<CuentaBancaria> =>
  axios.post(`${BASE}/cuentas-bancarias`, datos).then(r => r.data);

export const actualizarCuentaBancaria = (id: number, datos: Partial<CuentaBancariaCrear>): Promise<CuentaBancaria> =>
  axios.put(`${BASE}/cuentas-bancarias/${id}`, datos).then(r => r.data);

// ── Extractos Bancarios ──────────────────────────────────────
export const listarExtractos = (params?: { cuenta_bancaria_id?: number; estado?: string }): Promise<ExtractoBancario[]> =>
  axios.get(`${BASE}/extractos`, { params }).then(r => r.data);

export const obtenerExtracto = (id: number): Promise<ExtractoBancario> =>
  axios.get(`${BASE}/extractos/${id}`).then(r => r.data);

export const crearExtracto = (datos: ExtractoBancarioCrear): Promise<ExtractoBancario> =>
  axios.post(`${BASE}/extractos`, datos).then(r => r.data);

export const confirmarExtracto = (id: number): Promise<ExtractoBancario> =>
  axios.post(`${BASE}/extractos/${id}/confirmar`).then(r => r.data);

// ── Conciliaciones Bancarias ─────────────────────────────────
export const listarConciliaciones = (params?: { cuenta_bancaria_id?: number; estado?: string }): Promise<ConciliacionBancaria[]> =>
  axios.get(`${BASE}/conciliaciones`, { params }).then(r => r.data);

export const obtenerConciliacion = (id: number): Promise<ConciliacionBancaria> =>
  axios.get(`${BASE}/conciliaciones/${id}`).then(r => r.data);

export const crearConciliacion = (datos: ConciliacionBancariaCrear): Promise<ConciliacionBancaria> =>
  axios.post(`${BASE}/conciliaciones`, datos).then(r => r.data);

export const cerrarConciliacion = (id: number): Promise<ConciliacionBancaria> =>
  axios.post(`${BASE}/conciliaciones/${id}/cerrar`).then(r => r.data);

export const agregarMarcaConciliacion = (id: number, datos: MarcaConciliacionCrear): Promise<MarcaConciliacion> =>
  axios.post(`${BASE}/conciliaciones/${id}/marcas`, datos).then(r => r.data);

// ── Cajas Chicas ─────────────────────────────────────────────
export const listarCajas = (): Promise<CajaChica[]> =>
  axios.get(`${BASE}/cajas`).then(r => r.data);

export const crearCaja = (datos: CajaChicaCrear): Promise<CajaChica> =>
  axios.post(`${BASE}/cajas`, datos).then(r => r.data);

export const registrarMovimientoCaja = (cajaId: number, datos: MovimientoCajaCrear): Promise<MovimientoCaja> =>
  axios.post(`${BASE}/cajas/${cajaId}/movimientos`, datos).then(r => r.data);

export const listarMovimientosCaja = (cajaId: number): Promise<MovimientoCaja[]> =>
  axios.get(`${BASE}/cajas/${cajaId}/movimientos`).then(r => r.data);
