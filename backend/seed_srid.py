from app.db.session import SessionLocal
from app.models.parametro import ParametroSistema

db = SessionLocal()
if not db.query(ParametroSistema).filter_by(clave='SRID_LOCAL').first():
    db.add(ParametroSistema(
        clave='SRID_LOCAL',
        valor='32717',
        tipo_dato='int',
        descripcion='SRID para proyecciones metricas locales (Ej. UTM Zona 17S)'
    ))
db.commit()
db.close()
print("Parametro SRID_LOCAL sembrado exitosamente.")
