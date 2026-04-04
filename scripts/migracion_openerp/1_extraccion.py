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
    "user": "victor",
    "password": "victor",
    "connect_timeout": 10,
    "options": "-c default_transaction_read_only=on",  # garantía de solo lectura
}
OUTPUT_DIR = Path("/tmp/migracion")

# Consultas de extracción OpenERP (corregidas según esquema real)
CONSULTAS = {
    # ----------------------------------------------------------------
    # PRESUPUESTO: Partidas presupuestarias (budget_post)
    # ----------------------------------------------------------------
    "partidas_presupuestarias": """
        SELECT
            bp.id                           AS id_openerp,
            COALESCE(bp.name, '')           AS nombre,
            COALESCE(bp.code, '')           AS codigo,
            COALESCE(bp.tipo, 'GASTO')      AS tipo,
            COALESCE(bp.activo, true)       AS activo,
            bp.parent_id                    AS id_padre_openerp,
            bp.nivel                        AS nivel
        FROM budget_post bp
        ORDER BY bp.code
    """,

    # ----------------------------------------------------------------
    # PRESUPUESTO: Certificados presupuestarios (budget_certificate)
    # Columnas reales: id, number, amount_certified, state, date_confirmed, notes
    # ----------------------------------------------------------------
    "certificados_presupuestarios": """
        SELECT
            bc.id                           AS id_openerp,
            COALESCE(bc.number, bc.name)    AS numero_certificado,
            bc.create_date::date            AS fecha_solicitud,
            bc.date_confirmed               AS fecha_confirmacion,
            bc.state                        AS estado_openerp,
            COALESCE(bc.amount_certified, 0) AS monto_certificado,
            bc.notes                        AS concepto
        FROM budget_certificate bc
        WHERE bc.state != 'cancel'
        ORDER BY bc.create_date, bc.id
    """,

    # ----------------------------------------------------------------
    # RRHH: Empleados (hr_employee)
    # Columnas reales: sin campo active, usa state_system
    # ----------------------------------------------------------------
    "empleados": """
        SELECT
            he.id                               AS id_openerp,
            COALESCE(he.name, '')               AS identificacion,
            COALESCE(he.complete_name, he.employee_first_name, '') AS nombres_completos,
            he.birthday                         AS fecha_nacimiento,
            COALESCE(he.gender, '')             AS genero,
            COALESCE(he.state_system, false)    AS estado_sistema,
            COALESCE(he.mobile_phone, '')       AS telefono_celular,
            COALESCE(he.work_email, '')         AS correo_trabajo,
            COALESCE(he.email, '')              AS correo_personal,
            he.department_id                    AS id_area,
            COALESCE(he.employee_first_name, '')        AS primer_nombre,
            COALESCE(he.employee_second_name, '')       AS segundo_nombre,
            COALESCE(he.employee_first_lastname, '')    AS primer_apellido,
            COALESCE(he.employee_second_lastname, '')   AS segundo_apellido
        FROM hr_employee he
        ORDER BY he.name
    """,

    # ----------------------------------------------------------------
    # RRHH: Contratos históricos (hr_contract)
    # ----------------------------------------------------------------
    "contratos": """
        SELECT
            hc.id                           AS id_openerp,
            hc.employee_id                  AS id_empleado_openerp,
            hc.name                         AS nombre_contrato,
            hc.date_start                   AS fecha_inicio,
            hc.date_end                     AS fecha_fin,
            COALESCE(hc.wage, 0)            AS sueldo_pactado,
            hc.state                        AS estado_openerp,
            hc.type_id                      AS tipo_contrato_id
        FROM hr_contract hc
        ORDER BY hc.employee_id, hc.date_start
    """,

    # ----------------------------------------------------------------
    # CONTABILIDAD: Plan de cuentas (account_account)
    # level es columna real, no función
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
            aa.level                        AS nivel
        FROM account_account aa
        WHERE aa.company_id = 1
        ORDER BY aa.code
    """,

    # ----------------------------------------------------------------
    # CONTABILIDAD: Asientos contables (account_move + account_move_line)
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


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    log.info("=" * 60)
    log.info("EXTRACCIÓN OpenERP → %s", OUTPUT_DIR)
    log.info("Inicio: %s", datetime.now())
    log.info("=" * 60)

    try:
        conn = psycopg2.connect(**OPENERP_DSN)
        conn.set_session(readonly=True)
        log.info("Conectado a OpenERP (%s)", OPENERP_DSN["host"])
    except Exception as e:
        log.error("Error conectando a OpenERP: %s", e)
        log.error("Verifique que %s sea accesible y las credenciales sean correctas.", OPENERP_DSN["host"])
        return 1

    resumen = {}
    errores = []

    for nombre, query in CONSULTAS.items():
        log.info("Extrayendo %s...", nombre)
        try:
            cur = conn.cursor()
            cur.execute('SAVEPOINT sp_extract')
            cur.execute(query)
            filas = cur.fetchall()
            cols = [desc[0] for desc in cur.description]
            archivo = OUTPUT_DIR / f"{nombre}.csv"
            with open(archivo, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(cols)
                writer.writerows(filas)
            resumen[nombre] = len(filas)
            log.info("  → %s registros → %s", f"{len(filas):,}", archivo)
        except Exception as e:
            log.error("  ERROR en %s: %s", nombre, e)
            errores.append(nombre)
            try:
                conn.cursor().execute('ROLLBACK TO SAVEPOINT sp_extract')
            except Exception:
                pass

    conn.close()

    log.info("")
    log.info("=" * 60)
    log.info("RESUMEN DE EXTRACCIÓN")
    log.info("=" * 60)
    for k, v in resumen.items():
        log.info("  %-42s %s registros", k, f"{v:,}")

    if errores:
        log.warning("\nErrores en: %s", errores)
        return 1

    log.info("\nExtracción completada sin errores.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
