"""
Schemas Pydantic para el módulo de Contabilidad.
Nomenclatura en español conforme a Regla Arquitectónica 2.
"""
from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


# ---------------------------------------------------------------------------
# TipoCuenta
# ---------------------------------------------------------------------------

class TipoCuentaBase(BaseModel):
    codigo: str = Field(..., max_length=10, description="Código del tipo de cuenta")
    nombre: str = Field(..., max_length=100)
    naturaleza: str = Field(..., description="DEUDORA o ACREEDORA")
    descripcion: Optional[str] = None


class TipoCuentaCrear(TipoCuentaBase):
    pass


class TipoCuentaActualizar(BaseModel):
    nombre: Optional[str] = None
    naturaleza: Optional[str] = None
    descripcion: Optional[str] = None


class TipoCuentaRespuesta(TipoCuentaBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# CuentaContable
# ---------------------------------------------------------------------------

class CuentaContableBase(BaseModel):
    codigo: str = Field(..., max_length=50, description="Código jerárquico SIGEF")
    nombre: str = Field(..., max_length=200)
    descripcion: Optional[str] = None
    tipo_cuenta_id: int
    cuenta_padre_id: Optional[int] = None
    nivel: int = Field(..., ge=1, le=10)
    es_hoja: bool = True
    permite_movimientos: bool = True
    partida_presupuestaria: Optional[str] = Field(None, max_length=100)
    estado: str = Field("ACTIVA", description="ACTIVA | INACTIVA")


class CuentaContableCrear(CuentaContableBase):
    pass


class CuentaContableActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    partida_presupuestaria: Optional[str] = None
    estado: Optional[str] = None
    permite_movimientos: Optional[bool] = None


class CuentaContableRespuesta(CuentaContableBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


class CuentaContableArbol(CuentaContableRespuesta):
    subcuentas: List[CuentaContableArbol] = []

    model_config = {"from_attributes": True}


class SaldoCuenta(BaseModel):
    cuenta_id: int
    codigo: str
    nombre: str
    total_debe: Decimal
    total_haber: Decimal
    saldo: Decimal = Field(description="debe - haber (positivo = saldo deudor)")


# ---------------------------------------------------------------------------
# Diario
# ---------------------------------------------------------------------------

class DiarioBase(BaseModel):
    codigo: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=100)
    tipo: str = Field("GENERAL", description="GENERAL|VENTAS|COMPRAS|BANCO|CAJA|APERTURA|CIERRE|AJUSTE")
    cuenta_default_id: Optional[int] = None
    es_activo: bool = True


class DiarioCrear(DiarioBase):
    pass


class DiarioActualizar(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    cuenta_default_id: Optional[int] = None
    es_activo: Optional[bool] = None


class DiarioRespuesta(DiarioBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# PeriodoContable
# ---------------------------------------------------------------------------

class PeriodoContableBase(BaseModel):
    anio: int = Field(..., ge=2000, le=2100)
    mes: int = Field(..., ge=1, le=12)
    nombre: str = Field(..., max_length=50)
    fecha_inicio: date
    fecha_fin: date
    estado: str = Field("ABIERTO", description="ABIERTO | CERRADO | BLOQUEADO")


class PeriodoContableCrear(PeriodoContableBase):
    pass


class PeriodoContableRespuesta(PeriodoContableBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


class CambioEstadoPeriodo(BaseModel):
    estado: str = Field(..., description="ABIERTO | CERRADO | BLOQUEADO")


# ---------------------------------------------------------------------------
# LineaAsiento
# ---------------------------------------------------------------------------

class LineaAsientoBase(BaseModel):
    cuenta_id: int
    descripcion: Optional[str] = Field(None, max_length=255)
    debe: Decimal = Field(Decimal("0"), ge=0)
    haber: Decimal = Field(Decimal("0"), ge=0)
    orden: int = Field(1, ge=1)

    @model_validator(mode="after")
    def validar_debe_o_haber(self) -> "LineaAsientoBase":
        if self.debe > 0 and self.haber > 0:
            raise ValueError("Una línea no puede tener debe Y haber simultáneamente")
        return self


class LineaAsientoCrear(LineaAsientoBase):
    pass


class LineaAsientoRespuesta(LineaAsientoBase):
    id: int
    asiento_id: int

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# AsientoContable
# ---------------------------------------------------------------------------

class AsientoContableBase(BaseModel):
    diario_id: int
    periodo_id: int
    fecha: date
    referencia: Optional[str] = Field(None, max_length=100)
    concepto: str


class AsientoContableCrear(AsientoContableBase):
    lineas: List[LineaAsientoCrear] = Field(..., min_length=2,
                                             description="Mínimo 2 líneas (debe cuadrar)")

    @model_validator(mode="after")
    def validar_asiento_cuadrado(self) -> "AsientoContableCrear":
        total_debe = sum(l.debe for l in self.lineas)
        total_haber = sum(l.haber for l in self.lineas)
        if total_debe != total_haber:
            raise ValueError(
                f"El asiento no cuadra: Debe={total_debe} ≠ Haber={total_haber}"
            )
        if total_debe == 0:
            raise ValueError("El asiento no puede tener debe/haber en cero")
        return self


class AsientoContableRespuesta(AsientoContableBase):
    id: int
    numero: str
    estado: str
    total_debe: Decimal
    total_haber: Decimal
    usuario_id: Optional[int]
    fecha_publicacion: Optional[datetime]
    motivo_anulacion: Optional[str]
    lineas: List[LineaAsientoRespuesta] = []
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


class AnularAsiento(BaseModel):
    motivo_anulacion: str = Field(..., min_length=10,
                                   description="Motivo obligatorio (RN-11)")
