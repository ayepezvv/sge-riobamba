"""
Router FastAPI — Módulo Contabilidad
Rutas en español, esquema PostgreSQL: contabilidad
"""
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_db, get_current_user, require_role
from app.models.contabilidad import (
    TipoCuenta, CuentaContable, Diario, PeriodoContable,
    AsientoContable, LineaAsiento,
    EstadoCuenta, EstadoPeriodo, EstadoAsiento,
)
from app.models.user import User
from app.schemas.contabilidad import (
    TipoCuentaCrear, TipoCuentaActualizar, TipoCuentaRespuesta,
    CuentaContableCrear, CuentaContableActualizar, CuentaContableRespuesta, CuentaContableArbol, SaldoCuenta,
    DiarioCrear, DiarioActualizar, DiarioRespuesta,
    PeriodoContableCrear, PeriodoContableRespuesta, CambioEstadoPeriodo,
    AsientoContableCrear, AsientoContableRespuesta, AnularAsiento,
)

router = APIRouter()

# Solo SuperAdmin o Contabilidad pueden registrar/modificar movimientos contables
_require_contabilidad = require_role(["SuperAdmin", "Contabilidad"])


# ===========================================================================
# TIPOS DE CUENTA
# ===========================================================================

@router.get("/tipos-cuenta", response_model=List[TipoCuentaRespuesta], tags=["Contabilidad - Tipos Cuenta"])
def listar_tipos_cuenta(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(TipoCuenta).order_by(TipoCuenta.codigo).all()


@router.post("/tipos-cuenta", response_model=TipoCuentaRespuesta, status_code=status.HTTP_201_CREATED,
             tags=["Contabilidad - Tipos Cuenta"])
def crear_tipo_cuenta(
    datos: TipoCuentaCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    existente = db.query(TipoCuenta).filter(TipoCuenta.codigo == datos.codigo).first()
    if existente:
        raise HTTPException(status_code=400, detail=f"Ya existe un tipo de cuenta con código '{datos.codigo}'")
    tipo = TipoCuenta(**datos.model_dump(), creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    return tipo


@router.put("/tipos-cuenta/{tipo_id}", response_model=TipoCuentaRespuesta, tags=["Contabilidad - Tipos Cuenta"])
def actualizar_tipo_cuenta(
    tipo_id: int,
    datos: TipoCuentaActualizar,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    tipo = db.query(TipoCuenta).filter(TipoCuenta.id == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(tipo, campo, valor)
    tipo.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(tipo)
    return tipo


# ===========================================================================
# CUENTAS CONTABLES
# ===========================================================================

@router.get("/cuentas", response_model=List[CuentaContableRespuesta], tags=["Contabilidad - Cuentas"])
def listar_cuentas(
    tipo_cuenta_id: Optional[int] = None,
    nivel: Optional[int] = Query(None, ge=1, le=10),
    es_hoja: Optional[bool] = None,
    estado: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(CuentaContable)
    if tipo_cuenta_id:
        query = query.filter(CuentaContable.tipo_cuenta_id == tipo_cuenta_id)
    if nivel is not None:
        query = query.filter(CuentaContable.nivel == nivel)
    if es_hoja is not None:
        query = query.filter(CuentaContable.es_hoja == es_hoja)
    if estado:
        query = query.filter(CuentaContable.estado == estado)
    if q:
        query = query.filter(
            CuentaContable.nombre.ilike(f"%{q}%") | CuentaContable.codigo.ilike(f"%{q}%")
        )
    return query.order_by(CuentaContable.codigo).all()


@router.get("/cuentas/arbol", response_model=List[CuentaContableArbol], tags=["Contabilidad - Cuentas"])
def arbol_cuentas(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Retorna el árbol de cuentas raíz (nivel 1) con sus subcuentas anidadas."""
    raices = (
        db.query(CuentaContable)
        .options(selectinload(CuentaContable.subcuentas))
        .filter(CuentaContable.cuenta_padre_id.is_(None))
        .order_by(CuentaContable.codigo)
        .all()
    )
    return raices


@router.get("/cuentas/{cuenta_id}", response_model=CuentaContableRespuesta, tags=["Contabilidad - Cuentas"])
def obtener_cuenta(cuenta_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    cuenta = db.query(CuentaContable).filter(CuentaContable.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta contable no encontrada")
    return cuenta


@router.get("/cuentas/{cuenta_id}/saldo", response_model=SaldoCuenta, tags=["Contabilidad - Cuentas"])
def saldo_cuenta(
    cuenta_id: int,
    periodo_id: Optional[int] = None,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Calcula el saldo de una cuenta a partir de sus líneas de asiento PUBLICADAS."""
    cuenta = db.query(CuentaContable).filter(CuentaContable.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta contable no encontrada")

    q = (
        db.query(
            func.coalesce(func.sum(LineaAsiento.debe), 0).label("total_debe"),
            func.coalesce(func.sum(LineaAsiento.haber), 0).label("total_haber"),
        )
        .join(AsientoContable, LineaAsiento.asiento_id == AsientoContable.id)
        .filter(
            LineaAsiento.cuenta_id == cuenta_id,
            AsientoContable.estado == EstadoAsiento.PUBLICADO,
        )
    )
    if periodo_id:
        q = q.filter(AsientoContable.periodo_id == periodo_id)
    if fecha_desde:
        q = q.filter(AsientoContable.fecha >= fecha_desde)
    if fecha_hasta:
        q = q.filter(AsientoContable.fecha <= fecha_hasta)

    resultado = q.one()
    total_debe = Decimal(str(resultado.total_debe))
    total_haber = Decimal(str(resultado.total_haber))
    return SaldoCuenta(
        cuenta_id=cuenta_id,
        codigo=cuenta.codigo,
        nombre=cuenta.nombre,
        total_debe=total_debe,
        total_haber=total_haber,
        saldo=total_debe - total_haber,
    )


@router.post("/cuentas", response_model=CuentaContableRespuesta, status_code=status.HTTP_201_CREATED,
             tags=["Contabilidad - Cuentas"])
def crear_cuenta(
    datos: CuentaContableCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    existente = db.query(CuentaContable).filter(CuentaContable.codigo == datos.codigo).first()
    if existente:
        raise HTTPException(status_code=400, detail=f"Ya existe una cuenta con código '{datos.codigo}'")
    if datos.cuenta_padre_id:
        padre = db.query(CuentaContable).filter(CuentaContable.id == datos.cuenta_padre_id).first()
        if not padre:
            raise HTTPException(status_code=404, detail="Cuenta padre no encontrada")
        # Al agregar subcuenta, el padre deja de ser hoja
        if padre.es_hoja:
            padre.es_hoja = False
            padre.permite_movimientos = False
    cuenta = CuentaContable(**datos.model_dump(), creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(cuenta)
    db.commit()
    db.refresh(cuenta)
    return cuenta


@router.put("/cuentas/{cuenta_id}", response_model=CuentaContableRespuesta, tags=["Contabilidad - Cuentas"])
def actualizar_cuenta(
    cuenta_id: int,
    datos: CuentaContableActualizar,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    cuenta = db.query(CuentaContable).filter(CuentaContable.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta contable no encontrada")
    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(cuenta, campo, valor)
    cuenta.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(cuenta)
    return cuenta


# ===========================================================================
# DIARIOS
# ===========================================================================

@router.get("/diarios", response_model=List[DiarioRespuesta], tags=["Contabilidad - Diarios"])
def listar_diarios(
    solo_activos: bool = True,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(Diario)
    if solo_activos:
        q = q.filter(Diario.es_activo == True)
    return q.order_by(Diario.codigo).all()


@router.get("/diarios/{diario_id}", response_model=DiarioRespuesta, tags=["Contabilidad - Diarios"])
def obtener_diario(diario_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    diario = db.query(Diario).filter(Diario.id == diario_id).first()
    if not diario:
        raise HTTPException(status_code=404, detail="Diario no encontrado")
    return diario


@router.post("/diarios", response_model=DiarioRespuesta, status_code=status.HTTP_201_CREATED,
             tags=["Contabilidad - Diarios"])
def crear_diario(
    datos: DiarioCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    existente = db.query(Diario).filter(Diario.codigo == datos.codigo).first()
    if existente:
        raise HTTPException(status_code=400, detail=f"Ya existe un diario con código '{datos.codigo}'")
    diario = Diario(**datos.model_dump(), creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(diario)
    db.commit()
    db.refresh(diario)
    return diario


@router.put("/diarios/{diario_id}", response_model=DiarioRespuesta, tags=["Contabilidad - Diarios"])
def actualizar_diario(
    diario_id: int,
    datos: DiarioActualizar,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    diario = db.query(Diario).filter(Diario.id == diario_id).first()
    if not diario:
        raise HTTPException(status_code=404, detail="Diario no encontrado")
    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(diario, campo, valor)
    diario.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(diario)
    return diario


# ===========================================================================
# PERIODOS CONTABLES
# ===========================================================================

@router.get("/periodos", response_model=List[PeriodoContableRespuesta], tags=["Contabilidad - Periodos"])
def listar_periodos(
    anio: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(PeriodoContable)
    if anio:
        q = q.filter(PeriodoContable.anio == anio)
    if estado:
        q = q.filter(PeriodoContable.estado == estado)
    return q.order_by(PeriodoContable.anio, PeriodoContable.mes).all()


@router.post("/periodos", response_model=PeriodoContableRespuesta, status_code=status.HTTP_201_CREATED,
             tags=["Contabilidad - Periodos"])
def crear_periodo(
    datos: PeriodoContableCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    existente = db.query(PeriodoContable).filter(
        PeriodoContable.anio == datos.anio, PeriodoContable.mes == datos.mes
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail=f"Ya existe el período {datos.nombre}")
    periodo = PeriodoContable(**datos.model_dump(), creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(periodo)
    db.commit()
    db.refresh(periodo)
    return periodo


@router.patch("/periodos/{periodo_id}/estado", response_model=PeriodoContableRespuesta,
              tags=["Contabilidad - Periodos"])
def cambiar_estado_periodo(
    periodo_id: int,
    datos: CambioEstadoPeriodo,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    periodo = db.query(PeriodoContable).filter(PeriodoContable.id == periodo_id).first()
    if not periodo:
        raise HTTPException(status_code=404, detail="Período contable no encontrado")
    estados_validos = {e.value for e in EstadoPeriodo}
    if datos.estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Válidos: {estados_validos}")
    # RN-10: Máquina de estados estricta — transiciones unidireccionales
    TRANSICIONES_VALIDAS = {
        EstadoPeriodo.ABIERTO: {EstadoPeriodo.CERRADO},
        EstadoPeriodo.CERRADO: {EstadoPeriodo.BLOQUEADO},
        EstadoPeriodo.BLOQUEADO: set(),
    }
    destino = datos.estado if isinstance(datos.estado, EstadoPeriodo) else EstadoPeriodo(datos.estado)
    if destino not in TRANSICIONES_VALIDAS.get(periodo.estado, set()):
        raise HTTPException(
            status_code=400,
            detail=(
                f"Transición no permitida: {periodo.estado} → {destino} (RN-10). "
                "El flujo válido es ABIERTO → CERRADO → BLOQUEADO (unidireccional)."
            ),
        )
    periodo.estado = destino
    periodo.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(periodo)
    return periodo


# ===========================================================================
# ASIENTOS CONTABLES
# ===========================================================================

@router.get("/asientos", response_model=List[AsientoContableRespuesta], tags=["Contabilidad - Asientos"])
def listar_asientos(
    periodo_id: Optional[int] = None,
    diario_id: Optional[int] = None,
    estado: Optional[str] = None,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(AsientoContable).options(selectinload(AsientoContable.lineas))
    if periodo_id:
        q = q.filter(AsientoContable.periodo_id == periodo_id)
    if diario_id:
        q = q.filter(AsientoContable.diario_id == diario_id)
    if estado:
        q = q.filter(AsientoContable.estado == estado)
    if fecha_desde:
        q = q.filter(AsientoContable.fecha >= fecha_desde)
    if fecha_hasta:
        q = q.filter(AsientoContable.fecha <= fecha_hasta)
    return q.order_by(AsientoContable.fecha.desc(), AsientoContable.id.desc()).offset(skip).limit(limit).all()


@router.get("/asientos/{asiento_id}", response_model=AsientoContableRespuesta, tags=["Contabilidad - Asientos"])
def obtener_asiento(asiento_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    asiento = (
        db.query(AsientoContable)
        .options(selectinload(AsientoContable.lineas))
        .filter(AsientoContable.id == asiento_id)
        .first()
    )
    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento contable no encontrado")
    return asiento


@router.post("/asientos", response_model=AsientoContableRespuesta, status_code=status.HTTP_201_CREATED,
             tags=["Contabilidad - Asientos"])
def crear_asiento(
    datos: AsientoContableCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    # Validar período abierto
    periodo = db.query(PeriodoContable).filter(PeriodoContable.id == datos.periodo_id).first()
    if not periodo:
        raise HTTPException(status_code=404, detail="Período contable no encontrado")
    if periodo.estado != EstadoPeriodo.ABIERTO:
        raise HTTPException(status_code=400, detail=f"El período '{periodo.nombre}' está {periodo.estado} y no acepta asientos")

    # Validar diario activo
    diario = db.query(Diario).filter(Diario.id == datos.diario_id).first()
    if not diario or not diario.es_activo:
        raise HTTPException(status_code=400, detail="Diario no encontrado o inactivo")

    # Validar cuentas activas y que permitan movimientos
    for linea_datos in datos.lineas:
        cuenta = db.query(CuentaContable).filter(CuentaContable.id == linea_datos.cuenta_id).first()
        if not cuenta:
            raise HTTPException(status_code=404, detail=f"Cuenta {linea_datos.cuenta_id} no encontrada")
        if cuenta.estado != EstadoCuenta.ACTIVA:
            raise HTTPException(status_code=400, detail=f"La cuenta '{cuenta.codigo} - {cuenta.nombre}' está inactiva")
        if not cuenta.permite_movimientos:
            raise HTTPException(status_code=400, detail=f"La cuenta '{cuenta.codigo}' es de agrupación y no permite movimientos directos")

    total_debe = sum(l.debe for l in datos.lineas)
    total_haber = sum(l.haber for l in datos.lineas)

    # Número provisional (se actualiza al publicar)
    numero_borrador = f"BORRA/{datos.diario_id}/{datos.periodo_id}/{datos.fecha}"

    asiento = AsientoContable(
        numero=numero_borrador,
        diario_id=datos.diario_id,
        periodo_id=datos.periodo_id,
        fecha=datos.fecha,
        referencia=datos.referencia,
        concepto=datos.concepto,
        estado=EstadoAsiento.BORRADOR,
        total_debe=total_debe,
        total_haber=total_haber,
        usuario_id=usuario.id,
        creado_por_id=usuario.id,
        actualizado_por_id=usuario.id,
    )
    db.add(asiento)
    db.flush()  # Obtener ID sin commit

    for idx, linea_datos in enumerate(datos.lineas, start=1):
        linea = LineaAsiento(
            asiento_id=asiento.id,
            cuenta_id=linea_datos.cuenta_id,
            descripcion=linea_datos.descripcion,
            debe=linea_datos.debe,
            haber=linea_datos.haber,
            orden=linea_datos.orden if linea_datos.orden > 1 else idx,
            creado_por_id=usuario.id,
            actualizado_por_id=usuario.id,
        )
        db.add(linea)

    db.commit()
    db.refresh(asiento)
    return asiento


@router.patch("/asientos/{asiento_id}/publicar", response_model=AsientoContableRespuesta,
              tags=["Contabilidad - Asientos"])
def publicar_asiento(
    asiento_id: int,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    """Valida y publica el asiento. Genera número definitivo y verifica cuadre."""
    asiento = (
        db.query(AsientoContable)
        .options(selectinload(AsientoContable.lineas))
        .filter(AsientoContable.id == asiento_id)
        .first()
    )
    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")
    if asiento.estado != EstadoAsiento.BORRADOR:
        raise HTTPException(status_code=400, detail=f"Solo se pueden publicar asientos en BORRADOR (estado actual: {asiento.estado})")

    # Revalidar período
    periodo = db.query(PeriodoContable).filter(PeriodoContable.id == asiento.periodo_id).first()
    if periodo.estado != EstadoPeriodo.ABIERTO:
        raise HTTPException(status_code=400, detail=f"El período '{periodo.nombre}' ya no está ABIERTO")

    # Revalidar cuadre
    total_debe = sum(l.debe for l in asiento.lineas)
    total_haber = sum(l.haber for l in asiento.lineas)
    if total_debe != total_haber:
        raise HTTPException(status_code=400, detail=f"Asiento no cuadra: Debe={total_debe} ≠ Haber={total_haber}")

    # Generar número definitivo: DIARIO-ANIO-MES-SEQ
    # BL2: with_for_update() evita race condition en numeración concurrente
    seq = (
        db.query(func.count(AsientoContable.id))
        .with_for_update()
        .filter(
            AsientoContable.diario_id == asiento.diario_id,
            AsientoContable.periodo_id == asiento.periodo_id,
            AsientoContable.estado == EstadoAsiento.PUBLICADO,
        )
        .scalar()
    ) + 1
    diario = db.query(Diario).filter(Diario.id == asiento.diario_id).first()
    asiento.numero = f"{diario.codigo}/{periodo.anio}/{periodo.mes:02d}/{seq:05d}"
    asiento.estado = EstadoAsiento.PUBLICADO
    asiento.total_debe = total_debe
    asiento.total_haber = total_haber
    asiento.fecha_publicacion = datetime.now(timezone.utc)
    asiento.actualizado_por_id = usuario.id

    db.commit()
    db.refresh(asiento)
    return asiento


@router.patch("/asientos/{asiento_id}/anular", response_model=AsientoContableRespuesta,
              tags=["Contabilidad - Asientos"])
def anular_asiento(
    asiento_id: int,
    datos: AnularAsiento,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    """RN-11: Anulación de asiento — estado permanente, no se elimina físicamente.
    NIIF/NEC: Si el asiento está PUBLICADO, se crea asiento de reverso con debe/haber
    invertidos en el mismo período antes de marcar el original como ANULADO.
    """
    asiento = (
        db.query(AsientoContable)
        .options(selectinload(AsientoContable.lineas))
        .filter(AsientoContable.id == asiento_id)
        .first()
    )
    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")
    if asiento.estado == EstadoAsiento.ANULADO:
        raise HTTPException(status_code=400, detail="El asiento ya está ANULADO")

    # NIIF/NEC: asiento de reverso solo para asientos PUBLICADOS
    if asiento.estado == EstadoAsiento.PUBLICADO:
        periodo = db.query(PeriodoContable).filter(PeriodoContable.id == asiento.periodo_id).first()
        if not periodo or periodo.estado != EstadoPeriodo.ABIERTO:
            raise HTTPException(
                status_code=400,
                detail=f"No se puede anular: el período '{periodo.nombre if periodo else '?'}' no está ABIERTO. "
                       "Un período ABIERTO es requerido para registrar el asiento de reverso (NIIF/NEC).",
            )
        diario = db.query(Diario).filter(Diario.id == asiento.diario_id).first()
        # Número secuencial del reverso con for_update para evitar race condition
        seq_reverso = (
            db.query(func.count(AsientoContable.id))
            .with_for_update()
            .filter(
                AsientoContable.diario_id == asiento.diario_id,
                AsientoContable.periodo_id == asiento.periodo_id,
                AsientoContable.estado == EstadoAsiento.PUBLICADO,
            )
            .scalar()
        ) + 1
        numero_reverso = f"{diario.codigo}/{periodo.anio}/{periodo.mes:02d}/{seq_reverso:05d}-REV"

        reverso = AsientoContable(
            numero=numero_reverso,
            diario_id=asiento.diario_id,
            periodo_id=asiento.periodo_id,
            fecha=datetime.now(timezone.utc).date(),
            referencia=f"REVERSO-{asiento.numero}",
            concepto=f"Reverso por anulación de {asiento.numero}: {datos.motivo_anulacion}",
            estado=EstadoAsiento.PUBLICADO,
            total_debe=asiento.total_haber,
            total_haber=asiento.total_debe,
            fecha_publicacion=datetime.now(timezone.utc),
            usuario_id=usuario.id,
            creado_por_id=usuario.id,
            actualizado_por_id=usuario.id,
        )
        db.add(reverso)
        db.flush()

        for linea_orig in asiento.lineas:
            linea_rev = LineaAsiento(
                asiento_id=reverso.id,
                cuenta_id=linea_orig.cuenta_id,
                descripcion=f"Reverso: {linea_orig.descripcion or ''}",
                debe=linea_orig.haber,
                haber=linea_orig.debe,
                orden=linea_orig.orden,
                creado_por_id=usuario.id,
                actualizado_por_id=usuario.id,
            )
            db.add(linea_rev)

    asiento.estado = EstadoAsiento.ANULADO
    asiento.motivo_anulacion = datos.motivo_anulacion
    asiento.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(asiento)
    return asiento


# ===========================================================================
# PARÁMETROS CONTABLES (para auto-asientos, YXP-21)
# ===========================================================================

from app.models.contabilidad import ParametroContable
from app.schemas.contabilidad import (
    ParametroContableCrear, ParametroContableActualizar, ParametroContableRespuesta
)


@router.get("/parametros-contables", response_model=List[ParametroContableRespuesta],
            tags=["Contabilidad - Parámetros"])
def listar_parametros_contables(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Lista todos los parámetros configurados para generación automática de asientos."""
    return db.query(ParametroContable).order_by(ParametroContable.clave).all()


@router.get("/parametros-contables/{clave}", response_model=ParametroContableRespuesta,
            tags=["Contabilidad - Parámetros"])
def obtener_parametro_contable(clave: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    param = db.query(ParametroContable).filter(ParametroContable.clave == clave).first()
    if not param:
        raise HTTPException(status_code=404, detail=f"Parámetro '{clave}' no encontrado")
    return param


@router.post("/parametros-contables", response_model=ParametroContableRespuesta,
             status_code=status.HTTP_201_CREATED, tags=["Contabilidad - Parámetros"])
def crear_parametro_contable(
    datos: ParametroContableCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    existente = db.query(ParametroContable).filter(
        ParametroContable.clave == datos.clave).first()
    if existente:
        raise HTTPException(400, f"Ya existe el parámetro '{datos.clave}'")
    param = ParametroContable(
        **datos.model_dump(),
        creado_por_id=usuario.id,
        actualizado_por_id=usuario.id,
    )
    db.add(param)
    db.commit()
    db.refresh(param)
    return param


@router.put("/parametros-contables/{clave}", response_model=ParametroContableRespuesta,
            tags=["Contabilidad - Parámetros"])
def actualizar_parametro_contable(
    clave: str,
    datos: ParametroContableActualizar,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    param = db.query(ParametroContable).filter(ParametroContable.clave == clave).first()
    if not param:
        raise HTTPException(404, f"Parámetro '{clave}' no encontrado")
    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(param, campo, valor)
    param.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(param)
    return param


@router.delete("/parametros-contables/{clave}", status_code=status.HTTP_204_NO_CONTENT,
               tags=["Contabilidad - Parámetros"])
def eliminar_parametro_contable(
    clave: str,
    db: Session = Depends(get_db),
    usuario: User = Depends(_require_contabilidad),
):
    param = db.query(ParametroContable).filter(ParametroContable.clave == clave).first()
    if not param:
        raise HTTPException(404, f"Parámetro '{clave}' no encontrado")
    db.delete(param)
    db.commit()
