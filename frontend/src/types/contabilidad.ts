// ============================================================
// Tipos TypeScript — Módulo Contabilidad
// Nomenclatura en español conforme a Regla Arquitectónica 2
// ============================================================

// ── Tipo de Cuenta ──────────────────────────────────────────
export interface TipoCuenta {
  id: number;
  codigo: string;
  nombre: string;
  naturaleza: 'DEUDORA' | 'ACREEDORA';
  descripcion?: string;
  creado_en: string;
  actualizado_en: string;
}

export interface TipoCuentaCrear {
  codigo: string;
  nombre: string;
  naturaleza: 'DEUDORA' | 'ACREEDORA';
  descripcion?: string;
}

// ── Cuenta Contable ─────────────────────────────────────────
export interface CuentaContable {
  id: number;
  codigo: string;
  nombre: string;
  descripcion?: string;
  tipo_cuenta_id: number;
  cuenta_padre_id?: number;
  nivel: number;
  es_hoja: boolean;
  permite_movimientos: boolean;
  partida_presupuestaria?: string;
  estado: 'ACTIVA' | 'INACTIVA';
  creado_en: string;
  actualizado_en: string;
}

export interface CuentaContableArbol extends CuentaContable {
  subcuentas: CuentaContableArbol[];
}

export interface SaldoCuenta {
  cuenta_id: number;
  codigo: string;
  nombre: string;
  total_debe: number;
  total_haber: number;
  saldo: number;
}

export interface CuentaContableCrear {
  codigo: string;
  nombre: string;
  descripcion?: string;
  tipo_cuenta_id: number;
  cuenta_padre_id?: number;
  nivel: number;
  es_hoja: boolean;
  permite_movimientos: boolean;
  partida_presupuestaria?: string;
  estado?: string;
}

// ── Diario ──────────────────────────────────────────────────
export type TipoDiario = 'GENERAL' | 'VENTAS' | 'COMPRAS' | 'BANCO' | 'CAJA' | 'APERTURA' | 'CIERRE' | 'AJUSTE';

export interface Diario {
  id: number;
  codigo: string;
  nombre: string;
  tipo: TipoDiario;
  cuenta_default_id?: number;
  es_activo: boolean;
  creado_en: string;
  actualizado_en: string;
}

export interface DiarioCrear {
  codigo: string;
  nombre: string;
  tipo: TipoDiario;
  cuenta_default_id?: number;
  es_activo?: boolean;
}

// ── Período Contable ────────────────────────────────────────
export type EstadoPeriodo = 'ABIERTO' | 'CERRADO' | 'BLOQUEADO';

export interface PeriodoContable {
  id: number;
  anio: number;
  mes: number;
  nombre: string;
  fecha_inicio: string;
  fecha_fin: string;
  estado: EstadoPeriodo;
  creado_en: string;
  actualizado_en: string;
}

export interface PeriodoContableCrear {
  anio: number;
  mes: number;
  nombre: string;
  fecha_inicio: string;
  fecha_fin: string;
  estado?: EstadoPeriodo;
}

// ── Línea de Asiento ─────────────────────────────────────────
export interface LineaAsiento {
  id: number;
  asiento_id: number;
  cuenta_id: number;
  descripcion?: string;
  debe: number;
  haber: number;
  orden: number;
}

export interface LineaAsientoCrear {
  cuenta_id: number;
  descripcion?: string;
  debe: number;
  haber: number;
  orden: number;
}

// ── Asiento Contable ─────────────────────────────────────────
export type EstadoAsiento = 'BORRADOR' | 'PUBLICADO' | 'ANULADO';

export interface AsientoContable {
  id: number;
  numero: string;
  diario_id: number;
  periodo_id: number;
  fecha: string;
  referencia?: string;
  concepto: string;
  estado: EstadoAsiento;
  total_debe: number;
  total_haber: number;
  usuario_id?: number;
  fecha_publicacion?: string;
  motivo_anulacion?: string;
  lineas: LineaAsiento[];
  creado_en: string;
  actualizado_en: string;
}

export interface AsientoContableCrear {
  diario_id: number;
  periodo_id: number;
  fecha: string;
  referencia?: string;
  concepto: string;
  lineas: LineaAsientoCrear[];
}
