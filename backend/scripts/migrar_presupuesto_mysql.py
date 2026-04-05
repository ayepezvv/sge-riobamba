#!/usr/bin/env python3
"""
Script ETL: Migración de datos presupuestarios MySQL → PostgreSQL SGE
Fuente: MySQL 192.168.1.26:3307 (cont_emapar_2023/2024/2025)
Destino: PostgreSQL SGE schema presupuesto (192.168.1.15)

Ciclo de migración por año:
  tratacion       → presupuesto.tipo_contratacion  (catálogo, una vez)
  tramites        → presupuesto.tramite
  certificaciones → presupuesto.certificados_presupuestarios
  ejecucio(T=2)   → presupuesto.reformas_presupuestarias
  ejecucio(T=3)   → presupuesto.compromisos + devengados
  liquidaciones   → presupuesto.liquidacion

Regla 1: schema presupuesto (prohibido public)
Regla 2: nomenclatura en español
Regla 3: idempotente — usa ON CONFLICT DO NOTHING con id_mysql_origen+anio_fiscal

YXP-54 — MYSQL-3
"""
import sys
import os
import logging
from datetime import date, datetime
from decimal import Decimal

import pymysql
import psycopg2
import psycopg2.extras

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
MYSQL_CONFIG = {
    "host": "192.168.1.26",
    "port": 3307,
    "user": "redemapar",
    "password": "redemapar1",
    "charset": "latin1",
    "cursorclass": pymysql.cursors.DictCursor,
    "connect_timeout": 10,
}

ANIOS = [2023, 2024, 2025]

# Leer DSN de PostgreSQL del entorno SGE
POSTGRES_DSN = os.environ.get(
    "DATABASE_URL",
    "postgresql://sge_user:sge_pass@localhost:5432/sge_db"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("etl-presupuesto")


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def safe_date(val):
    """Convierte datetime/date de MySQL a date de Python; maneja fechas 0000-00-00."""
    if val is None:
        return None
    if isinstance(val, datetime):
        if val.year == 0:
            return None
        return val.date()
    if isinstance(val, date):
        if val.year == 0:
            return None
        return val
    return None


def safe_str(val, max_len=None):
    """Decodifica bytes, limpia None, trunca si necesario."""
    if val is None:
        return None
    if isinstance(val, bytes):
        val = val.decode("latin1", errors="replace")
    val = str(val).strip()
    if not val:
        return None
    if max_len and len(val) > max_len:
        val = val[:max_len]
    return val


def safe_decimal(val):
    """Convierte a Decimal, retorna 0 si None."""
    if val is None:
        return Decimal("0")
    try:
        return Decimal(str(val))
    except Exception:
        return Decimal("0")


def safe_int(val):
    """Convierte a int, retorna None si falla."""
    if val is None:
        return None
    try:
        return int(float(val))
    except Exception:
        return None


def mysql_conn(database: str):
    cfg = {**MYSQL_CONFIG, "database": database}
    return pymysql.connect(**cfg)


def pg_conn():
    return psycopg2.connect(POSTGRES_DSN)


# ---------------------------------------------------------------------------
# Paso 1: Catálogo tipo_contratacion (idempotente por código)
# ---------------------------------------------------------------------------

def migrar_tipo_contratacion(pg, my_2023):
    log.info("=== tipo_contratacion ===")
    cur_my = my_2023.cursor()
    cur_my.execute("SELECT idtrata, nombre FROM tratacion ORDER BY idtrata")
    rows = cur_my.fetchall()

    cur_pg = pg.cursor()
    insertas = 0
    for r in rows:
        codigo = str(int(float(r["idtrata"])))
        nombre = safe_str(r["nombre"], 100) or f"Tipo {codigo}"
        cur_pg.execute("""
            INSERT INTO presupuesto.tipo_contratacion
                (codigo, nombre, id_mysql_origen)
            VALUES (%s, %s, %s)
            ON CONFLICT (codigo) DO NOTHING
        """, (codigo, nombre, safe_int(r["idtrata"])))
        if cur_pg.rowcount > 0:
            insertas += 1

    pg.commit()
    log.info(f"  tipo_contratacion: {insertas} insertados ({len(rows)} total MySQL)")


# ---------------------------------------------------------------------------
# Paso 2: Tramites por año
# ---------------------------------------------------------------------------

def migrar_tramites(pg, my, anio: int):
    log.info(f"=== tramites {anio} ===")
    cur_my = my.cursor()
    cur_my.execute("""
        SELECT t.INTTRAMI, t.NUMERO, t.FECHA, t.NUMOFI, t.FECOFI,
               t.DESCRI, t.TOTMISO, t.estado, t.IDTRATA, t.swarrastre,
               ci.NOMCIU, ci.RUCCIU,
               d.NOMDEP, t.INTDEP
        FROM tramites t
        LEFT JOIN ciu ci ON ci.INTCIU = t.INTCIU
        LEFT JOIN departamentos d ON d.INTDEP = t.INTDEP
        ORDER BY t.INTTRAMI
    """)
    rows = cur_my.fetchall()

    # Obtener id_tipo_contratacion por código
    cur_pg = pg.cursor()
    cur_pg.execute("SELECT codigo, id_tipo_contratacion FROM presupuesto.tipo_contratacion")
    tipo_map = {r[0]: r[1] for r in cur_pg.fetchall()}

    insertas = 0
    for r in rows:
        codigo_tipo = str(int(float(r["IDTRATA"]))) if r["IDTRATA"] else None
        id_tipo = tipo_map.get(codigo_tipo) if codigo_tipo else None

        cur_pg.execute("""
            INSERT INTO presupuesto.tramite (
                anio_fiscal, numero, fecha, numero_oficio, fecha_oficio,
                descripcion, valor_comprometido, estado,
                id_tipo_contratacion, ruc_proveedor, nombre_proveedor,
                codigo_departamento, nombre_departamento,
                es_arrastre, id_mysql_origen
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (anio_fiscal, id_mysql_origen) DO NOTHING
        """, (
            anio,
            safe_int(r["NUMERO"]) or 0,
            safe_date(r["FECHA"]),
            safe_str(r["NUMOFI"], 20),
            safe_date(r["FECOFI"]),
            safe_str(r["DESCRI"], 500),
            safe_decimal(r["TOTMISO"]),
            safe_int(r["estado"]) or 0,
            id_tipo,
            safe_str(r["RUCCIU"], 15),
            safe_str(r["NOMCIU"], 100),
            safe_int(r["INTDEP"]),
            safe_str(r["NOMDEP"], 100),
            bool(r["swarrastre"]),
            int(float(r["INTTRAMI"])),
        ))
        if cur_pg.rowcount > 0:
            insertas += 1

    pg.commit()
    log.info(f"  tramites {anio}: {insertas} insertados ({len(rows)} MySQL)")
    return insertas


# ---------------------------------------------------------------------------
# Paso 3: Certificaciones por año
# ---------------------------------------------------------------------------

def migrar_certificaciones(pg, my, anio: int):
    log.info(f"=== certificaciones {anio} ===")
    cur_my = my.cursor()

    # Cargar el mapa: INTPRE_mysql → id_asignacion_pg
    cur_pg = pg.cursor()
    cur_pg.execute("""
        SELECT p.id_partida, p.codigo as codpar, a.id_asignacion
        FROM presupuesto.partidas_presupuestarias p
        JOIN presupuesto.asignaciones_presupuestarias a ON a.id_partida = p.id_partida
        JOIN presupuesto.presupuestos_anuales pa ON pa.id_presupuesto = a.id_presupuesto
        WHERE pa.anio_fiscal = %s
    """, (anio,))
    asig_por_codpar = {r[1]: r[2] for r in cur_pg.fetchall()}

    # Mapa INTPRE_mysql → CODPAR (para buscar asignacion)
    cur_my.execute("SELECT INTPRE, CODPAR FROM presupue")
    intpre_a_codpar = {
        int(float(r["INTPRE"])): safe_str(r["CODPAR"], 40)
        for r in cur_my.fetchall()
        if r["INTPRE"]
    }

    # Cargar certificaciones con la primera partida de partixcerti
    cur_my.execute("""
        SELECT c.IDCERTI, c.NUMERO, c.FECHA, c.VALOR, c.SALDO,
               c.EJECUTADA, c.DESCRIPCION, c.tipocerti, c.tipo,
               c.INTPRE as intpre_directo,
               ci.NOMCIU, ci.RUCCIU,
               pc.intpre as intpre_partixcerti, pc.valor as valor_partida
        FROM certificaciones c
        LEFT JOIN ciu ci ON ci.INTCIU = c.INTCIU
        LEFT JOIN (
            SELECT idcerti, intpre, valor
            FROM partixcerti
            WHERE idparxcer IN (
                SELECT MIN(idparxcer) FROM partixcerti GROUP BY idcerti
            )
        ) pc ON pc.idcerti = c.IDCERTI
        ORDER BY c.IDCERTI
    """)
    rows = cur_my.fetchall()

    insertas = 0
    sin_asignacion = 0
    for r in rows:
        # Buscar id_asignacion: primero por intpre_directo, luego por partixcerti
        id_asig = None
        for intpre_val in [r["intpre_directo"], r["intpre_partixcerti"]]:
            if intpre_val and int(float(intpre_val)) > 0:
                codpar = intpre_a_codpar.get(int(float(intpre_val)))
                if codpar:
                    id_asig = asig_por_codpar.get(codpar)
                    if id_asig:
                        break

        if id_asig is None:
            sin_asignacion += 1

        numero = safe_int(r["NUMERO"]) or 0
        numero_cert = f"CERT-{anio}-{numero:05d}"

        cur_pg.execute("""
            INSERT INTO presupuesto.certificados_presupuestarios (
                numero_certificado, id_asignacion,
                monto_certificado, concepto,
                fecha_solicitud, fecha_certificacion,
                estado,
                id_mysql_origen, anio_fiscal,
                tipo_mysql, tipo_certi, numero_mysql,
                ruc_proveedor, nombre_proveedor
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (numero_certificado) DO NOTHING
        """, (
            numero_cert,
            id_asig,
            safe_decimal(r["VALOR"]),
            safe_str(r["DESCRIPCION"], 2000) or "Sin descripción",
            safe_date(r["FECHA"]) or date(anio, 1, 1),
            safe_date(r["FECHA"]),
            "COMPROMETIDO" if r["EJECUTADA"] and int(float(r["EJECUTADA"])) > 0 else "APROBADO",
            int(float(r["IDCERTI"])),
            anio,
            safe_int(r["tipo"]),
            safe_str(r["tipocerti"], 30),
            safe_int(r["NUMERO"]),
            safe_str(r["RUCCIU"], 15),
            safe_str(r["NOMCIU"], 100),
        ))
        if cur_pg.rowcount > 0:
            insertas += 1

    pg.commit()
    log.info(f"  certificaciones {anio}: {insertas} insertados ({len(rows)} MySQL, {sin_asignacion} sin asignacion)")
    return insertas


# ---------------------------------------------------------------------------
# Paso 4: Reformas presupuestarias (ejecucio TIPEJE=2)
# ---------------------------------------------------------------------------

def migrar_reformas(pg, my, anio: int):
    log.info(f"=== reformas {anio} (ejecucio TIPEJE=2) ===")
    cur_my = my.cursor()
    cur_my.execute("""
        SELECT e.INTEJE, e.INTPRE, e.FECHA_EJE, e.MODIFI, e.CONCEP,
               rf.numero, rf.descri as descri_reforma
        FROM ejecucio e
        LEFT JOIN reformas rf ON rf.idrefo = e.INTEJE
        WHERE e.TIPEJE = 2
        ORDER BY e.INTEJE
    """)
    rows = cur_my.fetchall()

    # Mapa INTPRE_mysql → id_asignacion_pg
    cur_pg = pg.cursor()
    cur_pg.execute("""
        SELECT p.codigo, a.id_asignacion
        FROM presupuesto.partidas_presupuestarias p
        JOIN presupuesto.asignaciones_presupuestarias a ON a.id_partida = p.id_partida
        JOIN presupuesto.presupuestos_anuales pa ON pa.id_presupuesto = a.id_presupuesto
        WHERE pa.anio_fiscal = %s
    """, (anio,))
    asig_por_codpar = {r[0]: r[1] for r in cur_pg.fetchall()}

    cur_my2 = my.cursor()
    cur_my2.execute("SELECT INTPRE, CODPAR FROM presupue")
    intpre_a_codpar = {
        int(float(r["INTPRE"])): safe_str(r["CODPAR"], 40)
        for r in cur_my2.fetchall()
        if r["INTPRE"]
    }

    insertas = 0
    sin_asignacion = 0
    for r in rows:
        intpre = int(float(r["INTPRE"])) if r["INTPRE"] else 0
        codpar = intpre_a_codpar.get(intpre)
        id_asig = asig_por_codpar.get(codpar) if codpar else None

        if id_asig is None:
            sin_asignacion += 1
            continue  # sin asignacion no se puede insertar (FK not null)

        monto = safe_decimal(r["MODIFI"])
        tipo = "REDUCCION" if monto < 0 else "SUPLEMENTO"

        cur_pg.execute("""
            INSERT INTO presupuesto.reformas_presupuestarias (
                id_asignacion, tipo_reforma, monto,
                numero_resolucion, fecha_resolucion, motivo,
                estado, id_mysql_origen, anio_fiscal,
                numero_reforma_mysql
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (anio_fiscal, id_mysql_origen) DO NOTHING
        """, (
            id_asig,
            tipo,
            monto,
            f"MYSQL-{anio}-{safe_int(r['INTEJE'])}",
            safe_date(r["FECHA_EJE"]) or date(anio, 1, 1),
            safe_str(r["CONCEP"], 1000),
            "APROBADO",
            int(float(r["INTEJE"])),
            anio,
            safe_int(r["numero"]),
        ))
        if cur_pg.rowcount > 0:
            insertas += 1

    pg.commit()
    log.info(f"  reformas {anio}: {insertas} insertados ({len(rows)} MySQL, {sin_asignacion} sin asignacion)")
    return insertas


# ---------------------------------------------------------------------------
# Paso 5: Compromisos y Devengados (ejecucio TIPEJE=3)
# ---------------------------------------------------------------------------

def migrar_compromisos_devengados(pg, my, anio: int):
    log.info(f"=== compromisos+devengados {anio} (ejecucio TIPEJE=3) ===")
    cur_my = my.cursor()
    cur_my.execute("""
        SELECT INTEJE, INTPRE, INTTRAMI, FECHA_EJE,
               PRMISO, DEVENGADO, LIQUIDACION, SALDOMISOS,
               numcerti, CONCEP, SINCERTI
        FROM ejecucio
        WHERE TIPEJE = 3
        ORDER BY INTEJE
    """)
    rows = cur_my.fetchall()

    cur_pg = pg.cursor()

    # Mapa certificacion mysql → id_certificado_pg
    cur_pg.execute("""
        SELECT numero_mysql, anio_fiscal, id_certificado
        FROM presupuesto.certificados_presupuestarios
        WHERE anio_fiscal = %s AND numero_mysql IS NOT NULL
    """, (anio,))
    certi_map = {int(r[0]): r[2] for r in cur_pg.fetchall() if r[0]}

    # Mapa tramite mysql → id_tramite_pg
    cur_pg.execute("""
        SELECT id_mysql_origen, id_tramite
        FROM presupuesto.tramite
        WHERE anio_fiscal = %s
    """, (anio,))
    tramite_map = {r[0]: r[1] for r in cur_pg.fetchall()}

    compromisos = 0
    devengados = 0
    sin_certi = 0

    for r in rows:
        inteje = int(float(r["INTEJE"]))
        monto_comp = safe_decimal(r["PRMISO"])
        monto_dev = safe_decimal(r["DEVENGADO"])
        monto_liq = safe_decimal(r["LIQUIDACION"])
        numcerti = safe_int(r["numcerti"])
        inttrami = safe_int(r["INTTRAMI"]) if r["INTTRAMI"] else None

        # Buscar certificado padre
        id_cert = certi_map.get(numcerti) if numcerti else None
        if id_cert is None:
            sin_certi += 1

        id_tramite = tramite_map.get(inttrami) if inttrami else None

        numero_comp = f"COMP-{anio}-{inteje:07d}"

        cur_pg.execute("""
            INSERT INTO presupuesto.compromisos (
                id_certificado, numero_compromiso,
                monto_comprometido, concepto,
                fecha_compromiso, estado,
                id_tramite, id_mysql_origen, anio_fiscal,
                numero_certi_mysql, monto_devengado_mysql, monto_liquidado_mysql
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (anio_fiscal, id_mysql_origen) DO NOTHING
            RETURNING id_compromiso
        """, (
            id_cert,
            numero_comp,
            monto_comp,
            safe_str(r["CONCEP"], 2000) or "Sin concepto",
            safe_date(r["FECHA_EJE"]) or date(anio, 1, 1),
            "DEVENGADO" if monto_dev and monto_dev > 0 else "ACTIVO",
            id_tramite,
            inteje,
            anio,
            numcerti,
            monto_dev,
            monto_liq,
        ))
        row_comp = cur_pg.fetchone()
        if row_comp:
            compromisos += 1
            id_comp = row_comp[0]

            # Crear devengado si hay monto
            if monto_dev and monto_dev > 0:
                numero_dev = f"DEV-{anio}-{inteje:07d}"
                cur_pg.execute("""
                    INSERT INTO presupuesto.devengados (
                        id_compromiso, numero_devengado,
                        monto_devengado, concepto,
                        fecha_devengado, estado,
                        id_mysql_origen, anio_fiscal
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (anio_fiscal, id_mysql_origen) DO NOTHING
                """, (
                    id_comp,
                    numero_dev,
                    monto_dev,
                    safe_str(r["CONCEP"], 2000) or "Sin concepto",
                    safe_date(r["FECHA_EJE"]) or date(anio, 1, 1),
                    "PAGADO" if monto_liq and monto_liq > 0 else "REGISTRADO",
                    inteje,
                    anio,
                ))
                if cur_pg.rowcount > 0:
                    devengados += 1

    pg.commit()
    log.info(f"  compromisos {anio}: {compromisos} ({len(rows)} MySQL, {sin_certi} sin cert)")
    log.info(f"  devengados  {anio}: {devengados}")
    return compromisos, devengados


# ---------------------------------------------------------------------------
# Paso 6: Liquidaciones
# ---------------------------------------------------------------------------

def migrar_liquidaciones(pg, my, anio: int):
    log.info(f"=== liquidaciones {anio} ===")
    cur_my = my.cursor()
    cur_my.execute("""
        SELECT idliquida, inteje, intpre, fecha, valor, saldo,
               comprobante, observa, cuentaso, numliqui
        FROM liquidaciones
        ORDER BY idliquida
    """)
    rows = cur_my.fetchall()

    cur_pg = pg.cursor()

    # Mapa INTEJE_mysql → id_compromiso_pg
    cur_pg.execute("""
        SELECT id_mysql_origen, id_compromiso
        FROM presupuesto.compromisos
        WHERE anio_fiscal = %s AND id_mysql_origen IS NOT NULL
    """, (anio,))
    comp_map = {r[0]: r[1] for r in cur_pg.fetchall()}

    insertas = 0
    sin_compromiso = 0

    for r in rows:
        inteje = safe_int(r["inteje"])
        id_comp = comp_map.get(inteje) if inteje else None

        if id_comp is None:
            sin_compromiso += 1
            continue

        cur_pg.execute("""
            INSERT INTO presupuesto.liquidacion (
                anio_fiscal, id_compromiso, fecha, valor, saldo,
                numero_comprobante, observaciones, cuenta_contable,
                numero_liquidacion, id_mysql_origen
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (anio_fiscal, id_mysql_origen) DO NOTHING
        """, (
            anio,
            id_comp,
            safe_date(r["fecha"]) or date(anio, 1, 1),
            safe_decimal(r["valor"]),
            safe_decimal(r["saldo"]),
            safe_str(r["comprobante"], 20),
            safe_str(r["observa"], 500),
            safe_str(r["cuentaso"], 40),
            safe_int(r["numliqui"]),
            int(float(r["idliquida"])),
        ))
        if cur_pg.rowcount > 0:
            insertas += 1

    pg.commit()
    log.info(f"  liquidaciones {anio}: {insertas} insertados ({len(rows)} MySQL, {sin_compromiso} sin compromiso)")
    return insertas


# ---------------------------------------------------------------------------
# Validación final
# ---------------------------------------------------------------------------

def validar(pg, my, anio: int):
    log.info(f"=== VALIDACIÓN {anio} ===")
    cur_my = my.cursor()
    cur_pg = pg.cursor()

    checks = [
        ("presupue",        "presupuesto.asignaciones_presupuestarias", "anio_fiscal=%s", "WHERE TIPPAR=2"),
        ("certificaciones", "presupuesto.certificados_presupuestarios",  "anio_fiscal=%s", None),
        ("ejecucio(T=3)",   "presupuesto.compromisos",                   "anio_fiscal=%s", "WHERE TIPEJE=3"),
        ("liquidaciones",   "presupuesto.liquidacion",                   "anio_fiscal=%s", None),
    ]

    mysql_tables = ["presupue WHERE TIPPAR=2", "certificaciones",
                    "ejecucio WHERE TIPEJE=3", "liquidaciones"]
    pg_tables = [
        f"presupuesto.asignaciones_presupuestarias WHERE id_presupuesto=(SELECT id_presupuesto FROM presupuesto.presupuestos_anuales WHERE anio_fiscal={anio})",
        f"presupuesto.certificados_presupuestarios WHERE anio_fiscal={anio}",
        f"presupuesto.compromisos WHERE anio_fiscal={anio}",
        f"presupuesto.liquidacion WHERE anio_fiscal={anio}",
    ]
    labels = ["Partidas", "Certificaciones", "Compromisos", "Liquidaciones"]

    for lbl, my_tbl, pg_tbl in zip(labels, mysql_tables, pg_tables):
        cur_my.execute(f"SELECT COUNT(*) as n FROM {my_tbl}")
        n_my = cur_my.fetchone()["n"]
        cur_pg.execute(f"SELECT COUNT(*) FROM {pg_tbl}")
        n_pg = cur_pg.fetchone()[0]
        ok = "OK" if n_pg >= n_my * 0.95 else "WARN"  # 95% tolerancia
        log.info(f"  [{ok}] {lbl}: MySQL={n_my:,} PG={n_pg:,}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    log.info("Iniciando ETL presupuesto MySQL → PostgreSQL")
    log.info(f"PostgreSQL DSN: {POSTGRES_DSN[:40]}...")

    pg = pg_conn()
    pg.autocommit = False

    # Año 2023 para catálogo global
    my_2023 = mysql_conn("cont_emapar_2023")

    # Paso 1: catálogo tipo_contratacion (una sola vez)
    migrar_tipo_contratacion(pg, my_2023)

    totales = {}
    for anio in ANIOS:
        db_name = f"cont_emapar_{anio}"
        log.info(f"\n{'='*50}")
        log.info(f"  PROCESANDO AÑO {anio} — base {db_name}")
        log.info(f"{'='*50}")

        my = mysql_conn(db_name)

        n_tramites    = migrar_tramites(pg, my, anio)
        n_certis      = migrar_certificaciones(pg, my, anio)
        n_reformas    = migrar_reformas(pg, my, anio)
        n_comp, n_dev = migrar_compromisos_devengados(pg, my, anio)
        n_liqui       = migrar_liquidaciones(pg, my, anio)

        totales[anio] = {
            "tramites":       n_tramites,
            "certificaciones": n_certis,
            "reformas":        n_reformas,
            "compromisos":     n_comp,
            "devengados":      n_dev,
            "liquidaciones":   n_liqui,
        }

        validar(pg, my, anio)
        my.close()

    my_2023.close()
    pg.close()

    log.info("\n=== RESUMEN FINAL ===")
    for anio, t in totales.items():
        log.info(f"  {anio}: tramites={t['tramites']} certis={t['certificaciones']} "
                 f"reformas={t['reformas']} compr={t['compromisos']} "
                 f"dev={t['devengados']} liqui={t['liquidaciones']}")

    log.info("ETL completado exitosamente")


if __name__ == "__main__":
    main()
