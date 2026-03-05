from sqlalchemy import create_engine
from sqlalchemy import text
from app.db.session import SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text('CREATE SCHEMA IF NOT EXISTS administracion'))
    conn.execute(text('CREATE SCHEMA IF NOT EXISTS catastro'))
    conn.execute(text('CREATE SCHEMA IF NOT EXISTS comercial'))
    conn.execute(text('CREATE SCHEMA IF NOT EXISTS core'))
    conn.commit()
print("Schemas creados en la BD")
