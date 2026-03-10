path = "alembic/versions/d7c5d8e774cb_arquitectura_genealogia_reforma_pac.py"
with open(path, "r") as f:
    content = f.read()

import re
# Explicitly create enum type before adding column
enum_sql = "sa.Enum('ACTIVO', 'ELIMINADO_POR_REFORMA', 'MODIFICADO_POR_REFORMA', name='status_item_pac').create(op.get_bind(), checkfirst=True)\n    "
content = content.replace("op.add_column('item_pac', sa.Column('status'", enum_sql + "op.add_column('item_pac', sa.Column('status'")
with open(path, "w") as f:
    f.write(content)
