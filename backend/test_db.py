from sqlalchemy import create_engine, text
from app.db.session import SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
with engine.connect() as conn:
    res = conn.execute(text("SELECT schema_name FROM information_schema.schemata;")).fetchall()
    print([r[0] for r in res])
