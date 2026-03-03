from app.db.session import SessionLocal
from app.models.permission import Permission

db = SessionLocal()
perms = ["crear_usuario", "editar_usuario", "eliminar_usuario", "gestionar_roles", "anular_factura", "crear_contrato"]
for p in perms:
    if not db.query(Permission).filter_by(nombre_permiso=p).first():
        db.add(Permission(nombre_permiso=p))
db.commit()
db.close()
print("Permisos iniciales inyectados.")
