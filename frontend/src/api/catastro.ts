// ============================================================
// Servicio API — Módulo Catastro
// Base URL: /api/ciudadanos/, /api/comercial/
// ============================================================
import axios from 'utils/axios';

// ── Ciudadanos ────────────────────────────────────────────────
export const listarCiudadanos = () =>
  axios.get('/api/ciudadanos/').then(r => r.data);

export const crearCiudadano = (datos: any) =>
  axios.post('/api/ciudadanos/', datos).then(r => r.data);

export const actualizarCiudadano = (id: number, datos: any) =>
  axios.put(`/api/ciudadanos/${id}`, datos).then(r => r.data);

export const cambiarEstadoCiudadano = (id: number) =>
  axios.patch(`/api/ciudadanos/${id}/status`).then(r => r.data);

// ── Predios ───────────────────────────────────────────────────
export const listarPredios = () =>
  axios.get('/api/comercial/predios').then(r => r.data);

export const crearPredio = (datos: any) =>
  axios.post('/api/comercial/predios', datos).then(r => r.data);
