from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.api import deps
from app.models.user import User
from app.models.administrativo import Direccion, Unidad, Personal, TituloProfesional
from app.schemas.administrativo import (
    DireccionCreate, DireccionUpdate, DireccionResponse,
    UnidadCreate, UnidadUpdate, UnidadResponse,
    PersonalCreate, PersonalUpdate, PersonalResponse,
    TituloProfesionalCreate, TituloProfesionalResponse
)

router = APIRouter(prefix="/administrativo", tags=["Administrativo"])

# --- Direcciones ---
@router.post("/direcciones", response_model=DireccionResponse, status_code=status.HTTP_201_CREATED)
def crear_direccion(req: DireccionCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = Direccion(**req.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/direcciones", response_model=List[DireccionResponse])
def listar_direcciones(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(Direccion).all()

@router.put("/direcciones/{id}", response_model=DireccionResponse)
def actualizar_direccion(id: int, req: DireccionUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(Direccion).filter(Direccion.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Direccion no encontrada")
    for field, value in req.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/direcciones/{id}")
def eliminar_direccion(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(Direccion).filter(Direccion.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Direccion no encontrada")
    db.delete(db_obj)
    db.commit()
    return {"ok": True}

# --- Unidades ---
@router.post("/unidades", response_model=UnidadResponse, status_code=status.HTTP_201_CREATED)
def crear_unidad(req: UnidadCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = Unidad(**req.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/unidades", response_model=List[UnidadResponse])
def listar_unidades(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(Unidad).options(joinedload(Unidad.direccion)).all()

@router.put("/unidades/{id}", response_model=UnidadResponse)
def actualizar_unidad(id: int, req: UnidadUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(Unidad).filter(Unidad.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    for field, value in req.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/unidades/{id}")
def eliminar_unidad(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(Unidad).filter(Unidad.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    db.delete(db_obj)
    db.commit()
    return {"ok": True}

# --- Personal ---
@router.post("/personal", response_model=PersonalResponse, status_code=status.HTTP_201_CREATED)
def crear_personal(req: PersonalCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = Personal(**req.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/personal/me", response_model=PersonalResponse)
def obtener_mi_perfil(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(Personal).options(
        joinedload(Personal.unidad).joinedload(Unidad.direccion),
        joinedload(Personal.titulos)
    ).filter(Personal.usuario_id == current_user.id).first()
    
    if not db_obj:
        raise HTTPException(status_code=404, detail="Perfil de personal no encontrado para este usuario")
    return db_obj

@router.get("/personal", response_model=List[PersonalResponse])

def listar_personal(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(Personal).options(joinedload(Personal.unidad).joinedload(Unidad.direccion), joinedload(Personal.titulos)).all()

@router.put("/personal/{id}", response_model=PersonalResponse)
def actualizar_personal(id: int, req: PersonalUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(Personal).filter(Personal.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    for field, value in req.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/personal/{id}")
def eliminar_personal(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(Personal).filter(Personal.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    db.delete(db_obj)
    db.commit()
    return {"ok": True}

# --- Titulos Profesionales ---
@router.post("/personal/{id}/titulos", response_model=TituloProfesionalResponse, status_code=status.HTTP_201_CREATED)
def agregar_titulo(id: int, req: TituloProfesionalCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    personal = db.query(Personal).filter(Personal.id == id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    
    db_obj = TituloProfesional(**req.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/personal/titulos/{id}")
def eliminar_titulo(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(TituloProfesional).filter(TituloProfesional.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Titulo no encontrado")
    db.delete(db_obj)
    db.commit()
    return {"ok": True}
