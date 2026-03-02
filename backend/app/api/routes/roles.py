from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleResponse
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[RoleResponse])
def read_roles(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(deps.get_current_user)):
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles

@router.post("/", response_model=RoleResponse)
def create_role(role_in: RoleCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_role = Role(**role_in.model_dump())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role
