// ============================================================
// Servicio API — Módulo Usuarios
// Base URL: /api/users/
// ============================================================
import axios from 'utils/axios';

const BASE = '/api/users';
const BASE_ROLES = '/api/roles';

// ── Usuarios ──────────────────────────────────────────────────
export const listarUsuarios = () =>
  axios.get(`${BASE}/`).then(r => r.data);

export const crearUsuario = (datos: any) =>
  axios.post(`${BASE}/`, datos).then(r => r.data);

export const actualizarUsuario = (id: number, datos: any) =>
  axios.put(`${BASE}/${id}`, datos).then(r => r.data);

export const cambiarEstadoUsuario = (id: number) =>
  axios.patch(`${BASE}/${id}/status`).then(r => r.data);

// ── Roles (reutiliza para asignación en formulario de usuario) ─
export const listarRoles = () =>
  axios.get(`${BASE_ROLES}/`).then(r => r.data);
