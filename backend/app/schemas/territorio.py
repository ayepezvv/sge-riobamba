from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

# GeoJSON Helpers
class FeatureGeometry(BaseModel):
    type: str
    coordinates: Any

class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: FeatureGeometry
    properties: Dict[str, Any] = {}

class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]

# ================= REDES =================
class RedBase(BaseModel):
    nombre: str
    codigo: str

class RedCreate(RedBase):
    pass

class RedResponse(RedBase):
    id: int
    class Config:
        from_attributes = True

# ================= SECTORES =================
class SectorBase(BaseModel):
    nombre: str
    codigo_sector: str
    red_id: int

class SectorCreate(SectorBase):
    pass

class SectorResponse(SectorBase):
    id: int
    class Config:
        from_attributes = True

# ================= RUTAS =================
class RutaBase(BaseModel):
    nombre: str
    codigo_ruta: str
    sector_id: int

class RutaCreate(RutaBase):
    pass

class RutaResponse(RutaBase):
    id: int
    class Config:
        from_attributes = True

# ================= BARRIOS (GIS) =================
class BarrioBase(BaseModel):
    nombre: str

class BarrioCreate(BarrioBase):
    # Opcionalmente se puede enviar un WKT o GeoJSON dict desde el frontend
    geometria_geojson: Optional[Dict[str, Any]] = None 

class BarrioResponse(BarrioBase):
    id: int
    geojson: Optional[Dict[str, Any]] = None # Devolveremos Feature GeoJSON aqui
    
    class Config:
        from_attributes = True

# ================= CALLES (GIS) =================
class CalleBase(BaseModel):
    nombre: str
    tipo: str

class CalleCreate(CalleBase):
    geometria_geojson: Optional[Dict[str, Any]] = None 

class CalleResponse(CalleBase):
    id: int
    geojson: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True

