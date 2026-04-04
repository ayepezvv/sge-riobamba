"""
Router FastAPI — Módulo Tesorería
Rutas en español, esquema PostgreSQL: tesoreria
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_role

_ROLES_TESORERIA = ["SuperAdmin", "Tesoreria"]
from app.models.tesoreria import (
    EntidadBancaria, CuentaBancaria, ExtractoBancario, LineaExtracto,
    ConciliacionBancaria, MarcaConciliacion, CajaChica, MovimientoCaja,
    EstadoExtracto, EstadoConciliacion, EstadoCaja,
)
from app.models.user import User
from app.schemas.tesoreria import (
    EntidadBancariaCrear, EntidadBancariaActualizar, EntidadBancariaRespuesta,
    CuentaBancariaCrear, CuentaBancariaActualizar, CuentaBancariaRespuesta,
    ExtractoBancarioCrear, ExtractoBancarioActualizar, ExtractoBancarioRespuesta,
    LineaExtractoCrear, LineaExtractoRespuesta,
    ConciliacionBancariaCrear, ConciliacionBancariaActualizar, ConciliacionBancariaRespuesta,
    CerrarConciliacion, MarcaConciliacionCrear, MarcaConciliacionRespuesta,
    CajaChicaCrear, CajaChicaActualizar, CajaChicaRespuesta,
    MovimientoCajaCrear, MovimientoCajaRespuesta,
)

router = APIRouter()


# ===========================================================================
# ENTIDADES BANCARIAS
# ===========================================================================

@router.get("/entidades-bancarias", response_model=List[EntidadBancariaRespuesta],
             tags=["Tesorería - Entidades Bancarias"])
def listar_entidades_bancarias(
    solo_activas: bool = True,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(EntidadBancaria)
    if solo_activas:
        q = q.filter(EntidadBancaria.es_activa == True)
    return q.order_by(EntidadBancaria.nombre).all()


@router.post("/entidades-bancarias", response_model=EntidadBancariaRespuesta,
              status_code=status.HTTP_201_CREATED, tags=["Tesorería - Entidades Bancarias"])
def crear_entidad_bancaria(
    datos: EntidadBancariaCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    existente = db.query(EntidadBancaria).filter(EntidadBancaria.codigo == datos.codigo).first()
    if existente:
        raise HTTPException(400, f"Ya existe entidad bancaria con código '{datos.codigo}'")
    entidad = EntidadBancaria(**datos.model_dump(),
                               creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(entidad)
    db.commit()
    db.refresh(entidad)
    return entidad


@router.put("/entidades-bancarias/{entidad_id}", response_model=EntidadBancariaRespuesta,
             tags=["Tesorería - Entidades Bancarias"])
def actualizar_entidad_bancaria(
    entidad_id: int,
    datos: EntidadBancariaActualizar,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    entidad = db.query(EntidadBancaria).filter(EntidadBancaria.id == entidad_id).first()
    if not entidad:
        raise HTTPException(404, "Entidad bancaria no encontrada")
    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(entidad, campo, valor)
    entidad.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(entidad)
    return entidad


# ===========================================================================
# CUENTAS BANCARIAS
# ===========================================================================

@router.get("/cuentas-bancarias", response_model=List[CuentaBancariaRespuesta],
             tags=["Tesorería - Cuentas Bancarias"])
def listar_cuentas_bancarias(
    entidad_bancaria_id: Optional[int] = None,
    solo_activas: bool = True,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(CuentaBancaria)
    if entidad_bancaria_id:
        q = q.filter(CuentaBancaria.entidad_bancaria_id == entidad_bancaria_id)
    if solo_activas:
        q = q.filter(CuentaBancaria.es_activa == True)
    return q.order_by(CuentaBancaria.nombre).all()


@router.post("/cuentas-bancarias", response_model=CuentaBancariaRespuesta,
              status_code=status.HTTP_201_CREATED, tags=["Tesorería - Cuentas Bancarias"])
def crear_cuenta_bancaria(
    datos: CuentaBancariaCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    existente = db.query(CuentaBancaria).filter(
        CuentaBancaria.numero_cuenta == datos.numero_cuenta).first()
    if existente:
        raise HTTPException(400, f"Ya existe una cuenta con número '{datos.numero_cuenta}'")
    cuenta = CuentaBancaria(**datos.model_dump(),
                             creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(cuenta)
    db.commit()
    db.refresh(cuenta)
    return cuenta


@router.get("/cuentas-bancarias/{cuenta_id}", response_model=CuentaBancariaRespuesta,
             tags=["Tesorería - Cuentas Bancarias"])
def obtener_cuenta_bancaria(cuenta_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    cuenta = db.query(CuentaBancaria).filter(CuentaBancaria.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(404, "Cuenta bancaria no encontrada")
    return cuenta


@router.put("/cuentas-bancarias/{cuenta_id}", response_model=CuentaBancariaRespuesta,
             tags=["Tesorería - Cuentas Bancarias"])
def actualizar_cuenta_bancaria(
    cuenta_id: int,
    datos: CuentaBancariaActualizar,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    cuenta = db.query(CuentaBancaria).filter(CuentaBancaria.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(404, "Cuenta bancaria no encontrada")
    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(cuenta, campo, valor)
    cuenta.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(cuenta)
    return cuenta


# ===========================================================================
# EXTRACTOS BANCARIOS
# ===========================================================================

@router.get("/extractos", response_model=List[ExtractoBancarioRespuesta],
             tags=["Tesorería - Extractos"])
def listar_extractos(
    cuenta_bancaria_id: Optional[int] = None,
    estado: Optional[str] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(ExtractoBancario)
    if cuenta_bancaria_id:
        q = q.filter(ExtractoBancario.cuenta_bancaria_id == cuenta_bancaria_id)
    if estado:
        q = q.filter(ExtractoBancario.estado == estado)
    if fecha_desde:
        q = q.filter(ExtractoBancario.fecha_inicio >= fecha_desde)
    if fecha_hasta:
        q = q.filter(ExtractoBancario.fecha_fin <= fecha_hasta)
    return q.order_by(ExtractoBancario.fecha_inicio.desc()).all()


@router.post("/extractos", response_model=ExtractoBancarioRespuesta,
              status_code=status.HTTP_201_CREATED, tags=["Tesorería - Extractos"])
def crear_extracto(
    datos: ExtractoBancarioCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    # Verificar que no haya solapamiento de periodos para la misma cuenta
    solapado = db.query(ExtractoBancario).filter(
        ExtractoBancario.cuenta_bancaria_id == datos.cuenta_bancaria_id,
        ExtractoBancario.fecha_inicio <= datos.fecha_fin,
        ExtractoBancario.fecha_fin >= datos.fecha_inicio,
    ).first()
    if solapado:
        raise HTTPException(400, "Ya existe un extracto que solapa el período indicado")

    lineas_data = datos.lineas
    extracto_data = datos.model_dump(exclude={"lineas"})
    extracto = ExtractoBancario(**extracto_data,
                                 creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(extracto)
    db.flush()

    for linea_datos in lineas_data:
        linea = LineaExtracto(**linea_datos.model_dump(), extracto_id=extracto.id,
                               creado_por_id=usuario.id, actualizado_por_id=usuario.id)
        db.add(linea)

    db.commit()
    db.refresh(extracto)
    return extracto


@router.get("/extractos/{extracto_id}", response_model=ExtractoBancarioRespuesta,
             tags=["Tesorería - Extractos"])
def obtener_extracto(extracto_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    extracto = db.query(ExtractoBancario).filter(ExtractoBancario.id == extracto_id).first()
    if not extracto:
        raise HTTPException(404, "Extracto no encontrado")
    return extracto


@router.post("/extractos/{extracto_id}/confirmar", response_model=ExtractoBancarioRespuesta,
              tags=["Tesorería - Extractos"])
def confirmar_extracto(
    extracto_id: int,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    extracto = db.query(ExtractoBancario).filter(ExtractoBancario.id == extracto_id).first()
    if not extracto:
        raise HTTPException(404, "Extracto no encontrado")
    if extracto.estado != EstadoExtracto.BORRADOR:
        raise HTTPException(400, "Solo se pueden confirmar extractos en estado BORRADOR")
    extracto.estado = EstadoExtracto.CONFIRMADO
    extracto.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(extracto)
    return extracto


# ===========================================================================
# CONCILIACIONES BANCARIAS
# ===========================================================================

@router.get("/conciliaciones", response_model=List[ConciliacionBancariaRespuesta],
             tags=["Tesorería - Conciliaciones"])
def listar_conciliaciones(
    cuenta_bancaria_id: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(ConciliacionBancaria)
    if cuenta_bancaria_id:
        q = q.filter(ConciliacionBancaria.cuenta_bancaria_id == cuenta_bancaria_id)
    if estado:
        q = q.filter(ConciliacionBancaria.estado == estado)
    return q.order_by(ConciliacionBancaria.fecha_fin.desc()).all()


@router.post("/conciliaciones", response_model=ConciliacionBancariaRespuesta,
              status_code=status.HTTP_201_CREATED, tags=["Tesorería - Conciliaciones"])
def crear_conciliacion(
    datos: ConciliacionBancariaCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    diferencia = datos.saldo_banco - datos.saldo_libro
    conciliacion = ConciliacionBancaria(
        **datos.model_dump(),
        diferencia=diferencia,
        creado_por_id=usuario.id,
        actualizado_por_id=usuario.id,
    )
    db.add(conciliacion)
    db.commit()
    db.refresh(conciliacion)
    return conciliacion


@router.get("/conciliaciones/{conciliacion_id}", response_model=ConciliacionBancariaRespuesta,
             tags=["Tesorería - Conciliaciones"])
def obtener_conciliacion(conciliacion_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    conc = db.query(ConciliacionBancaria).filter(
        ConciliacionBancaria.id == conciliacion_id).first()
    if not conc:
        raise HTTPException(404, "Conciliación no encontrada")
    return conc


@router.post("/conciliaciones/{conciliacion_id}/cerrar",
              response_model=ConciliacionBancariaRespuesta,
              tags=["Tesorería - Conciliaciones"])
def cerrar_conciliacion(
    conciliacion_id: int,
    datos: CerrarConciliacion,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    """RN-T04: CERRADO es definitivo — no se puede reabrir."""
    conc = db.query(ConciliacionBancaria).filter(
        ConciliacionBancaria.id == conciliacion_id).first()
    if not conc:
        raise HTTPException(404, "Conciliación no encontrada")
    if conc.estado == EstadoConciliacion.CERRADO:
        raise HTTPException(400, "La conciliación ya está cerrada (RN-T04: estado definitivo)")
    if datos.observaciones:
        conc.observaciones = datos.observaciones
    conc.estado = EstadoConciliacion.CERRADO
    conc.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(conc)
    return conc


@router.post("/conciliaciones/{conciliacion_id}/marcas",
              response_model=MarcaConciliacionRespuesta,
              status_code=status.HTTP_201_CREATED,
              tags=["Tesorería - Conciliaciones"])
def agregar_marca(
    conciliacion_id: int,
    datos: MarcaConciliacionCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    """RN-T01: Marcado de líneas de extracto como conciliadas."""
    conc = db.query(ConciliacionBancaria).filter(
        ConciliacionBancaria.id == conciliacion_id).first()
    if not conc:
        raise HTTPException(404, "Conciliación no encontrada")
    if conc.estado == EstadoConciliacion.CERRADO:
        raise HTTPException(400, "No se puede modificar una conciliación cerrada")

    # Verificar línea no esté ya conciliada
    linea = db.query(LineaExtracto).filter(
        LineaExtracto.id == datos.linea_extracto_id).first()
    if not linea:
        raise HTTPException(404, "Línea de extracto no encontrada")
    if linea.esta_conciliada:
        raise HTTPException(400, "La línea ya está conciliada")

    marca = MarcaConciliacion(**datos.model_dump(), conciliacion_id=conciliacion_id,
                               creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(marca)

    # Marcar la línea como conciliada
    linea.esta_conciliada = True
    linea.actualizado_por_id = usuario.id

    # Recalcular diferencia
    total_conciliado = sum(m.valor_conciliado for m in conc.marcas) + datos.valor_conciliado
    conc.diferencia = conc.saldo_banco - conc.saldo_libro

    db.commit()
    db.refresh(marca)
    return marca


# ===========================================================================
# CAJAS CHICAS
# ===========================================================================

@router.get("/cajas", response_model=List[CajaChicaRespuesta], tags=["Tesorería - Caja Chica"])
def listar_cajas(
    solo_activas: bool = False,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(CajaChica)
    if solo_activas:
        q = q.filter(CajaChica.estado == EstadoCaja.ABIERTA)
    return q.order_by(CajaChica.codigo).all()


@router.post("/cajas", response_model=CajaChicaRespuesta,
              status_code=status.HTTP_201_CREATED, tags=["Tesorería - Caja Chica"])
def crear_caja(
    datos: CajaChicaCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    existente = db.query(CajaChica).filter(CajaChica.codigo == datos.codigo).first()
    if existente:
        raise HTTPException(400, f"Ya existe una caja con código '{datos.codigo}'")
    caja = CajaChica(**datos.model_dump(), monto_disponible=datos.monto_fijo,
                      creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(caja)
    db.commit()
    db.refresh(caja)
    return caja


@router.post("/cajas/{caja_id}/movimientos", response_model=MovimientoCajaRespuesta,
              status_code=status.HTTP_201_CREATED, tags=["Tesorería - Caja Chica"])
def registrar_movimiento_caja(
    caja_id: int,
    datos: MovimientoCajaCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    caja = db.query(CajaChica).filter(CajaChica.id == caja_id).first()
    if not caja:
        raise HTTPException(404, "Caja no encontrada")

    # Actualizar saldo disponible según tipo
    if datos.tipo in ("INGRESO", "APERTURA"):
        caja.monto_disponible += datos.monto
    elif datos.tipo in ("EGRESO", "CIERRE"):
        if caja.monto_disponible < datos.monto:
            raise HTTPException(400, "Saldo insuficiente en caja")
        caja.monto_disponible -= datos.monto

    movimiento = MovimientoCaja(**datos.model_dump(),
                                 creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(movimiento)
    caja.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(movimiento)
    return movimiento


@router.get("/cajas/{caja_id}/movimientos", response_model=List[MovimientoCajaRespuesta],
             tags=["Tesorería - Caja Chica"])
def listar_movimientos_caja(
    caja_id: int,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(MovimientoCaja).filter(MovimientoCaja.caja_id == caja_id)
    if fecha_desde:
        q = q.filter(MovimientoCaja.fecha >= fecha_desde)
    if fecha_hasta:
        q = q.filter(MovimientoCaja.fecha <= fecha_hasta)
    return q.order_by(MovimientoCaja.fecha.desc()).all()
