from sqlalchemy import create_engine
from sqlalchemy.sql import text
engine = create_engine("postgresql+psycopg2://sge_admin:SgeSuperSecretPassword123!@localhost:5433/sge_db")
with engine.connect() as conn:
    # Rename tables properly and retain data.
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS configuracion;"))
    try:
        conn.execute(text("ALTER TABLE administracion.users SET SCHEMA configuracion;"))
        conn.execute(text("ALTER TABLE configuracion.users RENAME TO usuarios;"))
    except: pass
    
    try:
        conn.execute(text("ALTER TABLE administracion.roles SET SCHEMA configuracion;"))
    except: pass
    
    try:
        conn.execute(text("ALTER TABLE administracion.permissions SET SCHEMA configuracion;"))
        conn.execute(text("ALTER TABLE configuracion.permissions RENAME TO permisos;"))
    except: pass
    
    try:
        conn.execute(text("ALTER TABLE administracion.role_permission SET SCHEMA configuracion;"))
        conn.execute(text("ALTER TABLE configuracion.role_permission RENAME TO rol_permiso;"))
    except: pass
    conn.commit()
