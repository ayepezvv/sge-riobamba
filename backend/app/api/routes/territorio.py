from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Any
import json
from app.api import deps
from app.models.user import User
from app.models.territorio import Red, Sector, Ruta, Barrio, Calle
from app.schemas.territorio import (
    RedCreate, RedResponse, 
    SectorCreate, SectorResponse, 
    RutaCreate, RutaResponse,
    BarrioCreate, BarrioResponse,
    CalleCreate, CalleResponse
)

router = APIRouter()

# ================= REDES =================
@router.get("/redes", response_model=List[RedResponse])
def get_redes(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(Red).all()

@router.post("/redes", response_model=RedResponse)
def create_red(item_in: RedCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_item = Red(**item_in.model_dump(), creado_por_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ================= SECTORES =================
@router.get("/sectores", response_model=List[SectorResponse])
def get_sectores(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(Sector).all()

@router.post("/sectores", response_model=SectorResponse)
def create_sector(item_in: SectorCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_item = Sector(**item_in.model_dump(), creado_por_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ================= RUTAS =================
@router.get("/rutas", response_model=List[RutaResponse])
def get_rutas(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(Ruta).all()

@router.post("/rutas", response_model=RutaResponse)
def create_ruta(item_in: RutaCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_item = Ruta(**item_in.model_dump(), creado_por_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ================= BARRIOS (GIS) =================
@router.get("/barrios", response_model=List[BarrioResponse])
def get_barrios(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    # Usamos ST_AsGeoJSON para que PostgreSQL haga el trabajo pesado de serializar la geometria
    query = db.query(
        Barrio.id, 
        Barrio.nombre, 
        func.ST_AsGeoJSON(Barrio.geometria).label('geojson_str')
    ).all()
    
    results = []
    for row in query:
        results.append({
            "id": row.id,
            "nombre": row.nombre,
            "geojson": json.loads(row.geojson_str) if row.geojson_str else None
        })
    return results

@router.post("/barrios", response_model=BarrioResponse)
def create_barrio(item_in: BarrioCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    geom_wkt = None
    if item_in.geometria_geojson:
        # Envia un ST_GeomFromGeoJSON desde SQLAlchemy (se haria directo en raw sql o func)
        # Para simplificar este insert base, asumimos que viene el WKT o convertimos el dict a json string
        geojson_str = json.dumps(item_in.geometria_geojson)
        geom_wkt = func.ST_SetSRID(func.ST_GeomFromGeoJSON(geojson_str), 4326)
    
    db_item = Barrio(nombre=item_in.nombre, creado_por_id=current_user.id)
    if geom_wkt is not None:
        db_item.geometria = geom_wkt
        
    db.add(db_item)
    db.commit()
    
    # Refetch para obtener el JSON renderizado
    row = db.query(Barrio.id, Barrio.nombre, func.ST_AsGeoJSON(Barrio.geometria).label('geojson_str')).filter(Barrio.id == db_item.id).first()
    return {
        "id": row.id,
        "nombre": row.nombre,
        "geojson": json.loads(row.geojson_str) if row.geojson_str else None
    }

# ================= CALLES (GIS) =================
@router.get("/calles", response_model=List[CalleResponse])
def get_calles(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    query = db.query(
        Calle.id, 
        Calle.nombre, 
        Calle.tipo,
        func.ST_AsGeoJSON(Calle.geometria).label('geojson_str')
    ).all()
    
    results = []
    for row in query:
        results.append({
            "id": row.id,
            "nombre": row.nombre,
            "tipo": row.tipo,
            "geojson": json.loads(row.geojson_str) if row.geojson_str else None
        })
    return results

