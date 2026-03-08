from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class TipoProcesoBase(BaseModel):
    nombre: str

class TipoProcesoResponse(TipoProcesoBase):
    id: int
    class Config:
        from_attributes = True

class PlantillaDocumentoBase(BaseModel):
    nombre: str
    ruta_archivo_docx: str
    tipo_proceso_id: Optional[int] = None

class PlantillaDocumentoResponse(PlantillaDocumentoBase):
    id: int
    class Config:
        from_attributes = True

class ProcesoContratacionBase(BaseModel):
    codigo_proceso: str
    nombre_proyecto: str
    descripcion: Optional[str] = None

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
