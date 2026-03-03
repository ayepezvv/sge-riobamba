from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import date

# ================= PREDIOS =================
class PredioBase(BaseModel):
    clave_catastral: str
    barrio_id: Optional[int] = None
    calle_principal_id: Optional[int] = None
    calle_secundaria_id: Optional[int] = None
    numero_casa: Optional[str] = None
    foto_fachada: Optional[str] = None
    croquis: Optional[str] = None

class PredioCreate(PredioBase):
    geometria_geojson: Optional[Dict[str, Any]] = None

class PredioResponse(PredioBase):
    id: int
    geojson: Optional[Dict[str, Any]] = None
    class Config:
        from_attributes = True

# ================= ACOMETIDAS =================
class AcometidaBase(BaseModel):
    predio_id: int
    ruta_id: Optional[int] = None
    diametro: Optional[float] = None
    material: Optional[str] = None

class AcometidaCreate(AcometidaBase):
    geometria_geojson: Optional[Dict[str, Any]] = None

class AcometidaResponse(AcometidaBase):
    id: int
    geojson: Optional[Dict[str, Any]] = None
    class Config:
        from_attributes = True

# ================= CUENTAS =================
class CuentaBase(BaseModel):
    acometida_id: int
    propietario_id: int
    responsable_pago_id: int
    secuencial_lectura: Optional[int] = None
    estado: Optional[str] = "Activa"
    tiene_alcantarillado: Optional[bool] = True

class CuentaCreate(CuentaBase):
    pass

class CuentaResponse(CuentaBase):
    id: int
    class Config:
        from_attributes = True

# ================= HISTORIAL Y MEDIDORES =================
class MedidorBase(BaseModel):
    marca: Optional[str] = None
    serie: str
    esferas: Optional[int] = 4

class MedidorResponse(MedidorBase):
    id: int
    class Config:
        from_attributes = True

class HistorialMedidorBase(BaseModel):
    cuenta_id: int
    medidor_id: int
    fecha_instalacion: date
    lectura_inicial: int

class HistorialMedidorCreate(HistorialMedidorBase):
    pass

class HistorialMedidorResponse(HistorialMedidorBase):
    id: int
    fecha_retiro: Optional[date] = None
    lectura_retiro: Optional[int] = None
    class Config:
        from_attributes = True

class HistorialTarifaBase(BaseModel):
    cuenta_id: int
    tipo_tarifa: str
    fecha_inicio: date

class HistorialTarifaCreate(HistorialTarifaBase):
    pass

class HistorialTarifaResponse(HistorialTarifaBase):
    id: int
    fecha_fin: Optional[date] = None
    class Config:
        from_attributes = True
