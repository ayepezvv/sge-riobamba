// ============================================================
// Tipos TypeScript — Módulo Inventario / Existencias
// Nomenclatura en español conforme a Regla Arquitectónica 2
// ============================================================

// ── Tipos de movimiento ──────────────────────────────────────
export type ENTRADA = 'ENTRADA';
export type SALIDA = 'SALIDA';

// ── Cuenta Contable de Inventario ───────────────────────────
export interface CuentaContableInventario {
  id: number;
  codigo_cuenta: string;
  nombre_cuenta: string;
  tipo_movimiento: number;
  nivel: number;
  cuenta_gasto?: string;
}

// ── Destino ──────────────────────────────────────────────────
export interface Destino {
  id: number;
  nombre: string;
  activo: boolean;
  id_origen_mysql?: number;
}

// ── Encargado ────────────────────────────────────────────────
export interface Encargado {
  id: number;
  nombre: string;
  cedula?: string;
  activo: boolean;
  id_origen_mysql?: number;
}

// ── Proveedor ────────────────────────────────────────────────
export interface Proveedor {
  id: number;
  nombre: string;
  ruc_cedula?: string;
  direccion?: string;
  telefono?: string;
  contacto?: string;
  activo: boolean;
  id_origen_mysql?: number;
}

// ── Unidad de Gestión ────────────────────────────────────────
export interface UnidadGestion {
  id: number;
  codigo: string;
  nombre: string;
  puede_mover: boolean;
  id_origen_mysql?: number;
}

// ── Artículo (listado resumido) ──────────────────────────────
export interface ArticuloListado {
  id: number;
  codigo_articulo: string;
  nombre: string;
  unidad_medida?: string;
  existencia_actual?: number;
  costo_actual: number;
  valor_total?: number;
  codigo_cuenta: string;
  anno_fiscal: number;
  activo: boolean;
}

// ── Artículo (detalle completo) ──────────────────────────────
export interface Articulo {
  id: number;
  codigo_articulo: string;
  nombre: string;
  descripcion_extendida?: string;
  codigo_cuenta: string;
  unidad_medida?: string;
  existencia_inicial?: number;
  costo_inicial?: number;
  existencia_actual?: number;
  costo_actual: number;
  valor_total?: number;
  stock_minimo?: number;
  stock_maximo?: number;
  codigo_barras?: string;
  anno_fiscal: number;
  activo: boolean;
  usuario_crea?: string;
  creado_en?: string;
  modificado_en?: string;
  id_origen_mysql?: number;
}

// ── Movimiento (listado resumido) ────────────────────────────
export interface MovimientoListado {
  id: number;
  numero_movimiento: number;
  fecha: string;
  tipo_movimiento: ENTRADA | SALIDA;
  costo_total?: number;
  observacion?: string;
  anno_fiscal: number;
  proveedor?: string;
  destino?: string;
  encargado?: string;
}

// ── Movimiento (detalle completo) ────────────────────────────
export interface Movimiento {
  id: number;
  numero_movimiento: number;
  fecha: string;
  tipo_movimiento: ENTRADA | SALIDA;
  subtipo?: string;
  costo_total?: number;
  numero_factura?: string;
  fecha_factura?: string;
  comprobante_egreso?: string;
  observacion?: string;
  numero_entrada_ref?: number;
  aprobado?: number;
  anexo?: string;
  anno_fiscal: number;
  id_proveedor?: number;
  id_destino?: number;
  id_encargado?: number;
  id_origen_mysql?: number;
  creado_en?: string;
  proveedor?: Proveedor;
  destino?: Destino;
  encargado?: Encargado;
}

// ── Línea de Kardex ──────────────────────────────────────────
export interface LineaKardex {
  id: number;
  id_movimiento: number;
  id_articulo: number;
  fecha: string;
  tipo_movimiento: ENTRADA | SALIDA;
  cantidad: number;
  costo_unitario: number;
  total_linea?: number;
  costo_promedio?: number;
  anno_fiscal: number;
  id_origen_mysql?: number;
  articulo?: Articulo;
}

// ── Resumen Anual ────────────────────────────────────────────
export interface ResumenAnualInventario {
  anno_fiscal: number;
  total_articulos: number;
  total_movimientos: number;
  total_lineas_kardex: number;
  valor_inventario_total?: number;
}
