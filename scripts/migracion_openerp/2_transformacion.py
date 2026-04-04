#!/usr/bin/env python3
"""
Script de Transformación — archivos CSV OpenERP → DataFrames SGE
Aplica nomenclatura en español y mapeo de campos.
"""
import csv
import json
import logging
from pathlib import Path
from datetime import datetime, date

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

INPUT_DIR = Path("/tmp/migracion")
OUTPUT_DIR = Path("/tmp/migracion/transformado")

# ================================================================
# MAPEO DE ESTADOS OpenERP → SGE
# ================================================================
ESTADO_CERTIFICADO = {
    "draft": "SOLICITADO",
    "confirm": "APROBADO",
    "done": "LIQUIDADO",
    "cancel": "ANULADO",
}

ESTADO_CONTRATO = {
    "draft": "BORRADOR",
    "open": "ACTIVO",
    "pending": "ACTIVO",
    "close": "TERMINADO",
    "cancel": "ANULADO",
}

TIPO_CUENTA = {
    "receivable": "ACTIVO",
    "payable": "PASIVO",
    "asset": "ACTIVO",
    "income": "INGRESOS",
    "expense": "GASTOS",
    "equity": "PATRIMONIO",
    "other": "ACTIVO",
    "view": "ACTIVO",
    "consolidation": "ACTIVO",
    "closed": "ACTIVO",
}

GENERO = {
    "male": "MASCULINO",
    "female": "FEMENINO",
    "other": "OTRO",
    None: None,
    "": None,
}


def leer_csv(nombre: str) -> list[dict]:
    archivo = INPUT_DIR / f"{nombre}.csv"
    if not archivo.exists():
        log.warning(f"Archivo no encontrado: {archivo}")
        return []
    with open(archivo, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def escribir_csv(nombre: str, filas: list[dict]) -> None:
    if not filas:
        log.warning(f"Sin datos para {nombre}")
        return
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    archivo = OUTPUT_DIR / f"{nombre}.csv"
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=filas[0].keys())
        writer.writeheader()
        writer.writerows(filas)
    log.info(f"  → {len(filas):,} registros → {archivo}")


def transformar_partidas(filas: list[dict]) -> list[dict]:
    """
    Mapea account.budget.post OpenERP → presupuesto.partidas_presupuestarias SGE
    """
    resultado = []
    for r in filas:
        tipo = "GASTO" if r.get("tipo", "").startswith("5") or r.get("tipo", "") == "expense" else "INGRESO"
        resultado.append({
            "id_openerp": r["id_openerp"],
            "codigo": r["codigo"] or "",
            "nombre": (r["nombre"] or "")[:255],
            "tipo": tipo,
            "nivel": len((r.get("codigo") or "").split(".")) if r.get("codigo") else 1,
            "es_hoja": "true",
            "id_partida_padre_openerp": r.get("id_padre_openerp") or "",
            "estado": "ACTIVO" if str(r.get("activo", "t")).lower() in ("t", "true", "1") else "INACTIVO",
        })
    return resultado


def transformar_empleados(filas: list[dict]) -> list[dict]:
    """
    Mapea hr.employee OpenERP → rrhh.empleado SGE
    """
    resultado = []
    for r in filas:
        if not r.get("identificacion"):
            continue  # saltear empleados sin cédula
        # Separar nombre completo en nombres/apellidos (heurística)
        nombre_completo = (r.get("nombres_completos") or "").strip()
        partes = nombre_completo.split()
        if len(partes) >= 4:
            apellidos = " ".join(partes[:2])
            nombres = " ".join(partes[2:])
        elif len(partes) >= 2:
            apellidos = partes[0]
            nombres = " ".join(partes[1:])
        else:
            apellidos = nombre_completo
            nombres = "SIN NOMBRE"

        resultado.append({
            "id_openerp": r["id_openerp"],
            "tipo_identificacion": "CEDULA",
            "identificacion": r["identificacion"].strip(),
            "nombres": nombres[:100],
            "apellidos": apellidos[:100],
            "fecha_nacimiento": r.get("fecha_nacimiento") or "1970-01-01",
            "genero": GENERO.get(r.get("genero")),
            "telefono_celular": (r.get("telefono_celular") or "")[:20] or None,
            "correo_personal": (r.get("correo_personal") or "")[:100] or None,
            "estado_empleado": "ACTIVO" if str(r.get("activo", "t")).lower() in ("t", "true", "1") else "DESVINCULADO",
            "aplica_iess": "true",
            "acumula_fondos_reserva": "true",
            "acumula_decimos": "false",
        })
    return resultado


def transformar_contratos(filas: list[dict]) -> list[dict]:
    """
    Mapea hr.contract OpenERP → rrhh.contrato SGE
    """
    resultado = []
    for r in filas:
        try:
            sueldo = float(r.get("sueldo_pactado") or 0)
        except ValueError:
            sueldo = 0.0

        resultado.append({
            "id_openerp": r["id_openerp"],
            "id_empleado_openerp": r["id_empleado_openerp"],
            "tipo_contrato": "NOMBRAMIENTO",  # valor por defecto; ajustar con tipo_contrato_id
            "fecha_inicio": r.get("fecha_inicio") or "2015-01-01",
            "fecha_fin": r.get("fecha_fin") or None,
            "sueldo_pactado": round(sueldo, 2),
            "estado_contrato": ESTADO_CONTRATO.get(r.get("estado_openerp", "open"), "ACTIVO"),
            "observaciones": f"Migrado de OpenERP ID={r[id_openerp]}",
        })
    return resultado


def transformar_cuentas(filas: list[dict]) -> list[dict]:
    """
    Mapea account.account OpenERP → contabilidad.cuentas_contables SGE
    """
    resultado = []
    for r in filas:
        resultado.append({
            "id_openerp": r["id_openerp"],
            "codigo": (r.get("codigo") or "")[:30],
            "nombre": (r.get("nombre") or "")[:200],
            "tipo": TIPO_CUENTA.get(r.get("tipo", "other"), "ACTIVO"),
            "nivel": int(r.get("nivel") or 1),
            "permite_movimientos": str(r.get("activo", "t")).lower() in ("t", "true", "1"),
            "es_hoja": "true",
            "id_cuenta_padre_openerp": r.get("id_padre_openerp") or "",
            "partida_presupuestaria": None,
        })
    return resultado


def main():
    log.info("="*60)
    log.info("TRANSFORMACIÓN OpenERP → SGE")
    log.info(f"Inicio: {datetime.now()}")
    log.info("="*60)

    datasets = {
        "partidas_presupuestarias": transformar_partidas,
        "empleados": transformar_empleados,
        "contratos": transformar_contratos,
        "cuentas_contables": transformar_cuentas,
    }

    for nombre, fn_transform in datasets.items():
        filas_raw = leer_csv(nombre)
        if not filas_raw:
            log.warning(f"Sin datos para transformar: {nombre}")
            continue
        log.info(f"Transformando {nombre} ({len(filas_raw):,} registros)...")
        filas_transformadas = fn_transform(filas_raw)
        escribir_csv(nombre, filas_transformadas)

    log.info(f"\nTransformación completada: {datetime.now()}")


if __name__ == "__main__":
    main()
