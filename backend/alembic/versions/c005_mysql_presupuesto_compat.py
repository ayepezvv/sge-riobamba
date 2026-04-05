"""c005 — Compatibilidad MySQL presupuesto: nuevas tablas + columnas tracking ETL

Revision ID: c005_mysql_presupuesto_compat
Revises: 6d89a0d673fd
Create Date: 2026-04-05

Objetivo: Adaptar schema presupuesto para importar datos de cont_emapar_2023/2024/2025
  - Nuevas tablas: tipo_contratacion, tramite, liquidacion
  - Columnas de tracking ETL en tablas existentes (id_mysql_origen, anio_fiscal)
  - id_asignacion nullable en certificados_presupuestarios para certifs sin partida directa

Regla 1: todas las tablas en schema presupuesto (prohibido public)
Regla 2: nomenclatura en español
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "c005_mysql_presupuesto_compat"
down_revision: Union[str, Sequence[str], None] = "6d89a0d673fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # -----------------------------------------------------------------------
    # 1. TABLA: tipo_contratacion (catálogo MySQL tratacion)
    # -----------------------------------------------------------------------
    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS presupuesto.tipo_contratacion (
            id_tipo_contratacion  BIGSERIAL PRIMARY KEY,
            codigo                VARCHAR(10) NOT NULL,
            nombre                VARCHAR(100) NOT NULL,
            descripcion           TEXT,
            activo                BOOLEAN NOT NULL DEFAULT TRUE,
            id_mysql_origen       BIGINT,
            creado_en             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            CONSTRAINT uq_tipo_contratacion_codigo UNIQUE (codigo)
        )
    """))

    # -----------------------------------------------------------------------
    # 2. TABLA: tramite (expediente de contratación — MySQL tramites)
    # -----------------------------------------------------------------------
    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS presupuesto.tramite (
            id_tramite            BIGSERIAL PRIMARY KEY,
            anio_fiscal           SMALLINT NOT NULL,
            numero                INTEGER NOT NULL,
            fecha                 DATE,
            numero_oficio         VARCHAR(20),
            fecha_oficio          DATE,
            descripcion           VARCHAR(500),
            valor_comprometido    NUMERIC(18,2) NOT NULL DEFAULT 0,
            estado                SMALLINT NOT NULL DEFAULT 0,
            id_tipo_contratacion  BIGINT REFERENCES presupuesto.tipo_contratacion(id_tipo_contratacion),
            ruc_proveedor         VARCHAR(15),
            nombre_proveedor      VARCHAR(100),
            codigo_departamento   INTEGER,
            nombre_departamento   VARCHAR(100),
            es_arrastre           BOOLEAN NOT NULL DEFAULT FALSE,
            id_mysql_origen       BIGINT NOT NULL,
            creado_en             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            CONSTRAINT uq_tramite_anio_origen UNIQUE (anio_fiscal, id_mysql_origen)
        )
    """))

    conn.execute(sa.text("""
        CREATE INDEX IF NOT EXISTS ix_tramite_anio_numero
            ON presupuesto.tramite (anio_fiscal, numero)
    """))

    # -----------------------------------------------------------------------
    # 3. TABLA: liquidacion (MySQL liquidaciones)
    # -----------------------------------------------------------------------
    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS presupuesto.liquidacion (
            id_liquidacion        BIGSERIAL PRIMARY KEY,
            anio_fiscal           SMALLINT NOT NULL,
            id_compromiso         BIGINT NOT NULL
                                  REFERENCES presupuesto.compromisos(id_compromiso)
                                  ON DELETE RESTRICT,
            fecha                 DATE NOT NULL,
            valor                 NUMERIC(18,2) NOT NULL,
            saldo                 NUMERIC(18,2) NOT NULL DEFAULT 0,
            numero_comprobante    VARCHAR(20),
            observaciones         VARCHAR(500),
            cuenta_contable       VARCHAR(40),
            numero_liquidacion    NUMERIC(12,0),
            id_mysql_origen       BIGINT NOT NULL,
            creado_en             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            CONSTRAINT uq_liquidacion_anio_origen UNIQUE (anio_fiscal, id_mysql_origen)
        )
    """))

    conn.execute(sa.text("""
        CREATE INDEX IF NOT EXISTS ix_liquidacion_anio_compromiso
            ON presupuesto.liquidacion (anio_fiscal, id_compromiso)
    """))

    # -----------------------------------------------------------------------
    # 4. COLUMNAS adicionales en certificados_presupuestarios
    # -----------------------------------------------------------------------
    # Hacer nullable id_asignacion (certifs MySQL pueden no tener partida directa)
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.certificados_presupuestarios
            ALTER COLUMN id_asignacion DROP NOT NULL
    """))

    conn.execute(sa.text("""
        ALTER TABLE presupuesto.certificados_presupuestarios
            ADD COLUMN IF NOT EXISTS id_mysql_origen BIGINT,
            ADD COLUMN IF NOT EXISTS anio_fiscal SMALLINT,
            ADD COLUMN IF NOT EXISTS tipo_mysql SMALLINT,
            ADD COLUMN IF NOT EXISTS tipo_certi VARCHAR(30),
            ADD COLUMN IF NOT EXISTS numero_mysql NUMERIC(12,0),
            ADD COLUMN IF NOT EXISTS ruc_proveedor VARCHAR(15),
            ADD COLUMN IF NOT EXISTS nombre_proveedor VARCHAR(100)
    """))

    conn.execute(sa.text("""
        CREATE UNIQUE INDEX IF NOT EXISTS uq_certificado_anio_origen
            ON presupuesto.certificados_presupuestarios (anio_fiscal, id_mysql_origen)
            WHERE id_mysql_origen IS NOT NULL
    """))

    # -----------------------------------------------------------------------
    # 5. COLUMNAS adicionales en compromisos
    # -----------------------------------------------------------------------
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.compromisos
            ADD COLUMN IF NOT EXISTS id_tramite BIGINT
                REFERENCES presupuesto.tramite(id_tramite),
            ADD COLUMN IF NOT EXISTS id_mysql_origen BIGINT,
            ADD COLUMN IF NOT EXISTS anio_fiscal SMALLINT,
            ADD COLUMN IF NOT EXISTS numero_certi_mysql NUMERIC(12,0),
            ADD COLUMN IF NOT EXISTS monto_devengado_mysql NUMERIC(18,2),
            ADD COLUMN IF NOT EXISTS monto_liquidado_mysql NUMERIC(18,2)
    """))

    conn.execute(sa.text("""
        CREATE UNIQUE INDEX IF NOT EXISTS uq_compromiso_anio_origen
            ON presupuesto.compromisos (anio_fiscal, id_mysql_origen)
            WHERE id_mysql_origen IS NOT NULL
    """))

    # -----------------------------------------------------------------------
    # 6. COLUMNAS adicionales en reformas_presupuestarias
    # -----------------------------------------------------------------------
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.reformas_presupuestarias
            ADD COLUMN IF NOT EXISTS id_mysql_origen BIGINT,
            ADD COLUMN IF NOT EXISTS anio_fiscal SMALLINT,
            ADD COLUMN IF NOT EXISTS numero_reforma_mysql NUMERIC(12,0)
    """))

    conn.execute(sa.text("""
        CREATE UNIQUE INDEX IF NOT EXISTS uq_reforma_anio_origen
            ON presupuesto.reformas_presupuestarias (anio_fiscal, id_mysql_origen)
            WHERE id_mysql_origen IS NOT NULL
    """))

    # -----------------------------------------------------------------------
    # 7. COLUMNAS adicionales en devengados
    # -----------------------------------------------------------------------
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.devengados
            ADD COLUMN IF NOT EXISTS id_mysql_origen BIGINT,
            ADD COLUMN IF NOT EXISTS anio_fiscal SMALLINT
    """))

    conn.execute(sa.text("""
        CREATE UNIQUE INDEX IF NOT EXISTS uq_devengado_anio_origen
            ON presupuesto.devengados (anio_fiscal, id_mysql_origen)
            WHERE id_mysql_origen IS NOT NULL
    """))


def downgrade() -> None:
    conn = op.get_bind()

    # Eliminar índices
    conn.execute(sa.text("DROP INDEX IF EXISTS presupuesto.uq_devengado_anio_origen"))
    conn.execute(sa.text("DROP INDEX IF EXISTS presupuesto.uq_reforma_anio_origen"))
    conn.execute(sa.text("DROP INDEX IF EXISTS presupuesto.uq_compromiso_anio_origen"))
    conn.execute(sa.text("DROP INDEX IF EXISTS presupuesto.uq_certificado_anio_origen"))
    conn.execute(sa.text("DROP INDEX IF EXISTS presupuesto.ix_liquidacion_anio_compromiso"))
    conn.execute(sa.text("DROP INDEX IF EXISTS presupuesto.ix_tramite_anio_numero"))

    # Eliminar columnas añadidas
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.devengados
            DROP COLUMN IF EXISTS id_mysql_origen,
            DROP COLUMN IF EXISTS anio_fiscal
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.reformas_presupuestarias
            DROP COLUMN IF EXISTS id_mysql_origen,
            DROP COLUMN IF EXISTS anio_fiscal,
            DROP COLUMN IF EXISTS numero_reforma_mysql
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.compromisos
            DROP COLUMN IF EXISTS id_tramite,
            DROP COLUMN IF EXISTS id_mysql_origen,
            DROP COLUMN IF EXISTS anio_fiscal,
            DROP COLUMN IF EXISTS numero_certi_mysql,
            DROP COLUMN IF EXISTS monto_devengado_mysql,
            DROP COLUMN IF EXISTS monto_liquidado_mysql
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.certificados_presupuestarios
            DROP COLUMN IF EXISTS id_mysql_origen,
            DROP COLUMN IF EXISTS anio_fiscal,
            DROP COLUMN IF EXISTS tipo_mysql,
            DROP COLUMN IF EXISTS tipo_certi,
            DROP COLUMN IF EXISTS numero_mysql,
            DROP COLUMN IF EXISTS ruc_proveedor,
            DROP COLUMN IF EXISTS nombre_proveedor
    """))
    conn.execute(sa.text("""
        ALTER TABLE presupuesto.certificados_presupuestarios
            ALTER COLUMN id_asignacion SET NOT NULL
    """))

    # Eliminar tablas nuevas
    conn.execute(sa.text("DROP TABLE IF EXISTS presupuesto.liquidacion"))
    conn.execute(sa.text("DROP TABLE IF EXISTS presupuesto.tramite"))
    conn.execute(sa.text("DROP TABLE IF EXISTS presupuesto.tipo_contratacion"))
