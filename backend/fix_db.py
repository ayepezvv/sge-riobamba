from sqlalchemy import create_engine
from sqlalchemy import text
from app.db.session import SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text('DROP SCHEMA IF EXISTS administracion CASCADE'))
    conn.execute(text('DROP SCHEMA IF EXISTS catastro CASCADE'))
    conn.execute(text('DROP SCHEMA IF EXISTS comercial CASCADE'))
    conn.execute(text('DROP SCHEMA IF EXISTS core CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS alembic_version CASCADE'))
    
    # Just in case they are still in public schema
    conn.execute(text('DROP TABLE IF EXISTS role_permission CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS roles CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS permissions CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS users CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS audit_logs CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS parametros_sistema CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS predios CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS acometidas CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS cuentas CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS medidores CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS historial_medidor_cuenta CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS historial_tarifa_cuenta CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS ciudadanos CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS referencias_ciudadanos CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS redes CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS sectores CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS rutas CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS barrios CASCADE'))
    conn.execute(text('DROP TABLE IF EXISTS calles CASCADE'))
    conn.commit()
