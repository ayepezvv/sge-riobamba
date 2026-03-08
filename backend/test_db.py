from sqlalchemy import create_engine, text
from app.db.session import SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as conn:
    res = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'plantilla_documento' AND table_schema='contratacion';")).fetchall()
    print(res)
