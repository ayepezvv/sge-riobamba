from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine("postgresql+psycopg2://sge_admin:SgeSuperSecretPassword123!@localhost:5433/sge_db")
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS configuracion;"))
    
    # Check if administracion.users exists, then rename it
    try:
        conn.execute(text("ALTER TABLE administracion.users SET SCHEMA configuracion;"))
        conn.execute(text("ALTER TABLE configuracion.users RENAME TO usuarios;"))
    except Exception as e:
        print("Users rename failed:", e)
        
    try:
        conn.execute(text("ALTER TABLE administracion.roles SET SCHEMA configuracion;"))
    except Exception as e:
        print("Roles rename failed:", e)
        
    try:
        conn.execute(text("ALTER TABLE administracion.permissions SET SCHEMA configuracion;"))
        conn.execute(text("ALTER TABLE configuracion.permissions RENAME TO permisos;"))
    except Exception as e:
        print("Permissions rename failed:", e)

    try:
        conn.execute(text("ALTER TABLE administracion.role_permission SET SCHEMA configuracion;"))
        conn.execute(text("ALTER TABLE configuracion.role_permission RENAME TO rol_permiso;"))
    except Exception as e:
        print("Role_permission rename failed:", e)
        
    # Also update alembic stamp
    conn.execute(text("UPDATE alembic_version SET version_num='0d7158ce8ae4';"))
    conn.commit()
