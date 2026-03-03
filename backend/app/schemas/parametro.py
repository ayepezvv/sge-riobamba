from pydantic import BaseModel
from typing import Optional

class ParametroBase(BaseModel):
    clave: str
    valor: str
    tipo_dato: str
    descripcion: Optional[str] = None

class ParametroCreate(ParametroBase):
    pass

class ParametroUpdate(BaseModel):
    valor: Optional[str] = None
    tipo_dato: Optional[str] = None
    descripcion: Optional[str] = None

class ParametroResponse(ParametroBase):
    id: int

    class Config:
        from_attributes = True
