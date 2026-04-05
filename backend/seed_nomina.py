"""
Seed Nómina — YXP-51
Pobla:
  1. rrhh.impuesto_renta_escala — tabla progresiva IR 2026 (SRI Ecuador, 9 tramos)
  2. rrhh.parametro_calculo     — parámetros SBU, IESS y Fondos de Reserva 2026
  3. rrhh.rubro_nomina          — catálogo mínimo de rubros (si está vacío)

Ejecutar desde /backend/:
  python seed_nomina.py
"""
from app.db.session import SessionLocal
from app.models.rrhh import ImpuestoRentaEscala, ParametroCalculo, RubroNomina

db = SessionLocal()

# ---------------------------------------------------------------------------
# 1. TABLA PROGRESIVA IR 2026 — SRI Ecuador (Resolución NAC-DGER vigente)
#    9 tramos, fraccion_basica en dólares anuales.
#    Fuente: publicación SRI Ecuador tabla 2026 personas naturales.
# ---------------------------------------------------------------------------
IR_2026 = [
    # (fraccion_basica, exceso_hasta, impuesto_fb, porc_excedente)
    (       0.00,   11_902.00,      0.00,  0.00),
    (  11_902.00,   15_159.00,      0.00,  5.00),
    (  15_159.00,   19_682.00,    163.00, 10.00),
    (  19_682.00,   26_031.00,    615.00, 12.00),
    (  26_031.00,   34_255.00,  1_377.00, 15.00),
    (  34_255.00,   45_407.00,  2_611.00, 20.00),
    (  45_407.00,   60_450.00,  4_841.00, 25.00),
    (  60_450.00,  141_320.00,  8_602.00, 30.00),
    ( 141_320.00,        None, 32_863.00, 35.00),  # en adelante
]

ya_existe = db.query(ImpuestoRentaEscala).filter(
    ImpuestoRentaEscala.anio_vigencia == 2026
).count()

if ya_existe == 0:
    for fb, eu, ifb, pfe in IR_2026:
        db.add(ImpuestoRentaEscala(
            anio_vigencia=2026,
            fraccion_basica=fb,
            exceso_hasta=eu,
            impuesto_fraccion_basica=ifb,
            porcentaje_fraccion_excedente=pfe,
        ))
    db.commit()
    print(f"[OK] IR 2026: {len(IR_2026)} tramos insertados.")
else:
    print(f"[SKIP] IR 2026 ya tiene {ya_existe} registros.")

# ---------------------------------------------------------------------------
# 2. PARÁMETROS DE CÁLCULO 2026
# ---------------------------------------------------------------------------
PARAMETROS_2026 = [
    # (codigo, descripcion, valor_numerico)
    ("SBU",            "Salario Básico Unificado 2026",               490.00),
    ("IESS_PERSONAL",  "Aporte personal IESS 2026 (%)",                9.45),
    ("IESS_PATRONAL",  "Aporte patronal IESS 2026 (%)",               11.15),
    ("FONDOS_RESERVA", "Fondos de reserva IESS 2026 (%)",              8.33),
]

for codigo, desc, valor in PARAMETROS_2026:
    existe = db.query(ParametroCalculo).filter(
        ParametroCalculo.anio_vigencia == 2026,
        ParametroCalculo.codigo_parametro == codigo,
    ).first()
    if not existe:
        db.add(ParametroCalculo(
            anio_vigencia=2026,
            codigo_parametro=codigo,
            descripcion=desc,
            valor_numerico=valor,
            estado="ACTIVO",
        ))
        print(f"[OK] Parámetro {codigo} 2026 = {valor}")
    else:
        print(f"[SKIP] Parámetro {codigo} 2026 ya existe.")
db.commit()

# ---------------------------------------------------------------------------
# 3. RUBROS DE NÓMINA (catálogo mínimo si está vacío)
# ---------------------------------------------------------------------------
RUBROS = [
    # (codigo, nombre, naturaleza, tipo_valor, orden, es_imponible)
    ("001", "SUELDO BÁSICO",           "INGRESO",   "FIJO",       1,  True),
    ("010", "APORTE PERSONAL IESS",    "DESCUENTO", "PORCENTAJE", 10, True),
    ("020", "APORTE PATRONAL IESS",    "PROVISION", "PORCENTAJE", 20, True),
    ("030", "FONDOS DE RESERVA",       "PROVISION", "PORCENTAJE", 30, True),
    ("040", "DÉCIMO TERCERO",          "PROVISION", "FORMULA",    40, False),
    ("050", "DÉCIMO CUARTO",           "PROVISION", "FORMULA",    50, False),
    ("060", "IMPUESTO A LA RENTA",     "DESCUENTO", "FORMULA",    60, False),
]

rubros_existentes = db.query(RubroNomina).count()
if rubros_existentes == 0:
    for cod, nom, nat, tv, orden, imp in RUBROS:
        db.add(RubroNomina(
            codigo_rubro=cod,
            nombre=nom,
            naturaleza=nat,
            tipo_valor=tv,
            orden_ejecucion=orden,
            es_imponible=imp,
            estado="ACTIVO",
        ))
    db.commit()
    print(f"[OK] {len(RUBROS)} rubros de nómina insertados.")
else:
    print(f"[SKIP] Rubros ya existen: {rubros_existentes} registros.")

db.close()
print("\n[DONE] Seed nómina completado.")
