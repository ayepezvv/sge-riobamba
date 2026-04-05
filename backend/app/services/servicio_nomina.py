"""
Servicio de Nómina — Motor de Cálculo de Rol de Pagos
Esquema: rrhh
Archivo: backend/app/services/servicio_nomina.py

Motor desacoplado que evalúa RubroNomina para cada empleado activo
y genera las líneas del rol de pagos con auditoría completa.
"""
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.rrhh import (
    Empleado, Contrato, RubroNomina, ParametroCalculo, ImpuestoRentaEscala,
    RolPago, LineaRolPago, DetalleLineaRol,
)

CUANTIA = Decimal("0.01")


def _redondear(valor: Decimal) -> Decimal:
    return valor.quantize(CUANTIA, rounding=ROUND_HALF_UP)


def _obtener_parametro(db: Session, anio: int, codigo: str) -> Optional[Decimal]:
    """Retorna valor_numerico de ParametroCalculo para año y código dados."""
    p = db.query(ParametroCalculo).filter(
        ParametroCalculo.anio_vigencia == anio,
        ParametroCalculo.codigo_parametro == codigo,
        ParametroCalculo.estado == "ACTIVO",
    ).first()
    return Decimal(str(p.valor_numerico)) if p and p.valor_numerico else None


def _calcular_ir_anual(db: Session, anio: int, base_imponible_anual: Decimal) -> Decimal:
    """
    Calcula el Impuesto a la Renta anual usando la tabla progresiva del SRI.
    Retorna el impuesto ANUAL; dividir por 12 para el descuento mensual.
    """
    escala = (
        db.query(ImpuestoRentaEscala)
        .filter(
            ImpuestoRentaEscala.anio_vigencia == anio,
            ImpuestoRentaEscala.fraccion_basica <= base_imponible_anual,
        )
        .order_by(ImpuestoRentaEscala.fraccion_basica.desc())
        .first()
    )
    if not escala:
        return Decimal("0.00")

    exceso = base_imponible_anual - Decimal(str(escala.fraccion_basica))
    impuesto_fraccion = Decimal(str(escala.impuesto_fraccion_basica))
    porcentaje = Decimal(str(escala.porcentaje_fraccion_excedente)) / Decimal("100")
    return _redondear(impuesto_fraccion + exceso * porcentaje)


def calcular_linea_empleado(
    db: Session,
    empleado: Empleado,
    anio: int,
    mes: int,
    tipo_rol: str,
    dias_trabajados: int = 30,
) -> dict:
    """
    Calcula todos los rubros para un empleado en un período dado.
    Retorna dict con totales y lista de detalles por rubro.
    """
    # 1. Obtener contrato vigente
    contrato = (
        db.query(Contrato)
        .filter(
            Contrato.id_empleado == empleado.id_empleado,
            Contrato.estado_contrato == "ACTIVO",
        )
        .order_by(Contrato.fecha_inicio.desc())
        .first()
    )
    if not contrato:
        return {
            "error": f"Empleado {empleado.id_empleado} no tiene contrato activo",
            "detalles": [],
            "total_ingresos": Decimal("0"),
            "total_descuentos": Decimal("0"),
            "total_provisiones": Decimal("0"),
            "liquido_a_recibir": Decimal("0"),
            "sueldo_base": Decimal("0"),
        }

    sueldo_base = Decimal(str(contrato.sueldo_pactado))
    sueldo_proporcional = _redondear(sueldo_base * Decimal(dias_trabajados) / Decimal("30"))

    # 2. Parámetros del año
    porc_iess_personal = _obtener_parametro(db, anio, "IESS_PERSONAL") or Decimal("9.45")
    porc_iess_patronal = _obtener_parametro(db, anio, "IESS_PATRONAL") or Decimal("11.15")
    porc_fondos_reserva = _obtener_parametro(db, anio, "FONDOS_RESERVA") or Decimal("8.33")
    sbu = _obtener_parametro(db, anio, "SBU") or Decimal("460.00")

    # 3. Calcular rubros
    rubros = (
        db.query(RubroNomina)
        .filter(RubroNomina.estado == "ACTIVO")
        .order_by(RubroNomina.orden_ejecucion)
        .all()
    )

    detalles = []
    total_ingresos = Decimal("0")
    total_descuentos = Decimal("0")
    total_provisiones = Decimal("0")
    base_imponible = sueldo_proporcional  # base para IESS y porcentajes

    # Acumular ingresos primero para calcular IR anual
    iess_personal = _redondear(base_imponible * porc_iess_personal / Decimal("100"))
    renta_imponible_anual = (base_imponible - iess_personal) * Decimal("12")
    # Restar deducciones cargas familiares (simplificado)
    cargas = [c for c in empleado.cargas if c.aplica_deduccion_ir and c.estado == "ACTIVO"]
    deduccion_cargas = Decimal(str(len(cargas))) * Decimal("2490.00") / Decimal("12")  # ~$207.50/mes aprox
    renta_imponible_anual = max(Decimal("0"), renta_imponible_anual - deduccion_cargas * Decimal("12"))
    ir_anual = _calcular_ir_anual(db, anio, renta_imponible_anual)
    ir_mensual = _redondear(ir_anual / Decimal("12"))

    for rubro in rubros:
        valor = Decimal("0")
        desc = ""

        codigo = rubro.codigo_rubro

        if codigo == "001":  # SUELDO BÁSICO
            valor = sueldo_proporcional
            desc = f"Sueldo pactado {sueldo_base} x {dias_trabajados}/30 días"

        elif codigo == "010":  # APORTE PERSONAL IESS
            valor = iess_personal
            desc = f"{base_imponible} x {porc_iess_personal}%"

        elif codigo == "020":  # APORTE PATRONAL IESS
            valor = _redondear(base_imponible * porc_iess_patronal / Decimal("100"))
            desc = f"{base_imponible} x {porc_iess_patronal}%"

        elif codigo == "030":  # FONDOS DE RESERVA
            if empleado.acumula_fondos_reserva:
                valor = _redondear(base_imponible * porc_fondos_reserva / Decimal("100"))
                desc = f"{base_imponible} x {porc_fondos_reserva}%"

        elif codigo == "040":  # DÉCIMO TERCERO
            if empleado.acumula_decimos:
                valor = _redondear(sueldo_proporcional / Decimal("12"))
                desc = f"{sueldo_proporcional} / 12 meses"

        elif codigo == "050":  # DÉCIMO CUARTO
            if empleado.acumula_decimos:
                valor = _redondear(sbu / Decimal("12"))
                desc = f"SBU {sbu} / 12 meses"

        elif codigo == "060":  # IMPUESTO A LA RENTA
            valor = ir_mensual
            desc = f"IR anual {ir_anual} / 12. Base imponible anual: {renta_imponible_anual}"

        else:
            # Rubros adicionales: por fórmula genérica o porcentaje
            # SGE-NOM-02: rubros FORMULA sin formula_calculo se omiten con advertencia
            if rubro.tipo_valor == "FORMULA" and not rubro.formula_calculo:
                desc = f"Rubro {rubro.codigo_rubro} pendiente de implementación (FORMULA sin definir)"
                # No calcular — omitir este rubro para no generar valor 0 silencioso
                continue
            elif rubro.tipo_valor == "PORCENTAJE" and rubro.formula_calculo:
                try:
                    pct = Decimal(rubro.formula_calculo)
                    valor = _redondear(base_imponible * pct / Decimal("100"))
                    desc = f"{base_imponible} x {pct}%"
                except Exception:
                    desc = "Error en fórmula"

        if valor == Decimal("0") and rubro.naturaleza != "INGRESO":
            continue  # Omitir rubros con valor 0 que no son ingresos

        detalles.append({
            "id_rubro": rubro.id_rubro,
            "codigo_rubro": rubro.codigo_rubro,
            "nombre_rubro": rubro.nombre,
            "naturaleza": rubro.naturaleza,
            "valor_calculado": valor,
            "descripcion_calculo": desc,
        })

        if rubro.naturaleza == "INGRESO":
            total_ingresos += valor
        elif rubro.naturaleza == "DESCUENTO":
            total_descuentos += valor
        elif rubro.naturaleza == "PROVISION":
            total_provisiones += valor

    liquido = _redondear(total_ingresos - total_descuentos)

    return {
        "sueldo_base": sueldo_base,
        "dias_trabajados": dias_trabajados,
        "total_ingresos": _redondear(total_ingresos),
        "total_descuentos": _redondear(total_descuentos),
        "total_provisiones": _redondear(total_provisiones),
        "liquido_a_recibir": liquido,
        "detalles": detalles,
    }


def generar_rol(
    db: Session,
    id_rol_pago: int,
    usuario_id: Optional[int] = None,
) -> RolPago:
    """
    Ejecuta el motor de cálculo para todos los empleados activos
    y actualiza las líneas del rol de pagos.
    Cambia estado: BORRADOR → CALCULADO.
    """
    rol = db.query(RolPago).filter(RolPago.id_rol_pago == id_rol_pago).first()
    if not rol:
        raise ValueError(f"Rol de pago {id_rol_pago} no encontrado")
    if rol.estado not in ("BORRADOR", "CALCULADO"):
        raise ValueError(f"El rol en estado {rol.estado} no puede re-calcularse")

    # Limpiar líneas previas
    for linea in rol.lineas:
        db.delete(linea)
    db.flush()

    # Obtener empleados activos
    empleados = (
        db.query(Empleado)
        .filter(
            Empleado.estado_empleado == "ACTIVO",
            Empleado.eliminado_en.is_(None),
        )
        .all()
    )

    for emp in empleados:
        resultado = calcular_linea_empleado(
            db=db,
            empleado=emp,
            anio=rol.periodo_anio,
            mes=rol.periodo_mes,
            tipo_rol=rol.tipo_rol,
        )
        if "error" in resultado:
            continue  # Saltar empleados sin contrato activo

        linea = LineaRolPago(
            id_rol_pago=rol.id_rol_pago,
            id_empleado=emp.id_empleado,
            sueldo_base=resultado["sueldo_base"],
            dias_trabajados=resultado["dias_trabajados"],
            total_ingresos=resultado["total_ingresos"],
            total_descuentos=resultado["total_descuentos"],
            total_provisiones=resultado["total_provisiones"],
            liquido_a_recibir=resultado["liquido_a_recibir"],
        )
        db.add(linea)
        db.flush()  # para obtener id_linea

        for det in resultado["detalles"]:
            detalle = DetalleLineaRol(
                id_linea=linea.id_linea,
                **det,
            )
            db.add(detalle)

    # SGE-NOM-01: validar que se generaron líneas — si no hay contratos activos,
    # el motor no puede calcular nómina real y debe rechazar la transición
    lineas_generadas = (
        db.query(LineaRolPago)
        .filter(LineaRolPago.id_rol_pago == id_rol_pago)
        .count()
    )
    if lineas_generadas == 0:
        db.rollback()
        raise ValueError(
            "No se encontraron empleados activos con contratos vigentes "
            f"para calcular la nómina {rol.tipo_rol} "
            f"{rol.periodo_anio}/{rol.periodo_mes:02d}. "
            "Verifique que existan empleados activos con contrato en estado ACTIVO."
        )

    rol.estado = "CALCULADO"
    db.commit()
    db.refresh(rol)
    return rol


def generar_archivo_spi(
    db: Session,
    rol: RolPago,
    ruc_empresa: str,
    cuenta_empresa: str,
) -> str:
    """
    Genera el contenido del archivo SPI (TXT pipe-delimited) para el BCE.
    Retorna el contenido como string para ser enviado como FileResponse.
    """
    if rol.estado not in ("APROBADO", "CERRADO"):
        raise ValueError("Solo se puede generar SPI de roles APROBADOS o CERRADOS")

    header = "RUC_EMPRESA|CTA_EMPRESA|RUC_BENEFICIARIO|NOMBRE_BENEFICIARIO|BANCO_DESTINO|CTA_DESTINO|TIPO_CUENTA|VALOR|REFERENCIA|DESCRIPCION"
    referencia = f"ROL{rol.periodo_anio}{rol.periodo_mes:02d}"
    desc = f"NOMINA {rol.tipo_rol} {rol.periodo_anio}/{rol.periodo_mes:02d}"

    filas = [header]
    for linea in rol.lineas:
        if linea.liquido_a_recibir <= 0 or not linea.cuenta_bancaria:
            continue
        emp = linea.empleado
        nombre = f"{emp.apellidos} {emp.nombres}".upper()
        fila = "|".join([
            ruc_empresa,
            cuenta_empresa,
            emp.identificacion,
            nombre,
            linea.banco_destino or "",
            linea.cuenta_bancaria,
            linea.tipo_cuenta or "CORRIENTE",
            str(linea.liquido_a_recibir),
            referencia,
            desc,
        ])
        filas.append(fila)

    return "\n".join(filas)
