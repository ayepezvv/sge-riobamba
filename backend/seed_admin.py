from app.db.session import SessionLocal
from app.models.role import Role
from app.models.user import User
from app.core.security import get_password_hash

def seed():
    db = SessionLocal()
    # Check if SuperAdmin role exists
    role = db.query(Role).filter(Role.nombre_rol == "SuperAdmin").first()
    if not role:
        role = Role(nombre_rol="SuperAdmin", descripcion="Administrador total del sistema")
        db.add(role)
        db.commit()
        db.refresh(role)
        print("Rol SuperAdmin creado.")
    
    # Check if admin user exists
    user = db.query(User).filter(User.correo == "admin@riobambaep.gob.ec").first()
    if not user:
        user = User(
            cedula="0000000000",
            nombres="Admin",
            apellidos="SGE",
            correo="admin@riobambaep.gob.ec",
            hashed_password=get_password_hash("Admin123*"),
            is_active=True,
            role_id=role.id
        )
        db.add(user)
        db.commit()
        print("Usuario administrador creado: admin@riobambaep.gob.ec / Admin123*")
    else:
        print("El usuario administrador ya existe.")
    
    db.close()

if __name__ == "__main__":
    print("Iniciando seed de base de datos...")
    seed()
    print("Seed finalizado.")
