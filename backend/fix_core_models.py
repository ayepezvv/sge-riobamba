import re

# 1. Update User Model
path_user = "app/models/user.py"
with open(path_user, "r") as f:
    content = f.read()
content = content.replace('__tablename__ = "users"', '__tablename__ = "usuarios"')
content = content.replace('__table_args__ = {"schema": "administracion"}', '__table_args__ = {"schema": "configuracion"}')
content = content.replace('ForeignKey("administracion.roles.id"', 'ForeignKey("configuracion.roles.id"')
with open(path_user, "w") as f:
    f.write(content)

# 2. Update Role Model
path_role = "app/models/role.py"
with open(path_role, "r") as f:
    content = f.read()

# Since the table structure might have spaces/tabs, lets use re.sub
new_table = """role_permission = Table(
    "rol_permiso",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("configuracion.roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("configuracion.permisos.id", ondelete="CASCADE"), primary_key=True),
    schema="configuracion"
)"""

content = re.sub(r'role_permission = Table\(.*?\)', new_table, content, flags=re.DOTALL)
content = content.replace('__tablename__ = "roles"', '__tablename__ = "roles"')
content = content.replace('__table_args__ = {"schema": "administracion"}', '__table_args__ = {"schema": "configuracion"}')
with open(path_role, "w") as f:
    f.write(content)

# 3. Update Permission Model
path_perm = "app/models/permission.py"
with open(path_perm, "r") as f:
    content = f.read()
content = content.replace('__tablename__ = "permissions"', '__tablename__ = "permisos"')
content = content.replace('__table_args__ = {"schema": "administracion"}', '__table_args__ = {"schema": "configuracion"}')
with open(path_perm, "w") as f:
    f.write(content)

# 4. Update Administrativo - Personal Model FK
path_admin = "app/models/administrativo.py"
with open(path_admin, "r") as f:
    content = f.read()
content = content.replace('ForeignKey("administracion.users.id"', 'ForeignKey("configuracion.usuarios.id"')
with open(path_admin, "w") as f:
    f.write(content)

# 5. Update Mixins (creado_por_id, actualizado_por_id)
path_mix = "app/models/mixins.py"
with open(path_mix, "r") as f:
    content = f.read()
content = content.replace('ForeignKey("administracion.users.id"', 'ForeignKey("configuracion.usuarios.id"')
with open(path_mix, "w") as f:
    f.write(content)

# 6. Update Contratacion - Proceso FK
path_contra = "app/models/contratacion.py"
with open(path_contra, "r") as f:
    content = f.read()
content = content.replace('ForeignKey("administracion.users.id"', 'ForeignKey("configuracion.usuarios.id"')
with open(path_contra, "w") as f:
    f.write(content)
