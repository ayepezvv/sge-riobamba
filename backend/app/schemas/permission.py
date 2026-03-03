from pydantic import BaseModel

class PermissionBase(BaseModel):
    nombre_permiso: str

class PermissionResponse(PermissionBase):
    id: int
    class Config:
        from_attributes = True
