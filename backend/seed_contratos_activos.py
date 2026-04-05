"""
Seed: Contratos activos para habilitar cálculo de nómina (YXP-51)
Crea contratos ACTIVOS para los primeros 15 empleados activos.
"""
from app.db.session import SessionLocal
from app.models.rrhh import Contrato, Empleado, EscalaSalarial, Cargo
import sqlalchemy as sa
from datetime import date

db = SessionLocal()

# Get first 15 active employees without existing ACTIVO contracts
existing = db.execute(sa.text(
    "SELECT id_empleado FROM rrhh.contrato WHERE estado_contrato = 'ACTIVO'"
)).fetchall()
existing_ids = {r[0] for r in existing}

empleados = db.execute(sa.text(
    "SELECT id_empleado FROM rrhh.empleado "
    "WHERE estado_empleado='ACTIVO' AND eliminado_en IS NULL "
    "ORDER BY id_empleado LIMIT 20"
)).fetchall()

# Get first escala and cargo
escala = db.execute(sa.text("SELECT id_escala, salario_base FROM rrhh.escala_salarial LIMIT 1")).fetchone()
cargo = db.execute(sa.text("SELECT id_cargo FROM rrhh.cargo LIMIT 1")).fetchone()

created = 0
for emp in empleados:
    emp_id = emp[0]
    if emp_id in existing_ids:
        continue
    if created >= 15:
        break
    contrato = Contrato(
        id_empleado=emp_id,
        id_escala_salarial=escala[0],
        id_cargo=cargo[0] if cargo else None,
        tipo_contrato="NOMBRAMIENTO",
        fecha_inicio=date(2024, 1, 1),
        fecha_fin=None,
        sueldo_pactado=float(escala[1]),
        estado_contrato="ACTIVO",
        observaciones="Seed automático YXP-51",
    )
    db.add(contrato)
    created += 1

db.commit()
print(f"[OK] {created} contratos ACTIVOS creados.")

total = db.execute(sa.text(
    "SELECT COUNT(*) FROM rrhh.contrato WHERE estado_contrato='ACTIVO'"
)).scalar()
print(f"[OK] Total contratos ACTIVOS en DB: {total}")

db.close()
