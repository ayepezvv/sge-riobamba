// ============================================================
// Servicio API — Módulo Administrativo
// Base URL: /administrativo/ (sin /api/ — ajustar si cambia el prefijo)
// ============================================================
import axios from 'utils/axios';

const BASE = '/administrativo';

export const listarEmpleadosAdministrativo = () =>
  axios.get(`${BASE}/empleados`).then(r => r.data);

export const listarUnidades = () =>
  axios.get(`${BASE}/unidades`).then(r => r.data);

export const listarPuestos = () =>
  axios.get(`${BASE}/puestos`).then(r => r.data);

export const crearEmpleadoAdministrativo = (datos: any) =>
  axios.post(`${BASE}/empleados`, datos).then(r => r.data);

export const eliminarEmpleadoAdministrativo = (id: number) =>
  axios.delete(`${BASE}/empleados/${id}`).then(r => r.data);

// También expuesto para el módulo de Informática
export const listarPersonalAdministrativo = () =>
  axios.get(`${BASE}/personal`).then(r => r.data);
