import re

path = "app/models/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Fix the enum import and usage
if "from sqlalchemy import Enum as SQLEnum" not in content:
    content = content.replace("from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Float", "from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Float, Enum as SQLEnum")

content = content.replace('status = Column(enum.Enum(StatusItemPac, name="status_item_pac"), default=StatusItemPac.ACTIVO, nullable=False)', 'status = Column(SQLEnum(StatusItemPac, name="status_item_pac"), default=StatusItemPac.ACTIVO, nullable=False)')

with open(path, "w") as f:
    f.write(content)
