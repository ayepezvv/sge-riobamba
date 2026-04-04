// ============================================================
// Servicio API — Módulo Roles y Permisos
// Base URL: /api/roles/, /api/permissions/
// ============================================================
import axios from 'utils/axios';

const BASE = '/api/roles';
const BASE_PERMISOS = '/api/permissions';

// ── Roles ─────────────────────────────────────────────────────
export const listarRoles = () =>
  axios.get(`${BASE}/`).then(r => r.data);

export const crearRol = (datos: any) =>
  axios.post(`${BASE}/`, datos).then(r => r.data);

export const actualizarRol = (id: number, datos: any) =>
  axios.put(`${BASE}/${id}`, datos).then(r => r.data);

// ── Permisos ──────────────────────────────────────────────────
export const listarPermisos = () =>
  axios.get(`${BASE_PERMISOS}/`).then(r => r.data);
