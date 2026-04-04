// ============================================================
// Servicio API — Módulo Presupuesto
// Base URL: /api/presupuesto/
// ============================================================
import axios from 'utils/axios';
import {
  PartidaPresupuestaria, PartidaPresupuestariaCrear, PartidaPresupuestariaActualizar,
  PresupuestoAnual, PresupuestoAnualCrear,
  AsignacionPresupuestaria, AsignacionPresupuestariaCrear,
  ReformaPresupuestaria, ReformaPresupuestariaCrear,
  CertificadoPresupuestario, CertificadoPresupuestarioCrear, CertificadoPresupuestarioEstado,
  Compromiso, CompromisoCrear,
  Devengado, DevengadoCrear,
  EjecucionPresupuestaria,
} from 'types/presupuesto';

const BASE = '/api/presupuesto';

// ── Partidas Presupuestarias ─────────────────────────────────
export const listarPartidas = (params?: { tipo?: string; solo_hojas?: boolean }): Promise<PartidaPresupuestaria[]> =>
  axios.get(`${BASE}/partidas`, { params }).then(r => r.data);

export const obtenerPartida = (id: number): Promise<PartidaPresupuestaria> =>
  axios.get(`${BASE}/partidas/${id}`).then(r => r.data);

export const crearPartida = (datos: PartidaPresupuestariaCrear): Promise<PartidaPresupuestaria> =>
  axios.post(`${BASE}/partidas`, datos).then(r => r.data);

export const actualizarPartida = (id: number, datos: PartidaPresupuestariaActualizar): Promise<PartidaPresupuestaria> =>
  axios.put(`${BASE}/partidas/${id}`, datos).then(r => r.data);

// ── Presupuestos Anuales ─────────────────────────────────────
export const listarPresupuestos = (): Promise<PresupuestoAnual[]> =>
  axios.get(`${BASE}/presupuestos`).then(r => r.data);

export const obtenerPresupuesto = (id: number): Promise<PresupuestoAnual> =>
  axios.get(`${BASE}/presupuestos/${id}`).then(r => r.data);

export const crearPresupuesto = (datos: PresupuestoAnualCrear): Promise<PresupuestoAnual> =>
  axios.post(`${BASE}/presupuestos`, datos).then(r => r.data);

// ── Asignaciones Presupuestarias ─────────────────────────────
export const listarAsignaciones = (params?: { id_presupuesto?: number }): Promise<AsignacionPresupuestaria[]> =>
  axios.get(`${BASE}/asignaciones`, { params }).then(r => r.data);

export const crearAsignacion = (datos: AsignacionPresupuestariaCrear): Promise<AsignacionPresupuestaria> =>
  axios.post(`${BASE}/asignaciones`, datos).then(r => r.data);

// ── Reformas Presupuestarias ─────────────────────────────────
export const listarReformas = (params?: { id_asignacion?: number }): Promise<ReformaPresupuestaria[]> =>
  axios.get(`${BASE}/reformas`, { params }).then(r => r.data);

export const crearReforma = (datos: ReformaPresupuestariaCrear): Promise<ReformaPresupuestaria> =>
  axios.post(`${BASE}/reformas`, datos).then(r => r.data);

// ── Certificados Presupuestarios ─────────────────────────────
export const listarCertificados = (params?: { id_asignacion?: number; estado?: string }): Promise<CertificadoPresupuestario[]> =>
  axios.get(`${BASE}/certificados`, { params }).then(r => r.data);

export const obtenerCertificado = (id: number): Promise<CertificadoPresupuestario> =>
  axios.get(`${BASE}/certificados/${id}`).then(r => r.data);

export const crearCertificado = (datos: CertificadoPresupuestarioCrear): Promise<CertificadoPresupuestario> =>
  axios.post(`${BASE}/certificados`, datos).then(r => r.data);

export const cambiarEstadoCertificado = (id: number, datos: CertificadoPresupuestarioEstado): Promise<CertificadoPresupuestario> =>
  axios.patch(`${BASE}/certificados/${id}/estado`, datos).then(r => r.data);

// ── Compromisos ──────────────────────────────────────────────
export const listarCompromisos = (params?: { estado?: string }): Promise<Compromiso[]> =>
  axios.get(`${BASE}/compromisos`, { params }).then(r => r.data);

export const crearCompromiso = (datos: CompromisoCrear): Promise<Compromiso> =>
  axios.post(`${BASE}/compromisos`, datos).then(r => r.data);

export const anularCompromiso = (id: number, motivo: string): Promise<Compromiso> =>
  axios.patch(`${BASE}/compromisos/${id}/anular`, null, { params: { motivo } }).then(r => r.data);

// ── Devengados ───────────────────────────────────────────────
export const listarDevengados = (params?: { estado?: string }): Promise<Devengado[]> =>
  axios.get(`${BASE}/devengados`, { params }).then(r => r.data);

export const crearDevengado = (datos: DevengadoCrear): Promise<Devengado> =>
  axios.post(`${BASE}/devengados`, datos).then(r => r.data);

// ── Ejecución Presupuestaria ─────────────────────────────────
export const obtenerEjecucion = (anioFiscal: number): Promise<EjecucionPresupuestaria[]> =>
  axios.get(`${BASE}/ejecucion/${anioFiscal}`).then(r => r.data);
