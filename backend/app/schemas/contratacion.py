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
