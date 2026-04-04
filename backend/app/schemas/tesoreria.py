"""
Schemas Pydantic para el módulo de Tesorería.
Nomenclatura en español conforme a Regla Arquitectónica 2.
"""
from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


# ---------------------------------------------------------------------------
# EntidadBancaria
# ---------------------------------------------------------------------------

class EntidadBancariaBase(BaseModel):
    codigo: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=150)
    sigla: Optional[str] = Field(None, max_length=20)
    es_activa: bool = True


class EntidadBancariaCrear(EntidadBancariaBase):
    pass


class EntidadBancariaActualizar(BaseModel):
    nombre: Optional[str] = None
    sigla: Optional[str] = None
    es_activa: Optional[bool] = None


class EntidadBancariaRespuesta(EntidadBancariaBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# CuentaBancaria
# ---------------------------------------------------------------------------

class CuentaBancariaBase(BaseModel):
    entidad_bancaria_id: int
    numero_cuenta: str = Field(..., max_length=50)
    nombre: str = Field(..., max_length=200)
    tipo: str = Field("CORRIENTE", description="CORRIENTE|AHORROS|RECAUDACION|PAGOS")
    moneda: str = Field("USD", max_length=3)
    cuenta_contable_id: Optional[int] = None
    saldo_inicial: Decimal = Field(Decimal("0"), ge=0)
    es_activa: bool = True


class CuentaBancariaCrear(CuentaBancariaBase):
    pass


class CuentaBancariaActualizar(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    cuenta_contable_id: Optional[int] = None
    es_activa: Optional[bool] = None


class CuentaBancariaRespuesta(CuentaBancariaBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# ExtractoBancario
# ---------------------------------------------------------------------------

class LineaExtractoCrear(BaseModel):
    fecha: date
    tipo_transaccion: str = Field("OTRO", description="IESS|SRI|BCE|SPI|TRANSFERENCIA|...")
    referencia: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    valor: Decimal = Field(..., description="Positivo=crédito, negativo=débito")


class LineaExtractoRespuesta(LineaExtractoCrear):
    id: int
    extracto_id: int
    esta_conciliada: bool
    creado_en: datetime

    model_config = {"from_attributes": True}


class ExtractoBancarioBase(BaseModel):
    cuenta_bancaria_id: int
    referencia: Optional[str] = Field(None, max_length=100)
    fecha_inicio: date
    fecha_fin: date
    saldo_inicial: Decimal = Decimal("0")
    saldo_final: Decimal = Decimal("0")


class ExtractoBancarioCrear(ExtractoBancarioBase):
    lineas: List[LineaExtractoCrear] = []


class ExtractoBancarioActualizar(BaseModel):
    referencia: Optional[str] = None
    saldo_inicial: Optional[Decimal] = None
    saldo_final: Optional[Decimal] = None
    estado: Optional[str] = None


class ExtractoBancarioRespuesta(ExtractoBancarioBase):
    id: int
    estado: str
    creado_en: datetime
    actualizado_en: datetime
    lineas: List[LineaExtractoRespuesta] = []

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# ConciliacionBancaria
# ---------------------------------------------------------------------------

class MarcaConciliacionCrear(BaseModel):
    linea_extracto_id: int
    asiento_contable_id: Optional[int] = None
    valor_conciliado: Decimal
    observacion: Optional[str] = Field(None, max_length=255)


class MarcaConciliacionRespuesta(MarcaConciliacionCrear):
    id: int
    conciliacion_id: int
    creado_en: datetime

    model_config = {"from_attributes": True}


class ConciliacionBancariaBase(BaseModel):
    cuenta_bancaria_id: int
    extracto_id: Optional[int] = None
    nombre: str = Field(..., max_length=100)
    fecha_inicio: date
    fecha_fin: date
    saldo_libro: Decimal = Decimal("0")
    saldo_banco: Decimal = Decimal("0")
    observaciones: Optional[str] = None


class ConciliacionBancariaCrear(ConciliacionBancariaBase):
    pass


class ConciliacionBancariaActualizar(BaseModel):
    nombre: Optional[str] = None
    saldo_libro: Optional[Decimal] = None
    saldo_banco: Optional[Decimal] = None
    observaciones: Optional[str] = None


class CerrarConciliacion(BaseModel):
    observaciones: Optional[str] = None


class ConciliacionBancariaRespuesta(ConciliacionBancariaBase):
    id: int
    diferencia: Decimal
    estado: str
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# CajaChica
# ---------------------------------------------------------------------------

class CajaChicaBase(BaseModel):
    codigo: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=150)
    monto_fijo: Decimal = Decimal("0")
    cuenta_contable_id: Optional[int] = None
    responsable_id: Optional[int] = None


class CajaChicaCrear(CajaChicaBase):
    pass


class CajaChicaActualizar(BaseModel):
    nombre: Optional[str] = None
    monto_fijo: Optional[Decimal] = None
    cuenta_contable_id: Optional[int] = None
    responsable_id: Optional[int] = None


class CajaChicaRespuesta(CajaChicaBase):
    id: int
    monto_disponible: Decimal
    estado: str
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# MovimientoCaja
# ---------------------------------------------------------------------------

class MovimientoCajaBase(BaseModel):
    caja_id: int
    fecha: date
    tipo: str = Field(..., description="INGRESO|EGRESO|APERTURA|CIERRE")
    concepto: str = Field(..., max_length=500)
    monto: Decimal = Field(..., gt=0)
    numero_comprobante: Optional[str] = Field(None, max_length=50)
    beneficiario: Optional[str] = Field(None, max_length=200)


class MovimientoCajaCrear(MovimientoCajaBase):
    pass


class MovimientoCajaRespuesta(MovimientoCajaBase):
    id: int
    asiento_contable_id: Optional[int]
    creado_en: datetime

    model_config = {"from_attributes": True}
