// ============================================================
// Servicio API — Módulo Bodega
// Base URL: /api/bodega/
// ============================================================
import axios from 'utils/axios';

const BASE = '/api/bodega';

// ── Categorías ────────────────────────────────────────────────
export const listarCategorias = () =>
  axios.get(`${BASE}/categorias`).then(r => r.data);

export const crearCategoria = (datos: any) =>
  axios.post(`${BASE}/categorias`, datos).then(r => r.data);

export const actualizarCategoria = (id: number, datos: any) =>
  axios.put(`${BASE}/categorias/${id}`, datos).then(r => r.data);

export const eliminarCategoria = (id: number) =>
  axios.delete(`${BASE}/categorias/${id}`).then(r => r.data);

// ── Activos ───────────────────────────────────────────────────
export const listarActivos = () =>
  axios.get(`${BASE}/activos`).then(r => r.data);

export const crearActivo = (datos: any) =>
  axios.post(`${BASE}/activos`, datos).then(r => r.data);
