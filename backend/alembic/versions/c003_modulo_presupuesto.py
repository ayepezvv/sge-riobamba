"""c003 — Módulo Presupuesto (schema presupuesto)

Revision ID: c003_modulo_presupuesto
Revises: c002_tesoreria_financiero
Create Date: 2026-04-04

Regla 1: todas las tablas en schema presupuesto (nunca en public)
Regla 2: nomenclatura en español
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "c003_modulo_presupuesto"
down_revision: Union[str, Sequence[str], None] = "c002_tesoreria_financiero"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    conn.execute(sa.text("CREATE SCHEMA IF NOT EXISTS presupuesto"))

    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS presupuesto.partidas_presupuestarias (
            id_partida        BIGSERIAL PRIMARY KEY,
            codigo            VARCHAR(30) NOT NULL,
            nombre            VARCHAR(255) NOT NULL,
            descripcion       TEXT,
            tipo              VARCHAR(20) NOT NULL CHECK (tipo IN ('INGRESO','GASTO')),
            nivel             INTEGER NOT NULL CHECK (nivel BETWEEN 1 AND 5),
            es_hoja           BOOLEAN DEFAULT TRUE,
            id_partida_padre  BIGINT REFERENCES presupuesto.partidas_presupuestarias(id_partida),
            estado            VARCHAR(20) DEFAULT 'ACTIVO',
            creado_en         TIMESTAMPTZ DEFAULT NOW(),
            CONSTRAINT uq_partida_codigo UNIQUE (codigo)
        )
    """))
    conn.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_partidas_codigo ON presupuesto.partidas_presupuestarias(codigo)"))

    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS presupuesto.presupuestos_anuales (
            id_presupuesto        BIGSERIAL PRIMARY KEY,
            anio_fiscal           INTEGER NOT NULL,
            denominacion          VARCHAR(255) NOT NULL,
            monto_inicial         NUMERIC(18,2) DEFAULT 0,
            monto_codificado      NUMERIC(18,2) DEFAULT 0,
            estado                VARCHAR(20) DEFAULT 'BORRADOR'
                                    CHECK (estado IN ('BORRADOR','APROBADO','LIQUIDADO','CERRADO')),
            fecha_aprobacion      DATE,
            resolucion_aprobacion VARCHAR(100),
            observaciones         TEXT,
            creado_en             TIMESTAMPTZ DEFAULT NOW(),
            actualizado_en        TIMESTAMPTZ DEFAULT NOW(),
            CONSTRAINT uq_presupuesto_anio_aprobado UNIQUE (anio_fiscal, estado)
        )
    """))
    conn.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_presupuestos_anio ON presupuesto.presupuestos_anuales(anio_fiscal)"))

    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS presupuesto.asignaciones_presupuestarias (
            id_asignacion       BIGSERIAL PRIMARY KEY,
            id_presupuesto      BIGINT NOT NULL
                REFERENCES presupuesto.presupuestos_anuales(id_presupuesto) ON DELETE RESTRICT,
            id_partida          BIGINT NOT NULL
                REFERENCES presupuesto.partidas_presupuestarias(id_partida) ON DELETE RESTRICT,
            monto_inicial       NUMERIC(18,2) DEFAULT 0,
            monto_codificado    NUMERIC(18,2) DEFAULT 0,
            monto_comprometido  NUMERIC(18,2) DEFAULT 0,
            monto_devengado     NUMERIC(18,2) DEFAULT 0,
            monto_pagado        NUMERIC(18,2) DEFAULT 0,
            estado              VARCHAR(20) DEFAULT 'ACTIVO',
            creado_en           TIMESTAMPTZ DEFAULT NOW(),
            CONSTRAINT uq_asignacion_presupuesto_partida UNIQUE (id_presupuesto, id_partida)
        )
    """))

    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS presupuesto.reformas_presupuestarias (
            id_reforma          BIGSERIAL PRIMARY KEY,
            id_asignacion       BIGINT NOT NULL
                REFERENCES presupuesto.asignaciones_presupuestarias(id_asignacion),
            tipo_reforma        VARCHAR(30) NOT NULL
                CHECK (tipo_reforma IN ('TRASPASO','SUPLEMENTO','REDUCCION')),
            monto               NUMERIC(18,2) NOT NULL,
            numero_resolucion   VARCHAR(100) NOT NULL,
            fecha_resolucion    DATE NOT NULL,
            motivo              TEXT,
            estado              VARCHAR(20) DEFAULT 'APROBADO',
            creado_en           TIMESTAMPTZ DEFAULT NOW()
        )
    """))

    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS presupuesto.certificados_presupuestarios (
            id_certificado          BIGSERIAL PRIMARY KEY,
            numero_certificado      VARCHAR(50) NOT NULL,
            id_asignacion           BIGINT NOT NULL
                REFERENCES presupuesto.asignaciones_presupuestarias(id_asignacion),
            monto_certificado       NUMERIC(18,2) NOT NULL CHECK (monto_certificado > 0),
            concepto                TEXT NOT NULL,
            fecha_solicitud         DATE NOT NULL,
            fecha_certificacion     DATE,
            fecha_vencimiento       DATE,
            estado                  VARCHAR(20) DEFAULT 'SOLICITADO'
                CHECK (estado IN ('SOLICITADO','APROBADO','COMPROMETIDO','DEVENGADO','LIQUIDADO','ANULADO')),
            motivo_anulacion        TEXT,
            referencia_tipo         VARCHAR(50),
            referencia_id           BIGINT,
            id_proceso_contratacion BIGINT
                REFERENCES contratacion.proceso_contratacion(id) ON DELETE SET NULL,
            creado_en               TIMESTAMPTZ DEFAULT NOW(),
            actualizado_en          TIMESTAMPTZ DEFAULT NOW(),
            CONSTRAINT uq_certificado_numero UNIQUE (numero_certificado)
        )
    """))
    conn.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_certificados_numero ON presupuesto.certificados_presupuestarios(numero_certificado)"))

    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS presupuesto.compromisos (
            id_compromiso       BIGSERIAL PRIMARY KEY,
            id_certificado      BIGINT NOT NULL
                REFERENCES presupuesto.certificados_presupuestarios(id_certificado),
            numero_compromiso   VARCHAR(50) NOT NULL,
            monto_comprometido  NUMERIC(18,2) NOT NULL CHECK (monto_comprometido > 0),
            concepto            TEXT NOT NULL,
            fecha_compromiso    DATE NOT NULL,
            estado              VARCHAR(20) DEFAULT 'ACTIVO'
                CHECK (estado IN ('ACTIVO','DEVENGADO','ANULADO')),
            motivo_anulacion    TEXT,
            creado_en           TIMESTAMPTZ DEFAULT NOW()
        )
    """))
    conn.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_compromisos_numero ON presupuesto.compromisos(numero_compromiso)"))

    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS presupuesto.devengados (
            id_devengado        BIGSERIAL PRIMARY KEY,
            id_compromiso       BIGINT NOT NULL
                REFERENCES presupuesto.compromisos(id_compromiso),
            numero_devengado    VARCHAR(50) NOT NULL,
            monto_devengado     NUMERIC(18,2) NOT NULL CHECK (monto_devengado > 0),
            concepto            TEXT NOT NULL,
            fecha_devengado     DATE NOT NULL,
            estado              VARCHAR(20) DEFAULT 'REGISTRADO'
                CHECK (estado IN ('REGISTRADO','PAGADO','ANULADO')),
            id_asiento_contable BIGINT
                REFERENCES contabilidad.asientos_contables(id) ON DELETE SET NULL,
            id_factura          BIGINT
                REFERENCES financiero.facturas(id) ON DELETE SET NULL,
            motivo_anulacion    TEXT,
            creado_en           TIMESTAMPTZ DEFAULT NOW()
        )
    """))
    conn.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_devengados_numero ON presupuesto.devengados(numero_devengado)"))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DROP TABLE IF EXISTS presupuesto.devengados CASCADE"))
    conn.execute(sa.text("DROP TABLE IF EXISTS presupuesto.compromisos CASCADE"))
    conn.execute(sa.text("DROP TABLE IF EXISTS presupuesto.certificados_presupuestarios CASCADE"))
    conn.execute(sa.text("DROP TABLE IF EXISTS presupuesto.reformas_presupuestarias CASCADE"))
    conn.execute(sa.text("DROP TABLE IF EXISTS presupuesto.asignaciones_presupuestarias CASCADE"))
    conn.execute(sa.text("DROP TABLE IF EXISTS presupuesto.presupuestos_anuales CASCADE"))
    conn.execute(sa.text("DROP TABLE IF EXISTS presupuesto.partidas_presupuestarias CASCADE"))
    conn.execute(sa.text("DROP SCHEMA IF EXISTS presupuesto CASCADE"))
