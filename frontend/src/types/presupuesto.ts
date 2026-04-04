// ============================================================
// Tipos TypeScript — Módulo Presupuesto
// Nomenclatura en español conforme a Regla Arquitectónica 2
// ============================================================

// ── PartidaPresupuestaria ────────────────────────────────────
export type TipoPartida = 'INGRESO' | 'GASTO';

export interface PartidaPresupuestaria {
  id_partida: number;
  codigo: string;
  nombre: string;
  descripcion?: string;
  tipo: TipoPartida;
  nivel: number;
  es_hoja: boolean;
  id_partida_padre?: number;
  estado: string;
  creado_en: string;
}

export interface PartidaPresupuestariaCrear {
  codigo: string;
  nombre: string;
  descripcion?: string;
  tipo: TipoPartida;
  nivel: number;
  es_hoja?: boolean;
  id_partida_padre?: number;
  estado?: string;
}

export interface PartidaPresupuestariaActualizar {
  nombre?: string;
  descripcion?: string;
  es_hoja?: boolean;
  estado?: string;
}

// ── PresupuestoAnual ─────────────────────────────────────────
export interface PresupuestoAnual {
  id_presupuesto: number;
  anio_fiscal: number;
  denominacion: string;
  monto_inicial: number;
  monto_codificado: number;
  estado: string;
  fecha_aprobacion?: string;
  resolucion_aprobacion?: string;
  observaciones?: string;
  creado_en: string;
}

export interface PresupuestoAnualCrear {
  anio_fiscal: number;
  denominacion: string;
  monto_inicial?: number;
  observaciones?: string;
}

// ── AsignacionPresupuestaria ─────────────────────────────────
export interface AsignacionPresupuestaria {
  id_asignacion: number;
  id_presupuesto: number;
  id_partida: number;
  monto_inicial: number;
  monto_codificado: number;
  monto_comprometido: number;
  monto_devengado: number;
  monto_pagado: number;
  saldo_disponible?: number;
  estado: string;
  creado_en: string;
}

export interface AsignacionPresupuestariaCrear {
  id_presupuesto: number;
  id_partida: number;
  monto_inicial?: number;
}

// ── ReformaPresupuestaria ────────────────────────────────────
export type TipoReforma = 'TRASPASO' | 'SUPLEMENTO' | 'REDUCCION';

export interface ReformaPresupuestaria {
  id_reforma: number;
  id_asignacion: number;
  tipo_reforma: TipoReforma;
  monto: number;
  numero_resolucion: string;
  fecha_resolucion: string;
  motivo?: string;
  estado: string;
  creado_en: string;
}

export interface ReformaPresupuestariaCrear {
  id_asignacion: number;
  tipo_reforma: TipoReforma;
  monto: number;
  numero_resolucion: string;
  fecha_resolucion: string;
  motivo?: string;
}

// ── CertificadoPresupuestario ────────────────────────────────
export type EstadoCertificado = 'PENDIENTE' | 'APROBADO' | 'ANULADO' | 'LIQUIDADO';

export interface CertificadoPresupuestario {
  id_certificado: number;
  id_asignacion: number;
  numero_certificado: string;
  monto_certificado: number;
  concepto: string;
  fecha_solicitud: string;
  fecha_certificacion?: string;
  fecha_vencimiento?: string;
  referencia_tipo?: string;
  referencia_id?: number;
  id_proceso_contratacion?: number;
  estado: EstadoCertificado;
  motivo_anulacion?: string;
  creado_en: string;
}

export interface CertificadoPresupuestarioCrear {
  id_asignacion: number;
  monto_certificado: number;
  concepto: string;
  fecha_solicitud: string;
  fecha_vencimiento?: string;
  referencia_tipo?: string;
  referencia_id?: number;
  id_proceso_contratacion?: number;
}

export interface CertificadoPresupuestarioEstado {
  estado: 'APROBADO' | 'ANULADO';
  motivo_anulacion?: string;
}

// ── Compromiso ───────────────────────────────────────────────
export interface Compromiso {
  id_compromiso: number;
  id_certificado: number;
  numero_compromiso: string;
  monto_comprometido: number;
  concepto: string;
  fecha_compromiso: string;
  estado: string;
  motivo_anulacion?: string;
  creado_en: string;
}

export interface CompromisoCrear {
  id_certificado: number;
  numero_compromiso: string;
  monto_comprometido: number;
  concepto: string;
  fecha_compromiso: string;
}

// ── Devengado ────────────────────────────────────────────────
export interface Devengado {
  id_devengado: number;
  id_compromiso: number;
  numero_devengado: string;
  monto_devengado: number;
  concepto: string;
  fecha_devengado: string;
  id_asiento_contable?: number;
  id_factura?: number;
  estado: string;
  motivo_anulacion?: string;
  creado_en: string;
}

export interface DevengadoCrear {
  id_compromiso: number;
  numero_devengado: string;
  monto_devengado: number;
  concepto: string;
  fecha_devengado: string;
  id_asiento_contable?: number;
  id_factura?: number;
}

// ── EjecucionPresupuestaria ──────────────────────────────────
export interface EjecucionPresupuestaria {
  anio_fiscal: number;
  codigo_partida: string;
  nombre_partida: string;
  monto_inicial: number;
  monto_codificado: number;
  monto_comprometido: number;
  monto_devengado: number;
  monto_pagado: number;
  saldo_disponible: number;
  porcentaje_ejecucion: number;
}
