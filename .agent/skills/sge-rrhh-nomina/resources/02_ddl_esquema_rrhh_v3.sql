-- ==============================================================================
-- MÓDULO: RRHH Y NÓMINA (SGE RIOBAMBA EP) - V3 CON MOTOR DE CÁLCULO
-- MOTOR: PostgreSQL
-- ==============================================================================

CREATE SCHEMA IF NOT EXISTS rrhh;

-- ==========================================
-- 1. MOTOR DE CÁLCULOS Y PARÁMETROS (INSPIRADO EN SYSPLAF)
-- ==========================================

-- Almacena valores globales por año (Ej: SBU, Porcentaje IESS Personal/Patronal)
CREATE TABLE rrhh.parametro_calculo (
    id_parametro BIGSERIAL PRIMARY KEY,
    anio_vigencia INTEGER NOT NULL,
    codigo_parametro VARCHAR(50) NOT NULL, -- Ej: 'SBU', 'IESS_PER', 'IESS_PAT'
    descripcion VARCHAR(150),
    valor_numerico NUMERIC(15, 6),
    valor_texto VARCHAR(255),
    estado VARCHAR(20) DEFAULT 'ACTIVO',
    UNIQUE (anio_vigencia, codigo_parametro)
);

-- Tabla progresiva para Impuesto a la Renta
CREATE TABLE rrhh.impuesto_renta_escala (
    id_escala BIGSERIAL PRIMARY KEY,
    anio_vigencia INTEGER NOT NULL,
    fraccion_basica NUMERIC(12, 2) NOT NULL,
    exceso_hasta NUMERIC(12, 2), -- NULL significa "En adelante"
    impuesto_fraccion_basica NUMERIC(12, 2) NOT NULL,
    porcentaje_fraccion_excedente NUMERIC(5, 2) NOT NULL
);

-- ==========================================
-- 2. ESTRUCTURA ORGANIZACIONAL Y CARGOS
-- ==========================================
CREATE TABLE rrhh.area_organizacional (
    id_area BIGSERIAL PRIMARY KEY,
    id_area_padre BIGINT REFERENCES rrhh.area_organizacional(id_area),
    tipo_area VARCHAR(50) NOT NULL, 
    nombre VARCHAR(150) NOT NULL,
    estado VARCHAR(20) DEFAULT 'ACTIVO'
);

CREATE TABLE rrhh.escala_salarial (
    id_escala BIGSERIAL PRIMARY KEY,
    grado VARCHAR(20) NOT NULL,
    salario_base NUMERIC(10, 2) NOT NULL,
    regimen_laboral VARCHAR(50) NOT NULL 
);

CREATE TABLE rrhh.cargo (
    id_cargo BIGSERIAL PRIMARY KEY,
    nombre_cargo VARCHAR(150) NOT NULL,
    id_escala_salarial BIGINT REFERENCES rrhh.escala_salarial(id_escala),
    estado VARCHAR(20) DEFAULT 'ACTIVO'
);

-- ==========================================
-- 3. GESTIÓN DEL EMPLEADO Y CARGAS FAMILIARES
-- ==========================================
CREATE TABLE rrhh.empleado (
    id_empleado BIGSERIAL PRIMARY KEY,
    tipo_identificacion VARCHAR(20) DEFAULT 'CEDULA',
    identificacion VARCHAR(20) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero VARCHAR(20),
    porcentaje_discapacidad NUMERIC(5, 2) DEFAULT 0, -- Vital para beneficios tributarios
    aplica_iess BOOLEAN DEFAULT TRUE,
    acumula_fondos_reserva BOOLEAN DEFAULT TRUE,
    acumula_decimos BOOLEAN DEFAULT FALSE,
    estado_empleado VARCHAR(50) DEFAULT 'ACTIVO',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fundamental para cálculos de Renta y Utilidades
CREATE TABLE rrhh.empleado_carga_familiar (
    id_carga BIGSERIAL PRIMARY KEY,
    id_empleado BIGINT NOT NULL REFERENCES rrhh.empleado(id_empleado),
    identificacion VARCHAR(20),
    nombres_completos VARCHAR(200) NOT NULL,
    parentesco VARCHAR(50) NOT NULL, -- HIJO, CONYUGE, DISCAPACITADO
    fecha_nacimiento DATE NOT NULL,
    aplica_deduccion_ir BOOLEAN DEFAULT TRUE,
    estado VARCHAR(20) DEFAULT 'ACTIVO'
);

CREATE TABLE rrhh.historial_laboral (
    id_historial BIGSERIAL PRIMARY KEY,
    id_empleado BIGINT NOT NULL REFERENCES rrhh.empleado(id_empleado),
    id_area BIGINT NOT NULL REFERENCES rrhh.area_organizacional(id_area),
    id_cargo BIGINT NOT NULL REFERENCES rrhh.cargo(id_cargo),
    tipo_contrato VARCHAR(50) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    salario_acordado NUMERIC(10, 2) NOT NULL
);

-- ==========================================
-- 4. NÓMINA INTELIGENTE (RUBROS CON FÓRMULAS)
-- ==========================================
CREATE TABLE rrhh.rubro_nomina (
    id_rubro BIGSERIAL PRIMARY KEY,
    codigo_rubro VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    naturaleza VARCHAR(20) NOT NULL, -- INGRESO, DESCUENTO, PROVISION
    tipo_valor VARCHAR(20) NOT NULL, -- FIJO, PORCENTAJE, FORMULA
    formula_calculo TEXT, -- Ej: '(SUELDO_BASE / 240) * HORAS_EXTRAS * 1.5'
    orden_ejecucion INTEGER NOT NULL, -- Define qué rubro se calcula primero
    es_imponible BOOLEAN DEFAULT TRUE,
    estado VARCHAR(20) DEFAULT 'ACTIVO'
);

-- (Las tablas rol_pago_cabecera, rol_pago_empleado y novedad_nomina se mantienen igual a la V2)