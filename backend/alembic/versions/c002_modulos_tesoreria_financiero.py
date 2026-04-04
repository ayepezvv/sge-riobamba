"""Módulos Tesorería y Financiero (AR/AP): schemas, modelos completos

Revision ID: c002_modulos_tesoreria_financiero
Revises: c001_modulo_contabilidad
Create Date: 2026-04-04 00:01:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'c002_tesoreria_financiero'
down_revision: Union[str, None] = 'c001_modulo_contabilidad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # =========================================================================
    # SCHEMA: tesoreria
    # =========================================================================
    op.execute("CREATE SCHEMA IF NOT EXISTS tesoreria")

    # --- entidades_bancarias ---
    op.create_table(
        'entidades_bancarias',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('codigo', sa.String(20), nullable=False),
        sa.Column('nombre', sa.String(150), nullable=False),
        sa.Column('sigla', sa.String(20), nullable=True),
        sa.Column('es_activa', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.UniqueConstraint('codigo', name='uq_entidades_bancarias_codigo'),
        schema='tesoreria',
    )

    # --- cuentas_bancarias ---
    op.create_table(
        'cuentas_bancarias',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('entidad_bancaria_id', sa.Integer(), sa.ForeignKey('tesoreria.entidades_bancarias.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('numero_cuenta', sa.String(50), nullable=False),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('tipo', sa.String(20), nullable=False, server_default='CORRIENTE'),
        sa.Column('moneda', sa.String(3), nullable=False, server_default='USD'),
        sa.Column('cuenta_contable_id', sa.Integer(), sa.ForeignKey('contabilidad.cuentas_contables.id', ondelete='SET NULL'), nullable=True),
        sa.Column('saldo_inicial', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('es_activa', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.UniqueConstraint('numero_cuenta', name='uq_cuentas_bancarias_numero'),
        schema='tesoreria',
    )

    # --- extractos_bancarios ---
    op.create_table(
        'extractos_bancarios',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('cuenta_bancaria_id', sa.Integer(), sa.ForeignKey('tesoreria.cuentas_bancarias.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('referencia', sa.String(100), nullable=True),
        sa.Column('fecha_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_fin', sa.Date(), nullable=False),
        sa.Column('saldo_inicial', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('saldo_final', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('estado', sa.String(15), nullable=False, server_default='BORRADOR'),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.UniqueConstraint('cuenta_bancaria_id', 'fecha_inicio', 'fecha_fin', name='uq_extracto_cuenta_periodo'),
        schema='tesoreria',
    )

    # --- lineas_extracto ---
    op.create_table(
        'lineas_extracto',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('extracto_id', sa.Integer(), sa.ForeignKey('tesoreria.extractos_bancarios.id', ondelete='CASCADE'), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('tipo_transaccion', sa.String(20), nullable=False, server_default='OTRO'),
        sa.Column('referencia', sa.String(100), nullable=True),
        sa.Column('descripcion', sa.String(500), nullable=True),
        sa.Column('valor', sa.Numeric(18, 2), nullable=False),
        sa.Column('esta_conciliada', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        schema='tesoreria',
    )

    # --- conciliaciones_bancarias ---
    op.create_table(
        'conciliaciones_bancarias',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('cuenta_bancaria_id', sa.Integer(), sa.ForeignKey('tesoreria.cuentas_bancarias.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('extracto_id', sa.Integer(), sa.ForeignKey('tesoreria.extractos_bancarios.id', ondelete='RESTRICT'), nullable=True),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('fecha_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_fin', sa.Date(), nullable=False),
        sa.Column('saldo_libro', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('saldo_banco', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('diferencia', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('estado', sa.String(10), nullable=False, server_default='ABIERTO'),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        schema='tesoreria',
    )

    # --- marcas_conciliacion ---
    op.create_table(
        'marcas_conciliacion',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('conciliacion_id', sa.Integer(), sa.ForeignKey('tesoreria.conciliaciones_bancarias.id', ondelete='CASCADE'), nullable=False),
        sa.Column('linea_extracto_id', sa.Integer(), sa.ForeignKey('tesoreria.lineas_extracto.id', ondelete='CASCADE'), nullable=False),
        sa.Column('asiento_contable_id', sa.Integer(), sa.ForeignKey('contabilidad.asientos_contables.id', ondelete='SET NULL'), nullable=True),
        sa.Column('valor_conciliado', sa.Numeric(18, 2), nullable=False),
        sa.Column('observacion', sa.String(255), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.UniqueConstraint('linea_extracto_id', name='uq_marca_linea_extracto'),
        schema='tesoreria',
    )

    # --- cajas_chicas ---
    op.create_table(
        'cajas_chicas',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('codigo', sa.String(20), nullable=False),
        sa.Column('nombre', sa.String(150), nullable=False),
        sa.Column('monto_fijo', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('monto_disponible', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('cuenta_contable_id', sa.Integer(), sa.ForeignKey('contabilidad.cuentas_contables.id', ondelete='SET NULL'), nullable=True),
        sa.Column('responsable_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('estado', sa.String(10), nullable=False, server_default='CERRADA'),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.UniqueConstraint('codigo', name='uq_cajas_chicas_codigo'),
        schema='tesoreria',
    )

    # --- movimientos_caja ---
    op.create_table(
        'movimientos_caja',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('caja_id', sa.Integer(), sa.ForeignKey('tesoreria.cajas_chicas.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('tipo', sa.String(15), nullable=False),
        sa.Column('concepto', sa.String(500), nullable=False),
        sa.Column('monto', sa.Numeric(18, 2), nullable=False),
        sa.Column('numero_comprobante', sa.String(50), nullable=True),
        sa.Column('beneficiario', sa.String(200), nullable=True),
        sa.Column('asiento_contable_id', sa.Integer(), sa.ForeignKey('contabilidad.asientos_contables.id', ondelete='SET NULL'), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.CheckConstraint('monto > 0', name='chk_movimiento_monto_positivo'),
        schema='tesoreria',
    )

    # =========================================================================
    # SCHEMA: financiero
    # =========================================================================
    op.execute("CREATE SCHEMA IF NOT EXISTS financiero")

    # --- tipos_documento ---
    op.create_table(
        'tipos_documento',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('codigo', sa.String(10), nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('tipo', sa.String(30), nullable=False),
        sa.Column('secuencia_prefijo', sa.String(10), nullable=True),
        sa.Column('secuencia_siguiente', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('es_activo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.UniqueConstraint('codigo', name='uq_tipos_documento_codigo'),
        schema='financiero',
    )

    # --- facturas ---
    op.create_table(
        'facturas',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('numero', sa.String(50), nullable=False),
        sa.Column('tipo_documento_id', sa.Integer(), sa.ForeignKey('financiero.tipos_documento.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('tipo', sa.String(15), nullable=False),
        sa.Column('estado', sa.String(10), nullable=False, server_default='BORRADOR'),
        sa.Column('tercero_id', sa.Integer(), nullable=True),
        sa.Column('nombre_tercero', sa.String(200), nullable=False),
        sa.Column('identificacion_tercero', sa.String(20), nullable=False),
        sa.Column('fecha_emision', sa.Date(), nullable=False),
        sa.Column('fecha_vencimiento', sa.Date(), nullable=True),
        sa.Column('subtotal', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('descuento', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('base_imponible', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('total_iva', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('total', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('saldo_pendiente', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('clave_acceso_sri', sa.String(49), nullable=True),
        sa.Column('numero_autorizacion_sri', sa.String(49), nullable=True),
        sa.Column('asiento_contable_id', sa.Integer(), sa.ForeignKey('contabilidad.asientos_contables.id', ondelete='SET NULL'), nullable=True),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.Column('motivo_anulacion', sa.Text(), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.UniqueConstraint('numero', name='uq_facturas_numero'),
        schema='financiero',
    )

    # --- lineas_factura ---
    op.create_table(
        'lineas_factura',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('factura_id', sa.Integer(), sa.ForeignKey('financiero.facturas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('orden', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('descripcion', sa.String(500), nullable=False),
        sa.Column('cuenta_contable_id', sa.Integer(), sa.ForeignKey('contabilidad.cuentas_contables.id', ondelete='RESTRICT'), nullable=True),
        sa.Column('cantidad', sa.Numeric(18, 4), nullable=False, server_default='1'),
        sa.Column('precio_unitario', sa.Numeric(18, 4), nullable=False, server_default='0'),
        sa.Column('descuento_linea', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('tipo_impuesto', sa.String(10), nullable=False, server_default='IVA_15'),
        sa.Column('porcentaje_impuesto', sa.Numeric(5, 2), nullable=False, server_default='15'),
        sa.Column('subtotal_linea', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('valor_impuesto', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('total_linea', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.CheckConstraint('cantidad > 0', name='chk_linea_factura_cantidad_positiva'),
        sa.CheckConstraint('precio_unitario >= 0', name='chk_linea_factura_precio_no_negativo'),
        schema='financiero',
    )

    # --- pagos ---
    op.create_table(
        'pagos',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('numero', sa.String(50), nullable=False),
        sa.Column('tipo', sa.String(15), nullable=False),
        sa.Column('estado', sa.String(15), nullable=False, server_default='BORRADOR'),
        sa.Column('tercero_id', sa.Integer(), nullable=True),
        sa.Column('nombre_tercero', sa.String(200), nullable=False),
        sa.Column('identificacion_tercero', sa.String(20), nullable=False),
        sa.Column('fecha_pago', sa.Date(), nullable=False),
        sa.Column('tipo_pago', sa.String(20), nullable=False, server_default='TRANSFERENCIA'),
        sa.Column('cuenta_bancaria_id', sa.Integer(), sa.ForeignKey('tesoreria.cuentas_bancarias.id', ondelete='SET NULL'), nullable=True),
        sa.Column('monto_total', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('referencia_bancaria', sa.String(100), nullable=True),
        sa.Column('asiento_contable_id', sa.Integer(), sa.ForeignKey('contabilidad.asientos_contables.id', ondelete='SET NULL'), nullable=True),
        sa.Column('asiento_traslado_id', sa.Integer(), sa.ForeignKey('contabilidad.asientos_contables.id', ondelete='SET NULL'), nullable=True),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.Column('motivo_anulacion', sa.Text(), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.UniqueConstraint('numero', name='uq_pagos_numero'),
        schema='financiero',
    )

    # --- lineas_pago ---
    op.create_table(
        'lineas_pago',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('pago_id', sa.Integer(), sa.ForeignKey('financiero.pagos.id', ondelete='CASCADE'), nullable=False),
        sa.Column('factura_id', sa.Integer(), sa.ForeignKey('financiero.facturas.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('monto_aplicado', sa.Numeric(18, 2), nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.CheckConstraint('monto_aplicado > 0', name='chk_linea_pago_monto_positivo'),
        schema='financiero',
    )

    # --- cierres_recaudacion ---
    op.create_table(
        'cierres_recaudacion',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('fecha', sa.Date(), nullable=False, unique=True),
        sa.Column('total_recaudado', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('numero_transacciones', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('asiento_recaudacion_id', sa.Integer(), sa.ForeignKey('contabilidad.asientos_contables.id', ondelete='SET NULL'), nullable=True),
        sa.Column('asiento_traslado_bce_id', sa.Integer(), sa.ForeignKey('contabilidad.asientos_contables.id', ondelete='SET NULL'), nullable=True),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('creado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.Integer(), sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.UniqueConstraint('fecha', name='uq_cierre_recaudacion_fecha'),
        schema='financiero',
    )

    # Indexes for performance
    op.create_index('ix_lineas_extracto_extracto_id', 'lineas_extracto', ['extracto_id'], schema='tesoreria')
    op.create_index('ix_conciliaciones_cuenta_id', 'conciliaciones_bancarias', ['cuenta_bancaria_id'], schema='tesoreria')
    op.create_index('ix_facturas_numero', 'facturas', ['numero'], schema='financiero')
    op.create_index('ix_facturas_identificacion', 'facturas', ['identificacion_tercero'], schema='financiero')
    op.create_index('ix_pagos_numero', 'pagos', ['numero'], schema='financiero')


def downgrade() -> None:
    # financiero
    op.drop_table('cierres_recaudacion', schema='financiero')
    op.drop_table('lineas_pago', schema='financiero')
    op.drop_table('pagos', schema='financiero')
    op.drop_table('lineas_factura', schema='financiero')
    op.drop_table('facturas', schema='financiero')
    op.drop_table('tipos_documento', schema='financiero')
    op.execute("DROP SCHEMA IF EXISTS financiero")
    # tesoreria
    op.drop_table('movimientos_caja', schema='tesoreria')
    op.drop_table('cajas_chicas', schema='tesoreria')
    op.drop_table('marcas_conciliacion', schema='tesoreria')
    op.drop_table('conciliaciones_bancarias', schema='tesoreria')
    op.drop_table('lineas_extracto', schema='tesoreria')
    op.drop_table('extractos_bancarios', schema='tesoreria')
    op.drop_table('cuentas_bancarias', schema='tesoreria')
    op.drop_table('entidades_bancarias', schema='tesoreria')
    op.execute("DROP SCHEMA IF EXISTS tesoreria")
