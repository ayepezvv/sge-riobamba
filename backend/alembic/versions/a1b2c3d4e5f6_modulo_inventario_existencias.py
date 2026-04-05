"""Modulo inventario existencias - schema inventario

Revision ID: a1b2c3d4e5f6
Revises: f52466dcba5e
Create Date: 2026-04-05 19:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "f52466dcba5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crear schema inventario
    op.execute("CREATE SCHEMA IF NOT EXISTS inventario")

    # Tabla: cuenta_contable
    op.create_table(
        "cuenta_contable",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("codigo_cuenta", sa.String(35), nullable=False),
        sa.Column("nombre_cuenta", sa.String(60), nullable=False),
        sa.Column("tipo_movimiento", sa.SmallInteger(), nullable=False),
        sa.Column("nivel", sa.SmallInteger(), nullable=False),
        sa.Column("cuenta_gasto", sa.String(35), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo_cuenta", name="uq_inv_cuenta_codigo"),
        schema="inventario",
    )
    op.create_index("ix_inv_cuenta_codigo", "cuenta_contable", ["codigo_cuenta"], schema="inventario")

    # Tabla: destino
    op.create_table(
        "destino",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("id_origen_mysql", sa.BigInteger(), nullable=True),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default="true"),
        sa.PrimaryKeyConstraint("id"),
        schema="inventario",
    )
    op.create_index("ix_inv_destino_origen", "destino", ["id_origen_mysql"], schema="inventario")

    # Tabla: encargado
    op.create_table(
        "encargado",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("id_origen_mysql", sa.BigInteger(), nullable=True),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("cedula", sa.String(10), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default="true"),
        sa.PrimaryKeyConstraint("id"),
        schema="inventario",
    )
    op.create_index("ix_inv_encargado_origen", "encargado", ["id_origen_mysql"], schema="inventario")

    # Tabla: proveedor
    op.create_table(
        "proveedor",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("id_origen_mysql", sa.BigInteger(), nullable=True),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("ruc_cedula", sa.String(13), nullable=True),
        sa.Column("direccion", sa.String(100), nullable=True),
        sa.Column("telefono", sa.String(15), nullable=True),
        sa.Column("contacto", sa.String(100), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default="true"),
        sa.PrimaryKeyConstraint("id"),
        schema="inventario",
    )
    op.create_index("ix_inv_proveedor_ruc", "proveedor", ["ruc_cedula"], schema="inventario")

    # Tabla: unidad_gestion
    op.create_table(
        "unidad_gestion",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("id_origen_mysql", sa.BigInteger(), nullable=True),
        sa.Column("codigo", sa.String(10), nullable=False),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("puede_mover", sa.Boolean(), nullable=False, server_default="true"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo", name="uq_inv_ug_codigo"),
        schema="inventario",
    )

    # Tabla: articulo
    op.create_table(
        "articulo",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("id_origen_mysql", sa.BigInteger(), nullable=True),
        sa.Column("codigo_articulo", sa.String(8), nullable=False),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("descripcion_extendida", sa.String(254), nullable=True),
        sa.Column("codigo_cuenta", sa.String(35), nullable=False),
        sa.Column("unidad_medida", sa.String(10), nullable=True),
        sa.Column("existencia_inicial", sa.Numeric(18, 2), nullable=True),
        sa.Column("costo_inicial", sa.Numeric(18, 4), nullable=True),
        sa.Column("existencia_actual", sa.Numeric(18, 4), nullable=True),
        sa.Column("costo_actual", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("valor_total", sa.Numeric(18, 4), nullable=True),
        sa.Column("stock_minimo", sa.Numeric(18, 2), nullable=True),
        sa.Column("stock_maximo", sa.Numeric(18, 2), nullable=True),
        sa.Column("codigo_barras", sa.String(45), nullable=True),
        sa.Column("anno_fiscal", sa.Integer(), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("usuario_crea", sa.String(50), nullable=True),
        sa.Column("creado_en", sa.DateTime(), nullable=True),
        sa.Column("usuario_modifica", sa.String(50), nullable=True),
        sa.Column("modificado_en", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["codigo_cuenta"], ["inventario.cuenta_contable.codigo_cuenta"],
            name="fk_articulo_cuenta"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo_articulo", "anno_fiscal", name="uq_inv_art_codigo_anno"),
        schema="inventario",
    )
    op.create_index("ix_inv_art_codigo", "articulo", ["codigo_articulo"], schema="inventario")
    op.create_index("ix_inv_art_anno", "articulo", ["anno_fiscal"], schema="inventario")
    op.create_index("ix_inv_art_origen", "articulo", ["id_origen_mysql"], schema="inventario")

    # Tabla: movimiento
    op.create_table(
        "movimiento",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("id_origen_mysql", sa.BigInteger(), nullable=True),
        sa.Column("numero_movimiento", sa.Integer(), nullable=False),
        sa.Column("fecha", sa.DateTime(), nullable=False),
        sa.Column("tipo_movimiento", sa.String(10), nullable=False),
        sa.Column("subtipo", sa.String(1), nullable=True),
        sa.Column("costo_total", sa.Numeric(18, 4), nullable=True),
        sa.Column("numero_factura", sa.String(20), nullable=True),
        sa.Column("fecha_factura", sa.DateTime(), nullable=True),
        sa.Column("comprobante_egreso", sa.String(20), nullable=True),
        sa.Column("observacion", sa.String(254), nullable=True),
        sa.Column("numero_entrada_ref", sa.BigInteger(), nullable=True),
        sa.Column("aprobado", sa.SmallInteger(), nullable=True),
        sa.Column("anexo", sa.String(20), nullable=True),
        sa.Column("anno_fiscal", sa.Integer(), nullable=False),
        sa.Column("id_proveedor", sa.BigInteger(), nullable=True),
        sa.Column("id_destino", sa.BigInteger(), nullable=True),
        sa.Column("id_encargado", sa.BigInteger(), nullable=True),
        sa.Column("usuario_crea", sa.String(50), nullable=True),
        sa.Column("creado_en", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["id_proveedor"], ["inventario.proveedor.id"],
                                name="fk_mov_proveedor"),
        sa.ForeignKeyConstraint(["id_destino"], ["inventario.destino.id"],
                                name="fk_mov_destino"),
        sa.ForeignKeyConstraint(["id_encargado"], ["inventario.encargado.id"],
                                name="fk_mov_encargado"),
        sa.PrimaryKeyConstraint("id"),
        schema="inventario",
    )
    op.create_index("ix_inv_mov_fecha", "movimiento", ["fecha"], schema="inventario")
    op.create_index("ix_inv_mov_anno", "movimiento", ["anno_fiscal"], schema="inventario")
    op.create_index("ix_inv_mov_origen", "movimiento", ["id_origen_mysql"], schema="inventario")

    # Tabla: movimiento_detalle
    op.create_table(
        "movimiento_detalle",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("id_origen_mysql", sa.BigInteger(), nullable=True),
        sa.Column("id_movimiento", sa.BigInteger(), nullable=False),
        sa.Column("id_articulo", sa.BigInteger(), nullable=False),
        sa.Column("fecha", sa.DateTime(), nullable=False),
        sa.Column("tipo_movimiento", sa.String(10), nullable=False),
        sa.Column("cantidad", sa.Numeric(18, 2), nullable=False),
        sa.Column("costo_unitario", sa.Numeric(18, 4), nullable=False),
        sa.Column("total_linea", sa.Numeric(18, 4), nullable=True),
        sa.Column("costo_promedio", sa.Numeric(18, 4), nullable=True),
        sa.Column("anno_fiscal", sa.Integer(), nullable=False),
        sa.Column("usuario_crea", sa.String(50), nullable=True),
        sa.Column("creado_en", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["id_movimiento"], ["inventario.movimiento.id"],
                                name="fk_detalle_movimiento"),
        sa.ForeignKeyConstraint(["id_articulo"], ["inventario.articulo.id"],
                                name="fk_detalle_articulo"),
        sa.PrimaryKeyConstraint("id"),
        schema="inventario",
    )
    op.create_index("ix_inv_det_movimiento", "movimiento_detalle", ["id_movimiento"], schema="inventario")
    op.create_index("ix_inv_det_articulo", "movimiento_detalle", ["id_articulo"], schema="inventario")
    op.create_index("ix_inv_det_anno", "movimiento_detalle", ["anno_fiscal"], schema="inventario")
    op.create_index("ix_inv_det_origen", "movimiento_detalle", ["id_origen_mysql"], schema="inventario")


def downgrade() -> None:
    op.drop_table("movimiento_detalle", schema="inventario")
    op.drop_table("movimiento", schema="inventario")
    op.drop_table("articulo", schema="inventario")
    op.drop_table("unidad_gestion", schema="inventario")
    op.drop_table("proveedor", schema="inventario")
    op.drop_table("encargado", schema="inventario")
    op.drop_table("destino", schema="inventario")
    op.drop_table("cuenta_contable", schema="inventario")
    op.execute("DROP SCHEMA IF EXISTS inventario CASCADE")
