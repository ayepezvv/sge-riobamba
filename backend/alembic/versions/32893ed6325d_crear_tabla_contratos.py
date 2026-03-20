"""Crear tabla contratos

Revision ID: 32893ed6325d
Revises: a1b2c3d4e5f7
Create Date: 2026-03-16 20:33:10.505464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '32893ed6325d'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('contrato',
    sa.Column('id_contrato', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('id_empleado', sa.BigInteger(), nullable=False),
    sa.Column('id_escala_salarial', sa.BigInteger(), nullable=True),
    sa.Column('id_cargo', sa.BigInteger(), nullable=False),
    sa.Column('tipo_contrato', sa.String(length=50), nullable=False),
    sa.Column('fecha_inicio', sa.Date(), nullable=False),
    sa.Column('fecha_fin', sa.Date(), nullable=True),
    sa.Column('sueldo_pactado', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('estado_contrato', sa.String(length=20), nullable=True),
    sa.Column('observaciones', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['id_cargo'], ['rrhh.cargo.id_cargo'], ),
    sa.ForeignKeyConstraint(['id_empleado'], ['rrhh.empleado.id_empleado'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_escala_salarial'], ['rrhh.escala_salarial.id_escala'], ),
    sa.PrimaryKeyConstraint('id_contrato'),
    schema='rrhh'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('contrato', schema='rrhh')
