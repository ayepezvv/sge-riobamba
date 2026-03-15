from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.api.deps import get_db

from app.models.bodega import CategoriaBien, ActivoFijo
from app.schemas.bodega import (
    CategoriaBienCreate, CategoriaBienUpdate, CategoriaBienSchema,
    ActivoFijoCreate, ActivoFijoUpdate, ActivoFijoSchema
)

router = APIRouter(tags=["Bodega y Activos Fijos"])

# --- Categorias ---
@router.get("/categorias", response_model=List[CategoriaBienSchema])
def get_categorias(db: Session = Depends(get_db)):
    from sqlalchemy import text
    try:
        db.execute(text("CREATE SCHEMA IF NOT EXISTS bodega;"))
        db.commit()
    except Exception:
        db.rollback()
    return db.query(CategoriaBien).all()

@router.post("/categorias", response_model=CategoriaBienSchema, status_code=status.HTTP_201_CREATED)
def create_categoria(req: CategoriaBienCreate, db: Session = Depends(get_db)):
    from sqlalchemy import text
    try:
        db.execute(text("CREATE SCHEMA IF NOT EXISTS bodega;"))
        db.commit()
    except Exception:
        db.rollback()
        
    db_obj = CategoriaBien(**req.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.put("/categorias/{id}", response_model=CategoriaBienSchema)
def update_categoria(id: int, req: CategoriaBienUpdate, db: Session = Depends(get_db)):
    db_obj = db.query(CategoriaBien).filter(CategoriaBien.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/categorias/{id}")
def delete_categoria(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(CategoriaBien).filter(CategoriaBien.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(db_obj)
    db.commit()
    return {"ok": True}

# --- Activos Fijos ---
@router.get("/activos", response_model=List[ActivoFijoSchema])
def get_activos(db: Session = Depends(get_db)):
    return db.query(ActivoFijo).options(joinedload(ActivoFijo.categoria)).all()

@router.post("/activos", response_model=ActivoFijoSchema, status_code=status.HTTP_201_CREATED)
def create_activo(req: ActivoFijoCreate, db: Session = Depends(get_db)):
    categoria = db.query(CategoriaBien).filter(CategoriaBien.id == req.categoria_id).first()
    if not categoria:
         raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db_obj = ActivoFijo(**req.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.put("/activos/{id}", response_model=ActivoFijoSchema)
def update_activo(id: int, req: ActivoFijoUpdate, db: Session = Depends(get_db)):
    db_obj = db.query(ActivoFijo).filter(ActivoFijo.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Activo Fijo no encontrado")
    
    if req.categoria_id:
        categoria = db.query(CategoriaBien).filter(CategoriaBien.id == req.categoria_id).first()
        if not categoria:
             raise HTTPException(status_code=404, detail="Categoría no encontrada")

    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/activos/{id}")
def delete_activo(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(ActivoFijo).filter(ActivoFijo.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Activo Fijo no encontrado")
    db.delete(db_obj)
    db.commit()
    return {"ok": True}
