"""
Rutas FastAPI — Motor de Nómina / Rol de Pagos
Prefijo: /api/rrhh/nomina
Esquema: rrhh
"""
from datetime import date
from io import StringIO, BytesIO
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.api import deps
from app.models.user import User
from app.models.rrhh import (
    RolPago, LineaRolPago, DetalleLineaRol,
    RubroNomina, Empleado,
)
from app.schemas.rrhh import (
    RolPagoCreate, RolPagoResponse, RolPagoDetalleResponse,
    LineaRolPagoUpdate, LineaRolPagoResponse,
    RubroNominaCreate, RubroNominaResponse,
)
from app.services.servicio_nomina import generar_rol, generar_archivo_spi, generar_asiento_nomina

router = APIRouter(tags=["Nómina / Rol de Pagos"])
_ROLES_RRHH = ["SuperAdmin", "RRHH"]


# =========================================================================
# RUBROS DE NÓMINA (catálogo)
# =========================================================================
@router.get("/rubros", response_model=List[RubroNominaResponse])
def listar_rubros(db: Session = Depends(deps.get_db),
                  _: User = Depends(deps.get_current_user)):
    return (db.query(RubroNomina)
            .order_by(RubroNomina.orden_ejecucion)
            .all())


@router.post("/rubros", response_model=RubroNominaResponse, status_code=201)
def crear_rubro(req: RubroNominaCreate, db: Session = Depends(deps.get_db),
                _: User = Depends(deps.require_role(_ROLES_RRHH))):
    if db.query(RubroNomina).filter(RubroNomina.codigo_rubro == req.codigo_rubro).first():
        raise HTTPException(400, f"Rubro con código {req.codigo_rubro} ya existe")
    obj = RubroNomina(**req.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj


@router.put("/rubros/{rubro_id}", response_model=RubroNominaResponse)
def actualizar_rubro(rubro_id: int, req: RubroNominaCreate,
                     db: Session = Depends(deps.get_db),
                     _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = db.query(RubroNomina).filter(RubroNomina.id_rubro == rubro_id).first()
    if not obj:
        raise HTTPException(404, "Rubro no encontrado")
    for k, v in req.model_dump().items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj


# =========================================================================
# ROL DE PAGOS — CRUD + FLUJO DE ESTADOS
# =========================================================================
@router.post("/roles", response_model=RolPagoResponse, status_code=201)
def crear_rol(req: RolPagoCreate, db: Session = Depends(deps.get_db),
              current_user: User = Depends(deps.require_role(_ROLES_RRHH))):
    """Crea cabecera del rol de pagos en estado BORRADOR."""
    existente = db.query(RolPago).filter(
        RolPago.periodo_anio == req.periodo_anio,
        RolPago.periodo_mes == req.periodo_mes,
        RolPago.tipo_rol == req.tipo_rol,
    ).first()
    if existente:
        raise HTTPException(400,
            f"Ya existe un rol {req.tipo_rol} para {req.periodo_anio}/{req.periodo_mes:02d}")
    obj = RolPago(
        **req.model_dump(),
        fecha_generacion=date.today(),
        creado_por_id=current_user.id,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return obj


@router.get("/roles", response_model=List[RolPagoResponse])
def listar_roles(anio: Optional[int] = None,
                 db: Session = Depends(deps.get_db),
                 _: User = Depends(deps.require_role(_ROLES_RRHH))):
    q = db.query(RolPago)
    if anio:
        q = q.filter(RolPago.periodo_anio == anio)
    return q.order_by(RolPago.periodo_anio.desc(), RolPago.periodo_mes.desc()).all()


@router.get("/roles/{id_rol}", response_model=RolPagoDetalleResponse)
def detalle_rol(id_rol: int, db: Session = Depends(deps.get_db),
                _: User = Depends(deps.require_role(_ROLES_RRHH))):
    obj = (
        db.query(RolPago)
        .options(
            joinedload(RolPago.lineas)
            .joinedload(LineaRolPago.detalles),
            joinedload(RolPago.lineas)
            .joinedload(LineaRolPago.empleado),
        )
        .filter(RolPago.id_rol_pago == id_rol)
        .first()
    )
    if not obj:
        raise HTTPException(404, "Rol de pago no encontrado")
    return obj


@router.post("/roles/{id_rol}/calcular", response_model=RolPagoResponse)
def calcular_rol(id_rol: int, db: Session = Depends(deps.get_db),
                 _: User = Depends(deps.require_role(_ROLES_RRHH))):
    """Ejecuta el motor de cálculo. Transiciona BORRADOR/CALCULADO → CALCULADO."""
    try:
        rol = generar_rol(db, id_rol)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return rol


@router.post("/roles/{id_rol}/aprobar", response_model=RolPagoResponse)
def aprobar_rol(id_rol: int, db: Session = Depends(deps.get_db),
                current_user: User = Depends(deps.require_role(_ROLES_RRHH))):
    """Aprueba el rol. CALCULADO → APROBADO."""
    obj = db.query(RolPago).filter(RolPago.id_rol_pago == id_rol).first()
    if not obj:
        raise HTTPException(404, "Rol de pago no encontrado")
    if obj.estado != "CALCULADO":
        raise HTTPException(400, f"Solo se pueden aprobar roles en estado CALCULADO (actual: {obj.estado})")
    obj.estado = "APROBADO"
    obj.fecha_aprobacion = date.today()
    obj.aprobado_por_id = current_user.id
    db.commit(); db.refresh(obj)
    return obj


@router.post("/roles/{id_rol}/cerrar", response_model=RolPagoResponse)
def cerrar_rol(id_rol: int, db: Session = Depends(deps.get_db),
               _: User = Depends(deps.require_role(_ROLES_RRHH))):
    """Cierra el rol. APROBADO → CERRADO."""
    obj = db.query(RolPago).filter(RolPago.id_rol_pago == id_rol).first()
    if not obj:
        raise HTTPException(404, "Rol de pago no encontrado")
    if obj.estado != "APROBADO":
        raise HTTPException(400, f"Solo se pueden cerrar roles en estado APROBADO (actual: {obj.estado})")
    obj.estado = "CERRADO"
    db.flush()
    generar_asiento_nomina(db, obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.post("/roles/{id_rol}/anular", response_model=RolPagoResponse)
def anular_rol(id_rol: int, db: Session = Depends(deps.get_db),
               _: User = Depends(deps.require_role(["SuperAdmin"]))):
    """Anula el rol. Solo SuperAdmin. No se puede anular CERRADO."""
    obj = db.query(RolPago).filter(RolPago.id_rol_pago == id_rol).first()
    if not obj:
        raise HTTPException(404, "Rol de pago no encontrado")
    if obj.estado == "CERRADO":
        raise HTTPException(400, "No se puede anular un rol CERRADO")
    obj.estado = "ANULADO"
    db.commit(); db.refresh(obj)
    return obj


# =========================================================================
# LÍNEAS — actualizar datos bancarios
# =========================================================================
@router.patch("/roles/{id_rol}/lineas/{id_linea}", response_model=LineaRolPagoResponse)
def actualizar_linea(id_rol: int, id_linea: int,
                     req: LineaRolPagoUpdate,
                     db: Session = Depends(deps.get_db),
                     _: User = Depends(deps.require_role(_ROLES_RRHH))):
    """Actualiza datos bancarios de una línea (para SPI)."""
    linea = db.query(LineaRolPago).filter(
        LineaRolPago.id_linea == id_linea,
        LineaRolPago.id_rol_pago == id_rol,
    ).first()
    if not linea:
        raise HTTPException(404, "Línea no encontrada")
    for k, v in req.model_dump(exclude_unset=True).items():
        setattr(linea, k, v)
    db.commit(); db.refresh(linea)
    return linea


# =========================================================================
# EXPORTACIONES
# =========================================================================
@router.get("/roles/{id_rol}/spi")
def exportar_spi(id_rol: int,
                 ruc_empresa: str = "1760001340001",
                 cuenta_empresa: str = "0",
                 db: Session = Depends(deps.get_db),
                 _: User = Depends(deps.require_role(_ROLES_RRHH))):
    """Genera archivo SPI para pagos masivos al BCE."""
    rol = (
        db.query(RolPago)
        .options(joinedload(RolPago.lineas).joinedload(LineaRolPago.empleado))
        .filter(RolPago.id_rol_pago == id_rol)
        .first()
    )
    if not rol:
        raise HTTPException(404, "Rol de pago no encontrado")
    try:
        contenido = generar_archivo_spi(db, rol, ruc_empresa, cuenta_empresa)
    except ValueError as e:
        raise HTTPException(400, str(e))

    nombre_archivo = f"SPI_{rol.tipo_rol}_{rol.periodo_anio}{rol.periodo_mes:02d}.txt"
    return StreamingResponse(
        iter([contenido]),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={nombre_archivo}"},
    )
