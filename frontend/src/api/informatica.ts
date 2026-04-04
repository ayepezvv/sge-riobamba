// ============================================================
// Servicio API — Módulo Informática
// Base URL: /api/informatica/
// ============================================================
import axios from 'utils/axios';

const BASE = '/api/informatica';

// ── Segmentos de Red ──────────────────────────────────────────
export const listarSegmentos = () =>
  axios.get(`${BASE}/segmentos`).then(r => r.data);

export const crearSegmento = (datos: any) =>
  axios.post(`${BASE}/segmentos`, datos).then(r => r.data);

// ── IPs ───────────────────────────────────────────────────────
export const listarIpsPorSegmento = (segmentoId: number) =>
  axios.get(`${BASE}/segmentos/${segmentoId}/ips`).then(r => r.data);

export const crearIp = (datos: any) =>
  axios.post(`${BASE}/ips`, datos).then(r => r.data);

export const eliminarIp = (id: number) =>
  axios.delete(`${BASE}/ips/${id}`).then(r => r.data);
