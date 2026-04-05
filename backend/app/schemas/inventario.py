from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ─────────────────────────────────────────────────────
# CUENTA CONTABLE INVENTARIO
# ─────────────────────────────────────────────────────
class CuentaContableInventarioBase(BaseModel):
    codigo_cuenta: str = Field(..., max_length=35)
    nombre_cuenta: str = Field(..., max_length=60)
    tipo_movimiento: int = Field(..., description="1=solo movimiento, 2=nivel padre")
    nivel: int = Field(..., description="3=titulo, 6=grupo, 9=cuenta movible")
    cuenta_gasto: Optional[str] = Field(None, max_length=35)

class CuentaContableInventarioCrear(CuentaContableInventarioBase):
    pass

class CuentaContableInventario(CuentaContableInventarioBase):
    id: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────
# DESTINO
# ─────────────────────────────────────────────────────
class DestinoBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    activo: bool = True

class DestinoCrear(DestinoBase):
    pass

class DestinoActualizar(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    activo: Optional[bool] = None

class Destino(DestinoBase):
    id: int
    id_origen_mysql: Optional[int] = None
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────
# ENCARGADO
# ─────────────────────────────────────────────────────
class EncargadoBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    cedula: Optional[str] = Field(None, max_length=10)
    activo: bool = True

class EncargadoCrear(EncargadoBase):
    pass

class EncargadoActualizar(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    cedula: Optional[str] = Field(None, max_length=10)
    activo: Optional[bool] = None

class Encargado(EncargadoBase):
    id: int
    id_origen_mysql: Optional[int] = None
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────
# PROVEEDOR
# ─────────────────────────────────────────────────────
class ProveedorBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    ruc_cedula: Optional[str] = Field(None, max_length=13)
    direccion: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=15)
    contacto: Optional[str] = Field(None, max_length=100)
    activo: bool = True

class ProveedorCrear(ProveedorBase):
    pass

class ProveedorActualizar(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    ruc_cedula: Optional[str] = Field(None, max_length=13)
    direccion: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=15)
    contacto: Optional[str] = Field(None, max_length=100)
    activo: Optional[bool] = None

class Proveedor(ProveedorBase):
    id: int
    id_origen_mysql: Optional[int] = None
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────
# UNIDAD DE GESTIÓN
# ─────────────────────────────────────────────────────
class UnidadGestionBase(BaseModel):
    codigo: str = Field(..., max_length=10)
    nombre: str = Field(..., max_length=100)
    puede_mover: bool = True

class UnidadGestionCrear(UnidadGestionBase):
    pass

class UnidadGestion(UnidadGestionBase):
    id: int
    id_origen_mysql: Optional[int] = None
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────
# ARTÍCULO INVENTARIO
# ─────────────────────────────────────────────────────
class ArticuloInventarioBase(BaseModel):
    codigo_articulo: str = Field(..., max_length=8)
    nombre: str = Field(..., max_length=100)
    descripcion_extendida: Optional[str] = Field(None, max_length=254)
    codigo_cuenta: str = Field(..., max_length=35)
    unidad_medida: Optional[str] = Field(None, max_length=10)
    existencia_inicial: Optional[Decimal] = None
    costo_inicial: Optional[Decimal] = None
    existencia_actual: Optional[Decimal] = None
    costo_actual: Decimal = Decimal("0")
    valor_total: Optional[Decimal] = None
    stock_minimo: Optional[Decimal] = None
    stock_maximo: Optional[Decimal] = None
    codigo_barras: Optional[str] = Field(None, max_length=45)
    anno_fiscal: int = Field(..., ge=2021, le=2025)
    activo: bool = True

class ArticuloInventarioCrear(ArticuloInventarioBase):
    pass

class ArticuloInventarioActualizar(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion_extendida: Optional[str] = Field(None, max_length=254)
    unidad_medida: Optional[str] = Field(None, max_length=10)
    existencia_actual: Optional[Decimal] = None
    costo_actual: Optional[Decimal] = None
    stock_minimo: Optional[Decimal] = None
    stock_maximo: Optional[Decimal] = None
    activo: Optional[bool] = None

class ArticuloInventario(ArticuloInventarioBase):
    id: int
    id_origen_mysql: Optional[int] = None
    creado_en: Optional[datetime] = None
    modificado_en: Optional[datetime] = None
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────
# MOVIMIENTO
# ─────────────────────────────────────────────────────
class MovimientoBase(BaseModel):
    numero_movimiento: int
    fecha: datetime
    tipo_movimiento: str = Field(..., description="ENTRADA o SALIDA")
    subtipo: Optional[str] = Field(None, max_length=1, description="R=Reversal")
    costo_total: Optional[Decimal] = None
    numero_factura: Optional[str] = Field(None, max_length=20)
    fecha_factura: Optional[datetime] = None
    comprobante_egreso: Optional[str] = Field(None, max_length=20)
    observacion: Optional[str] = Field(None, max_length=254)
    numero_entrada_ref: Optional[int] = None
    aprobado: Optional[int] = 0
    anexo: Optional[str] = Field(None, max_length=20)
    anno_fiscal: int = Field(..., ge=2021, le=2025)
    id_proveedor: Optional[int] = None
    id_destino: Optional[int] = None
    id_encargado: Optional[int] = None

class MovimientoCrear(MovimientoBase):
    pass

class Movimiento(MovimientoBase):
    id: int
    id_origen_mysql: Optional[int] = None
    creado_en: Optional[datetime] = None
    proveedor: Optional[Proveedor] = None
    destino: Optional[Destino] = None
    encargado: Optional[Encargado] = None
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────
# MOVIMIENTO DETALLE (KARDEX)
# ─────────────────────────────────────────────────────
class MovimientoDetalleBase(BaseModel):
    id_movimiento: int
    id_articulo: int
    fecha: datetime
    tipo_movimiento: str = Field(..., description="ENTRADA o SALIDA")
    cantidad: Decimal
    costo_unitario: Decimal
    total_linea: Optional[Decimal] = None
    costo_promedio: Optional[Decimal] = None
    anno_fiscal: int = Field(..., ge=2021, le=2025)

class MovimientoDetalleCrear(MovimientoDetalleBase):
    pass

class MovimientoDetalle(MovimientoDetalleBase):
    id: int
    id_origen_mysql: Optional[int] = None
    articulo: Optional[ArticuloInventario] = None
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────
# SCHEMAS DE CONSULTA / LISTADO
# ─────────────────────────────────────────────────────
class ArticuloListado(BaseModel):
    id: int
    codigo_articulo: str
    nombre: str
    unidad_medida: Optional[str] = None
    existencia_actual: Optional[Decimal] = None
    costo_actual: Decimal
    valor_total: Optional[Decimal] = None
    codigo_cuenta: str
    anno_fiscal: int
    activo: bool
    class Config:
        from_attributes = True


class MovimientoListado(BaseModel):
    id: int
    numero_movimiento: int
    fecha: datetime
    tipo_movimiento: str
    costo_total: Optional[Decimal] = None
    observacion: Optional[str] = None
    anno_fiscal: int
    proveedor: Optional[str] = None  # nombre
    destino: Optional[str] = None    # nombre
    encargado: Optional[str] = None  # nombre
    class Config:
        from_attributes = True


class ResumenAnualInventario(BaseModel):
    anno_fiscal: int
    total_articulos: int
    total_movimientos: int
    total_lineas_kardex: int
    valor_inventario_total: Optional[Decimal] = None
