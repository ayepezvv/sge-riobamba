"""
Servicio: Generación automática de asientos contables (YXP-21)
Esquema: contabilidad
Nomenclatura: español

Eventos soportados:
  - Factura de venta/compra aprobada   → asiento AR/AP
  - Pago confirmado                    → asiento de cancelación
  - Cierre de recaudación              → doble asiento (RN-F03)
  - Devengado presupuestario           → asiento gasto/CXP (RN-PRES-03)
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional, List, Tuple

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.contabilidad import (
    CuentaContable, Diario, PeriodoContable,
    AsientoContable, LineaAsiento, ParametroContable,
    EstadoCuenta, EstadoPeriodo, EstadoAsiento, TipoDiario,
)

log = logging.getLogger("sge.auto_asientos")


# ===========================================================================
# UTILIDADES INTERNAS
# ===========================================================================

def _obtener_parametro_cuenta(db: Session, clave: str) -> Optional[CuentaContable]:
    """Retorna la CuentaContable configurada para la clave dada, o None."""
    param = db.query(ParametroContable).filter(ParametroContable.clave == clave).first()
    if param and param.cuenta_id:
        return db.query(CuentaContable).filter(CuentaContable.id == param.cuenta_id).first()
    return None


def _obtener_parametro_diario(db: Session, clave: str) -> Optional[Diario]:
    """Retorna el Diario configurado para la clave dada, o None."""
    param = db.query(ParametroContable).filter(ParametroContable.clave == clave).first()
    if param and param.diario_id:
        return db.query(Diario).filter(Diario.id == param.diario_id).first()
    return None


def _obtener_periodo_por_fecha(db: Session, fecha: date) -> Optional[PeriodoContable]:
    """Encuentra el período ABIERTO que contiene la fecha dada."""
    return (
        db.query(PeriodoContable)
        .filter(
            PeriodoContable.estado == EstadoPeriodo.ABIERTO,
            PeriodoContable.fecha_inicio <= fecha,
            PeriodoContable.fecha_fin >= fecha,
        )
        .first()
    )


def _validar_cuadre(lineas: List[dict]) -> Tuple[Decimal, Decimal]:
    """Verifica que Σ debe == Σ haber. Retorna (total_debe, total_haber)."""
    total_debe = sum(Decimal(str(l["debe"])) for l in lineas)
    total_haber = sum(Decimal(str(l["haber"])) for l in lineas)
    if total_debe != total_haber:
        raise HTTPException(
            status_code=400,
            detail=f"Asiento no cuadra: Debe={total_debe} ≠ Haber={total_haber}",
        )
    return total_debe, total_haber


def _crear_y_publicar_asiento(
    db: Session,
    diario: Diario,
    periodo: PeriodoContable,
    fecha: date,
    referencia: str,
    concepto: str,
    lineas: List[dict],  # [{"cuenta_id": int, "descripcion": str, "debe": Decimal, "haber": Decimal}]
    usuario_id: Optional[int],
) -> AsientoContable:
    """
    Crea y publica un asiento contable en una sola operación.
    Valida: cuadre, cuentas activas, período abierto.
    """
    total_debe, total_haber = _validar_cuadre(lineas)

    # Verificar cuentas activas
    for idx, linea in enumerate(lineas, 1):
        cuenta = db.query(CuentaContable).filter(
            CuentaContable.id == linea["cuenta_id"]
        ).first()
        if not cuenta:
            raise HTTPException(400, f"Cuenta {linea['cuenta_id']} no encontrada (línea {idx})")
        if cuenta.estado != EstadoCuenta.ACTIVA:
            raise HTTPException(400, f"Cuenta '{cuenta.codigo}' inactiva (línea {idx})")
        if not cuenta.permite_movimientos:
            raise HTTPException(
                400, f"Cuenta '{cuenta.codigo}' es de agrupación y no permite movimientos"
            )

    # Generar número secuencial definitivo
    seq = (
        db.query(func.count(AsientoContable.id))
        .filter(
            AsientoContable.diario_id == diario.id,
            AsientoContable.periodo_id == periodo.id,
            AsientoContable.estado == EstadoAsiento.PUBLICADO,
        )
        .scalar()
        or 0
    ) + 1
    numero = f"{diario.codigo}/{periodo.anio}/{periodo.mes:02d}/{seq:05d}"

    ahora = datetime.now(timezone.utc)
    asiento = AsientoContable(
        numero=numero,
        diario_id=diario.id,
        periodo_id=periodo.id,
        fecha=fecha,
        referencia=referencia,
        concepto=concepto,
        estado=EstadoAsiento.PUBLICADO,
        total_debe=total_debe,
        total_haber=total_haber,
        usuario_id=usuario_id,
        fecha_publicacion=ahora,
        creado_por_id=usuario_id,
        actualizado_por_id=usuario_id,
    )
    db.add(asiento)
    db.flush()  # obtener ID

    for idx, linea in enumerate(lineas, 1):
        db.add(LineaAsiento(
            asiento_id=asiento.id,
            cuenta_id=linea["cuenta_id"],
            descripcion=linea.get("descripcion") or concepto,
            debe=Decimal(str(linea["debe"])),
            haber=Decimal(str(linea["haber"])),
            orden=idx,
            creado_por_id=usuario_id,
            actualizado_por_id=usuario_id,
        ))

    log.info("Asiento %s generado automáticamente (%s)", numero, concepto)
    return asiento


# ===========================================================================
# SERVICIO 1: ASIENTO DE FACTURA (AR/AP)
# ===========================================================================

def generar_asiento_factura(
    db: Session,
    factura,  # models.financiero.Factura
    usuario_id: Optional[int],
    omitir_si_sin_config: bool = True,
) -> Optional[AsientoContable]:
    """
    Genera asiento contable al aprobar una factura.

    Factura CLIENTE (AR):
      DEBE  → CXC (CUENTA_CXC) por el total
      HABER → Ingreso (cuenta_contable_id de cada línea) por subtotal_linea
      HABER → IVA Cobrado (CUENTA_IVA_COBRADO) por total_iva

    Factura PROVEEDOR (AP):
      DEBE  → Gasto/Activo (cuenta_contable_id de cada línea) por subtotal_linea
      DEBE  → IVA Pagado (CUENTA_IVA_PAGADO) por total_iva
      HABER → CXP (CUENTA_CXP) por el total
    """
    from app.models.financiero import TipoFactura

    periodo = _obtener_periodo_por_fecha(db, factura.fecha_emision)
    if not periodo:
        if omitir_si_sin_config:
            log.warning(
                "Factura %s: no hay período ABIERTO para %s — asiento no generado",
                factura.numero, factura.fecha_emision,
            )
            return None
        raise HTTPException(
            400,
            f"No existe período contable ABIERTO para la fecha {factura.fecha_emision}",
        )

    es_cliente = factura.tipo == TipoFactura.CLIENTE
    clave_contrapartida = "CUENTA_CXC" if es_cliente else "CUENTA_CXP"
    clave_iva = "CUENTA_IVA_COBRADO" if es_cliente else "CUENTA_IVA_PAGADO"
    clave_diario = "DIARIO_VENTAS" if es_cliente else "DIARIO_COMPRAS"

    cuenta_contrapartida = _obtener_parametro_cuenta(db, clave_contrapartida)
    diario = _obtener_parametro_diario(db, clave_diario)

    if not cuenta_contrapartida or not diario:
        if omitir_si_sin_config:
            log.warning(
                "Factura %s: parámetros %s o %s no configurados — asiento no generado",
                factura.numero, clave_contrapartida, clave_diario,
            )
            return None
        raise HTTPException(
            400,
            f"Parámetros contables '{clave_contrapartida}' o '{clave_diario}' no configurados",
        )

    lineas: List[dict] = []
    total = Decimal(str(factura.total))
    total_iva = Decimal(str(factura.total_iva))

    if es_cliente:
        # DEBE: CXC por total
        lineas.append({
            "cuenta_id": cuenta_contrapartida.id,
            "descripcion": f"CXC Factura {factura.numero} — {factura.nombre_tercero}",
            "debe": total,
            "haber": Decimal("0"),
        })
        # HABER: líneas de ingreso
        for linea in factura.lineas:
            if not linea.cuenta_contable_id:
                if omitir_si_sin_config:
                    log.warning(
                        "Línea %s de factura %s sin cuenta_contable_id — asiento no generado",
                        linea.id, factura.numero,
                    )
                    return None
                raise HTTPException(
                    400,
                    f"Línea {linea.id} de la factura no tiene cuenta contable asignada",
                )
            lineas.append({
                "cuenta_id": linea.cuenta_contable_id,
                "descripcion": linea.descripcion[:255],
                "debe": Decimal("0"),
                "haber": Decimal(str(linea.subtotal_linea)),
            })
        # HABER: IVA cobrado
        if total_iva > 0:
            cuenta_iva = _obtener_parametro_cuenta(db, clave_iva)
            if cuenta_iva:
                lineas.append({
                    "cuenta_id": cuenta_iva.id,
                    "descripcion": f"IVA cobrado — Factura {factura.numero}",
                    "debe": Decimal("0"),
                    "haber": total_iva,
                })
            else:
                log.warning("CUENTA_IVA_COBRADO no configurada — IVA incluido en primera línea")
                # Redistribuir el IVA en la contrapartida ya registrada (ajuste en DEBE)
                lineas[0]["debe"] = Decimal(str(factura.base_imponible))
    else:
        # DEBE: Gasto/Activo por línea
        for linea in factura.lineas:
            if not linea.cuenta_contable_id:
                if omitir_si_sin_config:
                    return None
                raise HTTPException(
                    400,
                    f"Línea {linea.id} de la factura no tiene cuenta contable asignada",
                )
            lineas.append({
                "cuenta_id": linea.cuenta_contable_id,
                "descripcion": linea.descripcion[:255],
                "debe": Decimal(str(linea.subtotal_linea)),
                "haber": Decimal("0"),
            })
        # DEBE: IVA pagado
        if total_iva > 0:
            cuenta_iva = _obtener_parametro_cuenta(db, clave_iva)
            if cuenta_iva:
                lineas.append({
                    "cuenta_id": cuenta_iva.id,
                    "descripcion": f"IVA pagado — Factura {factura.numero}",
                    "debe": total_iva,
                    "haber": Decimal("0"),
                })
        # HABER: CXP por total
        lineas.append({
            "cuenta_id": cuenta_contrapartida.id,
            "descripcion": f"CXP Factura {factura.numero} — {factura.nombre_tercero}",
            "debe": Decimal("0"),
            "haber": total,
        })

    return _crear_y_publicar_asiento(
        db=db,
        diario=diario,
        periodo=periodo,
        fecha=factura.fecha_emision,
        referencia=factura.numero,
        concepto=f"Factura {'venta' if es_cliente else 'compra'} {factura.numero} — {factura.nombre_tercero}",
        lineas=lineas,
        usuario_id=usuario_id,
    )


# ===========================================================================
# SERVICIO 2: ASIENTO DE PAGO (cancelación CXC/CXP)
# ===========================================================================

def generar_asiento_pago(
    db: Session,
    pago,  # models.financiero.Pago
    usuario_id: Optional[int],
    omitir_si_sin_config: bool = True,
) -> Optional[AsientoContable]:
    """
    Genera asiento contable al confirmar un pago.

    Pago CLIENTE (cobro AR):
      DEBE  → Banco/Caja (cuenta_contable de la cuenta bancaria)
      HABER → CXC (por el monto aplicado a cada factura)

    Pago PROVEEDOR (pago AP):
      DEBE  → CXP (por el monto aplicado a cada factura)
      HABER → Banco/Caja (cuenta_contable de la cuenta bancaria)
    """
    from app.models.financiero import TipoPago
    from app.models.tesoreria import CuentaBancaria

    periodo = _obtener_periodo_por_fecha(db, pago.fecha_pago)
    if not periodo:
        if omitir_si_sin_config:
            log.warning("Pago %s: sin período ABIERTO — asiento no generado", pago.numero)
            return None
        raise HTTPException(
            400, f"No existe período contable ABIERTO para la fecha {pago.fecha_pago}"
        )

    # Resolver cuenta del banco/caja
    cuenta_banco = None
    if pago.cuenta_bancaria_id:
        cb = db.query(CuentaBancaria).filter(
            CuentaBancaria.id == pago.cuenta_bancaria_id
        ).first()
        if cb and cb.cuenta_contable_id:
            cuenta_banco = db.query(CuentaContable).filter(
                CuentaContable.id == cb.cuenta_contable_id
            ).first()

    es_cliente = pago.tipo == "CLIENTE"
    clave_diario = (
        "DIARIO_CAJA"
        if pago.tipo_pago in ("EFECTIVO",)
        else "DIARIO_BANCO"
    )
    diario = _obtener_parametro_diario(db, clave_diario)

    if not cuenta_banco or not diario:
        if omitir_si_sin_config:
            log.warning(
                "Pago %s: cuenta banco o diario no configurados — asiento no generado",
                pago.numero,
            )
            return None
        raise HTTPException(
            400,
            "Cuenta bancaria sin cuenta contable asociada o diario no configurado",
        )

    monto_total = Decimal(str(pago.monto_total))
    lineas: List[dict] = []

    if es_cliente:
        # DEBE: banco/caja por monto total
        lineas.append({
            "cuenta_id": cuenta_banco.id,
            "descripcion": f"Cobro {pago.numero} — {pago.nombre_tercero}",
            "debe": monto_total,
            "haber": Decimal("0"),
        })
        # HABER: CXC por cada factura aplicada
        for lp in pago.lineas:
            cuenta_cxc = None
            # Intentar recuperar la cuenta CXC del asiento de la factura
            if lp.factura and lp.factura.asiento_contable_id:
                asiento_fac = db.query(AsientoContable).filter(
                    AsientoContable.id == lp.factura.asiento_contable_id
                ).first()
                if asiento_fac:
                    # La primera línea del asiento de factura cliente = CXC
                    primera_linea = (
                        db.query(LineaAsiento)
                        .filter(LineaAsiento.asiento_id == asiento_fac.id)
                        .order_by(LineaAsiento.orden)
                        .first()
                    )
                    if primera_linea:
                        cuenta_cxc = db.query(CuentaContable).filter(
                            CuentaContable.id == primera_linea.cuenta_id
                        ).first()
            if not cuenta_cxc:
                cuenta_cxc = _obtener_parametro_cuenta(db, "CUENTA_CXC")
            if not cuenta_cxc:
                if omitir_si_sin_config:
                    return None
                raise HTTPException(400, "CUENTA_CXC no configurada")
            lineas.append({
                "cuenta_id": cuenta_cxc.id,
                "descripcion": f"Cancelación Factura {lp.factura.numero if lp.factura else '?'}",
                "debe": Decimal("0"),
                "haber": Decimal(str(lp.monto_aplicado)),
            })
    else:
        # DEBE: CXP por cada factura aplicada
        for lp in pago.lineas:
            cuenta_cxp = _obtener_parametro_cuenta(db, "CUENTA_CXP")
            if not cuenta_cxp:
                if omitir_si_sin_config:
                    return None
                raise HTTPException(400, "CUENTA_CXP no configurada")
            lineas.append({
                "cuenta_id": cuenta_cxp.id,
                "descripcion": f"Cancelación Factura {lp.factura.numero if lp.factura else '?'}",
                "debe": Decimal(str(lp.monto_aplicado)),
                "haber": Decimal("0"),
            })
        # HABER: banco/caja por monto total
        lineas.append({
            "cuenta_id": cuenta_banco.id,
            "descripcion": f"Pago {pago.numero} — {pago.nombre_tercero}",
            "debe": Decimal("0"),
            "haber": monto_total,
        })

    if not lineas:
        log.warning("Pago %s sin líneas aplicadas — asiento no generado", pago.numero)
        return None

    return _crear_y_publicar_asiento(
        db=db,
        diario=diario,
        periodo=periodo,
        fecha=pago.fecha_pago,
        referencia=pago.numero,
        concepto=f"Pago {'cobro' if es_cliente else 'proveedor'} {pago.numero} — {pago.nombre_tercero}",
        lineas=lineas,
        usuario_id=usuario_id,
    )


# ===========================================================================
# SERVICIO 3: ASIENTO DE CIERRE DE RECAUDACIÓN (RN-F03 doble asiento)
# ===========================================================================

def generar_asientos_cierre_recaudacion(
    db: Session,
    cierre,  # models.financiero.CierreRecaudacion
    usuario_id: Optional[int],
    omitir_si_sin_config: bool = True,
) -> Tuple[Optional[AsientoContable], Optional[AsientoContable]]:
    """
    RN-F03: Genera doble asiento para cierre de recaudación.

    Asiento 1 (Recaudación):
      DEBE  → Caja Recaudación (CUENTA_CAJA_RECAUDACION)
      HABER → CXC (CUENTA_CXC)

    Asiento 2 (Traslado BCE):
      DEBE  → CUT-BCE (CUENTA_BCE_CUT)
      HABER → Caja Recaudación (CUENTA_CAJA_RECAUDACION)
    """
    periodo = _obtener_periodo_por_fecha(db, cierre.fecha)
    if not periodo:
        if omitir_si_sin_config:
            log.warning("Cierre %s: sin período ABIERTO — asientos no generados", cierre.fecha)
            return None, None
        raise HTTPException(
            400, f"No existe período contable ABIERTO para la fecha {cierre.fecha}"
        )

    cuenta_caja = _obtener_parametro_cuenta(db, "CUENTA_CAJA_RECAUDACION")
    cuenta_cxc = _obtener_parametro_cuenta(db, "CUENTA_CXC")
    cuenta_bce = _obtener_parametro_cuenta(db, "CUENTA_BCE_CUT")
    diario_caja = _obtener_parametro_diario(db, "DIARIO_CAJA")

    if not all([cuenta_caja, cuenta_cxc, cuenta_bce, diario_caja]):
        if omitir_si_sin_config:
            log.warning("Cierre recaudación: parámetros incompletos — asientos no generados")
            return None, None
        raise HTTPException(
            400,
            "Parámetros CUENTA_CAJA_RECAUDACION, CUENTA_CXC, CUENTA_BCE_CUT o DIARIO_CAJA no configurados",
        )

    monto = Decimal(str(cierre.total_recaudado))
    fecha_str = cierre.fecha.strftime("%Y-%m-%d")

    # Asiento 1: Recaudación del día
    asiento_recaudacion = _crear_y_publicar_asiento(
        db=db,
        diario=diario_caja,
        periodo=periodo,
        fecha=cierre.fecha,
        referencia=f"RECAUD-{fecha_str}",
        concepto=f"Recaudación del día {fecha_str} — {cierre.numero_transacciones} transacciones",
        lineas=[
            {"cuenta_id": cuenta_caja.id, "descripcion": "Ingreso caja recaudación", "debe": monto, "haber": Decimal("0")},
            {"cuenta_id": cuenta_cxc.id, "descripcion": "Cancelación CXC recaudadas", "debe": Decimal("0"), "haber": monto},
        ],
        usuario_id=usuario_id,
    )

    # Asiento 2: Traslado a BCE
    asiento_traslado = _crear_y_publicar_asiento(
        db=db,
        diario=diario_caja,
        periodo=periodo,
        fecha=cierre.fecha,
        referencia=f"TRASLADO-BCE-{fecha_str}",
        concepto=f"Traslado recaudación a CUT-BCE — {fecha_str}",
        lineas=[
            {"cuenta_id": cuenta_bce.id, "descripcion": "Depósito CUT-BCE", "debe": monto, "haber": Decimal("0")},
            {"cuenta_id": cuenta_caja.id, "descripcion": "Salida caja recaudación", "debe": Decimal("0"), "haber": monto},
        ],
        usuario_id=usuario_id,
    )

    return asiento_recaudacion, asiento_traslado


# ===========================================================================
# SERVICIO 4: ASIENTO DE DEVENGADO PRESUPUESTARIO (RN-PRES-03)
# ===========================================================================

def generar_asiento_devengado(
    db: Session,
    devengado,  # models.presupuesto.Devengado
    usuario_id: Optional[int],
    cuenta_gasto_id: Optional[int] = None,
    cuenta_cxp_id: Optional[int] = None,
    omitir_si_sin_config: bool = True,
) -> Optional[AsientoContable]:
    """
    RN-PRES-03: Asiento de reconocimiento del gasto devengado.

    DEBE  → Gasto/Activo (cuenta de la partida presupuestaria o cuenta_gasto_id)
    HABER → CXP (CUENTA_CXP o cuenta_cxp_id)
    """
    periodo = _obtener_periodo_por_fecha(db, devengado.fecha_devengado)
    if not periodo:
        if omitir_si_sin_config:
            log.warning("Devengado %s: sin período ABIERTO — asiento no generado",
                        devengado.numero_devengado)
            return None
        raise HTTPException(
            400,
            f"No existe período contable ABIERTO para la fecha {devengado.fecha_devengado}",
        )

    diario = _obtener_parametro_diario(db, "DIARIO_PRESUPUESTO")
    if not diario:
        # Fallback a diario GENERAL
        diario = (
            db.query(Diario)
            .filter(Diario.tipo == TipoDiario.GENERAL, Diario.es_activo == True)
            .first()
        )
    if not diario:
        if omitir_si_sin_config:
            log.warning("Devengado %s: diario presupuesto no configurado — asiento no generado",
                        devengado.numero_devengado)
            return None
        raise HTTPException(400, "DIARIO_PRESUPUESTO no configurado")

    # Resolver cuenta de gasto
    cuenta_gasto = None
    if cuenta_gasto_id:
        cuenta_gasto = db.query(CuentaContable).filter(
            CuentaContable.id == cuenta_gasto_id
        ).first()
    if not cuenta_gasto:
        # Intentar via partida presupuestaria → vinculación RN-02
        try:
            cert = devengado.compromiso.certificado
            partida = cert.asignacion.partida
            if partida:
                cuenta_gasto = (
                    db.query(CuentaContable)
                    .filter(
                        CuentaContable.partida_presupuestaria == partida.codigo,
                        CuentaContable.es_hoja == True,
                    )
                    .first()
                )
        except AttributeError:
            pass

    if not cuenta_gasto:
        if omitir_si_sin_config:
            log.warning("Devengado %s: cuenta de gasto no encontrada — asiento no generado",
                        devengado.numero_devengado)
            return None
        raise HTTPException(400, "Cuenta de gasto no encontrada para el devengado")

    # Resolver cuenta CXP
    cuenta_cxp = None
    if cuenta_cxp_id:
        cuenta_cxp = db.query(CuentaContable).filter(
            CuentaContable.id == cuenta_cxp_id
        ).first()
    if not cuenta_cxp:
        cuenta_cxp = _obtener_parametro_cuenta(db, "CUENTA_CXP")
    if not cuenta_cxp:
        if omitir_si_sin_config:
            log.warning("Devengado %s: CUENTA_CXP no configurada — asiento no generado",
                        devengado.numero_devengado)
            return None
        raise HTTPException(400, "CUENTA_CXP no configurada")

    monto = Decimal(str(devengado.monto_devengado))

    return _crear_y_publicar_asiento(
        db=db,
        diario=diario,
        periodo=periodo,
        fecha=devengado.fecha_devengado,
        referencia=devengado.numero_devengado,
        concepto=f"Devengado presupuestario {devengado.numero_devengado} — {devengado.concepto}",
        lineas=[
            {
                "cuenta_id": cuenta_gasto.id,
                "descripcion": f"Gasto devengado {devengado.numero_devengado}",
                "debe": monto,
                "haber": Decimal("0"),
            },
            {
                "cuenta_id": cuenta_cxp.id,
                "descripcion": f"CXP devengado {devengado.numero_devengado}",
                "debe": Decimal("0"),
                "haber": monto,
            },
        ],
        usuario_id=usuario_id,
    )
