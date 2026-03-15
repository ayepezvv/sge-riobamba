"""
Rutas FastAPI — Módulo Administrativo
Scope: Estructura organizacional base (Direcciones, Unidades, Puestos).

NOTA: Los endpoints de Empleado, EscalaSalarial, TituloProfesional y
CargaFamiliar fueron migrados a /api/rrhh (routes/rrhh.py) en la Fase V3.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.api import deps
from app.models.user import User
from app.models.administrativo import Direccion, Unidad, Puesto
from app.schemas.administrativo import (
    DireccionCreate, DireccionUpdate, DireccionResponse,
    UnidadCreate, UnidadUpdate, UnidadResponse,
    PuestoCreate, PuestoUpdate, PuestoResponse,
)

router = APIRouter(tags=["Administrativo - Estructura Organizacional"])


# =========================================================================
# DIRECCIONES
# =========================================================================

@router.post("/direcciones", response_model=DireccionResponse, status_code=status.HTTP_201_CREATED)
def crear_direccion(
    req: DireccionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_obj = Direccion(**req.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/direcciones", response_model=List[DireccionResponse])
def listar_direcciones(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return db.query(Direccion).filter(Direccion.es_activo == True).all()  # noqa: E712


@router.get("/direcciones/{dir_id}", response_model=DireccionResponse)
def obtener_direccion(
    dir_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    obj = db.query(Direccion).filter(Direccion.id == dir_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    return obj


@router.put("/direcciones/{dir_id}", response_model=DireccionResponse)
def actualizar_direccion(
    dir_id: int,
    req: DireccionUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    obj = db.query(Direccion).filter(Direccion.id == dir_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


# =========================================================================
# UNIDADES
# =========================================================================

@router.post("/unidades", response_model=UnidadResponse, status_code=status.HTTP_201_CREATED)
def crear_unidad(
    req: UnidadCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_obj = Unidad(**req.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/unidades", response_model=List[UnidadResponse])
def listar_unidades(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return (
        db.query(Unidad)
        .options(joinedload(Unidad.direccion))
        .filter(Unidad.es_activo == True)  # noqa: E712
        .all()
    )


@router.get("/unidades/{unidad_id}", response_model=UnidadResponse)
def obtener_unidad(
    unidad_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    obj = db.query(Unidad).options(joinedload(Unidad.direccion)).filter(Unidad.id == unidad_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    return obj


@router.put("/unidades/{unidad_id}", response_model=UnidadResponse)
def actualizar_unidad(
    unidad_id: int,
    req: UnidadUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    obj = db.query(Unidad).filter(Unidad.id == unidad_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


# =========================================================================
# PUESTOS
# =========================================================================

@router.post("/puestos", response_model=PuestoResponse, status_code=status.HTTP_201_CREATED)
def crear_puesto(
    req: PuestoCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_obj = Puesto(**req.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/puestos", response_model=List[PuestoResponse])
def listar_puestos(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return db.query(Puesto).filter(Puesto.es_activo == True).all()  # noqa: E712


@router.get("/puestos/{puesto_id}", response_model=PuestoResponse)
def obtener_puesto(
    puesto_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    obj = db.query(Puesto).filter(Puesto.id == puesto_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Puesto no encontrado")
    return obj


@router.put("/puestos/{puesto_id}", response_model=PuestoResponse)
def actualizar_puesto(
    puesto_id: int,
    req: PuestoUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    obj = db.query(Puesto).filter(Puesto.id == puesto_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Puesto no encontrado")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj
