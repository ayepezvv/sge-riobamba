from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import json
from app.api import deps
from app.models.user import User
from app.models.comercial import Predio, Acometida, Cuenta
from app.schemas.comercial import (
    PredioCreate, PredioResponse,
    AcometidaCreate, AcometidaResponse,
    CuentaCreate, CuentaResponse
)

router = APIRouter()

# ================= PREDIOS =================
@router.get("/predios", response_model=List[PredioResponse])
def get_predios(
    db: Session = Depends(deps.get_db), 
    skip: int = 0, 
    limit: int = 100, 
    clave_catastral: Optional[str] = Query(None, description="Filtrar por clave catastral"),
    current_user: User = Depends(deps.get_current_user)
):
    query = db.query(
        Predio.id, 
        Predio.clave_catastral,
        Predio.barrio_id,
        Predio.calle_principal_id,
        Predio.calle_secundaria_id,
        Predio.numero_casa,
        Predio.foto_fachada,
        Predio.croquis,
        func.ST_AsGeoJSON(Predio.geometria).label('geojson_str')
    )
    
    if clave_catastral:
        query = query.filter(Predio.clave_catastral.ilike(f"%{clave_catastral}%"))
        
    rows = query.offset(skip).limit(limit).all()
    
    results = []
    for row in rows:
        results.append({
            "id": row.id,
            "clave_catastral": row.clave_catastral,
            "barrio_id": row.barrio_id,
            "calle_principal_id": row.calle_principal_id,
            "calle_secundaria_id": row.calle_secundaria_id,
            "numero_casa": row.numero_casa,
            "foto_fachada": row.foto_fachada,
            "croquis": row.croquis,
            "geojson": json.loads(row.geojson_str) if row.geojson_str else None
        })
    return results

@router.post("/predios", response_model=PredioResponse)
def create_predio(
    item_in: PredioCreate, 
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_user)
):
    existente = db.query(Predio).filter(Predio.clave_catastral == item_in.clave_catastral).first()
    if existente:
        raise HTTPException(status_code=400, detail="La clave catastral ya existe")

    geom_wkt = None
    if item_in.geometria_geojson:
        geojson_str = json.dumps(item_in.geometria_geojson)
        geom_wkt = func.ST_SetSRID(func.ST_GeomFromGeoJSON(geojson_str), 4326)
    
    datos = item_in.model_dump(exclude={"geometria_geojson"})
    db_item = Predio(**datos, creado_por_id=current_user.id)
    
    if geom_wkt is not None:
        db_item.geometria = geom_wkt
        
    db.add(db_item)
    db.commit()
    
    # Refetch para JSON
    row = db.query(Predio.id, func.ST_AsGeoJSON(Predio.geometria).label('geojson_str')).filter(Predio.id == db_item.id).first()
    
    response_data = item_in.model_dump(exclude={"geometria_geojson"})
    response_data["id"] = db_item.id
    response_data["geojson"] = json.loads(row.geojson_str) if row.geojson_str else None
    return response_data

# ================= ACOMETIDAS =================
@router.get("/acometidas", response_model=List[AcometidaResponse])
def get_acometidas(
    db: Session = Depends(deps.get_db), 
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(deps.get_current_user)
):
    query = db.query(
        Acometida.id, 
        Acometida.predio_id,
        Acometida.ruta_id,
        Acometida.diametro,
        Acometida.material,
        func.ST_AsGeoJSON(Acometida.geometria).label('geojson_str')
    )
    rows = query.offset(skip).limit(limit).all()
    
    results = []
    for row in rows:
        results.append({
            "id": row.id,
            "predio_id": row.predio_id,
            "ruta_id": row.ruta_id,
            "diametro": row.diametro,
            "material": row.material,
            "geojson": json.loads(row.geojson_str) if row.geojson_str else None
        })
    return results

@router.post("/acometidas", response_model=AcometidaResponse)
def create_acometida(
    item_in: AcometidaCreate, 
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_user)
):
    geom_wkt = None
    if item_in.geometria_geojson:
        geojson_str = json.dumps(item_in.geometria_geojson)
        geom_wkt = func.ST_SetSRID(func.ST_GeomFromGeoJSON(geojson_str), 4326)
    
    datos = item_in.model_dump(exclude={"geometria_geojson"})
    db_item = Acometida(**datos, creado_por_id=current_user.id)
    
    if geom_wkt is not None:
        db_item.geometria = geom_wkt
        
    db.add(db_item)
    db.commit()
    
    row = db.query(Acometida.id, func.ST_AsGeoJSON(Acometida.geometria).label('geojson_str')).filter(Acometida.id == db_item.id).first()
    response_data = item_in.model_dump(exclude={"geometria_geojson"})
    response_data["id"] = db_item.id
    response_data["geojson"] = json.loads(row.geojson_str) if row.geojson_str else None
    return response_data

# ================= CUENTAS =================
@router.get("/cuentas", response_model=List[CuentaResponse])
def get_cuentas(
    db: Session = Depends(deps.get_db), 
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(deps.get_current_user)
):
    return db.query(Cuenta).offset(skip).limit(limit).all()

@router.post("/cuentas", response_model=CuentaResponse)
def create_cuenta(
    item_in: CuentaCreate, 
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_user)
):
    db_item = Cuenta(**item_in.model_dump(), creado_por_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
