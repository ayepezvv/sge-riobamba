"""
Schemas Pydantic — Módulo Administración
Scope: Estructura organizacional base (Direcciones, Unidades, Puestos).

NOTA: Los schemas de Empleado, EscalaSalarial, TituloProfesional y
CargaFamiliar fueron migrados a schemas/rrhh.py en la Fase V3.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


# ---------------------------------------------------------------------------
# DIRECCIÓN ORGANIZACIONAL
# ---------------------------------------------------------------------------
class DireccionBase(BaseModel):
    nombre: str = Field(..., max_length=150)
    descripcion: Optional[str] = Field(None, max_length=255)
    es_activo: bool = True


class DireccionCreate(DireccionBase):
    pass


class DireccionUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = Field(None, max_length=255)
    es_activo: Optional[bool] = None


class DireccionResponse(DireccionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# UNIDAD
# ---------------------------------------------------------------------------
class UnidadBase(BaseModel):
    direccion_id: int
    nombre: str = Field(..., max_length=150)
    descripcion: Optional[str] = Field(None, max_length=255)
    es_activo: bool = True


class UnidadCreate(UnidadBase):
    pass


class UnidadUpdate(BaseModel):
    direccion_id: Optional[int] = None
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = Field(None, max_length=255)
    es_activo: Optional[bool] = None


class UnidadResponse(UnidadBase):
    id: int
    direccion: Optional[DireccionResponse] = None
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# PUESTO
# ---------------------------------------------------------------------------
class PuestoBase(BaseModel):
    denominacion: str = Field(..., max_length=150)
    partida_presupuestaria: str = Field(..., max_length=100)
    es_activo: bool = True


class PuestoCreate(PuestoBase):
    pass


class PuestoUpdate(BaseModel):
    denominacion: Optional[str] = Field(None, max_length=150)
    partida_presupuestaria: Optional[str] = Field(None, max_length=100)
    es_activo: Optional[bool] = None


class PuestoResponse(PuestoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
