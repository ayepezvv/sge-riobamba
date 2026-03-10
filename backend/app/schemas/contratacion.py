from app.models.contratacion import StatusItemPac
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class TipoProcesoBase(BaseModel):
    nombre: str
    categoria: str
    condicion_monto: Optional[str] = None
    is_activo: Optional[bool] = True

class TipoProcesoCreate(TipoProcesoBase):
    pass

class TipoProcesoUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    condicion_monto: Optional[str] = None
    is_activo: Optional[bool] = None

class TipoProcesoResponse(TipoProcesoBase):
    id: int
    class Config:
        from_attributes = True

class PlantillaDocumentoBase(BaseModel):
    nombre: str
    ruta_archivo_docx: str
    tipo_proceso_id: Optional[int] = None
    anio: Optional[int] = 2026
    version: Optional[int] = 1
    is_activa: Optional[bool] = True

class PlantillaDocumentoResponse(PlantillaDocumentoBase):
    id: int
    class Config:
        from_attributes = True

class ProcesoContratacionBase(BaseModel):
    codigo_proceso: str
    nombre_proyecto: str
    descripcion: Optional[str] = None
    tipo_proceso_id: Optional[int] = None
    datos_formulario: Optional[Dict[str, Any]] = None

class ProcesoContratacionCreate(ProcesoContratacionBase):
    pass

class DocumentoGeneradoResponse(BaseModel):
    id: int
    plantilla_id: Optional[int]
    version: int
    datos_json: Dict[str, Any]
    ruta_archivo_generado: str
    fecha_generacion: datetime

    class Config:
        from_attributes = True

class ProcesoContratacionResponse(ProcesoContratacionBase):
    id: int
    fecha_creacion: datetime
    documentos: List[DocumentoGeneradoResponse] = []
    
    class Config:
        from_attributes = True

class GenerarDocumentoRequest(BaseModel):
    proceso_contratacion_id: int
    plantilla_id: int
    datos: Dict[str, Any]

class RegenerarDocumentoRequest(BaseModel):
    datos: Dict[str, Any]

class ItemPacBase(BaseModel):
    partida_presupuestaria: str
    cpc: Optional[str] = None
    tipo_compra: Optional[str] = None
    procedimiento: Optional[str] = None
    descripcion: str
    cantidad: float
    costo_unitario: float
    valor_total: float
    status: Optional[StatusItemPac] = StatusItemPac.ACTIVO

class ItemPacCreate(ItemPacBase):
    pass


class PacAnualSimpleResponse(BaseModel):
    id: int
    anio: int
    version_reforma: int
    
    class Config:
        from_attributes = True

class ItemPacResponse(ItemPacBase):
    id: int
    pac_anual_id: int
    status: Optional[StatusItemPac] = StatusItemPac.ACTIVO
    pac: Optional[PacAnualSimpleResponse] = None

    class Config:
        from_attributes = True


class PacAnualBase(BaseModel):
    anio: int
    version_reforma: int
    descripcion: Optional[str] = None
    es_activo: bool = True

class PacAnualCreate(PacAnualBase):
    pass

class PacAnualResponse(PacAnualBase):
    id: int
    items: List[ItemPacResponse] = []

    class Config:
        from_attributes = True

class ProcesoItemPacLinkCreate(BaseModel):
    item_pac_id: int
    monto_comprometido: float

# --- Reforma PAC ---
class MovimientoReformaCreate(BaseModel):
    item_origen_id: int
    item_destino_id: int
    monto_transferido: float

class ReformaPacCreate(BaseModel):
    numero_reforma: int
    resolucion_administrativa: Optional[str] = None
    descripcion_justificacion: str
    movimientos: List[MovimientoReformaCreate]
    nuevos_items: List[ItemPacCreate]

