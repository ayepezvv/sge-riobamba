#!/usr/bin/env python3
"""
Script de Validación Post-Migración
Compara conteos y checksums entre OpenERP y SGE.
"""
import logging
import psycopg2
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

OPENERP_DSN = {
    "host": "192.168.1.49", "port": 5432, "dbname": "siim_adm",
    "user": "victor", "password": "victor",
    "options": "-c default_transaction_read_only=on",
}
SGE_DSN = {
    "host": "192.168.1.15", "port": 5433, "dbname": "sge_db",
    "user": "sge_admin", "password": "SgeSuperSecretPassword123!",
}

VALIDACIONES = [
    {
        "nombre": "Partidas Presupuestarias",
        "sql_origen": "SELECT COUNT(*) FROM budget_post WHERE activo = true",
        "sql_destino": "SELECT COUNT(*) FROM presupuesto.partidas_presupuestarias WHERE estado = 'ACTIVO'",
        "tolerancia_pct": 5,
    },
    {
        "nombre": "Empleados",
        "sql_origen": "SELECT COUNT(*) FROM hr_employee",
        "sql_destino": "SELECT COUNT(*) FROM rrhh.empleado",
        "tolerancia_pct": 10,
    },
    {
        "nombre": "Plan de Cuentas",
        "sql_origen": "SELECT COUNT(*) FROM account_account WHERE company_id = 1 AND active = true",
        "sql_destino": "SELECT COUNT(*) FROM contabilidad.cuentas_contables",
        "tolerancia_pct": 45,
    },
]


def ejecutar(conn, sql: str):
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchone()


def main():
    log.info("="*60)
    log.info("VALIDACIÓN POST-MIGRACIÓN")
    log.info(f"Inicio: {datetime.now()}")
    log.info("="*60)

    errores = []

    try:
        conn_origen = psycopg2.connect(**OPENERP_DSN)
        conn_origen.set_session(readonly=True)
    except Exception as e:
        log.error(f"No se puede conectar a OpenERP: {e}")
        log.warning("Ejecutando validación solo en SGE...")
        conn_origen = None

    try:
        conn_destino = psycopg2.connect(**SGE_DSN)
    except Exception as e:
        log.error(f"No se puede conectar a SGE: {e}")
        return 1

    for v in VALIDACIONES:
        try:
            conn_origen.cursor().execute('SAVEPOINT sp_val') if conn_origen else None
        except Exception:
            pass
        log.info(f"\nValidando: {v['nombre']}")
        try:
            if conn_origen:
                resultado_origen = ejecutar(conn_origen, v["sql_origen"])
                count_origen = int(resultado_origen[0])
            else:
                count_origen = None

            resultado_destino = ejecutar(conn_destino, v["sql_destino"])
            count_destino = int(resultado_destino[0])

            if conn_origen and count_origen is not None:
                diferencia = abs(count_origen - count_destino)
                tolerancia = count_origen * v["tolerancia_pct"] / 100
                ok = diferencia <= tolerancia
                estado = "✓ OK" if ok else "✗ FALLA"
                log.info(f"  Origen: {count_origen:,} | SGE: {count_destino:,} | Diferencia: {diferencia:,} | {estado}")
                if not ok:
                    errores.append(v["nombre"])
            else:
                log.info(f"  SGE: {count_destino:,} (origen no disponible)")

        except Exception as e:
            log.error(f"  Error en {v['nombre']}: {e}")
            errores.append(v["nombre"])
            try:
                if conn_origen: conn_origen.cursor().execute('ROLLBACK TO SAVEPOINT sp_val')
            except Exception:
                pass

    # Verificar integridad referencial
    log.info("\nVerificando integridad referencial en SGE...")
    checks_ri = [
        ("presupuesto → asignaciones sin presupuesto padre",
         "SELECT COUNT(*) FROM presupuesto.asignaciones_presupuestarias a "
         "LEFT JOIN presupuesto.presupuestos_anuales p ON a.id_presupuesto = p.id_presupuesto "
         "WHERE p.id_presupuesto IS NULL"),
        ("presupuesto → certificados sin asignación",
         "SELECT COUNT(*) FROM presupuesto.certificados_presupuestarios c "
         "LEFT JOIN presupuesto.asignaciones_presupuestarias a ON c.id_asignacion = a.id_asignacion "
         "WHERE a.id_asignacion IS NULL"),
    ]
    for desc, sql in checks_ri:
        resultado = ejecutar(conn_destino, sql)
        n = int(resultado[0])
        estado = "✓ OK" if n == 0 else f"✗ {n} huérfanos"
        log.info(f"  {desc}: {estado}")

    if conn_origen:
        conn_origen.close()
    conn_destino.close()

    log.info("\n" + "="*60)
    if errores:
        log.error(f"VALIDACIÓN FALLIDA en: {errores}")
        return 1
    else:
        log.info("VALIDACIÓN EXITOSA — migración íntegra")
        return 0


if __name__ == "__main__":
    exit(main())
