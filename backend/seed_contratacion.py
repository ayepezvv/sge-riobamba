from app.db.session import SessionLocal
from app.models.contratacion import TipoProceso, PlantillaDocumento

db = SessionLocal()
if not db.query(TipoProceso).first():
    tp = TipoProceso(nombre="Subasta Inversa Electronica")
    db.add(tp)
    db.commit()
    db.refresh(tp)
    
    pl = PlantillaDocumento(
        nombre="TDR Estandar", 
        ruta_archivo_docx="templates/contratacion/dummy_template.docx",
        tipo_proceso_id=tp.id
    )
    db.add(pl)
    db.commit()

db.close()
