from sqlalchemy import create_engine, text
from app.db.session import SQLALCHEMY_DATABASE_URL
from app.db.base_class import Base
import app.models  # Import to register metadata

engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text('DROP SCHEMA IF EXISTS administracion CASCADE'))
    conn.execute(text('DROP SCHEMA IF EXISTS catastro CASCADE'))
    conn.execute(text('DROP SCHEMA IF EXISTS comercial CASCADE'))
    conn.execute(text('DROP SCHEMA IF EXISTS core CASCADE'))
    conn.execute(text('CREATE SCHEMA administracion'))
    conn.execute(text('CREATE SCHEMA catastro'))
    conn.execute(text('CREATE SCHEMA comercial'))
    conn.execute(text('CREATE SCHEMA core'))
    conn.commit()

Base.metadata.create_all(engine)
print("Tablas creadas exitosamente en schemas")
