"""
Schemas Pydantic — Módulo Presupuesto
Nomenclatura en español (Regla 2 obligatoria).
"""
from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


# ===========================================================================
# PARTIDA PRESUPUESTARIA
# ===========================================================================

class PartidaPresupuestariaBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código SIGEF ej: 5.1.01.05.001")
    nombre: str = Field(..., max_length=255)
    descripcion: Optional[str] = None
    tipo: str = Field(..., pattern="^(INGRESO|GASTO)$")
    nivel: int = Field(..., ge=1, le=5)
    es_hoja: bool = True
    id_partida_padre: Optional[int] = None
    estado: str = "ACTIVO"


class PartidaPresupuestariaCrear(PartidaPresupuestariaBase):
    pass


class PartidaPresupuestariaActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    es_hoja: Optional[bool] = None
    estado: Optional[str] = None


class PartidaPresupuestariaRespuesta(PartidaPresupuestariaBase):
    id_partida: int
    creado_en: datetime

    class Config:
        from_attributes = True


# ===========================================================================
# PRESUPUESTO ANUAL
# ===========================================================================

class PresupuestoAnualBase(BaseModel):
    anio_fiscal: int = Field(..., ge=2000, le=2100)
    denominacion: str = Field(..., max_length=255)
    monto_inicial: Decimal = Field(default=Decimal("0.00"), ge=0)
    observaciones: Optional[str] = None


class PresupuestoAnualCrear(PresupuestoAnualBase):
    pass


class PresupuestoAnualActualizar(BaseModel):
    denominacion: Optional[str] = None
    monto_codificado: Optional[Decimal] = None
    estado: Optional[str] = None
    fecha_aprobacion: Optional[date] = None
    resolucion_aprobacion: Optional[str] = None
    observaciones: Optional[str] = None


class PresupuestoAnualRespuesta(PresupuestoAnualBase):
    id_presupuesto: int
    monto_codificado: Decimal
    estado: str
    fecha_aprobacion: Optional[date]
    resolucion_aprobacion: Optional[str]
    creado_en: datetime

    class Config:
        from_attributes = True


# ===========================================================================
# ASIGNACIÓN PRESUPUESTARIA
# ===========================================================================

class AsignacionPresupuestariaBase(BaseModel):
    id_presupuesto: int
    id_partida: int
    monto_inicial: Decimal = Field(default=Decimal("0.00"), ge=0)


class AsignacionPresupuestariaCrear(AsignacionPresupuestariaBase):
    pass


class AsignacionPresupuestariaRespuesta(AsignacionPresupuestariaBase):
    id_asignacion: int
    monto_codificado: Decimal
    monto_comprometido: Decimal
    monto_devengado: Decimal
    monto_pagado: Decimal
    saldo_disponible: Optional[Decimal] = None
    estado: str
    creado_en: datetime

    class Config:
        from_attributes = True


# ===========================================================================
# REFORMA PRESUPUESTARIA
# ===========================================================================

class ReformaPresupuestariaCrear(BaseModel):
    id_asignacion: int
    tipo_reforma: str = Field(..., pattern="^(TRASPASO|SUPLEMENTO|REDUCCION)$")
    monto: Decimal = Field(..., description="Positivo=aumento, negativo=reducción")
    numero_resolucion: str = Field(..., max_length=100)
    fecha_resolucion: date
    motivo: Optional[str] = None


class ReformaPresupuestariaRespuesta(ReformaPresupuestariaCrear):
    id_reforma: int
    estado: str
    creado_en: datetime

    class Config:
        from_attributes = True


# ===========================================================================
# CERTIFICADO PRESUPUESTARIO
# ===========================================================================

class CertificadoPresupuestariaBase(BaseModel):
    id_asignacion: int
    monto_certificado: Decimal = Field(..., gt=0)
    concepto: str
    fecha_solicitud: date
    fecha_vencimiento: Optional[date] = None
    referencia_tipo: Optional[str] = None
    referencia_id: Optional[int] = None
    id_proceso_contratacion: Optional[int] = None


class CertificadoPresupuestariaCrear(CertificadoPresupuestariaBase):
    pass


class CertificadoPresupuestariaEstado(BaseModel):
    estado: str = Field(..., pattern="^(APROBADO|ANULADO)$")
    motivo_anulacion: Optional[str] = None

    @model_validator(mode="after")
    def validar_motivo_anulacion(self) -> "CertificadoPresupuestariaEstado":
        if self.estado == "ANULADO" and not self.motivo_anulacion:
            raise ValueError("motivo_anulacion es obligatorio al anular")
        return self


class CertificadoPresupuestariaRespuesta(CertificadoPresupuestariaBase):
    id_certificado: int
    numero_certificado: str
    fecha_certificacion: Optional[date]
    estado: str
    motivo_anulacion: Optional[str]
    creado_en: datetime

    class Config:
        from_attributes = True


# ===========================================================================
# COMPROMISO
# ===========================================================================

class CompromisoCrear(BaseModel):
    id_certificado: int
    numero_compromiso: str = Field(..., max_length=50)
    monto_comprometido: Decimal = Field(..., gt=0)
    concepto: str
    fecha_compromiso: date


class CompromisoRespuesta(CompromisoCrear):
    id_compromiso: int
    estado: str
    motivo_anulacion: Optional[str]
    creado_en: datetime

    class Config:
        from_attributes = True


# ===========================================================================
# DEVENGADO
# ===========================================================================

class DevengadoCrear(BaseModel):
    id_compromiso: int
    numero_devengado: str = Field(..., max_length=50)
    monto_devengado: Decimal = Field(..., gt=0)
    concepto: str
    fecha_devengado: date
    id_asiento_contable: Optional[int] = None
    id_factura: Optional[int] = None


class DevengadoRespuesta(DevengadoCrear):
    id_devengado: int
    estado: str
    motivo_anulacion: Optional[str]
    creado_en: datetime

    class Config:
        from_attributes = True


# ===========================================================================
# RESUMEN EJECUCIÓN PRESUPUESTARIA
# ===========================================================================

class EjecucionPresupuestariaRespuesta(BaseModel):
    anio_fiscal: int
    codigo_partida: str
    nombre_partida: str
    monto_inicial: Decimal
    monto_codificado: Decimal
    monto_comprometido: Decimal
    monto_devengado: Decimal
    monto_pagado: Decimal
    saldo_disponible: Decimal
    porcentaje_ejecucion: Decimal

    class Config:
        from_attributes = True
