"""
Schemas Pydantic para el módulo Financiero (AR/AP).
Nomenclatura en español conforme a Regla Arquitectónica 2.
"""
from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


# ---------------------------------------------------------------------------
# TipoDocumentoConfig
# ---------------------------------------------------------------------------

class TipoDocumentoBase(BaseModel):
    codigo: str = Field(..., max_length=10)
    nombre: str = Field(..., max_length=100)
    tipo: str = Field(..., description="FACTURA|NOTA_CREDITO|NOTA_DEBITO|LIQUIDACION|PROFORMA|CERTIFICADO_PRESUPUESTARIO")
    secuencia_prefijo: Optional[str] = Field(None, max_length=10)
    es_activo: bool = True


class TipoDocumentoCrear(TipoDocumentoBase):
    pass


class TipoDocumentoActualizar(BaseModel):
    nombre: Optional[str] = None
    secuencia_prefijo: Optional[str] = None
    es_activo: Optional[bool] = None


class TipoDocumentoRespuesta(TipoDocumentoBase):
    id: int
    secuencia_siguiente: int
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# LineaFactura
# ---------------------------------------------------------------------------

class LineaFacturaCrear(BaseModel):
    orden: int = 1
    descripcion: str = Field(..., max_length=500)
    cuenta_contable_id: Optional[int] = None
    cantidad: Decimal = Field(Decimal("1"), gt=0)
    precio_unitario: Decimal = Field(Decimal("0"), ge=0)
    descuento_linea: Decimal = Decimal("0")
    tipo_impuesto: str = Field("IVA_15", description="IVA_15|IVA_12|IVA_5|IVA_0|EXENTO|ICE")
    porcentaje_impuesto: Decimal = Decimal("15")


class LineaFacturaRespuesta(LineaFacturaCrear):
    id: int
    factura_id: int
    subtotal_linea: Decimal
    valor_impuesto: Decimal
    total_linea: Decimal
    creado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Factura
# ---------------------------------------------------------------------------

class FacturaBase(BaseModel):
    tipo_documento_id: int
    tipo: str = Field(..., description="CLIENTE | PROVEEDOR")
    tercero_id: Optional[int] = None
    nombre_tercero: str = Field(..., max_length=200)
    identificacion_tercero: str = Field(..., max_length=20)
    fecha_emision: date
    fecha_vencimiento: Optional[date] = None
    clave_acceso_sri: Optional[str] = Field(None, max_length=49)
    numero_autorizacion_sri: Optional[str] = Field(None, max_length=49)
    observaciones: Optional[str] = None


class FacturaCrear(FacturaBase):
    lineas: List[LineaFacturaCrear] = []


class FacturaActualizar(BaseModel):
    fecha_vencimiento: Optional[date] = None
    clave_acceso_sri: Optional[str] = None
    numero_autorizacion_sri: Optional[str] = None
    observaciones: Optional[str] = None


class AprobarFactura(BaseModel):
    numero: Optional[str] = Field(None, description="Si se omite, se genera automáticamente")


class AnularFactura(BaseModel):
    motivo_anulacion: str = Field(..., min_length=5)


class FacturaRespuesta(FacturaBase):
    id: int
    numero: str
    estado: str
    subtotal: Decimal
    descuento: Decimal
    base_imponible: Decimal
    total_iva: Decimal
    total: Decimal
    saldo_pendiente: Decimal
    asiento_contable_id: Optional[int]
    lineas: List[LineaFacturaRespuesta] = []
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


class ResumenFactura(BaseModel):
    id: int
    numero: str
    tipo: str
    estado: str
    nombre_tercero: str
    identificacion_tercero: str
    fecha_emision: date
    total: Decimal
    saldo_pendiente: Decimal

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Pago
# ---------------------------------------------------------------------------

class LineaPagoCrear(BaseModel):
    factura_id: int
    monto_aplicado: Decimal = Field(..., gt=0)


class LineaPagoRespuesta(LineaPagoCrear):
    id: int
    pago_id: int
    creado_en: datetime

    model_config = {"from_attributes": True}


class PagoBase(BaseModel):
    tipo: str = Field(..., description="CLIENTE | PROVEEDOR")
    tercero_id: Optional[int] = None
    nombre_tercero: str = Field(..., max_length=200)
    identificacion_tercero: str = Field(..., max_length=20)
    fecha_pago: date
    tipo_pago: str = Field("TRANSFERENCIA", description="EFECTIVO|CHEQUE|TRANSFERENCIA|SPI|BCE|NOTA_CREDITO")
    cuenta_bancaria_id: Optional[int] = None
    monto_total: Decimal = Field(..., gt=0)
    referencia_bancaria: Optional[str] = Field(None, max_length=100)
    observaciones: Optional[str] = None


class PagoCrear(PagoBase):
    lineas: List[LineaPagoCrear] = []

    @model_validator(mode="after")
    def validar_suma_lineas(self) -> "PagoCrear":
        if self.lineas:
            suma = sum(l.monto_aplicado for l in self.lineas)
            if suma != self.monto_total:
                raise ValueError(
                    f"La suma de líneas ({suma}) no coincide con monto_total ({self.monto_total})")
        return self


class ConfirmarPago(BaseModel):
    numero: Optional[str] = Field(None, description="Si se omite, se genera automáticamente")


class AnularPago(BaseModel):
    motivo_anulacion: str = Field(..., min_length=5)


class PagoRespuesta(PagoBase):
    id: int
    numero: str
    estado: str
    asiento_contable_id: Optional[int]
    asiento_traslado_id: Optional[int]
    lineas: List[LineaPagoRespuesta] = []
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# CierreRecaudacion
# ---------------------------------------------------------------------------

class CierreRecaudacionCrear(BaseModel):
    fecha: date
    total_recaudado: Decimal
    numero_transacciones: int = 0
    observaciones: Optional[str] = None


class CierreRecaudacionRespuesta(CierreRecaudacionCrear):
    id: int
    asiento_recaudacion_id: Optional[int]
    asiento_traslado_bce_id: Optional[int]
    creado_en: datetime

    model_config = {"from_attributes": True}
