from sqlalchemy import create_session, select
from app.db.session import SessionLocal
from app.models.administrativo import Empleado
from app.models.informatica import DireccionIpAsignada

def test_cross_schema_relation():
    db = SessionLocal()
    try:
        print("--- Iniciando Prueba de Relación Cruzada ---")
        
        # 1. Buscar un empleado
        empleado = db.query(Empleado).first()
        if not empleado:
            print("[INFO] No hay empleados para probar. Por favor, ejecute una semilla.")
            return

        print(f"[TEST] Empleado encontrado: {empleado.nombres} {empleado.apellidos} (ID: {empleado.id})")

        # 2. Buscar IPs vinculadas a este empleado
        ips = db.query(DireccionIpAsignada).filter(DireccionIpAsignada.personal_id == empleado.id).all()
        
        print(f"[TEST] IPs asignadas en esquema 'informatica' para este empleado: {len(ips)}")
        for ip in ips:
            print(f"   - IP: {ip.direccion_ip} | Equipo: {ip.nombre_equipo}")
            
        print("--- Prueba Finalizada Exitosamente ---")
        
    except Exception as e:
        print(f"[ERROR] Falló la validación cross-schema: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    test_cross_schema_relation()
