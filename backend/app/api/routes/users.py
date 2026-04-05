from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.security import get_password_hash

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(deps.get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def obtener_usuario_por_id(user_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.get("/", response_model=List[UserResponse])

def read_users(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(deps.require_superadmin)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_superadmin)):
    """Solo SuperAdmin puede crear usuarios."""
    user = db.query(User).filter(User.correo == user_in.correo).first()
    if user:
        raise HTTPException(status_code=400, detail="The user with this email already exists in the system.")
    user_data = user_in.model_dump(exclude={"password"})
    user_data["hashed_password"] = get_password_hash(user_in.password)
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{usuario_id}", response_model=UserResponse)
def obtener_usuario_por_id(usuario_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    usuario = db.query(User).filter(User.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    """SuperAdmin puede modificar cualquier usuario. Un usuario puede modificarse a sí mismo."""
    es_superadmin = current_user.role and current_user.role.nombre_rol == "SuperAdmin"
    if not es_superadmin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tiene permiso para modificar este usuario")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_in.model_dump(exclude_unset=True)

    # Solo SuperAdmin puede cambiar el role_id
    if "role_id" in update_data and not es_superadmin:
        raise HTTPException(status_code=403, detail="Solo SuperAdmin puede cambiar el rol de un usuario")

    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]
    elif "password" in update_data:
        del update_data["password"]

    for field, value in update_data.items():
        setattr(user, field, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.patch("/{user_id}/status", response_model=UserResponse)
def toggle_user_status(user_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.require_superadmin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # BUG-01: Protección contra bloqueo del único SuperAdmin activo
    if user.is_active and user.role and user.role.nombre_rol == "SuperAdmin":
        otros_superadmin_activos = (
            db.query(User)
            .join(Role, User.role_id == Role.id)
            .filter(
                Role.nombre_rol == "SuperAdmin",
                User.is_active == True,
                User.id != user.id,
            )
            .count()
        )
        if otros_superadmin_activos == 0:
            raise HTTPException(
                status_code=400,
                detail="No se puede desactivar al único SuperAdmin activo del sistema",
            )
    user.is_active = not user.is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
