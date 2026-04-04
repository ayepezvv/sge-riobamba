"""c004 — Parámetros contables para auto-asientos (YXP-21)

Revision ID: c004_parametros_contables_auto_asientos
Revises: c003_modulo_presupuesto
Create Date: 2026-04-04

Regla 1: tabla en schema contabilidad (nunca en public)
Regla 2: nomenclatura en español
Objetivo: tabla parametros_contables para configurar cuentas/diarios
          usados en la generación automática de asientos contables.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "c004"
down_revision: Union[str, None] = "c003_modulo_presupuesto"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # El schema contabilidad ya debe existir (creado en c001)
    # pero por seguridad lo aseguramos
    conn.execute(sa.text("CREATE SCHEMA IF NOT EXISTS contabilidad"))

    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS contabilidad.parametros_contables (
            id                  SERIAL PRIMARY KEY,
            clave               VARCHAR(50)     NOT NULL,
            descripcion         VARCHAR(255),
            cuenta_id           INTEGER         REFERENCES contabilidad.cuentas_contables(id) ON DELETE RESTRICT,
            diario_id           INTEGER         REFERENCES contabilidad.diarios(id) ON DELETE RESTRICT,
            creado_por_id       INTEGER         REFERENCES configuracion.usuarios(id) ON DELETE SET NULL,
            actualizado_por_id  INTEGER         REFERENCES configuracion.usuarios(id) ON DELETE SET NULL,
            creado_en           TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            actualizado_en      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            CONSTRAINT uq_parametros_contables_clave UNIQUE (clave)
        )
    """))

    # Índice para búsqueda rápida por clave
    conn.execute(sa.text("""
        CREATE INDEX IF NOT EXISTS ix_parametros_contables_clave
        ON contabilidad.parametros_contables (clave)
    """))

    # Insertar claves predefinidas (sin valores — el admin las configura)
    claves_default = [
        ("CUENTA_CXC",             "Cuenta por cobrar (AR) por defecto"),
        ("CUENTA_CXP",             "Cuenta por pagar (AP) por defecto"),
        ("CUENTA_IVA_COBRADO",     "IVA en ventas (15/12%)"),
        ("CUENTA_IVA_PAGADO",      "IVA en compras (15/12%)"),
        ("CUENTA_CAJA_RECAUDACION","Caja de recaudación diaria"),
        ("CUENTA_BCE_CUT",         "Cuenta Única del Tesoro - BCE"),
        ("DIARIO_VENTAS",          "Diario para facturas de venta"),
        ("DIARIO_COMPRAS",         "Diario para facturas de compra"),
        ("DIARIO_BANCO",           "Diario para pagos/cobros bancarios"),
        ("DIARIO_CAJA",            "Diario para operaciones de caja"),
        ("DIARIO_PRESUPUESTO",     "Diario para asientos de ejecución presupuestaria"),
    ]
    for clave, descripcion in claves_default:
        conn.execute(sa.text("""
            INSERT INTO contabilidad.parametros_contables (clave, descripcion)
            VALUES (:clave, :descripcion)
            ON CONFLICT (clave) DO NOTHING
        """), {"clave": clave, "descripcion": descripcion})


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text(
        "DROP TABLE IF EXISTS contabilidad.parametros_contables CASCADE"
    ))
