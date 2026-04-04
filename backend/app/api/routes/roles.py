from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.role import Role
from app.models.permission import Permission
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[RoleResponse])
def read_roles(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(deps.get_current_user)):
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles

@router.post("/", response_model=RoleResponse)
def create_role(role_in: RoleCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_superadmin)):
    """Solo SuperAdmin puede crear roles."""
    db_role = Role(nombre_rol=role_in.nombre_rol, descripcion=role_in.descripcion)
    if role_in.permission_ids:
        perms = db.query(Permission).filter(Permission.id.in_(role_in.permission_ids)).all()
        db_role.permissions = perms
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/{rol_id}", response_model=RoleResponse)
def obtener_rol_por_id(rol_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    rol = db.query(Role).filter(Role.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role_in: RoleUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_superadmin)):
    """Solo SuperAdmin puede modificar roles."""
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role_in.nombre_rol is not None:
        db_role.nombre_rol = role_in.nombre_rol
    if role_in.descripcion is not None:
        db_role.descripcion = role_in.descripcion

    if role_in.permission_ids is not None:
        perms = db.query(Permission).filter(Permission.id.in_(role_in.permission_ids)).all()
        db_role.permissions = perms

    db.commit()
    db.refresh(db_role)
    return db_role
