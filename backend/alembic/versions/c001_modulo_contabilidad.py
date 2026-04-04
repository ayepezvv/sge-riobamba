"""Modulo contabilidad: esquema, tipos de cuenta, cuentas contables, diarios, periodos, asientos

Revision ID: c001_modulo_contabilidad
Revises: 32893ed6325d
Create Date: 2026-04-04 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'c001_modulo_contabilidad'
down_revision: Union[str, Sequence[str], None] = '32893ed6325d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Crear esquema
    op.execute("CREATE SCHEMA IF NOT EXISTS contabilidad")

    # 2. tipos_cuenta
    op.create_table(
        'tipos_cuenta',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('codigo', sa.String(length=10), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('naturaleza', sa.String(length=10), nullable=False,
                  comment='DEUDORA o ACREEDORA'),
        sa.Column('descripcion', sa.String(length=255), nullable=True),
        # AuditMixin
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo', name='uq_tipos_cuenta_codigo'),
        schema='contabilidad',
    )
    op.create_index('ix_contabilidad_tipos_cuenta_id', 'tipos_cuenta', ['id'], schema='contabilidad')

    # 3. cuentas_contables
    op.create_table(
        'cuentas_contables',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('codigo', sa.String(length=50), nullable=False),
        sa.Column('nombre', sa.String(length=200), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('tipo_cuenta_id', sa.Integer(), sa.ForeignKey('contabilidad.tipos_cuenta.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('cuenta_padre_id', sa.Integer(), sa.ForeignKey('contabilidad.cuentas_contables.id', ondelete='RESTRICT'), nullable=True),
        sa.Column('nivel', sa.Integer(), nullable=False),
        sa.Column('es_hoja', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('permite_movimientos', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('partida_presupuestaria', sa.String(length=100), nullable=True),
        sa.Column('estado', sa.String(length=10), nullable=False, server_default='ACTIVA'),
        # AuditMixin
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo', name='uq_cuentas_contables_codigo'),
        sa.CheckConstraint('nivel BETWEEN 1 AND 10', name='chk_nivel_cuenta'),
        schema='contabilidad',
    )
    op.create_index('ix_contabilidad_cuentas_contables_id', 'cuentas_contables', ['id'], schema='contabilidad')
    op.create_index('ix_contabilidad_cuentas_contables_codigo', 'cuentas_contables', ['codigo'], schema='contabilidad')

    # 4. diarios
    op.create_table(
        'diarios',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('codigo', sa.String(length=20), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('tipo', sa.String(length=20), nullable=False, server_default='GENERAL'),
        sa.Column('cuenta_default_id', sa.Integer(), sa.ForeignKey('contabilidad.cuentas_contables.id', ondelete='SET NULL'), nullable=True),
        sa.Column('es_activo', sa.Boolean(), nullable=False, server_default='true'),
        # AuditMixin
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo', name='uq_diarios_codigo'),
        schema='contabilidad',
    )
    op.create_index('ix_contabilidad_diarios_id', 'diarios', ['id'], schema='contabilidad')

    # 5. periodos_contables
    op.create_table(
        'periodos_contables',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('anio', sa.Integer(), nullable=False),
        sa.Column('mes', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=50), nullable=False),
        sa.Column('fecha_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_fin', sa.Date(), nullable=False),
        sa.Column('estado', sa.String(length=10), nullable=False, server_default='ABIERTO'),
        # AuditMixin
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('anio', 'mes', name='uq_periodos_anio_mes'),
        sa.CheckConstraint('mes BETWEEN 1 AND 12', name='chk_mes_periodo'),
        schema='contabilidad',
    )
    op.create_index('ix_contabilidad_periodos_contables_id', 'periodos_contables', ['id'], schema='contabilidad')

    # 6. asientos_contables
    op.create_table(
        'asientos_contables',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('numero', sa.String(length=30), nullable=False),
        sa.Column('diario_id', sa.Integer(), sa.ForeignKey('contabilidad.diarios.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('periodo_id', sa.Integer(), sa.ForeignKey('contabilidad.periodos_contables.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('referencia', sa.String(length=100), nullable=True),
        sa.Column('concepto', sa.Text(), nullable=False),
        sa.Column('estado', sa.String(length=10), nullable=False, server_default='BORRADOR'),
        sa.Column('total_debe', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('total_haber', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('fecha_publicacion', sa.DateTime(timezone=True), nullable=True),
        sa.Column('motivo_anulacion', sa.Text(), nullable=True),
        # AuditMixin
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('numero', name='uq_asientos_numero'),
        schema='contabilidad',
    )
    op.create_index('ix_contabilidad_asientos_contables_id', 'asientos_contables', ['id'], schema='contabilidad')
    op.create_index('ix_contabilidad_asientos_contables_numero', 'asientos_contables', ['numero'], schema='contabilidad')

    # 7. lineas_asiento
    op.create_table(
        'lineas_asiento',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('asiento_id', sa.Integer(), sa.ForeignKey('contabilidad.asientos_contables.id', ondelete='CASCADE'), nullable=False),
        sa.Column('cuenta_id', sa.Integer(), sa.ForeignKey('contabilidad.cuentas_contables.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('descripcion', sa.String(length=255), nullable=True),
        sa.Column('debe', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('haber', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('orden', sa.Integer(), nullable=False, server_default='1'),
        # AuditMixin
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint(
            '(debe >= 0 AND haber >= 0) AND NOT (debe > 0 AND haber > 0)',
            name='chk_linea_debe_o_haber'
        ),
        schema='contabilidad',
    )
    op.create_index('ix_contabilidad_lineas_asiento_id', 'lineas_asiento', ['id'], schema='contabilidad')


def downgrade() -> None:
    op.drop_table('lineas_asiento', schema='contabilidad')
    op.drop_table('asientos_contables', schema='contabilidad')
    op.drop_table('periodos_contables', schema='contabilidad')
    op.drop_table('diarios', schema='contabilidad')
    op.drop_table('cuentas_contables', schema='contabilidad')
    op.drop_table('tipos_cuenta', schema='contabilidad')
    op.execute("DROP SCHEMA IF EXISTS contabilidad CASCADE")
