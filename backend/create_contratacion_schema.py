from sqlalchemy import create_engine, text
from app.db.session import SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text('CREATE SCHEMA IF NOT EXISTS contratacion'))
    conn.commit()
print("Schema contratacion asegurado.")
