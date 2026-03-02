from pydantic import BaseModel
from typing import Optional

class RoleBase(BaseModel):
    nombre_rol: str
    descripcion: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True
