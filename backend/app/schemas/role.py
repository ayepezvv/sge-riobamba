from pydantic import BaseModel
from typing import Optional, List
from .permission import PermissionResponse

class RoleBase(BaseModel):
    nombre_rol: str
    descripcion: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: List[int] = []

class RoleUpdate(RoleBase):
    nombre_rol: Optional[str] = None
    descripcion: Optional[str] = None
    permission_ids: Optional[List[int]] = None

class RoleResponse(RoleBase):
    id: int
    permissions: List[PermissionResponse] = []

    class Config:
        from_attributes = True
