import os

env_path = "alembic/env.py"
with open(env_path, "r") as f:
    content = f.read()

imports = """
import sys
import os
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.db.base_class import Base
import app.models  # Import all models to register them with Base.metadata
"""

content = content.replace("from alembic import context", "from alembic import context\n" + imports)
content = content.replace("target_metadata = None", "target_metadata = Base.metadata")

with open(env_path, "w") as f:
    f.write(content)
