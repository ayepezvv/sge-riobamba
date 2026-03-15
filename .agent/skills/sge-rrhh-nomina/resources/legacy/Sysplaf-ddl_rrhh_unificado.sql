-- DDL para el Sistema Unificado de RRHH y Roles
-- Motor: PostgreSQL

-- 1. Creación de Esquemas
CREATE SCHEMA IF NOT EXISTS rrhh;
CREATE SCHEMA IF NOT EXISTS nomina;

-- 2. Catálogos Maestros (Esquema rrhh)

CREATE TABLE rrhh.cat_tipo_contrato (
    id_tipo_contrato SERIAL PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Poblar catálogo inicial basado en las 5 bases de datos actuales
INSERT INTO rrhh.cat_tipo_contrato (codigo, nombre) VALUES
('LOEP_C', 'Contratados LOEP'),
('LOEP_E', 'Empleados LOEP'),
('LOEP_R', 'Requeridos LOEP'),
('CT_C', 'Trabajadores Contratados (Código de Trabajo)'),
('CT_T', 'Trabajadores (Código de Trabajo)');

CREATE TABLE rrhh.cat_departamento (
    id_departamento SERIAL PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    area_superior_id INTEGER REFERENCES rrhh.cat_departamento(id_departamento)
);

CREATE TABLE rrhh.cat_cargo (
    id_cargo SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    sueldo_base NUMERIC(12, 2) DEFAULT 0.00
);

CREATE TABLE rrhh.persona (
    id_persona SERIAL PRIMARY KEY,
    identificacion VARCHAR(13) UNIQUE NOT NULL, -- Cédula o RUC
    apellidos VARCHAR(100) NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    genero CHAR(1),
    correo_personal VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT
);

CREATE TABLE rrhh.empleado (
    id_empleado SERIAL PRIMARY KEY,
    persona_id INTEGER NOT NULL REFERENCES rrhh.persona(id_persona),
    codigo_empleado VARCHAR(20) UNIQUE, -- El antiguo CODEMP
    fecha_ingreso DATE,
    fecha_salida DATE,
    cuenta_bancaria VARCHAR(25),
    id_institucion_financiera INTEGER, -- Podría crearse otro catálogo
    activo BOOLEAN DEFAULT TRUE,
    foto_path TEXT
);

CREATE TABLE rrhh.contrato (
    id_contrato SERIAL PRIMARY KEY,
    empleado_id INTEGER NOT NULL REFERENCES rrhh.empleado(id_empleado),
    tipo_contrato_id INTEGER NOT NULL REFERENCES rrhh.cat_tipo_contrato(id_tipo_contrato),
    cargo_id INTEGER NOT NULL REFERENCES rrhh.cat_cargo(id_cargo),
    departamento_id INTEGER NOT NULL REFERENCES rrhh.cat_departamento(id_departamento),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    sueldo_pactado NUMERIC(12, 2) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- 3. Gestión de Nómina (Esquema nomina)

CREATE TABLE nomina.cat_rubro (
    id_rubro SERIAL PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(15) CHECK (tipo IN ('INGRESO', 'EGRESO', 'PROVISION', 'INFORMATIVO')),
    es_fijo BOOLEAN DEFAULT FALSE,
    cuenta_contable_debe VARCHAR(50),
    cuenta_contable_haber VARCHAR(50)
);

CREATE TABLE nomina.periodo (
    id_periodo SERIAL PRIMARY KEY,
    mes INTEGER CHECK (mes BETWEEN 1 AND 12),
    anio INTEGER,
    fecha_cierre DATE,
    abierto BOOLEAN DEFAULT TRUE,
    UNIQUE(mes, anio)
);

CREATE TABLE nomina.rol_pago_cabecera (
    id_rol_cabecera SERIAL PRIMARY KEY,
    contrato_id INTEGER NOT NULL REFERENCES rrhh.contrato(id_contrato),
    periodo_id INTEGER NOT NULL REFERENCES nomina.periodo(id_periodo),
    total_ingresos NUMERIC(12, 2) DEFAULT 0.00,
    total_egresos NUMERIC(12, 2) DEFAULT 0.00,
    liquido_recibir NUMERIC(12, 2) DEFAULT 0.00,
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'BORRADOR'
);

CREATE TABLE nomina.rol_pago_detalle (
    id_rol_detalle SERIAL PRIMARY KEY,
    rol_cabecera_id INTEGER NOT NULL REFERENCES nomina.rol_pago_cabecera(id_rol_cabecera),
    rubro_id INTEGER NOT NULL REFERENCES nomina.cat_rubro(id_rubro),
    valor NUMERIC(12, 2) NOT NULL,
    cantidad NUMERIC(10, 2) DEFAULT 1.0, -- Para horas extras o días
    tipo_calculo VARCHAR(50) -- MANUAL, SISTEMA, FORMULA
);

-- 4. Índices para Optimización
CREATE INDEX idx_empleado_persona ON rrhh.empleado(persona_id);
CREATE INDEX idx_contrato_empleado ON rrhh.contrato(empleado_id);
CREATE INDEX idx_rol_contrato ON nomina.rol_pago_cabecera(contrato_id);
CREATE INDEX idx_rol_periodo ON nomina.rol_pago_cabecera(periodo_id);

-- 5. Comentarios de Tabla para Documentación
COMMENT ON TABLE rrhh.persona IS 'Datos básicos de identidad de todas las personas relacionadas con la institución.';
COMMENT ON TABLE rrhh.contrato IS 'Registro de vinculación laboral. Permite que una persona tenga múltiples contratos históricos o simultáneos (segmentados por tipo).';
COMMENT ON TABLE nomina.rol_pago_cabecera IS 'Consolidado mensual de pagos por contrato.';
