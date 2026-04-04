// ============================================================
// Servicio API — Módulo RRHH
// Base URL: /api/rrhh/
// ============================================================
import axios from 'utils/axios';

const BASE = '/api/rrhh';

// ── Empleados ─────────────────────────────────────────────────
export const listarEmpleados = () =>
  axios.get(`${BASE}/empleados`).then(r => r.data);

export const crearEmpleado = (datos: any) =>
  axios.post(`${BASE}/empleados`, datos).then(r => r.data);

export const crearHistorialEmpleado = (empleadoId: number, datos: any) =>
  axios.post(`${BASE}/empleados/${empleadoId}/historial`, datos).then(r => r.data);

export const desvincularEmpleado = (empleadoId: number) =>
  axios.delete(`${BASE}/empleados/${empleadoId}`).then(r => r.data);

// ── Áreas ─────────────────────────────────────────────────────
export const listarAreas = () =>
  axios.get(`${BASE}/areas`).then(r => r.data);

export const crearArea = (datos: any) =>
  axios.post(`${BASE}/areas`, datos).then(r => r.data);

export const actualizarArea = (id: number, datos: any) =>
  axios.put(`${BASE}/areas/${id}`, datos).then(r => r.data);

// ── Cargos ────────────────────────────────────────────────────
export const listarCargos = () =>
  axios.get(`${BASE}/cargos`).then(r => r.data);

export const crearCargo = (datos: any) =>
  axios.post(`${BASE}/cargos`, datos).then(r => r.data);

export const actualizarCargo = (id: number, datos: any) =>
  axios.put(`${BASE}/cargos/${id}`, datos).then(r => r.data);

// ── Escalas Salariales ────────────────────────────────────────
export const listarEscalasSalariales = () =>
  axios.get(`${BASE}/escalas-salariales`).then(r => r.data);

export const crearEscalaSalarial = (datos: any) =>
  axios.post(`${BASE}/escalas-salariales`, datos).then(r => r.data);

export const actualizarEscalaSalarial = (id: number, datos: any) =>
  axios.put(`${BASE}/escalas-salariales/${id}`, datos).then(r => r.data);

// ── Contratos ─────────────────────────────────────────────────
export const listarContratos = () =>
  axios.get(`${BASE}/contratos`).then(r => r.data);

export const crearContrato = (datos: any) =>
  axios.post(`${BASE}/contratos`, datos).then(r => r.data);

export const actualizarContrato = (id: number, datos: any) =>
  axios.put(`${BASE}/contratos/${id}`, datos).then(r => r.data);
