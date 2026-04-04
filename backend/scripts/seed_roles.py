"""
Script idempotente de preparación de BD para go-live.

Ejecutar desde backend/:
    python scripts/seed_roles.py

Operaciones:
  1. SGE-ROLES-SEED  — Insertar roles funcionales si no existen.
  2. SGE-DB-CLEANUP  — Eliminar roles/usuarios de prueba contaminados por IDOR.
                       Restaurar datos del usuario administrador.
"""

import sys
import os

# Asegurar que el módulo `app` sea encontrado cuando se ejecuta desde backend/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.role import Role
from app.models.user import User


# ─── Configuración ────────────────────────────────────────────────────────────

ROLES_FUNCIONALES = [
    ("SuperAdmin",     "Administrador total del sistema"),
    ("RRHH",           "Recursos Humanos"),
    ("Contabilidad",   "Módulo de Contabilidad"),
    ("Presupuesto",    "Módulo de Presupuesto"),
    ("Tesoreria",      "Módulo de Tesorería"),
    ("Financiero",     "Módulo Financiero"),
    ("Bodega",         "Módulo de Bodega"),
    ("Informatica",    "Módulo de Informática"),
    ("Contratacion",   "Módulo de Contratación"),
]

ROLES_BASURA = [
    "HackerRole", "TestRole", "TestRole2",
    "H4x", "TestHack", "HackRole",
]

CORREO_BASURA = "hacker@evil.com"

# Usuario admin (id=1) — nombre corrompido por IDOR testing
ADMIN_ID = 1
ADMIN_NOMBRES_CORRECTO = "Admin"


# ─── Funciones ────────────────────────────────────────────────────────────────

def seed_roles(db):
    """Inserta los roles funcionales si no existen (idempotente)."""
    print("\n[SGE-ROLES-SEED] Verificando roles funcionales...")
    creados = 0
    for nombre, descripcion in ROLES_FUNCIONALES:
        existe = db.query(Role).filter(Role.nombre_rol == nombre).first()
        if not existe:
            db.add(Role(nombre_rol=nombre, descripcion=descripcion))
            print(f"  + Rol creado: {nombre}")
            creados += 1
        else:
            print(f"  ✓ Ya existe: {nombre}")
    if creados:
        db.commit()
    print(f"[SGE-ROLES-SEED] {creados} rol(es) creado(s).")


def cleanup_roles_basura(db):
    """Elimina roles de prueba que no deben existir en producción."""
    print("\n[SGE-DB-CLEANUP] Limpiando roles de prueba...")
    eliminados = 0
    for nombre in ROLES_BASURA:
        rol = db.query(Role).filter(Role.nombre_rol == nombre).first()
        if rol:
            # Desvincular usuarios que apunten a este rol antes de eliminarlo
            db.query(User).filter(User.role_id == rol.id).update(
                {"role_id": None}, synchronize_session=False
            )
            db.delete(rol)
            print(f"  - Rol eliminado: {nombre}")
            eliminados += 1
        else:
            print(f"  ✓ No encontrado (OK): {nombre}")
    if eliminados:
        db.commit()
    print(f"[SGE-DB-CLEANUP] {eliminados} rol(es) de prueba eliminado(s).")


def cleanup_usuarios_basura(db):
    """Elimina usuarios de prueba y restaura datos del admin."""
    print("\n[SGE-DB-CLEANUP] Limpiando usuarios de prueba...")

    # 1. Eliminar hacker@evil.com
    hacker = db.query(User).filter(User.correo == CORREO_BASURA).first()
    if hacker:
        db.delete(hacker)
        db.commit()
        print(f"  - Usuario eliminado: {CORREO_BASURA} (id={hacker.id})")
    else:
        print(f"  ✓ No encontrado (OK): {CORREO_BASURA}")

    # 2. Restaurar nombres del admin (id=1) si fue corrompido por IDOR
    admin = db.query(User).filter(User.id == ADMIN_ID).first()
    if admin:
        if admin.nombres != ADMIN_NOMBRES_CORRECTO:
            print(f"  ~ Restaurando nombres admin: '{admin.nombres}' → '{ADMIN_NOMBRES_CORRECTO}'")
            admin.nombres = ADMIN_NOMBRES_CORRECTO
            db.commit()
            print(f"  ✓ Admin restaurado.")
        else:
            print(f"  ✓ Nombres del admin ya son correctos: '{admin.nombres}'")
    else:
        print(f"  ! ADVERTENCIA: No se encontró usuario con id={ADMIN_ID}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  SGE Riobamba EP — Seed & Cleanup de BD (pre-deploy)")
    print("=" * 60)

    db = SessionLocal()
    try:
        seed_roles(db)
        cleanup_roles_basura(db)
        cleanup_usuarios_basura(db)
        print("\n[OK] Script completado exitosamente.")
    except Exception as exc:
        db.rollback()
        print(f"\n[ERROR] Se revirtieron los cambios: {exc}")
        raise
    finally:
        db.close()

    print("=" * 60)


if __name__ == "__main__":
    main()
