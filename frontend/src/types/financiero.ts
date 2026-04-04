// ============================================================
// Tipos TypeScript — Módulo Financiero (AR/AP)
// Nomenclatura en español conforme a Regla Arquitectónica 2
// ============================================================

// ── TipoDocumento ───────────────────────────────────────────
export type TipoDocumentoTipo =
  | 'FACTURA'
  | 'NOTA_CREDITO'
  | 'NOTA_DEBITO'
  | 'LIQUIDACION'
  | 'PROFORMA'
  | 'CERTIFICADO_PRESUPUESTARIO';

export interface TipoDocumento {
  id: number;
  codigo: string;
  nombre: string;
  tipo: TipoDocumentoTipo;
  secuencia_prefijo?: string;
  secuencia_siguiente: number;
  es_activo: boolean;
  creado_en: string;
  actualizado_en: string;
}

export interface TipoDocumentoCrear {
  codigo: string;
  nombre: string;
  tipo: TipoDocumentoTipo;
  secuencia_prefijo?: string;
  es_activo?: boolean;
}

// ── Factura ─────────────────────────────────────────────────
export type EstadoFactura = 'BORRADOR' | 'APROBADA' | 'ANULADA';
export type TipoFactura = 'CLIENTE' | 'PROVEEDOR';
export type TipoImpuesto = 'IVA_15' | 'IVA_12' | 'IVA_5' | 'IVA_0' | 'EXENTO' | 'ICE';

export interface LineaFactura {
  id: number;
  factura_id: number;
  orden: number;
  descripcion: string;
  cuenta_contable_id?: number;
  cantidad: number;
  precio_unitario: number;
  descuento_linea: number;
  tipo_impuesto: TipoImpuesto;
  porcentaje_impuesto: number;
  subtotal_linea: number;
  valor_impuesto: number;
  total_linea: number;
  creado_en: string;
}

export interface LineaFacturaCrear {
  orden?: number;
  descripcion: string;
  cuenta_contable_id?: number;
  cantidad?: number;
  precio_unitario: number;
  descuento_linea?: number;
  tipo_impuesto?: TipoImpuesto;
  porcentaje_impuesto?: number;
}

export interface Factura {
  id: number;
  numero: string;
  tipo_documento_id: number;
  tipo: TipoFactura;
  tercero_id?: number;
  nombre_tercero: string;
  identificacion_tercero: string;
  fecha_emision: string;
  fecha_vencimiento?: string;
  clave_acceso_sri?: string;
  numero_autorizacion_sri?: string;
  observaciones?: string;
  estado: EstadoFactura;
  subtotal: number;
  descuento: number;
  base_imponible: number;
  total_iva: number;
  total: number;
  saldo_pendiente: number;
  asiento_contable_id?: number;
  lineas: LineaFactura[];
  creado_en: string;
  actualizado_en: string;
}

export interface ResumenFactura {
  id: number;
  numero: string;
  tipo: TipoFactura;
  estado: EstadoFactura;
  nombre_tercero: string;
  identificacion_tercero: string;
  fecha_emision: string;
  total: number;
  saldo_pendiente: number;
}

export interface FacturaCrear {
  tipo_documento_id: number;
  tipo: TipoFactura;
  tercero_id?: number;
  nombre_tercero: string;
  identificacion_tercero: string;
  fecha_emision: string;
  fecha_vencimiento?: string;
  clave_acceso_sri?: string;
  numero_autorizacion_sri?: string;
  observaciones?: string;
  lineas: LineaFacturaCrear[];
}

// ── Pago ─────────────────────────────────────────────────────
export type EstadoPago = 'BORRADOR' | 'CONFIRMADO' | 'ANULADO';
export type TipoPago = 'CLIENTE' | 'PROVEEDOR';
export type MetodoPago = 'EFECTIVO' | 'CHEQUE' | 'TRANSFERENCIA' | 'SPI' | 'BCE' | 'NOTA_CREDITO';

export interface LineaPago {
  id: number;
  pago_id: number;
  factura_id: number;
  monto_aplicado: number;
  creado_en: string;
}

export interface LineaPagoCrear {
  factura_id: number;
  monto_aplicado: number;
}

export interface Pago {
  id: number;
  numero: string;
  tipo: TipoPago;
  tercero_id?: number;
  nombre_tercero: string;
  identificacion_tercero: string;
  fecha_pago: string;
  tipo_pago: MetodoPago;
  cuenta_bancaria_id?: number;
  monto_total: number;
  referencia_bancaria?: string;
  observaciones?: string;
  estado: EstadoPago;
  asiento_contable_id?: number;
  asiento_traslado_id?: number;
  lineas: LineaPago[];
  creado_en: string;
  actualizado_en: string;
}

export interface PagoCrear {
  tipo: TipoPago;
  tercero_id?: number;
  nombre_tercero: string;
  identificacion_tercero: string;
  fecha_pago: string;
  tipo_pago: MetodoPago;
  cuenta_bancaria_id?: number;
  monto_total: number;
  referencia_bancaria?: string;
  observaciones?: string;
  lineas?: LineaPagoCrear[];
}

// ── CierreRecaudacion ────────────────────────────────────────
export interface CierreRecaudacion {
  id: number;
  fecha: string;
  total_recaudado: number;
  numero_transacciones: number;
  observaciones?: string;
  asiento_recaudacion_id?: number;
  asiento_traslado_bce_id?: number;
  creado_en: string;
}

export interface CierreRecaudacionCrear {
  fecha: string;
  total_recaudado: number;
  numero_transacciones?: number;
  observaciones?: string;
}
