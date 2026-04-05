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
    ArchivoSpi, LineaSpi, EstadoArchivoSpi,
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
    ArchivoSpiCrear, ArchivoSpiRespuesta, ArchivoSpiResumen,
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


# ===========================================================================
# SPI — Pagos Masivos BCE
# ===========================================================================

def _generar_numero_lote(db: Session) -> str:
    """Genera número secuencial: SPI-YYYYMMDD-NNN."""
    from datetime import date as _date
    hoy = _date.today().strftime("%Y%m%d")
    prefijo = f"SPI-{hoy}-"
    ultimo = (
        db.query(ArchivoSpi)
        .filter(ArchivoSpi.numero_lote.like(f"{prefijo}%"))
        .order_by(ArchivoSpi.id_archivo_spi.desc())
        .first()
    )
    if ultimo:
        try:
            seq = int(ultimo.numero_lote.split("-")[-1]) + 1
        except ValueError:
            seq = 1
    else:
        seq = 1
    return f"{prefijo}{seq:03d}"


@router.post("/spi/lotes", response_model=ArchivoSpiRespuesta,
             status_code=status.HTTP_201_CREATED, tags=["Tesorería - SPI"])
def crear_lote_spi(
    datos: ArchivoSpiCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    """Crea un lote SPI con sus líneas de beneficiarios."""
    cuenta = db.query(CuentaBancaria).filter(
        CuentaBancaria.id == datos.id_cuenta_bancaria
    ).first()
    if not cuenta:
        raise HTTPException(404, "Cuenta bancaria no encontrada")

    numero_lote = _generar_numero_lote(db)
    monto_total = sum(l.valor for l in datos.lineas)

    lote = ArchivoSpi(
        numero_lote=numero_lote,
        estado=EstadoArchivoSpi.BORRADOR,
        monto_total=monto_total,
        id_cuenta_bancaria=datos.id_cuenta_bancaria,
        tipo_pago=datos.tipo_pago,
        creado_por_id=usuario.id,
        actualizado_por_id=usuario.id,
    )
    db.add(lote)
    db.flush()

    for i, linea_datos in enumerate(datos.lineas, start=1):
        linea = LineaSpi(
            id_archivo_spi=lote.id_archivo_spi,
            creado_por_id=usuario.id,
            actualizado_por_id=usuario.id,
            **linea_datos.model_dump(),
        )
        db.add(linea)

    db.commit()
    db.refresh(lote)
    return lote


@router.get("/spi/lotes", response_model=List[ArchivoSpiResumen],
            tags=["Tesorería - SPI"])
def listar_lotes_spi(
    tipo_pago: Optional[str] = None,
    estado: Optional[str] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Lista lotes SPI con filtros opcionales."""
    q = db.query(ArchivoSpi)
    if tipo_pago:
        q = q.filter(ArchivoSpi.tipo_pago == tipo_pago)
    if estado:
        q = q.filter(ArchivoSpi.estado == estado)
    if fecha_desde:
        q = q.filter(ArchivoSpi.creado_en >= fecha_desde)
    if fecha_hasta:
        q = q.filter(ArchivoSpi.creado_en <= fecha_hasta)
    return q.order_by(ArchivoSpi.id_archivo_spi.desc()).all()


@router.get("/spi/lotes/{id_lote}", response_model=ArchivoSpiRespuesta,
            tags=["Tesorería - SPI"])
def detalle_lote_spi(
    id_lote: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Detalle de un lote SPI con todas sus líneas."""
    lote = db.query(ArchivoSpi).filter(ArchivoSpi.id_archivo_spi == id_lote).first()
    if not lote:
        raise HTTPException(404, "Lote SPI no encontrado")
    return lote


@router.post("/spi/lotes/{id_lote}/generar-archivo",
             tags=["Tesorería - SPI"])
def generar_archivo_spi_lote(
    id_lote: int,
    ruc_empresa: str = Query(..., description="RUC de la institución"),
    cuenta_empresa: str = Query(..., description="Número de cuenta origen"),
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    """Genera el archivo TXT en formato BCE para el lote SPI."""
    lote = db.query(ArchivoSpi).filter(ArchivoSpi.id_archivo_spi == id_lote).first()
    if not lote:
        raise HTTPException(404, "Lote SPI no encontrado")
    if lote.estado not in (EstadoArchivoSpi.BORRADOR, EstadoArchivoSpi.GENERADO):
        raise HTTPException(400, f"No se puede regenerar un lote en estado {lote.estado}")
    if not lote.lineas:
        raise HTTPException(400, "El lote no tiene líneas. Agregue beneficiarios primero.")

    header = "RUC_EMPRESA|CTA_EMPRESA|RUC_BENEFICIARIO|NOMBRE_BENEFICIARIO|BANCO_DESTINO|CTA_DESTINO|TIPO_CUENTA|VALOR|REFERENCIA|DESCRIPCION"
    filas = [header]
    for linea in lote.lineas:
        if linea.valor <= 0:
            continue
        fila = "|".join([
            ruc_empresa,
            cuenta_empresa,
            linea.ruc_beneficiario,
            linea.nombre_beneficiario.upper(),
            linea.banco_destino,
            linea.cuenta_destino,
            linea.tipo_cuenta,
            str(linea.valor),
            linea.referencia or lote.numero_lote,
            linea.descripcion or f"PAGO {lote.tipo_pago} {lote.numero_lote}",
        ])
        filas.append(fila)

    if len(filas) == 1:
        raise HTTPException(400, "No hay líneas con valor > 0 para generar el archivo.")

    contenido = "\n".join(filas)
    nombre_archivo = f"{lote.numero_lote}.txt"

    lote.nombre_archivo = nombre_archivo
    lote.estado = EstadoArchivoSpi.GENERADO
    lote.actualizado_por_id = usuario.id
    db.commit()

    from fastapi.responses import Response
    return Response(
        content=contenido,
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'},
    )


@router.post("/spi/lotes/{id_lote}/marcar-enviado",
             response_model=ArchivoSpiResumen,
             tags=["Tesorería - SPI"])
def marcar_lote_enviado(
    id_lote: int,
    fecha_envio: Optional[date] = None,
    db: Session = Depends(get_db),
    usuario: User = Depends(require_role(_ROLES_TESORERIA)),
):
    """Marca el lote como ENVIADO al BCE."""
    lote = db.query(ArchivoSpi).filter(ArchivoSpi.id_archivo_spi == id_lote).first()
    if not lote:
        raise HTTPException(404, "Lote SPI no encontrado")
    if lote.estado != EstadoArchivoSpi.GENERADO:
        raise HTTPException(400, f"Solo se puede marcar como enviado un lote en estado GENERADO (actual: {lote.estado})")

    from datetime import date as _date
    lote.estado = EstadoArchivoSpi.ENVIADO
    lote.fecha_envio = fecha_envio or _date.today()
    lote.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(lote)
    return lote
