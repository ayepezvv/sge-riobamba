// ============================================================
// Servicio API — Módulo Financiero (AR/AP)
// Base URL: /api/financiero/
// ============================================================
import axios from 'utils/axios';
import {
  TipoDocumento, TipoDocumentoCrear,
  ResumenFactura, Factura, FacturaCrear,
  Pago, PagoCrear,
  CierreRecaudacion, CierreRecaudacionCrear,
} from 'types/financiero';

const BASE = '/api/financiero';

// ── Tipos de Documento ───────────────────────────────────────
export const listarTiposDocumento = (soloActivos = true): Promise<TipoDocumento[]> =>
  axios.get(`${BASE}/tipos-documento`, { params: { solo_activos: soloActivos } }).then(r => r.data);

export const crearTipoDocumento = (datos: TipoDocumentoCrear): Promise<TipoDocumento> =>
  axios.post(`${BASE}/tipos-documento`, datos).then(r => r.data);

// ── Facturas ─────────────────────────────────────────────────
export const listarFacturas = (params?: {
  tipo?: string;
  estado?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  tercero_id?: number;
  skip?: number;
  limit?: number;
}): Promise<ResumenFactura[]> =>
  axios.get(`${BASE}/facturas`, { params }).then(r => r.data);

export const obtenerFactura = (id: number): Promise<Factura> =>
  axios.get(`${BASE}/facturas/${id}`).then(r => r.data);

export const crearFactura = (datos: FacturaCrear): Promise<Factura> =>
  axios.post(`${BASE}/facturas`, datos).then(r => r.data);

export const aprobarFactura = (id: number, numero?: string): Promise<Factura> =>
  axios.post(`${BASE}/facturas/${id}/aprobar`, { numero }).then(r => r.data);

export const anularFactura = (id: number, motivoAnulacion: string): Promise<Factura> =>
  axios.post(`${BASE}/facturas/${id}/anular`, { motivo_anulacion: motivoAnulacion }).then(r => r.data);

// ── Pagos ────────────────────────────────────────────────────
export const listarPagos = (params?: {
  tipo?: string;
  estado?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  tercero_id?: number;
  skip?: number;
  limit?: number;
}): Promise<Pago[]> =>
  axios.get(`${BASE}/pagos`, { params }).then(r => r.data);

export const obtenerPago = (id: number): Promise<Pago> =>
  axios.get(`${BASE}/pagos/${id}`).then(r => r.data);

export const crearPago = (datos: PagoCrear): Promise<Pago> =>
  axios.post(`${BASE}/pagos`, datos).then(r => r.data);

export const confirmarPago = (id: number, numero?: string): Promise<Pago> =>
  axios.post(`${BASE}/pagos/${id}/confirmar`, { numero }).then(r => r.data);

export const anularPago = (id: number, motivoAnulacion: string): Promise<Pago> =>
  axios.post(`${BASE}/pagos/${id}/anular`, { motivo_anulacion: motivoAnulacion }).then(r => r.data);

// ── Cierres de Recaudación ───────────────────────────────────
export const listarCierresRecaudacion = (params?: { fecha_inicio?: string; fecha_fin?: string }): Promise<CierreRecaudacion[]> =>
  axios.get(`${BASE}/cierres-recaudacion`, { params }).then(r => r.data);

export const obtenerCierreRecaudacion = (id: number): Promise<CierreRecaudacion> =>
  axios.get(`${BASE}/cierres-recaudacion/${id}`).then(r => r.data);

export const crearCierreRecaudacion = (datos: CierreRecaudacionCrear): Promise<CierreRecaudacion> =>
  axios.post(`${BASE}/cierres-recaudacion`, datos).then(r => r.data);
