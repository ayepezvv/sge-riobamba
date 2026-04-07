// ============================================================
// Servicio API — Módulo Inventario / Existencias
// Base URL: /api/inventario/
// ============================================================
import axios from "utils/axios";
import {
  CuentaContableInventario,
  Destino, Encargado, Proveedor, UnidadGestion,
  ArticuloListado, Articulo,
  MovimientoListado, Movimiento,
  LineaKardex,
  ResumenAnualInventario,
} from "types/inventario";

const BASE = "/api/inventario";

// ── Resumen ───────────────────────────────────────────────────
export const obtenerResumen = (): Promise<ResumenAnualInventario[]> =>
  axios.get(`${BASE}/resumen`).then((r) => r.data);

// ── Cuentas Contables ─────────────────────────────────────────
export const listarCuentasInventario = (): Promise<CuentaContableInventario[]> =>
  axios.get(`${BASE}/cuentas`).then((r) => r.data);

// ── Artículos ─────────────────────────────────────────────────
export const listarArticulos = (params?: {
  anno?: number;
  activo?: boolean;
  buscar?: string;
  skip?: number;
  limit?: number;
}): Promise<ArticuloListado[]> =>
  axios.get(`${BASE}/articulos`, { params }).then((r) => r.data);

export const obtenerArticulo = (id: number): Promise<Articulo> =>
  axios.get(`${BASE}/articulos/${id}`).then((r) => r.data);

export const obtenerArticuloPorCodigo = (
  codigo: string,
  anno = 2025
): Promise<Articulo> =>
  axios.get(`${BASE}/articulos/codigo/${codigo}`, { params: { anno } }).then((r) => r.data);

// ── Movimientos ───────────────────────────────────────────────
export const listarMovimientos = (params?: {
  anno?: number;
  tipo?: "ENTRADA" | "SALIDA";
  skip?: number;
  limit?: number;
}): Promise<MovimientoListado[]> =>
  axios.get(`${BASE}/movimientos`, { params }).then((r) => r.data);

export const obtenerMovimiento = (id: number): Promise<Movimiento> =>
  axios.get(`${BASE}/movimientos/${id}`).then((r) => r.data);

export const obtenerDetalleMovimiento = (id: number): Promise<LineaKardex[]> =>
  axios.get(`${BASE}/movimientos/${id}/detalle`).then((r) => r.data);

// ── Kardex ────────────────────────────────────────────────────
export const obtenerKardex = (
  articuloId: number,
  params?: { anno?: number; skip?: number; limit?: number }
): Promise<LineaKardex[]> =>
  axios.get(`${BASE}/kardex/${articuloId}`, { params }).then((r) => r.data);

// ── Maestros ──────────────────────────────────────────────────
export const listarDestinos = (activo?: boolean): Promise<Destino[]> =>
  axios.get(`${BASE}/destinos`, { params: { activo } }).then((r) => r.data);

export const listarEncargados = (activo?: boolean): Promise<Encargado[]> =>
  axios.get(`${BASE}/encargados`, { params: { activo } }).then((r) => r.data);

export const listarProveedores = (params?: {
  activo?: boolean;
  buscar?: string;
}): Promise<Proveedor[]> =>
  axios.get(`${BASE}/proveedores`, { params }).then((r) => r.data);

export const listarUnidadesGestion = (): Promise<UnidadGestion[]> =>
  axios.get(`${BASE}/unidades-gestion`).then((r) => r.data);
