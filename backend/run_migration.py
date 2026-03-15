import os
import sys
from alembic.config import Config
from alembic import command

def run_upgrade():
    # Establecer el directorio de trabajo al backend
    backend_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(backend_dir)
    sys.path.append(backend_dir)

    print(f"Directorio de trabajo: {os.getcwd()}")
    
    # Cargar la configuración de alembic.ini
    alembic_cfg = Config("alembic.ini")
    
    try:
        print("Generando nueva revisión de migración...")
        # Nota: autogenerate requiere que el engine esté configurado en env.py
        command.revision(alembic_cfg, message="refactor_rrhh_nomina", autogenerate=True)
        
        print("Ejecutando actualización de base de datos (upgrade head)...")
        command.upgrade(alembic_cfg, "head")
        
        print("¡Migración completada con éxito!")
    except Exception as e:
        print(f"Error durante la migración: {e}")

if __name__ == "__main__":
    run_upgrade()
