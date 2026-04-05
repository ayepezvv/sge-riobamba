"""c005b — Fix check constraints para compatibilidad con datos MySQL heredados

Revision ID: c005b_fix_check_constraints
Revises: c005_mysql_presupuesto_compat
Create Date: 2026-04-05

MySQL permite montos = 0 en certificaciones y compromisos (registros cancelados).
También: id_certificado puede ser NULL en compromisos sin certificado previo.
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "c005b_fix_check_constraints"
down_revision: Union[str, Sequence[str], None] = "c005_mysql_presupuesto_compat"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # Permitir monto_certificado = 0 (certifs canceladas en MySQL)
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.certificados_presupuestarios
            DROP CONSTRAINT IF EXISTS certificados_presupuestarios_monto_certificado_check
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.certificados_presupuestarios
            ADD CONSTRAINT certificados_presupuestarios_monto_certificado_check
            CHECK (monto_certificado >= 0)
    """))

    # Permitir monto_comprometido = 0 (ejecucio sin monto comprometido en MySQL)
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.compromisos
            DROP CONSTRAINT IF EXISTS compromisos_monto_comprometido_check
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.compromisos
            ADD CONSTRAINT compromisos_monto_comprometido_check
            CHECK (monto_comprometido >= 0)
    """))

    # id_certificado nullable — ejecucio con SINCERTI=1 no tienen certificado
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.compromisos
            ALTER COLUMN id_certificado DROP NOT NULL
    """))

    # Ampliar concepto en compromisos a 2000 chars (glosas largas MySQL)
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.compromisos
            ALTER COLUMN concepto TYPE VARCHAR(2000)
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.certificados_presupuestarios
            ALTER COLUMN concepto TYPE VARCHAR(2000)
    """))


def downgrade() -> None:
    conn = op.get_bind()

    conn.execute(sa.text("""
        ALTER TABLE presupuesto.compromisos
            ALTER COLUMN concepto TYPE VARCHAR(500)
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.certificados_presupuestarios
            ALTER COLUMN concepto TYPE VARCHAR(500)
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.compromisos
            ALTER COLUMN id_certificado SET NOT NULL
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.compromisos
            DROP CONSTRAINT IF EXISTS compromisos_monto_comprometido_check
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.compromisos
            ADD CONSTRAINT compromisos_monto_comprometido_check
            CHECK (monto_comprometido > 0)
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.certificados_presupuestarios
            DROP CONSTRAINT IF EXISTS certificados_presupuestarios_monto_certificado_check
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.certificados_presupuestarios
            ADD CONSTRAINT certificados_presupuestarios_monto_certificado_check
            CHECK (monto_certificado > 0)
    """))
