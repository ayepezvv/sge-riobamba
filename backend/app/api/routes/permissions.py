from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.permission import Permission
from app.schemas.permission import PermissionResponse
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[PermissionResponse])
def read_permissions(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(deps.get_current_user)):
    permissions = db.query(Permission).offset(skip).limit(limit).all()
    return permissions
