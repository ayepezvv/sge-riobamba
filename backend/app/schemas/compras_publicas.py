"""
Esquemas Pydantic — Módulo Compras Públicas
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


# ---------------------------------------------------------------------------
# CarpetaAnual
# ---------------------------------------------------------------------------

class CarpetaAnualBase(BaseModel):
    anio: int = Field(..., ge=2000, le=2100)
    nombre_area: str = Field(..., max_length=200)
    tipo_area: str = Field(default="UNIDAD", pattern="^(DIRECCION|UNIDAD)$")
    descripcion: Optional[str] = None
    activa: bool = True


class CarpetaAnualCrear(CarpetaAnualBase):
    pass


class CarpetaAnualActualizar(BaseModel):
    anio: Optional[int] = Field(None, ge=2000, le=2100)
    nombre_area: Optional[str] = Field(None, max_length=200)
    tipo_area: Optional[str] = Field(None, pattern="^(DIRECCION|UNIDAD)$")
    descripcion: Optional[str] = None
    activa: Optional[bool] = None


class CarpetaAnualRespuesta(CarpetaAnualBase):
    id: int
    creada_en: datetime
    actualizada_en: datetime
    total_procesos: Optional[int] = 0

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# ProcesoCompra
# ---------------------------------------------------------------------------

class ProcesoCompraBase(BaseModel):
    carpeta_anual_id: int
    pac_item_id: Optional[int] = None
    codigo_sercop: Optional[str] = Field(None, max_length=50)
    nombre_proceso: str = Field(..., max_length=500)
    objeto_contratacion: Optional[str] = None
    tipo_contratacion: str = Field(..., max_length=100)
    procedimiento: Optional[str] = Field(None, max_length=100)
    partida_presupuestaria: Optional[str] = Field(None, max_length=50)
    presupuesto_referencial: Decimal = Field(default=Decimal("0"), ge=0)
    monto_adjudicado: Optional[Decimal] = Field(None, ge=0)
    proveedor: Optional[str] = Field(None, max_length=300)
    numero_contrato: Optional[str] = Field(None, max_length=100)
    fecha_inicio_proceso: Optional[date] = None
    fecha_fin_planificada: Optional[date] = None
    fecha_adjudicacion: Optional[date] = None
    fecha_firma_contrato: Optional[date] = None
    estado: str = Field(default="ACTIVO", pattern="^(ACTIVO|ANULADO|FINALIZADO)$")
    etapa_actual: Optional[str] = Field(
        default="PREPARATORIA",
        pattern="^(PREPARATORIA|PRECONTRACTUAL|CONTRACTUAL|EJECUCION|LIQUIDACION)$",
    )
    administrador_contrato: Optional[str] = Field(None, max_length=200)
    fiscalizador: Optional[str] = Field(None, max_length=200)
    observaciones: Optional[str] = None


class ProcesoCompraCrear(ProcesoCompraBase):
    pass


class ProcesoCompraActualizar(BaseModel):
    pac_item_id: Optional[int] = None
    codigo_sercop: Optional[str] = Field(None, max_length=50)
    nombre_proceso: Optional[str] = Field(None, max_length=500)
    objeto_contratacion: Optional[str] = None
    tipo_contratacion: Optional[str] = Field(None, max_length=100)
    procedimiento: Optional[str] = Field(None, max_length=100)
    partida_presupuestaria: Optional[str] = Field(None, max_length=50)
    presupuesto_referencial: Optional[Decimal] = Field(None, ge=0)
    monto_adjudicado: Optional[Decimal] = Field(None, ge=0)
    proveedor: Optional[str] = Field(None, max_length=300)
    numero_contrato: Optional[str] = Field(None, max_length=100)
    fecha_inicio_proceso: Optional[date] = None
    fecha_fin_planificada: Optional[date] = None
    fecha_adjudicacion: Optional[date] = None
    fecha_firma_contrato: Optional[date] = None
    estado: Optional[str] = Field(None, pattern="^(ACTIVO|ANULADO|FINALIZADO)$")
    etapa_actual: Optional[str] = Field(
        None,
        pattern="^(PREPARATORIA|PRECONTRACTUAL|CONTRACTUAL|EJECUCION|LIQUIDACION)$",
    )
    administrador_contrato: Optional[str] = Field(None, max_length=200)
    fiscalizador: Optional[str] = Field(None, max_length=200)
    observaciones: Optional[str] = None


class ProcesoCompraRespuesta(ProcesoCompraBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


class ProcesoCompraDetalle(ProcesoCompraRespuesta):
    """Respuesta con relaciones incluidas"""
    seguimiento: Optional["SeguimientoProcesosRespuesta"] = None
    plazos: List["PlazoProcesosRespuesta"] = []
    documentos: List["ChecklistDocumentalRespuesta"] = []


# ---------------------------------------------------------------------------
# SeguimientoProceso
# ---------------------------------------------------------------------------

class SeguimientoProcesoBase(BaseModel):
    avance_fisico_pct: Decimal = Field(default=Decimal("0"), ge=0, le=100)
    avance_financiero_pct: Decimal = Field(default=Decimal("0"), ge=0, le=100)
    valor_ejecutado: Decimal = Field(default=Decimal("0"), ge=0)
    valor_pendiente: Decimal = Field(default=Decimal("0"), ge=0)
    dias_retraso: int = Field(default=0, ge=0)
    motivo_retraso: Optional[str] = None
    accion_correctiva: Optional[str] = None
    ultima_actualizacion: Optional[date] = None
    observaciones: Optional[str] = None


class SeguimientoProcesoCrear(SeguimientoProcesoBase):
    proceso_id: int


class SeguimientoProcesoActualizar(SeguimientoProcesoBase):
    pass


class SeguimientoProcesosRespuesta(SeguimientoProcesoBase):
    id: int
    proceso_id: int
    actualizado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# PlazoProceso
# ---------------------------------------------------------------------------

class PlazoProcesoBase(BaseModel):
    etapa: str = Field(
        ...,
        pattern="^(PREPARATORIA|PRECONTRACTUAL|CONTRACTUAL|EJECUCION|LIQUIDACION)$",
    )
    descripcion_actividad: Optional[str] = Field(None, max_length=300)
    fecha_planificada: Optional[date] = None
    fecha_real: Optional[date] = None
    plazo_legal_dias: Optional[int] = Field(None, ge=0)
    plazo_planificado_dias: Optional[int] = Field(None, ge=0)
    dias_atraso: int = Field(default=0, ge=0)
    cumplido: bool = False
    observaciones: Optional[str] = None


class PlazoProcesoCrear(PlazoProcesoBase):
    proceso_id: int


class PlazoProcesoActualizar(BaseModel):
    descripcion_actividad: Optional[str] = Field(None, max_length=300)
    fecha_planificada: Optional[date] = None
    fecha_real: Optional[date] = None
    plazo_legal_dias: Optional[int] = Field(None, ge=0)
    plazo_planificado_dias: Optional[int] = Field(None, ge=0)
    dias_atraso: Optional[int] = Field(None, ge=0)
    cumplido: Optional[bool] = None
    observaciones: Optional[str] = None


class PlazoProcesosRespuesta(PlazoProcesoBase):
    id: int
    proceso_id: int
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# ChecklistDocumental
# ---------------------------------------------------------------------------

class ChecklistDocumentalBase(BaseModel):
    nombre_documento: str = Field(..., max_length=300)
    tipo_documento: Optional[str] = Field(None, max_length=100)
    etapa: Optional[str] = Field(
        None,
        pattern="^(PREPARATORIA|PRECONTRACTUAL|CONTRACTUAL|EJECUCION|LIQUIDACION)$",
    )
    obligatorio: bool = True
    estado: str = Field(default="PENDIENTE", pattern="^(PENDIENTE|PRESENTADO|APROBADO|RECHAZADO)$")
    fecha_presentacion: Optional[date] = None
    observaciones: Optional[str] = None


class ChecklistDocumentalCrear(ChecklistDocumentalBase):
    proceso_id: int


class ChecklistDocumentalActualizar(BaseModel):
    nombre_documento: Optional[str] = Field(None, max_length=300)
    tipo_documento: Optional[str] = Field(None, max_length=100)
    etapa: Optional[str] = Field(
        None,
        pattern="^(PREPARATORIA|PRECONTRACTUAL|CONTRACTUAL|EJECUCION|LIQUIDACION)$",
    )
    obligatorio: Optional[bool] = None
    estado: Optional[str] = Field(None, pattern="^(PENDIENTE|PRESENTADO|APROBADO|RECHAZADO)$")
    fecha_presentacion: Optional[date] = None
    observaciones: Optional[str] = None


class ChecklistDocumentalRespuesta(ChecklistDocumentalBase):
    id: int
    proceso_id: int
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

class DashboardKPIs(BaseModel):
    total_procesos: int
    procesos_activos: int
    procesos_finalizados: int
    procesos_anulados: int
    presupuesto_total: Decimal
    monto_adjudicado_total: Decimal
    porcentaje_ejecucion: float
    procesos_con_retraso: int


class DashboardRespuesta(BaseModel):
    kpis: DashboardKPIs
    procesos_por_etapa: List[dict]
    procesos_por_tipo: List[dict]
    semaforo_plazos: dict


# Actualizar forward references
ProcesoCompraDetalle.model_rebuild()
