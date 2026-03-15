"""
Script de migración Fase 1 - RRHH Directorio de Personal
Ejecutar desde: /backend/
Comandos:
    alembic revision --autogenerate -m "fase1_personal"
    alembic upgrade head
"""
from alembic.config import Config
from alembic import command
import os, sys

# Asegurar que el directorio backend esté en el path
backend_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

alembic_cfg = Config(os.path.join(backend_dir, "alembic.ini"))

print("=" * 60)
print("MIGRACIÓN FASE 1 - RRHH: Directorio de Personal")
print("=" * 60)

try:
    print("\n[1/2] Generando revisión automática (autogenerate)...")
    command.revision(alembic_cfg, message="fase1_personal", autogenerate=True)
    
    print("\n[2/2] Aplicando migración a la base de datos (upgrade head)...")
    command.upgrade(alembic_cfg, "head")
    
    print("\n✅ Migración completada exitosamente.")
    print("   Tablas creadas en esquema 'administracion':")
    print("   - empleados")
    print("   - direcciones")
    print("   - unidades")
    print("   - puestos")
    print("   - escala_salarial")
    print("   - titulos_profesionales")
    print("   - empleado_carga_familiar")
    
except Exception as e:
    print(f"\n❌ Error durante la migración: {e}")
    print("\nAlternativa manual desde el directorio /backend/:")
    print("  alembic revision --autogenerate -m \"fase1_personal\"")
    print("  alembic upgrade head")
