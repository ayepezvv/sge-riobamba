from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.parametro import ParametroSistema
from app.schemas.parametro import ParametroCreate, ParametroResponse, ParametroUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[ParametroResponse])
def read_parametros(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(deps.get_current_user)):
    return db.query(ParametroSistema).offset(skip).limit(limit).all()

@router.post("/", response_model=ParametroResponse)
def create_parametro(param_in: ParametroCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_param = db.query(ParametroSistema).filter(ParametroSistema.clave == param_in.clave).first()
    if db_param:
        raise HTTPException(status_code=400, detail="El parametro con esa clave ya existe.")
    
    nuevo_parametro = ParametroSistema(
        **param_in.model_dump(),
        creado_por_id=current_user.id,
        actualizado_por_id=current_user.id
    )
    db.add(nuevo_parametro)
    db.commit()
    db.refresh(nuevo_parametro)
    return nuevo_parametro

@router.put("/{param_id}", response_model=ParametroResponse)
def update_parametro(param_id: int, param_in: ParametroUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_param = db.query(ParametroSistema).filter(ParametroSistema.id == param_id).first()
    if not db_param:
        raise HTTPException(status_code=404, detail="Parametro no encontrado")
        
    update_data = param_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_param, field, value)
    
    db_param.actualizado_por_id = current_user.id
    db.commit()
    db.refresh(db_param)
    return db_param
