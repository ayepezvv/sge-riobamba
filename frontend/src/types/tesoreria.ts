// ============================================================
// Tipos TypeScript — Módulo Tesorería
// Nomenclatura en español conforme a Regla Arquitectónica 2
// ============================================================

// ── EntidadBancaria ─────────────────────────────────────────
export interface EntidadBancaria {
  id: number;
  codigo: string;
  nombre: string;
  sigla?: string;
  es_activa: boolean;
  creado_en: string;
  actualizado_en: string;
}

export interface EntidadBancariaCrear {
  codigo: string;
  nombre: string;
  sigla?: string;
  es_activa?: boolean;
}

// ── CuentaBancaria ──────────────────────────────────────────
export type TipoCuentaBancaria = 'CORRIENTE' | 'AHORROS' | 'RECAUDACION' | 'PAGOS';

export interface CuentaBancaria {
  id: number;
  entidad_bancaria_id: number;
  numero_cuenta: string;
  nombre: string;
  tipo: TipoCuentaBancaria;
  moneda: string;
  cuenta_contable_id?: number;
  saldo_inicial: number;
  es_activa: boolean;
  creado_en: string;
  actualizado_en: string;
}

export interface CuentaBancariaCrear {
  entidad_bancaria_id: number;
  numero_cuenta: string;
  nombre: string;
  tipo: TipoCuentaBancaria;
  moneda?: string;
  cuenta_contable_id?: number;
  saldo_inicial?: number;
  es_activa?: boolean;
}

// ── ExtractoBancario ────────────────────────────────────────
export type EstadoExtracto = 'BORRADOR' | 'CONFIRMADO';

export interface LineaExtracto {
  id: number;
  extracto_id: number;
  fecha: string;
  tipo_transaccion: string;
  referencia?: string;
  descripcion?: string;
  valor: number;
  esta_conciliada: boolean;
  creado_en: string;
}

export interface LineaExtractoCrear {
  fecha: string;
  tipo_transaccion: string;
  referencia?: string;
  descripcion?: string;
  valor: number;
}

export interface ExtractoBancario {
  id: number;
  cuenta_bancaria_id: number;
  referencia?: string;
  fecha_inicio: string;
  fecha_fin: string;
  saldo_inicial: number;
  saldo_final: number;
  estado: EstadoExtracto;
  creado_en: string;
  actualizado_en: string;
  lineas?: LineaExtracto[];
}

export interface ExtractoBancarioCrear {
  cuenta_bancaria_id: number;
  referencia?: string;
  fecha_inicio: string;
  fecha_fin: string;
  saldo_inicial?: number;
  saldo_final?: number;
  lineas?: LineaExtractoCrear[];
}

// ── ConciliacionBancaria ────────────────────────────────────
export type EstadoConciliacion = 'ABIERTA' | 'CERRADA';

export interface MarcaConciliacion {
  id: number;
  conciliacion_id: number;
  linea_extracto_id: number;
  monto: number;
  notas?: string;
  creado_en: string;
}

export interface MarcaConciliacionCrear {
  linea_extracto_id: number;
  monto: number;
  notas?: string;
}

export interface ConciliacionBancaria {
  id: number;
  cuenta_bancaria_id: number;
  extracto_id: number;
  fecha_inicio: string;
  fecha_fin: string;
  saldo_libro: number;
  saldo_extracto: number;
  estado: EstadoConciliacion;
  notas?: string;
  creado_en: string;
  actualizado_en: string;
  marcas?: MarcaConciliacion[];
}

export interface ConciliacionBancariaCrear {
  cuenta_bancaria_id: number;
  extracto_id: number;
  fecha_inicio: string;
  fecha_fin: string;
  saldo_libro: number;
  saldo_extracto: number;
  notas?: string;
}

// ── CajaChica ───────────────────────────────────────────────
export type EstadoCaja = 'ABIERTA' | 'CERRADA';
export type TipoMovimientoCaja = 'APERTURA' | 'EGRESO' | 'REPOSICION' | 'CIERRE';

export interface MovimientoCaja {
  id: number;
  caja_id: number;
  tipo: TipoMovimientoCaja;
  fecha: string;
  descripcion: string;
  valor: number;
  referencia?: string;
  creado_en: string;
}

export interface MovimientoCajaCrear {
  tipo: TipoMovimientoCaja;
  fecha: string;
  descripcion: string;
  valor: number;
  referencia?: string;
}

export interface CajaChica {
  id: number;
  nombre: string;
  monto_autorizado: number;
  saldo_actual: number;
  responsable?: string;
  cuenta_contable_id?: number;
  estado: EstadoCaja;
  creado_en: string;
  actualizado_en: string;
}

export interface CajaChicaCrear {
  nombre: string;
  monto_autorizado: number;
  responsable?: string;
  cuenta_contable_id?: number;
}
