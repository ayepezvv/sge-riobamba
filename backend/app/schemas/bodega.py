from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum

class EstadoFisicoSchema(str, Enum):
    BUENO = "BUENO"
    REGULAR = "REGULAR"
    MALO = "MALO"
    DE_BAJA = "DE_BAJA"

# Categoría Schemas
class CategoriaBienBase(BaseModel):
    nombre: str = Field(..., description="Nombre de la categoría")
    descripcion: Optional[str] = None
    is_active: bool = True

class CategoriaBienCreate(CategoriaBienBase):
    pass

class CategoriaBienUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    is_active: Optional[bool] = None

class CategoriaBienSchema(CategoriaBienBase):
    id: int
    class Config:
        from_attributes = True

# Activo Fijo Schemas
class ActivoFijoBase(BaseModel):
    codigo_inventario: str = Field(..., description="Código único de inventario")
    nombre: str
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None
    costo_inicial: Optional[float] = None
    valor_depreciado: Optional[float] = None
    fecha_compra: Optional[date] = None
    factura_referencia: Optional[str] = None
    estado_fisico: EstadoFisicoSchema = EstadoFisicoSchema.BUENO
    categoria_id: int
    is_active: bool = True

class ActivoFijoCreate(ActivoFijoBase):
    pass

class ActivoFijoUpdate(BaseModel):
    codigo_inventario: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None
    costo_inicial: Optional[float] = None
    valor_depreciado: Optional[float] = None
    fecha_compra: Optional[date] = None
    factura_referencia: Optional[str] = None
    estado_fisico: Optional[EstadoFisicoSchema] = None
    categoria_id: Optional[int] = None
    is_active: Optional[bool] = None

class ActivoFijoSchema(ActivoFijoBase):
    id: int
    categoria: Optional[CategoriaBienSchema] = None
    class Config:
        from_attributes = True
