#!/usr/bin/env python3
"""
Script de Carga — DataFrames transformados → PostgreSQL SGE
Destino: 192.168.1.15, puerto 5433 (Docker)

Estrategia:
- INSERT con ON CONFLICT DO NOTHING (idempotente — se puede re-ejecutar)
- Guarda rollback SQL antes de cada tabla
- Progreso con logging

PREREQUISITO: Ejecutar primero 1_extraccion.py y 2_transformacion.py
"""
import csv
import logging
import psycopg2
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

INPUT_DIR = Path("/tmp/migracion/transformado")
ROLLBACK_DIR = Path("/tmp/migracion/rollback")

SGE_DSN = {
    "host": "192.168.1.15",
    "port": 5433,
    "dbname": "sge_db",
    "user": "sge_admin",
    "password": "SgeSuperSecretPassword123!",
    "connect_timeout": 10,
}

# Mapeo tipos OpenERP → tipo_cuenta SGE
MAPA_TIPO_CUENTA = {
    "ACTIVO": "ACTIVO",
    "PASIVO": "PASIVO",
    "PATRIMONIO": "PATRIMONIO",
    "INGRESO": "INGRESO",
    "GASTO": "GASTO",
    "view": "ACTIVO",  # vistas se tratan como activo
    "other": "ACTIVO",
    "receivable": "ACTIVO",
    "payable": "PASIVO",
    "liquidity": "ACTIVO",
    "income": "INGRESO",
    "expense": "GASTO",
    "equity": "PATRIMONIO",
}

TIPOS_CUENTA_BASE = [
    ("ACTIVO", "DEUDOR", True),
    ("PASIVO", "ACREEDOR", True),
    ("PATRIMONIO", "ACREEDOR", True),
    ("INGRESO", "ACREEDOR", False),
    ("GASTO", "DEUDOR", False),
]


def leer_csv(nombre: str) -> list[dict]:
    archivo = INPUT_DIR / f"{nombre}.csv"
    if not archivo.exists():
        log.warning(f"Archivo no encontrado: {archivo}")
        return []
    with open(archivo, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def guardar_rollback(schema: str, tabla: str) -> None:
    ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)
    archivo = ROLLBACK_DIR / f"rollback_{tabla}.sql"
    sql = f"-- Rollback para {schema}.{tabla}\n"
    sql += f"-- Generado: {datetime.now()}\n"
    sql += f"DELETE FROM {schema}.{tabla} WHERE creado_en > NOW() - INTERVAL '1 day';\n"
    with open(archivo, "w") as f:
        f.write(sql)
    log.info(f"  Rollback guardado en: {archivo}")


def inicializar_tipos_cuenta(conn) -> dict:
    """Asegura que existan los tipos de cuenta base y devuelve mapeo nombre→id."""
    cur = conn.cursor()

    # Verificar columnas de la tabla
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema='contabilidad' AND table_name='tipos_cuenta'
        ORDER BY ordinal_position
    """)
    cols = [r[0] for r in cur.fetchall()]
    log.info(f"  tipos_cuenta columnas: {cols}")

    # Insertar tipos base si no existen
    if 'nombre' in cols and 'codigo' in cols:
        for nombre, naturaleza, es_balance in TIPOS_CUENTA_BASE:
            try:
                cur.execute("""
                    INSERT INTO contabilidad.tipos_cuenta (nombre, codigo)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, (nombre, nombre))
            except Exception:
                conn.rollback()
                break
        conn.commit()

    # Obtener mapeo
    cur.execute("SELECT id, nombre FROM contabilidad.tipos_cuenta")
    rows = cur.fetchall()
    mapeo = {r[1]: r[0] for r in rows}
    log.info(f"  Tipos de cuenta disponibles: {mapeo}")
    return mapeo


def cargar_partidas(conn, filas: list[dict]) -> int:
    """Carga partidas presupuestarias."""
    guardar_rollback("presupuesto", "partidas_presupuestarias")
    sql = """
        INSERT INTO presupuesto.partidas_presupuestarias
            (codigo, nombre, tipo, nivel, es_hoja, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (codigo) DO NOTHING
    """
    cargados = 0
    with conn.cursor() as cur:
        for r in filas:
            try:
                tipo = r.get("tipo", "GASTO").upper()
                if tipo not in ("INGRESO", "GASTO"):
                    tipo = "GASTO"
                cur.execute(sql, (
                    r["codigo"][:30],
                    r["nombre"][:255],
                    tipo,
                    int(r.get("nivel") or 1),
                    str(r.get("es_hoja", "true")).lower() == "true",
                    r.get("estado", "ACTIVO"),
                ))
                if cur.rowcount:
                    cargados += 1
            except Exception as e:
                log.debug(f"  Skip partida {r.get('codigo')}: {e}")
        conn.commit()
    return cargados


def cargar_empleados(conn, filas: list[dict]) -> int:
    """Carga empleados al schema rrhh."""
    guardar_rollback("rrhh", "empleado")
    sql = """
        INSERT INTO rrhh.empleado
            (tipo_identificacion, identificacion, nombres, apellidos,
             fecha_nacimiento, genero, telefono_celular, correo_personal,
             estado_empleado, aplica_iess, acumula_fondos_reserva, acumula_decimos)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (identificacion) DO NOTHING
    """
    cargados = 0
    with conn.cursor() as cur:
        for r in filas:
            try:
                cur.execute(sql, (
                    r.get("tipo_identificacion", "CEDULA"),
                    r["identificacion"][:20],
                    (r.get("nombres") or "SIN NOMBRE")[:100],
                    (r.get("apellidos") or "SIN APELLIDO")[:100],
                    r.get("fecha_nacimiento") or "1970-01-01",
                    r.get("genero") or None,
                    (r.get("telefono_celular") or "")[:20] or None,
                    (r.get("correo_personal") or "")[:100] or None,
                    r.get("estado_empleado", "ACTIVO"),
                    str(r.get("aplica_iess", "true")).lower() == "true",
                    str(r.get("acumula_fondos_reserva", "true")).lower() == "true",
                    str(r.get("acumula_decimos", "false")).lower() == "true",
                ))
                if cur.rowcount:
                    cargados += 1
            except Exception as e:
                log.debug(f"  Skip empleado {r.get('identificacion')}: {e}")
        conn.commit()
    return cargados


def cargar_cuentas_contables(conn, filas: list[dict], mapeo_tipos: dict) -> int:
    """Carga plan de cuentas. Requiere tipos_cuenta poblados."""
    if not mapeo_tipos:
        log.warning("  No hay tipos de cuenta — omitiendo cuentas_contables")
        return 0

    guardar_rollback("contabilidad", "cuentas_contables")
    sql = """
        INSERT INTO contabilidad.cuentas_contables
            (codigo, nombre, tipo_cuenta_id, nivel, es_hoja, permite_movimientos, estado)
        VALUES (%s, %s, %s, %s, %s, %s, 'ACTIVA')
        ON CONFLICT (codigo) DO NOTHING
    """
    cargados = 0
    omitidos = 0
    with conn.cursor() as cur:
        for r in filas:
            tipo_raw = MAPA_TIPO_CUENTA.get(r.get("tipo", "ACTIVO").upper(), "ACTIVO")
            tipo_id = mapeo_tipos.get(tipo_raw)
            if not tipo_id:
                # Usar primer tipo disponible
                tipo_id = next(iter(mapeo_tipos.values()), None)
            if not tipo_id:
                omitidos += 1
                continue
            try:
                cur.execute(sql, (
                    r["codigo"][:50],
                    r["nombre"][:200],
                    tipo_id,
                    int(r.get("nivel") or 1),
                    str(r.get("es_hoja", "true")).lower() == "true",
                    str(r.get("permite_movimientos", "true")).lower() == "true",
                ))
                if cur.rowcount:
                    cargados += 1
            except Exception as e:
                log.debug(f"  Skip cuenta {r.get('codigo')}: {e}")
        conn.commit()
    if omitidos:
        log.warning(f"  {omitidos} cuentas omitidas por tipo_cuenta no encontrado")
    return cargados


def main():
    log.info("="*60)
    log.info("CARGA → SGE PostgreSQL 192.168.1.15:5433")
    log.info(f"Inicio: {datetime.now()}")
    log.info("="*60)

    try:
        conn = psycopg2.connect(**SGE_DSN)
    except Exception as e:
        log.error(f"Error conectando al SGE: {e}")
        return 1

    resultados = {}

    # 1. Partidas presupuestarias
    filas = leer_csv("partidas_presupuestarias")
    if filas:
        n = cargar_partidas(conn, filas)
        resultados["presupuesto.partidas_presupuestarias"] = n
        log.info(f"  partidas_presupuestarias: {n:,} cargados")

    # 2. Empleados
    filas = leer_csv("empleados")
    if filas:
        n = cargar_empleados(conn, filas)
        resultados["rrhh.empleado"] = n
        log.info(f"  rrhh.empleado: {n:,} cargados")

    # 3. Tipos de cuenta (prerequisito)
    log.info("  Inicializando tipos de cuenta...")
    mapeo_tipos = inicializar_tipos_cuenta(conn)

    # 4. Plan de cuentas contables
    filas = leer_csv("cuentas_contables")
    if filas:
        n = cargar_cuentas_contables(conn, filas, mapeo_tipos)
        resultados["contabilidad.cuentas_contables"] = n
        log.info(f"  cuentas_contables: {n:,} cargados")

    conn.close()

    log.info("\n" + "="*60)
    log.info("RESUMEN CARGA")
    log.info("="*60)
    for tabla, total in resultados.items():
        log.info(f"  {tabla:<50} {total:>8,} insertados")
    log.info(f"\nCarga completada: {datetime.now()}")
    log.info(f"Scripts de rollback en: {ROLLBACK_DIR}")
    return 0


if __name__ == "__main__":
    exit(main())
