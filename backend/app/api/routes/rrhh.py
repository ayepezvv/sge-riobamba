"""
Rutas FastAPI — Módulo RRHH V3 (Súper Modelo)
Prefijo: /api/rrhh
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.api import deps
from app.models.user import User
from app.models.rrhh import (
    AreaOrganizacional, EscalaSalarial, Cargo,
    Empleado, EmpleadoCargaFamiliar, HistorialLaboral,
    Contrato, ParametroCalculo
)
from app.schemas.rrhh import (
    AreaOrganizacionalCreate, AreaOrganizacionalUpdate, AreaOrganizacionalResponse,
    EscalaSalarialCreate, EscalaSalarialResponse,
    CargoCreate, CargoUpdate, CargoResponse,
    EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse,
    CargaFamiliarCreate, CargaFamiliarResponse,
    HistorialLaboralCreate, HistorialLaboralResponse,
    ContratoCreate, ContratoUpdate, ContratoResponse,
    ParametroCalculoCreate, ParametroCalculoResponse,
)

router = APIRouter(tags=["RRHH V3"])

_ROLES_RRHH = ["SuperAdmin", "RRHH"]


# =========================================================================
# ÁREA ORGANIZACIONAL
# =========================================================================
@router.get("/areas", response_model=List[AreaOrganizacionalResponse])
def listar_areas(db: Session = Depends(deps.get_db),
                 _: User = Depends(deps.get_current_user)):
    return db.query(AreaOrganizacional).filter(AreaOrganizacional.estado == "ACTIVO").all()

@router.post("/areas", response_model=AreaOrganizacionalResponse, status_code=201)
def crear_area(req: AreaOrganizacionalCreate, db: Session = Depends(deps.get_db),
               _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = AreaOrganizacional(**req.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.put("/areas/{area_id}", response_model=AreaOrganizacionalResponse)
def actualizar_area(area_id: int, req: AreaOrganizacionalUpdate,
                    db: Session = Depends(deps.get_db),
                    _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = db.query(AreaOrganizacional).filter(AreaOrganizacional.id_area == area_id).first()
    if not obj:
        raise HTTPException(404, "Área no encontrada")
    for k, v in req.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj


# =========================================================================
# ESCALA SALARIAL
# =========================================================================
@router.get("/escalas-salariales", response_model=List[EscalaSalarialResponse])
def listar_escalas(db: Session = Depends(deps.get_db),
                   _: User = Depends(deps.get_current_user)):
    return db.query(EscalaSalarial).all()

@router.post("/escalas-salariales", response_model=EscalaSalarialResponse, status_code=201)
def crear_escala(req: EscalaSalarialCreate, db: Session = Depends(deps.get_db),
                 _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = EscalaSalarial(**req.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.put("/escalas-salariales/{escala_id}", response_model=EscalaSalarialResponse)
def actualizar_escala(escala_id: int, req: EscalaSalarialCreate,
                      db: Session = Depends(deps.get_db),
                      _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = db.query(EscalaSalarial).filter(EscalaSalarial.id_escala == escala_id).first()
    if not obj:
        raise HTTPException(404, "Escala salarial no encontrada")
    for k, v in req.model_dump().items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

# =========================================================================
# CARGO
# =========================================================================
@router.get("/cargos", response_model=List[CargoResponse])
def listar_cargos(db: Session = Depends(deps.get_db),
                  _: User = Depends(deps.get_current_user)):
    return (db.query(Cargo)
            .options(joinedload(Cargo.escala))
            .filter(Cargo.estado == "ACTIVO").all())

@router.post("/cargos", response_model=CargoResponse, status_code=201)
def crear_cargo(req: CargoCreate, db: Session = Depends(deps.get_db),
                _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = Cargo(**req.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.put("/cargos/{cargo_id}", response_model=CargoResponse)
def actualizar_cargo(cargo_id: int, req: CargoUpdate,
                     db: Session = Depends(deps.get_db),
                     _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = db.query(Cargo).filter(Cargo.id_cargo == cargo_id).first()
    if not obj:
        raise HTTPException(404, "Cargo no encontrado")
    for k, v in req.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj


# =========================================================================
# EMPLEADO — CRUD COMPLETO
# =========================================================================
@router.get("/empleados", response_model=List[EmpleadoResponse])
def listar_empleados(db: Session = Depends(deps.get_db),
                     _: User = Depends(deps.require_role(_ROLES_RRHH))):
    return (
        db.query(Empleado)
        .options(
            joinedload(Empleado.historial).joinedload(HistorialLaboral.area),
            joinedload(Empleado.historial).joinedload(HistorialLaboral.cargo)
                .joinedload(Cargo.escala),
            joinedload(Empleado.cargas),
        )
        .filter(Empleado.eliminado_en.is_(None))
        .order_by(Empleado.apellidos, Empleado.nombres)
        .all()
    )

@router.get("/empleados/{empleado_id}", response_model=EmpleadoResponse)
def obtener_empleado(empleado_id: int, db: Session = Depends(deps.get_db),
                     _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = (
        db.query(Empleado)
        .options(
            joinedload(Empleado.historial).joinedload(HistorialLaboral.area),
            joinedload(Empleado.historial).joinedload(HistorialLaboral.cargo)
                .joinedload(Cargo.escala),
            joinedload(Empleado.cargas),
        )
        .filter(Empleado.id_empleado == empleado_id, Empleado.eliminado_en.is_(None))
        .first()
    )
    if not obj:
        raise HTTPException(404, "Empleado no encontrado")
    return obj

@router.post("/empleados", response_model=EmpleadoResponse, status_code=201)
def crear_empleado(req: EmpleadoCreate, db: Session = Depends(deps.get_db),
                   current_user: User = Depends(deps.require_role(_ROLES_RRHH))):
    if db.query(Empleado).filter(Empleado.identificacion == req.identificacion).first():
        raise HTTPException(400, f"Ya existe un empleado con identificación {req.identificacion}")
    data = req.model_dump()
    obj = Empleado(**data, creado_por_id=current_user.id)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.put("/empleados/{empleado_id}", response_model=EmpleadoResponse)
def actualizar_empleado(empleado_id: int, req: EmpleadoUpdate,
                        db: Session = Depends(deps.get_db),
                        current_user: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = db.query(Empleado).filter(Empleado.id_empleado == empleado_id).first()
    if not obj:
        raise HTTPException(404, "Empleado no encontrado")
    for k, v in req.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.actualizado_por_id = current_user.id
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/empleados/{empleado_id}", status_code=204)
def desvincular_empleado(empleado_id: int, db: Session = Depends(deps.get_db),
                         current_user: User = Depends(deps.require_role(_ROLES_RRHH))):
    """Soft Delete: registra eliminado_en + estado DESVINCULADO."""
    obj = db.query(Empleado).filter(Empleado.id_empleado == empleado_id).first()
    if not obj:
        raise HTTPException(404, "Empleado no encontrado")
    obj.eliminado_en = datetime.utcnow()
    obj.estado_empleado = "DESVINCULADO"
    obj.actualizado_por_id = current_user.id
    db.commit()


# =========================================================================
# HISTORIAL LABORAL (Effective Dating)
# =========================================================================
@router.post("/empleados/{empleado_id}/historial",
             response_model=HistorialLaboralResponse, status_code=201)
def registrar_historial(empleado_id: int, req: HistorialLaboralCreate,
                        db: Session = Depends(deps.get_db),
                        _: User = Depends(deps.require_role(_ROLES_RRHH))):
    """
    Implementa Effective Dating:
    1. Cierra registro activo anterior (fecha_fin = hoy).
    2. Inserta nuevo registro.
    """
    if not db.query(Empleado).filter(Empleado.id_empleado == empleado_id).first():
        raise HTTPException(404, "Empleado no encontrado")

    activo = (db.query(HistorialLaboral)
              .filter(HistorialLaboral.id_empleado == empleado_id,
                      HistorialLaboral.fecha_fin.is_(None))
              .first())
    if activo:
        activo.fecha_fin = req.fecha_inicio

    obj = HistorialLaboral(**req.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/empleados/{empleado_id}/historial",
            response_model=List[HistorialLaboralResponse])
def historial_empleado(empleado_id: int, db: Session = Depends(deps.get_db),
                       _: User = Depends(deps.require_role(_ROLES_RRHH))):
    return (db.query(HistorialLaboral)
            .options(joinedload(HistorialLaboral.area),
                     joinedload(HistorialLaboral.cargo))
            .filter(HistorialLaboral.id_empleado == empleado_id)
            .order_by(HistorialLaboral.fecha_inicio.desc())
            .all())


# =========================================================================
# CARGAS FAMILIARES
# =========================================================================
@router.post("/empleados/{empleado_id}/cargas",
             response_model=CargaFamiliarResponse, status_code=201)
def agregar_carga(empleado_id: int, req: CargaFamiliarCreate,
                  db: Session = Depends(deps.get_db),
                  _: User = Depends(deps.require_role(_ROLES_RRHH))):
    if not db.query(Empleado).filter(Empleado.id_empleado == empleado_id).first():
        raise HTTPException(404, "Empleado no encontrado")
    obj = EmpleadoCargaFamiliar(**req.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete("/cargas/{carga_id}", status_code=204)
def eliminar_carga(carga_id: int, db: Session = Depends(deps.get_db),
                   _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = db.query(EmpleadoCargaFamiliar).filter(
        EmpleadoCargaFamiliar.id_carga == carga_id).first()
    if not obj:
        raise HTTPException(404, "Carga familiar no encontrada")
    db.delete(obj); db.commit()

# =========================================================================
# CONTRATOS
# =========================================================================
@router.get("/contratos", response_model=List[ContratoResponse])
def listar_contratos(db: Session = Depends(deps.get_db),
                     _: User = Depends(deps.get_current_user)):
    return (db.query(Contrato)
            .options(joinedload(Contrato.empleado),
                     joinedload(Contrato.cargo),
                     joinedload(Contrato.escala))
            .order_by(Contrato.fecha_inicio.desc()).all())

@router.get("/contratos/{contrato_id}", response_model=ContratoResponse)
def detalle_contrato(contrato_id: int, db: Session = Depends(deps.get_db),
                     _: User = Depends(deps.get_current_user)):
    obj = db.query(Contrato).filter(Contrato.id_contrato == contrato_id).first()
    if not obj: raise HTTPException(404, "Contrato no encontrado")
    return obj

@router.post("/contratos", response_model=ContratoResponse, status_code=201)
def crear_contrato(req: ContratoCreate, db: Session = Depends(deps.get_db),
                   _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = Contrato(**req.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.put("/contratos/{contrato_id}", response_model=ContratoResponse)
def actualizar_contrato(contrato_id: int, req: ContratoUpdate,
                        db: Session = Depends(deps.get_db),
                        _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = db.query(Contrato).filter(Contrato.id_contrato == contrato_id).first()
    if not obj: raise HTTPException(404, "Contrato no encontrado")
    for k, v in req.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

# =========================================================================
# PARAMETROS DE NOMINA (ParametroCalculo)
# =========================================================================
@router.get("/parametros-calculo", response_model=List[ParametroCalculoResponse])
def listar_parametros(db: Session = Depends(deps.get_db),
                      _: User = Depends(deps.get_current_user)):
    return db.query(ParametroCalculo).order_by(ParametroCalculo.anio_vigencia.desc(), ParametroCalculo.codigo_parametro).all()

@router.post("/parametros-calculo", response_model=ParametroCalculoResponse, status_code=201)
def crear_parametro(req: ParametroCalculoCreate, db: Session = Depends(deps.get_db),
                    _: User = Depends(deps.require_role(_ROLES_RRHH))):
    # validar uq
    exists = db.query(ParametroCalculo).filter(
        ParametroCalculo.anio_vigencia == req.anio_vigencia,
        ParametroCalculo.codigo_parametro == req.codigo_parametro
    ).first()
    if exists: raise HTTPException(400, "El parámetro ya existe para ese año")
    obj = ParametroCalculo(**req.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.put("/parametros-calculo/{param_id}", response_model=ParametroCalculoResponse)
def actualizar_parametro(param_id: int, req: ParametroCalculoCreate,
                         db: Session = Depends(deps.get_db),
                         _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = db.query(ParametroCalculo).filter(ParametroCalculo.id_parametro == param_id).first()
    if not obj: raise HTTPException(404, "Parámetro no encontrado")
    for k, v in req.model_dump().items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj
