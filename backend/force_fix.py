from sqlalchemy import create_engine, text
from app.db.session import SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text("ALTER TABLE contratacion.plantilla_documento DROP COLUMN IF EXISTS is_activo;"))
    conn.execute(text("ALTER TABLE contratacion.plantilla_documento DROP COLUMN IF EXISTS categoria;"))
    conn.execute(text("ALTER TABLE contratacion.plantilla_documento DROP COLUMN IF EXISTS condicion_monto;"))
    conn.execute(text("ALTER TABLE contratacion.plantilla_documento ADD COLUMN IF NOT EXISTS anio INTEGER DEFAULT 2026;"))
    conn.execute(text("ALTER TABLE contratacion.plantilla_documento ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;"))
    conn.execute(text("ALTER TABLE contratacion.plantilla_documento ADD COLUMN IF NOT EXISTS is_activa BOOLEAN DEFAULT TRUE;"))
    conn.commit()
print("Force fix applied.")
