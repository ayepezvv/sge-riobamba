from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://sge_admin:SgeSuperSecretPassword123!@localhost:5433/sge_db")
with engine.connect() as conn:
    conn.execute("ALTER SCHEMA administracion RENAME TO configuracion;")
