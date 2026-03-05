from sqlalchemy import create_engine
from sqlalchemy import text
from app.db.session import SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text('DROP TABLE IF EXISTS alembic_version CASCADE'))
    conn.execute(text('DROP SCHEMA IF EXISTS administracion CASCADE'))
    conn.execute(text('DROP SCHEMA IF EXISTS catastro CASCADE'))
    conn.execute(text('DROP SCHEMA IF EXISTS comercial CASCADE'))
    conn.execute(text('DROP SCHEMA IF EXISTS core CASCADE'))
    conn.execute(text('CREATE SCHEMA administracion'))
    conn.execute(text('CREATE SCHEMA catastro'))
    conn.execute(text('CREATE SCHEMA comercial'))
    conn.execute(text('CREATE SCHEMA core'))
    conn.commit()
