"""Nomina rol de pagos — tablas rol_pago, linea_rol_pago, detalle_linea_rol

Revision ID: a3b7c9d2e1f4
Revises: f52466dcba5e
Create Date: 2026-04-05 05:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a3b7c9d2e1f4'
down_revision: Union[str, None] = 'a5dd8cea9dd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Schema rrhh ya existe — no recrear

    # -----------------------------------------------------------------------
    # rrhh.rol_pago — cabecera de nómina por período
    # -----------------------------------------------------------------------
    op.create_table(
        "rol_pago",
        sa.Column("id_rol_pago", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("periodo_anio", sa.Integer, nullable=False),
        sa.Column("periodo_mes", sa.Integer, nullable=False),
        sa.Column("tipo_rol", sa.String(50), nullable=False, server_default="MENSUAL"),
        sa.Column("estado", sa.String(30), nullable=False, server_default="BORRADOR"),
        sa.Column("fecha_generacion", sa.Date, nullable=False),
        sa.Column("fecha_aprobacion", sa.Date, nullable=True),
        sa.Column("aprobado_por_id", sa.BigInteger,
                  sa.ForeignKey("configuracion.usuarios.id", ondelete="SET NULL"),
                  nullable=True),
        sa.Column("observaciones", sa.Text, nullable=True),
        sa.Column("creado_por_id", sa.BigInteger,
                  sa.ForeignKey("configuracion.usuarios.id", ondelete="SET NULL"),
                  nullable=True),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("periodo_anio", "periodo_mes", "tipo_rol",
                            name="uq_rol_pago_periodo_tipo"),
        schema="rrhh",
    )
    op.create_check_constraint(
        "ck_rol_pago_mes",
        "rol_pago",
        "periodo_mes BETWEEN 1 AND 12",
        schema="rrhh",
    )

    # -----------------------------------------------------------------------
    # rrhh.linea_rol_pago — una línea por empleado
    # -----------------------------------------------------------------------
    op.create_table(
        "linea_rol_pago",
        sa.Column("id_linea", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("id_rol_pago", sa.BigInteger,
                  sa.ForeignKey("rrhh.rol_pago.id_rol_pago", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("id_empleado", sa.BigInteger,
                  sa.ForeignKey("rrhh.empleado.id_empleado", ondelete="RESTRICT"),
                  nullable=False),
        sa.Column("sueldo_base", sa.Numeric(12, 2), nullable=False),
        sa.Column("dias_trabajados", sa.Integer, nullable=False, server_default="30"),
        sa.Column("total_ingresos", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("total_descuentos", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("total_provisiones", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("liquido_a_recibir", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("banco_destino", sa.String(100), nullable=True),
        sa.Column("cuenta_bancaria", sa.String(30), nullable=True),
        sa.Column("tipo_cuenta", sa.String(20), nullable=True),
        sa.Column("estado", sa.String(20), nullable=False, server_default="ACTIVO"),
        sa.UniqueConstraint("id_rol_pago", "id_empleado", name="uq_linea_rol_empleado"),
        schema="rrhh",
    )

    # -----------------------------------------------------------------------
    # rrhh.detalle_linea_rol — un renglón por rubro calculado
    # -----------------------------------------------------------------------
    op.create_table(
        "detalle_linea_rol",
        sa.Column("id_detalle", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("id_linea", sa.BigInteger,
                  sa.ForeignKey("rrhh.linea_rol_pago.id_linea", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("id_rubro", sa.BigInteger,
                  sa.ForeignKey("rrhh.rubro_nomina.id_rubro", ondelete="RESTRICT"),
                  nullable=False),
        sa.Column("codigo_rubro", sa.String(20), nullable=False),
        sa.Column("nombre_rubro", sa.String(100), nullable=False),
        sa.Column("naturaleza", sa.String(20), nullable=False),
        sa.Column("valor_calculado", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("descripcion_calculo", sa.Text, nullable=True),
        schema="rrhh",
    )


def downgrade() -> None:
    op.drop_table("detalle_linea_rol", schema="rrhh")
    op.drop_table("linea_rol_pago", schema="rrhh")
    op.drop_table("rol_pago", schema="rrhh")
