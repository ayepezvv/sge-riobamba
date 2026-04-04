import ipaddress
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.informatica import SegmentoRed, DireccionIpAsignada
from app.schemas.informatica import (
    SegmentoRedCreate, SegmentoRedUpdate, SegmentoRed as SegmentoRedSchema,
    DireccionIpAsignadaCreate, DireccionIpAsignadaUpdate, DireccionIpAsignada as DireccionIpSchema
)

router = APIRouter()

# --- SegmentoRed Endpoints ---

@router.get("/segmentos", response_model=List[SegmentoRedSchema])
def get_segmentos(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(SegmentoRed).order_by(SegmentoRed.nombre).all()

@router.get("/segmentos/{id}", response_model=SegmentoRedSchema)
def get_segmento(id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    segmento = db.query(SegmentoRed).filter(SegmentoRed.id == id).first()
    if not segmento:
        raise HTTPException(status_code=404, detail="Segmento no encontrado")
    return segmento

@router.post("/segmentos", response_model=SegmentoRedSchema)
def create_segmento(req: SegmentoRedCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    from sqlalchemy import text
    try:
        db.execute(text("CREATE SCHEMA IF NOT EXISTS informatica;"))
        db.commit()
    except Exception:
        db.rollback()

    db_obj = SegmentoRed(
        id=req.id or str(uuid.uuid4()),
        nombre=req.nombre,
        red_cidr=req.red_cidr,
        descripcion=req.descripcion,
        is_active=req.is_active
    )
    db.add(db_obj)
    try:
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_obj

@router.put("/segmentos/{id}", response_model=SegmentoRedSchema)
def update_segmento(id: str, req: SegmentoRedUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    segmento = db.query(SegmentoRed).filter(SegmentoRed.id == id).first()
    if not segmento:
        raise HTTPException(status_code=404, detail="Segmento no encontrado")

    update_data = req.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(segmento, key, value)

    db.commit()
    db.refresh(segmento)
    return segmento

@router.delete("/segmentos/{id}")
def delete_segmento(id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    segmento = db.query(SegmentoRed).filter(SegmentoRed.id == id).first()
    if not segmento:
        raise HTTPException(status_code=404, detail="Segmento no encontrado")
    db.delete(segmento)
    db.commit()
    return {"ok": True}

# --- DireccionIpAsignada Endpoints ---

@router.get("/segmentos/{segmento_id}/ips", response_model=List[DireccionIpSchema])
def get_ips_by_segmento(segmento_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(DireccionIpAsignada).options(joinedload(DireccionIpAsignada.personal), joinedload(DireccionIpAsignada.activo)).filter(DireccionIpAsignada.segmento_id == segmento_id).all()

@router.post("/ips", response_model=DireccionIpSchema)
def create_ip(req: DireccionIpAsignadaCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    from sqlalchemy import text
    try:
        db.execute(text("CREATE SCHEMA IF NOT EXISTS informatica;"))
        db.commit()
    except Exception:
        db.rollback()

    segmento = db.query(SegmentoRed).filter(SegmentoRed.id == req.segmento_id).first()
    if not segmento:
        raise HTTPException(status_code=404, detail="Segmento de red no encontrado")

    cidr = ipaddress.IPv4Network(segmento.red_cidr, strict=False)
    ip_add = ipaddress.IPv4Address(req.direccion_ip)

    if ip_add not in cidr:
        raise HTTPException(status_code=400, detail="La IP no pertenece a este segmento")

    existing_ip = db.query(DireccionIpAsignada).filter(DireccionIpAsignada.direccion_ip == req.direccion_ip).first()
    if existing_ip:
        raise HTTPException(status_code=400, detail="La dirección IP ya está asignada")

    db_obj = DireccionIpAsignada(
        id=req.id or str(uuid.uuid4()),
        segmento_id=req.segmento_id,
        direccion_ip=req.direccion_ip,
        mac_address=req.mac_address,
        nombre_equipo=req.nombre_equipo,
        dominio=req.dominio,
        ubicacion_geografica=req.ubicacion_geografica,
        personal_id=req.personal_id,
        activo_id=req.activo_id,
        is_active=req.is_active
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.put("/ips/{id}", response_model=DireccionIpSchema)
def update_ip(id: str, req: DireccionIpAsignadaUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    ip_obj = db.query(DireccionIpAsignada).filter(DireccionIpAsignada.id == id).first()
    if not ip_obj:
        raise HTTPException(status_code=404, detail="IP no encontrada")

    new_ip = req.direccion_ip if req.direccion_ip else ip_obj.direccion_ip
    new_segmento_id = req.segmento_id if req.segmento_id else ip_obj.segmento_id

    segmento = db.query(SegmentoRed).filter(SegmentoRed.id == new_segmento_id).first()
    if not segmento:
        raise HTTPException(status_code=404, detail="Segmento de red no encontrado")

    cidr = ipaddress.IPv4Network(segmento.red_cidr, strict=False)
    ip_add = ipaddress.IPv4Address(new_ip)
    if ip_add not in cidr:
        raise HTTPException(status_code=400, detail="La IP no pertenece a este segmento")

    update_data = req.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ip_obj, key, value)

    db.commit()
    db.refresh(ip_obj)
    return ip_obj

@router.delete("/ips/{id}")
def delete_ip(id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    ip_obj = db.query(DireccionIpAsignada).filter(DireccionIpAsignada.id == id).first()
    if not ip_obj:
        raise HTTPException(status_code=404, detail="IP no encontrada")
    db.delete(ip_obj)
    db.commit()
    return {"ok": True}

@router.get("/stats", response_model=dict)
def get_ipam_stats(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    segmentos = db.query(SegmentoRed).count()
    ips = db.query(DireccionIpAsignada).count()
    return {"total_segmentos": segmentos, "total_ips_asignadas": ips}
