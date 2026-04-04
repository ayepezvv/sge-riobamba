#!/usr/bin/env python3
"""
Script de Extracción — OpenERP → archivos intermedios
Origen: PostgreSQL 192.168.1.49 (SOLO LECTURA)
Destino: /tmp/migracion/*.csv

IMPORTANTE: Este script nunca escribe en OpenERP.
            Requiere solo SELECT en siim_adm.
"""
import os
import csv
import logging
import psycopg2
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# ============================================================
# CONFIGURACIÓN
# ============================================================
OPENERP_DSN = {
    "host": "192.168.1.49",
    "port": 5432,
    "dbname": "siim_adm",
    "user": "openerp",
    "password": "openerp",
    "connect_timeout": 10,
    "options": "-c default_transaction_read_only=on",  # garantía de solo lectura
}
OUTPUT_DIR = Path("/tmp/migracion")

# Consultas de extracción OpenERP
CONSULTAS = {
    # ----------------------------------------------------------------
    # PRESUPUESTO: Partidas presupuestarias (account.budget.post)
    # ----------------------------------------------------------------
    "partidas_presupuestarias": """
        SELECT
            abp.id                          AS id_openerp,
            abp.name                        AS nombre,
            abp.code                        AS codigo,
            abp.type                        AS tipo,
            abp.active                      AS activo,
            abp.parent_id                   AS id_padre_openerp
        FROM account_budget_post abp
        ORDER BY abp.code
    """,

    # ----------------------------------------------------------------
    # PRESUPUESTO: Certificados presupuestarios (budget.certificate)
    # ----------------------------------------------------------------
    "certificados_presupuestarios": """
        SELECT
            bc.id                           AS id_openerp,
            bc.name                         AS numero_certificado,
            bc.date_from                    AS fecha_solicitud,
            bc.date_to                      AS fecha_vencimiento,
            bc.state                        AS estado_openerp,
            bc.planned_amount               AS monto_certificado,
            bc.general_budget_id            AS id_partida_openerp,
            bc.description                  AS concepto
        FROM budget_certificate bc
        WHERE bc.state != 'cancel'
        ORDER BY bc.date_from, bc.id
    """,

    # ----------------------------------------------------------------
    # RRHH: Empleados (hr.employee)
    # ----------------------------------------------------------------
    "empleados": """
        SELECT
            he.id                           AS id_openerp,
            he.identification_id            AS identificacion,
            he.name                         AS nombres_completos,
            he.birthday                     AS fecha_nacimiento,
            he.gender                       AS genero,
            he.active                       AS activo,
            he.mobile_phone                 AS telefono_celular,
            he.work_email                   AS correo_personal,
            he.address_home_id              AS id_direccion,
            he.contract_id                  AS id_contrato_activo,
            he.job_id                       AS id_cargo,
            he.department_id                AS id_area
        FROM hr_employee he
        WHERE he.active = true
        ORDER BY he.identification_id
    """,

    # ----------------------------------------------------------------
    # RRHH: Contratos históricos (hr.contract)
    # ----------------------------------------------------------------
    "contratos": """
        SELECT
            hc.id                           AS id_openerp,
            hc.employee_id                  AS id_empleado_openerp,
            hc.name                         AS nombre_contrato,
            hc.date_start                   AS fecha_inicio,
            hc.date_end                     AS fecha_fin,
            hc.wage                         AS sueldo_pactado,
            hc.state                        AS estado_openerp,
            hc.type_id                      AS tipo_contrato_id
        FROM hr_contract hc
        ORDER BY hc.employee_id, hc.date_start
    """,

    # ----------------------------------------------------------------
    # CONTABILIDAD: Plan de cuentas (account.account)
    # ----------------------------------------------------------------
    "cuentas_contables": """
        SELECT
            aa.id                           AS id_openerp,
            aa.code                         AS codigo,
            aa.name                         AS nombre,
            aa.type                         AS tipo,
            aa.user_type                    AS tipo_usuario,
            aa.parent_id                    AS id_padre_openerp,
            aa.active                       AS activo,
            aa.reconcile                    AS permite_conciliacion,
            level(aa.parent_left, aa.parent_right) AS nivel
        FROM account_account aa
        WHERE aa.company_id = 1
        ORDER BY aa.code
    """,

    # ----------------------------------------------------------------
    # CONTABILIDAD: Asientos contables (account.move)
    # ----------------------------------------------------------------
    "asientos_contables": """
        SELECT
            am.id                           AS id_openerp,
            am.name                         AS numero_asiento,
            am.ref                          AS referencia,
            am.date                         AS fecha,
            am.state                        AS estado,
            am.journal_id                   AS id_diario,
            am.period_id                    AS id_periodo,
            aml.account_id                  AS id_cuenta,
            aml.name                        AS concepto_linea,
            aml.debit                       AS debe,
            aml.credit                      AS haber,
            aml.partner_id                  AS id_tercero
        FROM account_move am
        JOIN account_move_line aml ON aml.move_id = am.id
        WHERE am.state = 'posted'
          AND am.date >= '2015-01-01'
        ORDER BY am.date, am.id
        LIMIT 100000
    """,
}


def extraer(consulta_nombre: str, sql: str, conn) -> int:
    """Ejecuta una consulta y guarda el resultado en CSV."""
    output_file = OUTPUT_DIR / f"{consulta_nombre}.csv"
    log.info(f"Extrayendo {consulta_nombre}...")

    with conn.cursor() as cur:
        cur.execute(sql)
        columnas = [desc[0] for desc in cur.description]
        filas = cur.fetchall()

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columnas)
        writer.writerows(filas)

    log.info(f"  → {len(filas):,} registros → {output_file}")
    return len(filas)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    log.info("="*60)
    log.info(f"EXTRACCIÓN OpenERP → {OUTPUT_DIR}")
    log.info(f"Inicio: {datetime.now()}")
    log.info("="*60)

    try:
        conn = psycopg2.connect(**OPENERP_DSN)
        conn.set_session(readonly=True, autocommit=True)
    except Exception as e:
        log.error(f"Error conectando a OpenERP: {e}")
        log.error("Verifique que 192.168.1.49 sea accesible y las credenciales sean correctas.")
        return 1

    totales = {}
    errores = []

    for nombre, sql in CONSULTAS.items():
        try:
            n = extraer(nombre, sql, conn)
            totales[nombre] = n
        except Exception as e:
            log.error(f"  ERROR en {nombre}: {e}")
            errores.append(nombre)

    conn.close()

    log.info("\n" + "="*60)
    log.info("RESUMEN DE EXTRACCIÓN")
    log.info("="*60)
    for nombre, total in totales.items():
        log.info(f"  {nombre:<40} {total:>10,} registros")

    if errores:
        log.warning(f"\nErrores en: {errores}")
        return 1

    log.info(f"\nExtracción completada: {datetime.now()}")
    return 0


if __name__ == "__main__":
    exit(main())
