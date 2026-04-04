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
    "user": "sge",
    "password": "sge",
    "connect_timeout": 10,
}


def leer_csv(nombre: str) -> list[dict]:
    archivo = INPUT_DIR / f"{nombre}.csv"
    if not archivo.exists():
        log.warning(f"Archivo no encontrado: {archivo}")
        return []
    with open(archivo, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def guardar_rollback(conn, tabla_schema: str, tabla_nombre: str) -> None:
    """Guarda SQL de borrado para poder hacer rollback."""
    ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)
    archivo = ROLLBACK_DIR / f"rollback_{tabla_nombre}.sql"
    sql = f"-- Rollback para {tabla_schema}.{tabla_nombre}\n"
    sql += f"-- Generado: {datetime.now()}\n"
    sql += f"DELETE FROM {tabla_schema}.{tabla_nombre} WHERE creado_en > NOW() - INTERVAL 1 day;\n"
    with open(archivo, "w") as f:
        f.write(sql)
    log.info(f"  Rollback guardado en: {archivo}")


def cargar_partidas(conn, filas: list[dict]) -> int:
    """Carga partidas presupuestarias."""
    guardar_rollback(conn, "presupuesto", "partidas_presupuestarias")
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
                cur.execute(sql, (
                    r["codigo"][:30],
                    r["nombre"][:255],
                    r["tipo"],
                    int(r["nivel"] or 1),
                    r["es_hoja"].lower() == "true",
                    r["estado"],
                ))
                if cur.rowcount:
                    cargados += 1
            except Exception as e:
                log.debug(f"  Skip partida {r.get(codigo)}: {e}")
        conn.commit()
    return cargados


def cargar_empleados(conn, filas: list[dict]) -> int:
    """Carga empleados al schema rrhh."""
    guardar_rollback(conn, "rrhh", "empleado")
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
                    r["identificacion"],
                    r["nombres"][:100],
                    r["apellidos"][:100],
                    r.get("fecha_nacimiento") or "1970-01-01",
                    r.get("genero") or None,
                    r.get("telefono_celular") or None,
                    r.get("correo_personal") or None,
                    r.get("estado_empleado", "ACTIVO"),
                    r.get("aplica_iess", "true").lower() == "true",
                    r.get("acumula_fondos_reserva", "true").lower() == "true",
                    r.get("acumula_decimos", "false").lower() == "true",
                ))
                if cur.rowcount:
                    cargados += 1
            except Exception as e:
                log.debug(f"  Skip empleado {r.get(identificacion)}: {e}")
        conn.commit()
    return cargados


def cargar_tabla(conn, schema: str, tabla: str, filas: list[dict],
                 columnas: list[str], conflict_col: str = None) -> int:
    """Carga genérica."""
    if not filas:
        return 0
    guardar_rollback(conn, schema, tabla)
    placeholders = ", ".join(["%s"] * len(columnas))
    cols_str = ", ".join(columnas)
    conflict = f"ON CONFLICT ({conflict_col}) DO NOTHING" if conflict_col else ""
    sql = f"INSERT INTO {schema}.{tabla} ({cols_str}) VALUES ({placeholders}) {conflict}"

    cargados = 0
    with conn.cursor() as cur:
        for r in filas:
            try:
                valores = [r.get(c) or None for c in columnas]
                cur.execute(sql, valores)
                if cur.rowcount:
                    cargados += 1
            except Exception as e:
                log.debug(f"  Skip {tabla}: {e}")
        conn.commit()
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
        log.error("Verifique que el contenedor Docker esté activo en 192.168.1.15:5433")
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

    # 3. Cuentas contables (sin actualizar padre por ahora — se resuelve en paso siguiente)
    filas = leer_csv("cuentas_contables")
    if filas:
        columnas = ["codigo", "nombre", "tipo", "nivel", "permite_movimientos", "es_hoja"]
        validos = []
        for r in filas:
            try:
                validos.append({
                    "codigo": r["codigo"][:30],
                    "nombre": r["nombre"][:200],
                    "tipo": r["tipo"],
                    "nivel": int(r.get("nivel") or 1),
                    "permite_movimientos": r.get("permite_movimientos", "true").lower() != "false",
                    "es_hoja": True,
                })
            except Exception:
                pass
        n = cargar_tabla(conn, "contabilidad", "cuentas_contables", validos, columnas, "codigo")
        resultados["contabilidad.cuentas_contables"] = n
        log.info(f"  contabilidad.cuentas_contables: {n:,} cargados")

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
