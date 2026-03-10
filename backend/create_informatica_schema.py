import os
import sys

# Script para forzar la creacion del schema informatica
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
from app.db.session import engine
from sqlalchemy import text

def create_schema():
    with engine.connect() as con:
        con.execute(text("CREATE SCHEMA IF NOT EXISTS informatica;"))
        con.commit()
    print("Schema informatica created successfully.")

if __name__ == "__main__":
    create_schema()
