"""rrhh_super_modelo_v3

Migración maestra única: Esquema RRHH V3 + Super Modelo Empleado
+ Migración quirúrgica cross-schema (informatica → rrhh).

ORDEN DE OPERACIONES (estricto):
1.  Crear esquema rrhh.
2.  Motor de cálculos (parametro_calculo, impuesto_renta_escala).
3.  Estructura organizacional (area_organizacional, escala_salarial, cargo).
4.  Super Modelo rrhh.empleado (V3 + campos enriquecidos + auditoría).
5.  Tablas satélite (empleado_carga_familiar, historial_laboral).
6.  Catálogo de rubros (rubro_nomina).
7.  DROP CONSTRAINT quirúrgico: FK de informatica.direccion_ip_asignada
    hacia cualquier tabla de empleados vieja (DO $$ para nombre desconocido).
8.  RENAME COLUMN personal_id → empleado_id.
9.  ALTER COLUMN empleado_id → BIGINT.
10. CREATE FK nueva: informatica.direccion_ip_asignada → rrhh.empleado.id_empleado.
11. DROP TABLE administracion.personal (ya sin dependencias).

Revision ID: a1b2c3d4e5f7
Revises: 29f0ea2413ff
Create Date: 2026-03-15 10:09:00.000000
"""
from typing import Union
from alembic import op
import sqlalchemy as sa

revision: str = 'a1b2c3d4e5f7'
down_revision: Union[str, None] = '29f0ea2413ff'
branch_labels = None
depends_on = None


def upgrade() -> None:

    # ================================================================
    # PASO 1: Crear esquema rrhh
    # ================================================================
    op.execute("CREATE SCHEMA IF NOT EXISTS rrhh")

    # ================================================================
    # PASO 2: Motor de cálculos
    # ================================================================
    op.create_table(
        'parametro_calculo',
        sa.Column('id_parametro', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('anio_vigencia', sa.Integer(), nullable=False),
        sa.Column('codigo_parametro', sa.String(50), nullable=False),
        sa.Column('descripcion', sa.String(150), nullable=True),
        sa.Column('valor_numerico', sa.Numeric(15, 6), nullable=True),
        sa.Column('valor_texto', sa.String(255), nullable=True),
        sa.Column('estado', sa.String(20), server_default='ACTIVO'),
        sa.UniqueConstraint('anio_vigencia', 'codigo_parametro',
                            name='uq_parametro_anio_codigo_rrhh'),
        schema='rrhh'
    )

    op.create_table(
        'impuesto_renta_escala',
        sa.Column('id_escala', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('anio_vigencia', sa.Integer(), nullable=False),
        sa.Column('fraccion_basica', sa.Numeric(12, 2), nullable=False),
        sa.Column('exceso_hasta', sa.Numeric(12, 2), nullable=True),
        sa.Column('impuesto_fraccion_basica', sa.Numeric(12, 2), nullable=False),
        sa.Column('porcentaje_fraccion_excedente', sa.Numeric(5, 2), nullable=False),
        schema='rrhh'
    )

    # ================================================================
    # PASO 3: Estructura organizacional
    # ================================================================
    op.create_table(
        'area_organizacional',
        sa.Column('id_area', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('id_area_padre', sa.BigInteger(),
                  sa.ForeignKey('rrhh.area_organizacional.id_area'), nullable=True),
        sa.Column('tipo_area', sa.String(50), nullable=False),
        sa.Column('nombre', sa.String(150), nullable=False),
        sa.Column('estado', sa.String(20), server_default='ACTIVO'),
        schema='rrhh'
    )

    op.create_table(
        'escala_salarial',
        sa.Column('id_escala', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('grado', sa.String(20), nullable=False),
        sa.Column('salario_base', sa.Numeric(10, 2), nullable=False),
        sa.Column('regimen_laboral', sa.String(50), nullable=False),
        schema='rrhh'
    )

    op.create_table(
        'cargo',
        sa.Column('id_cargo', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('nombre_cargo', sa.String(150), nullable=False),
        sa.Column('id_escala_salarial', sa.BigInteger(),
                  sa.ForeignKey('rrhh.escala_salarial.id_escala'), nullable=True),
        sa.Column('partida_presupuestaria', sa.String(100), nullable=True),
        sa.Column('estado', sa.String(20), server_default='ACTIVO'),
        schema='rrhh'
    )

    # ================================================================
    # PASO 4: Super Modelo rrhh.empleado (V3 + Campos enriquecidos)
    # ================================================================
    op.create_table(
        'empleado',
        sa.Column('id_empleado', sa.BigInteger(), primary_key=True, autoincrement=True),
        # Identificación
        sa.Column('tipo_identificacion', sa.String(20), server_default='CEDULA'),
        sa.Column('identificacion', sa.String(20), nullable=False),
        # Datos personales
        sa.Column('nombres', sa.String(100), nullable=False),
        sa.Column('apellidos', sa.String(100), nullable=False),
        sa.Column('fecha_nacimiento', sa.Date(), nullable=False),
        sa.Column('genero', sa.String(20), nullable=True),
        # Datos previsionales (V3 base)
        sa.Column('porcentaje_discapacidad', sa.Numeric(5, 2), server_default='0'),
        sa.Column('aplica_iess', sa.Boolean(), server_default='true'),
        sa.Column('acumula_fondos_reserva', sa.Boolean(), server_default='true'),
        sa.Column('acumula_decimos', sa.Boolean(), server_default='false'),
        # Campos enriquecidos (Fase 1 robusta)
        sa.Column('regimen_legal', sa.String(50), nullable=True),
        sa.Column('tipo_contrato_actual', sa.String(50), nullable=True),
        sa.Column('codigo_sercop', sa.String(100), nullable=True),
        sa.Column('archivo_firma_electronica', sa.String(), nullable=True),
        # Datos de contacto
        sa.Column('telefono_celular', sa.String(20), nullable=True),
        sa.Column('correo_personal', sa.String(100), nullable=True),
        sa.Column('direccion_domicilio', sa.String(255), nullable=True),
        sa.Column('foto_perfil', sa.String(), nullable=True),
        # Vinculación al sistema
        sa.Column('usuario_id', sa.BigInteger(),
                  sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'),
                  nullable=True),
        # Estado y soft delete
        sa.Column('estado_empleado', sa.String(50), server_default='ACTIVO'),
        sa.Column('eliminado_en', sa.DateTime(timezone=True), nullable=True),
        # Auditoría completa
        sa.Column('creado_por_id', sa.BigInteger(),
                  sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('actualizado_por_id', sa.BigInteger(),
                  sa.ForeignKey('configuracion.usuarios.id', ondelete='SET NULL'), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        # Constraints
        sa.UniqueConstraint('identificacion', name='uq_rrhh_empleado_identificacion'),
        sa.UniqueConstraint('usuario_id', name='uq_rrhh_empleado_usuario_id'),
        schema='rrhh'
    )

    # ================================================================
    # PASO 5: Tablas satélite
    # ================================================================
    op.create_table(
        'empleado_carga_familiar',
        sa.Column('id_carga', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('id_empleado', sa.BigInteger(),
                  sa.ForeignKey('rrhh.empleado.id_empleado', ondelete='CASCADE'), nullable=False),
        sa.Column('identificacion', sa.String(20), nullable=True),
        sa.Column('nombres_completos', sa.String(200), nullable=False),
        sa.Column('parentesco', sa.String(50), nullable=False),
        sa.Column('fecha_nacimiento', sa.Date(), nullable=False),
        sa.Column('aplica_deduccion_ir', sa.Boolean(), server_default='true'),
        sa.Column('estado', sa.String(20), server_default='ACTIVO'),
        schema='rrhh'
    )

    op.create_table(
        'historial_laboral',
        sa.Column('id_historial', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('id_empleado', sa.BigInteger(),
                  sa.ForeignKey('rrhh.empleado.id_empleado', ondelete='CASCADE'), nullable=False),
        sa.Column('id_area', sa.BigInteger(),
                  sa.ForeignKey('rrhh.area_organizacional.id_area'), nullable=False),
        sa.Column('id_cargo', sa.BigInteger(),
                  sa.ForeignKey('rrhh.cargo.id_cargo'), nullable=False),
        sa.Column('tipo_contrato', sa.String(50), nullable=False),
        sa.Column('fecha_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_fin', sa.Date(), nullable=True),
        sa.Column('salario_acordado', sa.Numeric(10, 2), nullable=False),
        schema='rrhh'
    )

    # ================================================================
    # PASO 6: Catálogo de rubros
    # ================================================================
    op.create_table(
        'rubro_nomina',
        sa.Column('id_rubro', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('codigo_rubro', sa.String(20), nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('naturaleza', sa.String(20), nullable=False),
        sa.Column('tipo_valor', sa.String(20), nullable=False),
        sa.Column('formula_calculo', sa.Text(), nullable=True),
        sa.Column('orden_ejecucion', sa.Integer(), nullable=False),
        sa.Column('es_imponible', sa.Boolean(), server_default='true'),
        sa.Column('estado', sa.String(20), server_default='ACTIVO'),
        sa.UniqueConstraint('codigo_rubro', name='uq_rrhh_codigo_rubro'),
        schema='rrhh'
    )

    # ================================================================
    # PASO 7: DROP CONSTRAINT quirúrgico en informatica (DO $$ seguro)
    # Detecta automáticamente el nombre de la FK sin importar cómo se
    # llamó en la migración anterior.
    # ================================================================
    op.execute("""
        DO $$
        DECLARE
            v_constraint TEXT;
        BEGIN
            SELECT tc.constraint_name
            INTO   v_constraint
            FROM   information_schema.table_constraints  tc
            JOIN   information_schema.key_column_usage   kcu
                   ON tc.constraint_name = kcu.constraint_name
                   AND tc.table_schema   = kcu.table_schema
            WHERE  tc.constraint_type = 'FOREIGN KEY'
              AND  tc.table_schema     = 'informatica'
              AND  tc.table_name       = 'direccion_ip_asignada'
              AND  kcu.column_name    IN ('personal_id', 'empleado_id')
            LIMIT 1;

            IF v_constraint IS NOT NULL THEN
                EXECUTE format(
                    'ALTER TABLE informatica.direccion_ip_asignada DROP CONSTRAINT %I',
                    v_constraint
                );
                RAISE NOTICE 'FK eliminada: %', v_constraint;
            ELSE
                RAISE NOTICE 'No se encontró FK de personal/empleado en direccion_ip_asignada';
            END IF;
        END $$;
    """)

    # ================================================================
    # PASO 8 & 9: Renombrar personal_id → empleado_id y cambiar tipo
    # ================================================================
    op.execute("""
        DO $$
        BEGIN
            -- Renombrar columna si aún existe como personal_id
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_schema = 'informatica'
                  AND table_name   = 'direccion_ip_asignada'
                  AND column_name  = 'personal_id'
            ) THEN
                ALTER TABLE informatica.direccion_ip_asignada
                    RENAME COLUMN personal_id TO empleado_id;
                RAISE NOTICE 'Columna renombrada: personal_id → empleado_id';
            END IF;

            -- Cambiar tipo a BIGINT (compatible con BIGSERIAL de rrhh.empleado)
            ALTER TABLE informatica.direccion_ip_asignada
                ALTER COLUMN empleado_id TYPE BIGINT USING empleado_id::BIGINT;
        END $$;
    """)

    # ================================================================
    # PASO 10: Crear nueva FK → rrhh.empleado.id_empleado
    # ================================================================
    op.create_foreign_key(
        'fk_ip_asignada_rrhh_empleado',
        'direccion_ip_asignada',
        'empleado',
        ['empleado_id'],
        ['id_empleado'],
        source_schema='informatica',
        referent_schema='rrhh',
        ondelete='SET NULL'
    )

    # ================================================================
    # PASO 11: DROP TABLE administracion.personal (ya sin dependencias)
    # Solo si existe — puede que ya haya sido eliminada en migraciones previas.
    # ================================================================
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = 'administracion'
                  AND table_name   = 'personal'
            ) THEN
                DROP TABLE administracion.personal CASCADE;
                RAISE NOTICE 'Tabla administracion.personal eliminada con CASCADE';
            END IF;
        END $$;
    """)


def downgrade() -> None:
    """Revierte la migración en orden inverso seguro."""

    # Restaurar administracion.personal — NO APLICA (datos históricos perdidos)
    # Se documenta como operación unidireccional.

    # 1. Eliminar FK nueva en informatica
    op.drop_constraint('fk_ip_asignada_rrhh_empleado', 'direccion_ip_asignada',
                       schema='informatica', type_='foreignkey')

    # 2. Revertir columna empleado_id → personal_id
    op.execute("""
        ALTER TABLE informatica.direccion_ip_asignada
            ALTER COLUMN empleado_id TYPE INTEGER USING empleado_id::INTEGER;
        ALTER TABLE informatica.direccion_ip_asignada
            RENAME COLUMN empleado_id TO personal_id;
    """)

    # 3. Eliminar tablas rrhh en orden inverso
    op.drop_table('rubro_nomina', schema='rrhh')
    op.drop_table('historial_laboral', schema='rrhh')
    op.drop_table('empleado_carga_familiar', schema='rrhh')
    op.drop_table('empleado', schema='rrhh')
    op.drop_table('cargo', schema='rrhh')
    op.drop_table('escala_salarial', schema='rrhh')
    op.drop_table('area_organizacional', schema='rrhh')
    op.drop_table('impuesto_renta_escala', schema='rrhh')
    op.drop_table('parametro_calculo', schema='rrhh')
    op.execute("DROP SCHEMA IF EXISTS rrhh CASCADE")
