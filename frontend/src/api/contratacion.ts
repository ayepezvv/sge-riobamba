// ============================================================
// Servicio API — Módulo Contratación
// Base URL: /api/contratacion/
// ============================================================
import axios from 'utils/axios';

const BASE = '/api/contratacion';

// ── Tipos de Proceso ──────────────────────────────────────────
export const listarTiposProceso = () =>
  axios.get(`${BASE}/tipos`).then(r => r.data);

export const crearTipoProceso = (datos: any) =>
  axios.post(`${BASE}/tipos`, datos).then(r => r.data);

export const actualizarTipoProceso = (id: number, datos: any) =>
  axios.put(`${BASE}/tipos/${id}`, datos).then(r => r.data);

// ── Plantillas ────────────────────────────────────────────────
export const listarPlantillas = (params?: { tipo_proceso_id?: number; is_activa?: boolean }) =>
  axios.get(`${BASE}/plantillas`, { params }).then(r => r.data);

export const obtenerEsquemaPlantilla = (plantillaId: number) =>
  axios.get(`${BASE}/plantillas/${plantillaId}/esquema`).then(r => r.data);

export const subirPlantilla = (formData: FormData) =>
  axios.post(`${BASE}/plantillas/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }).then(r => r.data);

// ── Procesos / Documentos ─────────────────────────────────────
export const listarProcesos = () =>
  axios.get(`${BASE}/procesos`).then(r => r.data);

export const crearProceso = (datos: any) =>
  axios.post(`${BASE}/procesos`, datos).then(r => r.data);

export const obtenerProceso = (id: number) =>
  axios.get(`${BASE}/procesos/${id}`).then(r => r.data);

export const obtenerDatosDocumento = (documentoId: number) =>
  axios.get(`${BASE}/documento/${documentoId}/datos`).then(r => r.data);

// Devuelve respuesta completa para acceder a headers del blob
export const crearDocumento = (datos: any) =>
  axios.post(`${BASE}/documento`, datos, { responseType: 'blob' });

// Devuelve la respuesta completa (no solo .data) para acceder a headers blob
export const regenerarDocumento = (documentoId: number, datos: any) =>
  axios.put(`${BASE}/documento/${documentoId}/regenerar`, { datos }, { responseType: 'blob' });

export const descargarDocumento = (documentoId: number) =>
  axios.get(`${BASE}/documento/${documentoId}/descargar`, { responseType: 'blob' });
