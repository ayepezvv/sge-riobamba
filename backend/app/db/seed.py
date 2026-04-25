"""
Seed de datos iniciales — roles funcionales del sistema.
Se ejecuta automáticamente al iniciar el servidor (idempotente).
"""

import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.role import Role

logger = logging.getLogger(__name__)

ROLES_FUNCIONALES = [
    ("SuperAdmin",   "Administrador total del sistema"),
    ("RRHH",         "Recursos Humanos"),
    ("Contabilidad", "Módulo de Contabilidad"),
    ("Presupuesto",  "Módulo de Presupuesto"),
    ("Tesoreria",    "Módulo de Tesorería"),
    ("Financiero",   "Módulo Financiero"),
    ("Bodega",       "Módulo de Bodega"),
    ("Informatica",  "Módulo de Informática"),
    ("Contratacion", "Módulo de Contratación"),
]


def seed_roles(db: Session) -> None:
    """Inserta los roles funcionales si no existen (idempotente)."""
    creados = 0
    for nombre, descripcion in ROLES_FUNCIONALES:
        if not db.query(Role).filter(Role.nombre_rol == nombre).first():
            db.add(Role(nombre_rol=nombre, descripcion=descripcion))
            creados += 1
    if creados:
        db.commit()
        logger.info("[seed] %d rol(es) funcional(es) creado(s).", creados)
    else:
        logger.debug("[seed] Todos los roles funcionales ya existen.")


def run_startup_seed() -> None:
    """Punto de entrada para el startup de FastAPI."""
    db = SessionLocal()
    try:
        seed_roles(db)
    except Exception:
        db.rollback()
        logger.exception("[seed] Error al insertar roles en startup. Se revirtieron los cambios.")
    finally:
        db.close()
