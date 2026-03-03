from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.models.ciudadano import Ciudadano, ReferenciaCiudadano
from app.schemas.ciudadano import CiudadanoCreate, CiudadanoResponse, ReferenciaCreate, ReferenciaResponse
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[CiudadanoResponse])
def get_ciudadanos(
    db: Session = Depends(deps.get_db), 
    skip: int = 0, 
    limit: int = 100, 
    identificacion: Optional[str] = Query(None, description="Buscar por cedula/RUC"),
    current_user: User = Depends(deps.get_current_user)
):
    query = db.query(Ciudadano)
    if identificacion:
        query = query.filter(Ciudadano.identificacion.ilike(f"%{identificacion}%"))
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=CiudadanoResponse)
def create_ciudadano(
    item_in: CiudadanoCreate, 
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_user)
):
    existente = db.query(Ciudadano).filter(Ciudadano.identificacion == item_in.identificacion).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un ciudadano registrado con esa identificacion.")
    
    # Extraer y preparar datos
    datos = item_in.model_dump(exclude={"referencias"})
    
    db_item = Ciudadano(**datos, creado_por_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # Si hay referencias anidadas, insertarlas
    if item_in.referencias:
        for ref_in in item_in.referencias:
            db_ref = ReferenciaCiudadano(**ref_in.model_dump(), ciudadano_id=db_item.id, creado_por_id=current_user.id)
            db.add(db_ref)
        db.commit()
        db.refresh(db_item)

    return db_item

@router.post("/{ciudadano_id}/referencias", response_model=ReferenciaResponse)
def add_referencia(
    ciudadano_id: int,
    item_in: ReferenciaCreate, 
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_user)
):
    existente = db.query(Ciudadano).filter(Ciudadano.id == ciudadano_id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="Ciudadano no encontrado.")
        
    db_item = ReferenciaCiudadano(**item_in.model_dump(), ciudadano_id=ciudadano_id, creado_por_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/{ciudadano_id}", response_model=CiudadanoResponse)
def update_ciudadano(
    ciudadano_id: int,
    item_in: dict, # Using dict directly for dynamic partial update
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_user)
):
    db_item = db.query(Ciudadano).filter(Ciudadano.id == ciudadano_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Ciudadano no encontrado")
        
    for field, value in item_in.items():
        if hasattr(db_item, field) and field != "referencias":
            setattr(db_item, field, value)
            
    db.commit()
    db.refresh(db_item)
    return db_item


@router.patch("/{ciudadano_id}/status", response_model=CiudadanoResponse)
def toggle_ciudadano_status(
    ciudadano_id: int, 
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_user)
):
    db_item = db.query(Ciudadano).filter(Ciudadano.id == ciudadano_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Ciudadano no encontrado")
    
    db_item.is_active = not db_item.is_active
    db.commit()
    db.refresh(db_item)
    return db_item
