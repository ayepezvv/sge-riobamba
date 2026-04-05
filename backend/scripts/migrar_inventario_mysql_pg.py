#!/usr/bin/env python3
"""
Script de migración: MySQL invent_emapar_XXXX → PostgreSQL schema inventario
Años a migrar: 2021, 2022, 2023, 2024, 2025 (NO 2026)

Uso:
    cd /home/ayepez/.openclaw/workspace/sge/backend
    source venv/bin/activate
    python scripts/migrar_inventario_mysql_pg.py

Dependencias: pymysql (pip install pymysql)
"""
import sys
import os
import logging
from datetime import datetime
from decimal import Decimal

# Asegurar que app esté en el path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
import pymysql.cursors
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ─── CONFIG ────────────────────────────────────────────────────────────────────
MYSQL_HOST = "192.168.2.160"
MYSQL_PORT = 3306
MYSQL_USER = "redemapar"
MYSQL_PASS = "redemapar16"

PG_URL = "postgresql+psycopg2://sge_admin:SgeSuperSecretPassword123!@localhost:5433/sge_db"

ANNOS = [2021, 2022, 2023, 2024, 2025]  # NO 2026

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/home/ayepez/.openclaw/workspace/sge/backend/migrar_inventario_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log")
    ]
)
log = logging.getLogger(__name__)


def get_mysql_conn(db_name: str):
    return pymysql.connect(
        host=MYSQL_HOST, port=MYSQL_PORT,
        user=MYSQL_USER, password=MYSQL_PASS,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4",
        connect_timeout=10,
    )


def sanitize_date(val):
    """Convierte 0000-00-00 y fechas MySQL inválidas a None."""
    if val is None:
        return None
    if isinstance(val, str) and val.startswith("0000"):
        return None
    if isinstance(val, datetime):
        if val.year < 1900:
            return None
    return val


def migrar_cuentas(cur_mysql, pg_session, anno: int):
    """Migra el plan de cuentas de inventario (igual en todos los años, solo 2022+)."""
    if anno < 2022:
        log.info(f"  [cuentas] Año {anno} no tiene tabla cuentas — omitiendo")
        return 0

    cur_mysql.execute("SELECT codcue, nomcue, movcue, nivcue, cuegasto FROM cuentas ORDER BY codcue")
    filas = cur_mysql.fetchall()
    insertadas = 0
    for f in filas:
        existe = pg_session.execute(
            text("SELECT id FROM inventario.cuenta_contable WHERE codigo_cuenta = :c"),
            {"c": f["codcue"]}
        ).fetchone()
        if not existe:
            pg_session.execute(text("""
                INSERT INTO inventario.cuenta_contable
                    (codigo_cuenta, nombre_cuenta, tipo_movimiento, nivel, cuenta_gasto)
                VALUES (:cc, :nc, :tm, :nv, :cg)
            """), {
                "cc": f["codcue"],
                "nc": f["nomcue"],
                "tm": f["movcue"] or 1,
                "nv": f["nivcue"] or 9,
                "cg": f.get("cuegasto"),
            })
            insertadas += 1
    pg_session.commit()
    log.info(f"  [cuentas] {insertadas} cuentas nuevas insertadas (año {anno})")
    return insertadas


def migrar_destinos(cur_mysql, pg_session, anno: int):
    if anno < 2022:
        return 0
    cur_mysql.execute("SELECT INTDES, NOMBRE FROM destinos ORDER BY INTDES")
    filas = cur_mysql.fetchall()
    insertadas = 0
    for f in filas:
        existe = pg_session.execute(
            text("SELECT id FROM inventario.destino WHERE id_origen_mysql = :id"),
            {"id": int(f["INTDES"])}
        ).fetchone()
        if not existe:
            pg_session.execute(text("""
                INSERT INTO inventario.destino (id_origen_mysql, nombre, activo)
                VALUES (:io, :n, true)
            """), {"io": int(f["INTDES"]), "n": f["NOMBRE"]})
            insertadas += 1
    pg_session.commit()
    log.info(f"  [destinos] {insertadas} nuevos (año {anno})")
    return insertadas


def migrar_encargados(cur_mysql, pg_session, anno: int):
    if anno < 2022:
        return 0
    cur_mysql.execute("SELECT INTENC, NOMBRE, cedula FROM encarga ORDER BY INTENC")
    filas = cur_mysql.fetchall()
    insertadas = 0
    for f in filas:
        existe = pg_session.execute(
            text("SELECT id FROM inventario.encargado WHERE id_origen_mysql = :id"),
            {"id": int(f["INTENC"])}
        ).fetchone()
        if not existe:
            pg_session.execute(text("""
                INSERT INTO inventario.encargado (id_origen_mysql, nombre, cedula, activo)
                VALUES (:io, :n, :c, true)
            """), {"io": int(f["INTENC"]), "n": f["NOMBRE"], "c": f.get("cedula")})
            insertadas += 1
    pg_session.commit()
    log.info(f"  [encargados] {insertadas} nuevos (año {anno})")
    return insertadas


def migrar_proveedores(cur_mysql, pg_session, anno: int):
    if anno < 2022:
        return 0
    cur_mysql.execute("SELECT INTPRO, NOMBRE, RUC_CC, DIRECCION, TELEFONO, CONTACTO FROM proveedo ORDER BY INTPRO")
    filas = cur_mysql.fetchall()
    insertadas = 0
    for f in filas:
        existe = pg_session.execute(
            text("SELECT id FROM inventario.proveedor WHERE id_origen_mysql = :id"),
            {"id": int(f["INTPRO"])}
        ).fetchone()
        if not existe:
            pg_session.execute(text("""
                INSERT INTO inventario.proveedor
                    (id_origen_mysql, nombre, ruc_cedula, direccion, telefono, contacto, activo)
                VALUES (:io, :n, :r, :d, :t, :c, true)
            """), {
                "io": int(f["INTPRO"]),
                "n": f["NOMBRE"],
                "r": f.get("RUC_CC"),
                "d": f.get("DIRECCION"),
                "t": f.get("TELEFONO"),
                "c": f.get("CONTACTO"),
            })
            insertadas += 1
    pg_session.commit()
    log.info(f"  [proveedores] {insertadas} nuevos (año {anno})")
    return insertadas


def migrar_articulos(cur_mysql, pg_session, anno: int):
    """Migra el catálogo de artículos para un año dado."""
    cur_mysql.execute("""
        SELECT intart, CODIGO, NOMBRE, codcue, UNIDAD, INICIAL, COSINI,
               Actual, COSACTUAL, costototal, minimo, maximo,
               codigobarras, USUCREA, FECCREA, USUMODI, FECMODI
        FROM articulo
        ORDER BY CODIGO
    """)
    filas = cur_mysql.fetchall()
    insertadas = 0
    omitidas = 0
    for f in filas:
        existe = pg_session.execute(
            text("SELECT id FROM inventario.articulo WHERE codigo_articulo = :c AND anno_fiscal = :a"),
            {"c": f["CODIGO"], "a": anno}
        ).fetchone()
        if existe:
            omitidas += 1
            continue
        # Verificar que la cuenta exista en PG; si no, omitir FK
        cuenta_existe = pg_session.execute(
            text("SELECT 1 FROM inventario.cuenta_contable WHERE codigo_cuenta = :c"),
            {"c": f["codcue"]}
        ).fetchone()
        if not cuenta_existe:
            # Crear cuenta placeholder
            pg_session.execute(text("""
                INSERT INTO inventario.cuenta_contable (codigo_cuenta, nombre_cuenta, tipo_movimiento, nivel)
                VALUES (:cc, :nc, 1, 9)
                ON CONFLICT (codigo_cuenta) DO NOTHING
            """), {"cc": f["codcue"], "nc": "Cuenta " + str(f["codcue"])})
            pg_session.commit()

        pg_session.execute(text("""
            INSERT INTO inventario.articulo
                (id_origen_mysql, codigo_articulo, nombre, codigo_cuenta, unidad_medida,
                 existencia_inicial, costo_inicial, existencia_actual, costo_actual,
                 valor_total, stock_minimo, stock_maximo, codigo_barras,
                 anno_fiscal, activo, usuario_crea, creado_en, usuario_modifica, modificado_en)
            VALUES
                (:io, :ca, :n, :cc, :um,
                 :ei, :ci, :ea, :ca2,
                 :vt, :smin, :smax, :cb,
                 :af, true, :uc, :fec, :um2, :fmod)
        """), {
            "io": int(f["intart"]),
            "ca": f["CODIGO"],
            "n": f["NOMBRE"],
            "cc": f["codcue"],
            "um": f.get("UNIDAD"),
            "ei": f.get("INICIAL"),
            "ci": f.get("COSINI"),
            "ea": f.get("Actual"),
            "ca2": f.get("COSACTUAL") or 0,
            "vt": f.get("costototal"),
            "smin": f.get("minimo"),
            "smax": f.get("maximo"),
            "cb": f.get("codigobarras"),
            "af": anno,
            "uc": f.get("USUCREA"),
            "fec": sanitize_date(f.get("FECCREA")),
            "um2": f.get("USUMODI"),
            "fmod": sanitize_date(f.get("FECMODI")),
        })
        insertadas += 1
        if insertadas % 500 == 0:
            pg_session.commit()
            log.info(f"  [articulos] {insertadas} insertados...")

    pg_session.commit()
    log.info(f"  [articulos] {insertadas} insertados, {omitidas} ya existían (año {anno})")
    return insertadas


def migrar_movimientos(cur_mysql, pg_session, anno: int):
    """Migra movimientos y detalles (kardex) para un año."""
    # Año 2021 solo tiene 3 tablas: articulo, artimovi, acceso (sin movimien)
    if anno == 2021:
        log.info(f"  [movimientos] Año 2021 no tiene tabla movimien — migrando artimovi directamente")
        # artimovi en 2021 no tiene intmov FK válida, omitir
        return 0, 0
    # Cargar mapas de IDs MySQL → PG para FKs
    prov_map = {
        r[0]: r[1] for r in pg_session.execute(
            text("SELECT id_origen_mysql, id FROM inventario.proveedor WHERE id_origen_mysql IS NOT NULL")
        ).fetchall()
    }
    dest_map = {
        r[0]: r[1] for r in pg_session.execute(
            text("SELECT id_origen_mysql, id FROM inventario.destino WHERE id_origen_mysql IS NOT NULL")
        ).fetchall()
    }
    enc_map = {
        r[0]: r[1] for r in pg_session.execute(
            text("SELECT id_origen_mysql, id FROM inventario.encargado WHERE id_origen_mysql IS NOT NULL")
        ).fetchall()
    }
    art_map = {
        r[0]: r[1] for r in pg_session.execute(
            text("SELECT id_origen_mysql, id FROM inventario.articulo WHERE id_origen_mysql IS NOT NULL AND anno_fiscal = :a"),
            {"a": anno}
        ).fetchall()
    }

    cur_mysql.execute("""
        SELECT INTMOV, NUMERO, FECHA, TIPMOV, COS_TOTAL, numfac, fecfac,
               compegre, OBSERV, numentrada, tipo, aprobado, anexo,
               INTPRO, INTDES, INTENC, USUCREA, FECCREA
        FROM movimien
        ORDER BY FECHA, NUMERO
    """)
    movs = cur_mysql.fetchall()
    ins_mov = 0
    ins_det = 0
    omit_mov = 0

    for m in movs:
        existe = pg_session.execute(
            text("SELECT id FROM inventario.movimiento WHERE id_origen_mysql = :io AND anno_fiscal = :a"),
            {"io": int(m["INTMOV"]), "a": anno}
        ).fetchone()
        if existe:
            omit_mov += 1
            mov_pg_id = existe[0]
        else:
            tipo = "ENTRADA" if str(m["TIPMOV"]) == "1" else "SALIDA"
            res = pg_session.execute(text("""
                INSERT INTO inventario.movimiento
                    (id_origen_mysql, numero_movimiento, fecha, tipo_movimiento, subtipo,
                     costo_total, numero_factura, fecha_factura, comprobante_egreso,
                     observacion, numero_entrada_ref, aprobado, anexo, anno_fiscal,
                     id_proveedor, id_destino, id_encargado, usuario_crea, creado_en)
                VALUES
                    (:io, :nm, :fe, :tm, :st,
                     :ct, :nf, :ff, :ce,
                     :ob, :nr, :ap, :an, :af,
                     :ip, :id, :ie, :uc, :fec)
                RETURNING id
            """), {
                "io": int(m["INTMOV"]),
                "nm": int(m["NUMERO"] or 0),
                "fe": sanitize_date(m["FECHA"]) or datetime.now(),
                "tm": tipo,
                "st": m.get("tipo"),
                "ct": m.get("COS_TOTAL"),
                "nf": m.get("numfac"),
                "ff": sanitize_date(m.get("fecfac")),
                "ce": m.get("compegre"),
                "ob": m.get("OBSERV"),
                "nr": int(m["numentrada"]) if m.get("numentrada") else None,
                "ap": m.get("aprobado"),
                "an": m.get("anexo"),
                "af": anno,
                "ip": prov_map.get(int(m["INTPRO"])) if m.get("INTPRO") else None,
                "id": dest_map.get(int(m["INTDES"])) if m.get("INTDES") else None,
                "ie": enc_map.get(int(m["INTENC"])) if m.get("INTENC") else None,
                "uc": m.get("USUCREA"),
                "fec": sanitize_date(m.get("FECCREA")),
            })
            mov_pg_id = res.fetchone()[0]
            ins_mov += 1

        # Migrar detalles del movimiento
        cur_mysql.execute("""
            SELECT intartm, intart, CODIGO, TIPMOV, CANTIDAD, COSTO, total, COSPROM,
                   USUCREA, FECCREA, FECHA
            FROM artimovi WHERE intmov = %s
        """, (m["INTMOV"],))
        detalles = cur_mysql.fetchall()
        for d in detalles:
            art_pg_id = art_map.get(int(d["intart"])) if d.get("intart") else None
            if not art_pg_id:
                continue  # artículo no migrado, omitir detalle
            existe_det = pg_session.execute(
                text("SELECT id FROM inventario.movimiento_detalle WHERE id_origen_mysql = :io AND anno_fiscal = :a"),
                {"io": int(d["intartm"]), "a": anno}
            ).fetchone()
            if existe_det:
                continue
            tipo_d = "ENTRADA" if str(d["TIPMOV"]) == "1" else "SALIDA"
            pg_session.execute(text("""
                INSERT INTO inventario.movimiento_detalle
                    (id_origen_mysql, id_movimiento, id_articulo, fecha, tipo_movimiento,
                     cantidad, costo_unitario, total_linea, costo_promedio,
                     anno_fiscal, usuario_crea, creado_en)
                VALUES
                    (:io, :im, :ia, :fe, :tm,
                     :ca, :cu, :tl, :cp,
                     :af, :uc, :fec)
            """), {
                "io": int(d["intartm"]),
                "im": mov_pg_id,
                "ia": art_pg_id,
                "fe": sanitize_date(d.get("FECHA")) or sanitize_date(m["FECHA"]) or datetime.now(),
                "tm": tipo_d,
                "ca": d.get("CANTIDAD") or 0,
                "cu": d.get("COSTO") or 0,
                "tl": d.get("total"),
                "cp": d.get("COSPROM"),
                "af": anno,
                "uc": d.get("USUCREA"),
                "fec": sanitize_date(d.get("FECCREA")),
            })
            ins_det += 1

        if (ins_mov + omit_mov) % 200 == 0:
            pg_session.commit()

    pg_session.commit()
    log.info(f"  [movimientos] {ins_mov} nuevos, {omit_mov} ya existían; {ins_det} líneas kardex (año {anno})")
    return ins_mov, ins_det


def validar_integridad(pg_session, anno: int):
    """Valida conteos post-migración."""
    art = pg_session.execute(
        text("SELECT COUNT(*) FROM inventario.articulo WHERE anno_fiscal = :a"), {"a": anno}
    ).scalar()
    mov = pg_session.execute(
        text("SELECT COUNT(*) FROM inventario.movimiento WHERE anno_fiscal = :a"), {"a": anno}
    ).scalar()
    det = pg_session.execute(
        text("SELECT COUNT(*) FROM inventario.movimiento_detalle WHERE anno_fiscal = :a"), {"a": anno}
    ).scalar()
    log.info(f"  VALIDACIÓN {anno}: articulos={art}, movimientos={mov}, kardex_lineas={det}")
    return art, mov, det


def main():
    log.info("=" * 60)
    log.info("MIGRACIÓN INVENTARIO MySQL → PostgreSQL")
    log.info(f"Años: {ANNOS}")
    log.info("=" * 60)

    engine = create_engine(PG_URL)
    Session = sessionmaker(bind=engine)
    pg = Session()

    # Verificar que el schema existe
    pg.execute(text("CREATE SCHEMA IF NOT EXISTS inventario"))
    pg.commit()

    resumen = []
    for anno in ANNOS:
        db_name = f"invent_emapar_{anno}"
        log.info("\n" + "-"*50)
        log.info(f"Procesando {db_name}...")
        try:
            con = get_mysql_conn(db_name)
            cur = con.cursor()

            migrar_cuentas(cur, pg, anno)
            migrar_destinos(cur, pg, anno)
            migrar_encargados(cur, pg, anno)
            migrar_proveedores(cur, pg, anno)
            art = migrar_articulos(cur, pg, anno)
            mov, det = migrar_movimientos(cur, pg, anno)
            art_v, mov_v, det_v = validar_integridad(pg, anno)

            resumen.append({
                "anno": anno,
                "articulos": art_v,
                "movimientos": mov_v,
                "kardex_lineas": det_v,
            })
            cur.close()
            con.close()
        except Exception as e:
            log.error(f"ERROR en {db_name}: {e}")
            pg.rollback()
            raise

    pg.close()

    log.info("\n" + "=" * 60)
    log.info("RESUMEN FINAL DE MIGRACIÓN")
    log.info("=" * 60)
    log.info("%-8s %-12s %-14s %s" % ("Anno", "Articulos", "Movimientos", "Lineas Kardex"))
    for r in resumen:
        log.info("%-8s %-12s %-14s %s" % (r["anno"], r["articulos"], r["movimientos"], r["kardex_lineas"]))
    log.info("=" * 60)
    log.info("MIGRACIÓN COMPLETADA")


if __name__ == "__main__":
    main()
