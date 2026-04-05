"""YXP-48: tablas SPI tesoreria archivo_spi linea_spi

Revision ID: 6d89a0d673fd
Revises: a3b7c9d2e1f4
Create Date: 2026-04-05

"""
from alembic import op
import sqlalchemy as sa


revision = '6d89a0d673fd'
down_revision = 'a3b7c9d2e1f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Tabla cabecera de lotes SPI
    op.create_table(
        'archivo_spi',
        sa.Column('id_archivo_spi', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('numero_lote', sa.String(length=30), nullable=False),
        sa.Column('fecha_envio', sa.Date(), nullable=True),
        sa.Column('estado', sa.String(length=20), nullable=False, server_default='BORRADOR'),
        sa.Column('monto_total', sa.Numeric(precision=18, scale=2), nullable=False, server_default='0'),
        sa.Column('id_cuenta_bancaria', sa.Integer(), nullable=False),
        sa.Column('tipo_pago', sa.String(length=20), nullable=False),
        sa.Column('ruta_archivo', sa.String(length=500), nullable=True),
        sa.Column('nombre_archivo', sa.String(length=200), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('creado_por_id', sa.Integer(), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), nullable=True),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['id_cuenta_bancaria'], ['tesoreria.cuentas_bancarias.id'],
                                ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['creado_por_id'], ['configuracion.usuarios.id'],
                                ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['actualizado_por_id'], ['configuracion.usuarios.id'],
                                ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id_archivo_spi'),
        sa.UniqueConstraint('numero_lote', name='uq_archivo_spi_numero_lote'),
        schema='tesoreria',
    )
    op.create_index(
        'ix_tesoreria_archivo_spi_numero_lote',
        'archivo_spi', ['numero_lote'], unique=False, schema='tesoreria'
    )

    # Tabla líneas de archivos SPI
    op.create_table(
        'linea_spi',
        sa.Column('id_linea_spi', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('id_archivo_spi', sa.BigInteger(), nullable=False),
        sa.Column('ruc_beneficiario', sa.String(length=20), nullable=False),
        sa.Column('nombre_beneficiario', sa.String(length=200), nullable=False),
        sa.Column('banco_destino', sa.String(length=100), nullable=False),
        sa.Column('cuenta_destino', sa.String(length=30), nullable=False),
        sa.Column('tipo_cuenta', sa.String(length=20), nullable=False, server_default='CORRIENTE'),
        sa.Column('valor', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('referencia', sa.String(length=50), nullable=True),
        sa.Column('descripcion', sa.String(length=200), nullable=True),
        sa.Column('estado', sa.String(length=20), nullable=False, server_default='PENDIENTE'),
        sa.Column('origen_tipo', sa.String(length=10), nullable=False, server_default='OTRO'),
        sa.Column('origen_id', sa.BigInteger(), nullable=True),
        sa.Column('creado_por_id', sa.Integer(), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['id_archivo_spi'], ['tesoreria.archivo_spi.id_archivo_spi'],
                                ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['creado_por_id'], ['configuracion.usuarios.id'],
                                ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['actualizado_por_id'], ['configuracion.usuarios.id'],
                                ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id_linea_spi'),
        schema='tesoreria',
    )


def downgrade() -> None:
    op.drop_table('linea_spi', schema='tesoreria')
    op.drop_index('ix_tesoreria_archivo_spi_numero_lote', table_name='archivo_spi', schema='tesoreria')
    op.drop_table('archivo_spi', schema='tesoreria')
