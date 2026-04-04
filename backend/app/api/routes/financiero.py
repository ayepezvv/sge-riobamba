"""
Router FastAPI — Módulo Financiero (AR/AP)
Rutas en español, esquema PostgreSQL: financiero
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.financiero import (
    TipoDocumentoConfig, Factura, LineaFactura, Pago, LineaPago,
    CierreRecaudacion, EstadoFactura, EstadoPago,
)
from app.models.user import User
from app.services.auto_asientos import (
    generar_asiento_factura,
    generar_asiento_pago,
    generar_asientos_cierre_recaudacion,
)

from app.schemas.financiero import (
    TipoDocumentoCrear, TipoDocumentoActualizar, TipoDocumentoRespuesta,
    FacturaCrear, FacturaActualizar, FacturaRespuesta, ResumenFactura,
    AprobarFactura, AnularFactura,
    PagoCrear, PagoRespuesta, ConfirmarPago, AnularPago,
    LineaPagoCrear,
    CierreRecaudacionCrear, CierreRecaudacionRespuesta,
)

router = APIRouter()


# ===========================================================================
# TIPOS DE DOCUMENTO
# ===========================================================================

@router.get("/tipos-documento", response_model=List[TipoDocumentoRespuesta],
             tags=["Financiero - Tipos Documento"])
def listar_tipos_documento(
    solo_activos: bool = True,
    tipo: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(TipoDocumentoConfig)
    if solo_activos:
        q = q.filter(TipoDocumentoConfig.es_activo == True)
    if tipo:
        q = q.filter(TipoDocumentoConfig.tipo == tipo)
    return q.order_by(TipoDocumentoConfig.codigo).all()


@router.post("/tipos-documento", response_model=TipoDocumentoRespuesta,
              status_code=status.HTTP_201_CREATED, tags=["Financiero - Tipos Documento"])
def crear_tipo_documento(
    datos: TipoDocumentoCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user),
):
    existente = db.query(TipoDocumentoConfig).filter(
        TipoDocumentoConfig.codigo == datos.codigo).first()
    if existente:
        raise HTTPException(400, f"Ya existe tipo de documento con código '{datos.codigo}'")
    td = TipoDocumentoConfig(**datos.model_dump(),
                               creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(td)
    db.commit()
    db.refresh(td)
    return td


# ===========================================================================
# FACTURAS
# ===========================================================================

@router.get("/facturas", response_model=List[ResumenFactura], tags=["Financiero - Facturas"])
def listar_facturas(
    tipo: Optional[str] = Query(None, description="CLIENTE | PROVEEDOR"),
    estado: Optional[str] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    identificacion_tercero: Optional[str] = None,
    q_texto: Optional[str] = Query(None, alias="q"),
    db: Session = Depends(get_db),
):
    q = db.query(Factura)
    if tipo:
        q = q.filter(Factura.tipo == tipo)
    if estado:
        q = q.filter(Factura.estado == estado)
    if fecha_desde:
        q = q.filter(Factura.fecha_emision >= fecha_desde)
    if fecha_hasta:
        q = q.filter(Factura.fecha_emision <= fecha_hasta)
    if identificacion_tercero:
        q = q.filter(Factura.identificacion_tercero == identificacion_tercero)
    if q_texto:
        q = q.filter(
            Factura.nombre_tercero.ilike(f"%{q_texto}%") |
            Factura.numero.ilike(f"%{q_texto}%")
        )
    return q.order_by(Factura.fecha_emision.desc()).all()


@router.post("/facturas", response_model=FacturaRespuesta,
              status_code=status.HTTP_201_CREATED, tags=["Financiero - Facturas"])
def crear_factura(
    datos: FacturaCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user),
):
    # Verificar tipo de documento existe
    tipo_doc = db.query(TipoDocumentoConfig).filter(
        TipoDocumentoConfig.id == datos.tipo_documento_id).first()
    if not tipo_doc:
        raise HTTPException(404, "Tipo de documento no encontrado")

    lineas_data = datos.lineas
    factura_data = datos.model_dump(exclude={"lineas"})

    # Calcular totales
    subtotal = Decimal("0")
    descuento = Decimal("0")
    total_iva = Decimal("0")

    for ld in lineas_data:
        sub_linea = (ld.cantidad * ld.precio_unitario) - ld.descuento_linea
        iva_linea = sub_linea * (ld.porcentaje_impuesto / 100)
        subtotal += ld.cantidad * ld.precio_unitario
        descuento += ld.descuento_linea
        total_iva += iva_linea

    base_imponible = subtotal - descuento
    total = base_imponible + total_iva

    # Número provisional en borrador
    numero_provisional = f"BORR-{tipo_doc.secuencia_prefijo or ''}{tipo_doc.secuencia_siguiente:06d}"

    factura = Factura(
        **factura_data,
        numero=numero_provisional,
        subtotal=subtotal,
        descuento=descuento,
        base_imponible=base_imponible,
        total_iva=total_iva,
        total=total,
        saldo_pendiente=total,
        creado_por_id=usuario.id,
        actualizado_por_id=usuario.id,
    )
    db.add(factura)
    db.flush()

    for i, ld in enumerate(lineas_data, 1):
        sub_linea = (ld.cantidad * ld.precio_unitario) - ld.descuento_linea
        iva_linea = sub_linea * (ld.porcentaje_impuesto / 100)
        linea = LineaFactura(
            **ld.model_dump(),
            factura_id=factura.id,
            orden=i,
            subtotal_linea=sub_linea,
            valor_impuesto=iva_linea,
            total_linea=sub_linea + iva_linea,
            creado_por_id=usuario.id,
            actualizado_por_id=usuario.id,
        )
        db.add(linea)

    db.commit()
    db.refresh(factura)
    return factura


@router.get("/facturas/{factura_id}", response_model=FacturaRespuesta, tags=["Financiero - Facturas"])
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(404, "Factura no encontrada")
    return factura


@router.post("/facturas/{factura_id}/aprobar", response_model=FacturaRespuesta,
              tags=["Financiero - Facturas"])
def aprobar_factura(
    factura_id: int,
    datos: AprobarFactura,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user),
):
    """
    Aprueba la factura y genera número secuencial definitivo.
    RN-F05: Aquí se generaría el asiento contable automático (hook de integración).
    """
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(404, "Factura no encontrada")
    if factura.estado != EstadoFactura.BORRADOR:
        raise HTTPException(400, f"Solo se pueden aprobar facturas en BORRADOR (estado actual: {factura.estado})")

    # BL2: with_for_update() evita race condition en la secuencia de numeración
    tipo_doc = (
        db.query(TipoDocumentoConfig)
        .with_for_update()
        .filter(TipoDocumentoConfig.id == factura.tipo_documento_id)
        .first()
    )

    if datos.numero:
        # Verificar que no exista
        existente = db.query(Factura).filter(Factura.numero == datos.numero).first()
        if existente and existente.id != factura_id:
            raise HTTPException(400, f"Ya existe factura con número '{datos.numero}'")
        factura.numero = datos.numero
    else:
        # Generar número secuencial
        prefijo = tipo_doc.secuencia_prefijo or ""
        factura.numero = f"{prefijo}{tipo_doc.secuencia_siguiente:06d}"
        tipo_doc.secuencia_siguiente += 1

    factura.estado = EstadoFactura.APROBADA
    factura.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(factura)

    # RN-F05: Generar asiento contable automático (YXP-21)
    from sqlalchemy.orm import selectinload
    factura = (
        db.query(Factura)
        .options(selectinload(Factura.lineas))
        .filter(Factura.id == factura_id)
        .first()
    )
    asiento = generar_asiento_factura(db, factura, usuario.id)
    if asiento:
        factura.asiento_contable_id = asiento.id
        db.commit()
        db.refresh(factura)

    return factura


@router.post("/facturas/{factura_id}/anular", response_model=FacturaRespuesta,
              tags=["Financiero - Facturas"])
def anular_factura(
    factura_id: int,
    datos: AnularFactura,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user),
):
    """RN-F04: Estado ANULADA es permanente (no se puede revertir)."""
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(404, "Factura no encontrada")
    if factura.estado == EstadoFactura.ANULADA:
        raise HTTPException(400, "La factura ya está anulada (RN-F04: estado permanente)")
    if factura.estado == EstadoFactura.PAGADA:
        raise HTTPException(400, "No se puede anular una factura completamente pagada")
    factura.estado = EstadoFactura.ANULADA
    factura.motivo_anulacion = datos.motivo_anulacion
    factura.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(factura)
    return factura


# ===========================================================================
# PAGOS
# ===========================================================================

@router.get("/pagos", response_model=List[PagoRespuesta], tags=["Financiero - Pagos"])
def listar_pagos(
    tipo: Optional[str] = None,
    estado: Optional[str] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    identificacion_tercero: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Pago)
    if tipo:
        q = q.filter(Pago.tipo == tipo)
    if estado:
        q = q.filter(Pago.estado == estado)
    if fecha_desde:
        q = q.filter(Pago.fecha_pago >= fecha_desde)
    if fecha_hasta:
        q = q.filter(Pago.fecha_pago <= fecha_hasta)
    if identificacion_tercero:
        q = q.filter(Pago.identificacion_tercero == identificacion_tercero)
    return q.order_by(Pago.fecha_pago.desc()).all()


@router.post("/pagos", response_model=PagoRespuesta,
              status_code=status.HTTP_201_CREATED, tags=["Financiero - Pagos"])
def crear_pago(
    datos: PagoCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user),
):
    lineas_data = datos.lineas
    pago_data = datos.model_dump(exclude={"lineas"})

    # Número provisional
    from datetime import datetime
    numero_provisional = f"PAG-BORR-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    pago = Pago(
        **pago_data,
        numero=numero_provisional,
        creado_por_id=usuario.id,
        actualizado_por_id=usuario.id,
    )
    db.add(pago)
    db.flush()

    for ld in lineas_data:
        # Verificar que la factura existe y tiene saldo
        factura = db.query(Factura).filter(Factura.id == ld.factura_id).first()
        if not factura:
            raise HTTPException(404, f"Factura {ld.factura_id} no encontrada")
        if factura.estado not in (EstadoFactura.APROBADA, EstadoFactura.PARCIAL):
            raise HTTPException(400,
                f"Factura {factura.numero} debe estar APROBADA o PARCIAL para recibir pagos")
        if ld.monto_aplicado > factura.saldo_pendiente:
            raise HTTPException(400,
                f"Monto aplicado ({ld.monto_aplicado}) supera saldo pendiente de {factura.numero} ({factura.saldo_pendiente})")

        linea = LineaPago(**ld.model_dump(), pago_id=pago.id,
                           creado_por_id=usuario.id, actualizado_por_id=usuario.id)
        db.add(linea)

        # Actualizar saldo de la factura
        factura.saldo_pendiente -= ld.monto_aplicado
        if factura.saldo_pendiente <= Decimal("0"):
            factura.estado = EstadoFactura.PAGADA
        else:
            factura.estado = EstadoFactura.PARCIAL
        factura.actualizado_por_id = usuario.id

    db.commit()
    db.refresh(pago)
    return pago


@router.get("/pagos/{pago_id}", response_model=PagoRespuesta, tags=["Financiero - Pagos"])
def obtener_pago(pago_id: int, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago:
        raise HTTPException(404, "Pago no encontrado")
    return pago


@router.post("/pagos/{pago_id}/confirmar", response_model=PagoRespuesta,
              tags=["Financiero - Pagos"])
def confirmar_pago(
    pago_id: int,
    datos: ConfirmarPago,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user),
):
    """
    Confirma el pago y genera número secuencial.
    RN-F05: Hook para generación de asiento contable automático.
    """
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago:
        raise HTTPException(404, "Pago no encontrado")
    if pago.estado != EstadoPago.BORRADOR:
        raise HTTPException(400, "Solo se pueden confirmar pagos en BORRADOR")

    if datos.numero:
        pago.numero = datos.numero
    else:
        from datetime import datetime
        pago.numero = f"PAG-{datetime.now().strftime('%Y%m%d')}-{pago.id:06d}"

    pago.estado = EstadoPago.CONFIRMADO
    pago.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(pago)

    # RN-F05: Generar asiento de cancelación (YXP-21)
    from sqlalchemy.orm import selectinload
    pago = (
        db.query(Pago)
        .options(selectinload(Pago.lineas))
        .filter(Pago.id == pago_id)
        .first()
    )
    asiento = generar_asiento_pago(db, pago, usuario.id)
    if asiento:
        pago.asiento_contable_id = asiento.id
        db.commit()
        db.refresh(pago)

    return pago


@router.post("/pagos/{pago_id}/anular", response_model=PagoRespuesta, tags=["Financiero - Pagos"])
def anular_pago(
    pago_id: int,
    datos: AnularPago,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user),
):
    """RN-F04: Estado ANULADO permanente."""
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago:
        raise HTTPException(404, "Pago no encontrado")
    if pago.estado == EstadoPago.ANULADO:
        raise HTTPException(400, "El pago ya está anulado (RN-F04)")

    # Revertir saldos en facturas
    for linea in pago.lineas:
        factura = linea.factura
        factura.saldo_pendiente += linea.monto_aplicado
        if factura.saldo_pendiente >= factura.total:
            factura.estado = EstadoFactura.APROBADA
        else:
            factura.estado = EstadoFactura.PARCIAL
        factura.actualizado_por_id = usuario.id

    pago.estado = EstadoPago.ANULADO
    pago.motivo_anulacion = datos.motivo_anulacion
    pago.actualizado_por_id = usuario.id
    db.commit()
    db.refresh(pago)
    return pago


# ===========================================================================
# CIERRES DE RECAUDACIÓN
# ===========================================================================

@router.get("/cierres-recaudacion", response_model=List[CierreRecaudacionRespuesta],
             tags=["Financiero - Cierres Recaudación"])
def listar_cierres_recaudacion(
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db),
):
    q = db.query(CierreRecaudacion)
    if fecha_desde:
        q = q.filter(CierreRecaudacion.fecha >= fecha_desde)
    if fecha_hasta:
        q = q.filter(CierreRecaudacion.fecha <= fecha_hasta)
    return q.order_by(CierreRecaudacion.fecha.desc()).all()


@router.post("/cierres-recaudacion", response_model=CierreRecaudacionRespuesta,
              status_code=status.HTTP_201_CREATED,
              tags=["Financiero - Cierres Recaudación"])
def crear_cierre_recaudacion(
    datos: CierreRecaudacionCrear,
    db: Session = Depends(get_db),
    usuario: User = Depends(get_current_user),
):
    """
    RN-F02: Un solo cierre por día (UNIQUE date).
    RN-F03: Genera doble asiento contable (recaudación + traslado BCE).
    """
    existente = db.query(CierreRecaudacion).filter(
        CierreRecaudacion.fecha == datos.fecha).first()
    if existente:
        raise HTTPException(400, f"Ya existe cierre de recaudación para la fecha {datos.fecha} (RN-F02)")

    cierre = CierreRecaudacion(**datos.model_dump(),
                                creado_por_id=usuario.id, actualizado_por_id=usuario.id)
    db.add(cierre)
    db.commit()
    db.refresh(cierre)

    # RN-F03: Doble asiento contable automático (YXP-21)
    asiento_rec, asiento_tral = generar_asientos_cierre_recaudacion(db, cierre, usuario.id)
    if asiento_rec:
        cierre.asiento_recaudacion_id = asiento_rec.id
    if asiento_tral:
        cierre.asiento_traslado_bce_id = asiento_tral.id
    if asiento_rec or asiento_tral:
        db.commit()
        db.refresh(cierre)

    return cierre


@router.get("/cierres-recaudacion/{cierre_id}", response_model=CierreRecaudacionRespuesta,
             tags=["Financiero - Cierres Recaudación"])
def obtener_cierre_recaudacion(cierre_id: int, db: Session = Depends(get_db)):
    cierre = db.query(CierreRecaudacion).filter(CierreRecaudacion.id == cierre_id).first()
    if not cierre:
        raise HTTPException(404, "Cierre de recaudación no encontrado")
    return cierre
