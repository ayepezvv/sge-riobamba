--
-- PostgreSQL database dump
--

-- Dumped from database version 15.8 (Debian 15.8-1.pgdg110+1)
-- Dumped by pg_dump version 15.8 (Debian 15.8-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY core.parametros_sistema DROP CONSTRAINT IF EXISTS parametros_sistema_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY core.parametros_sistema DROP CONSTRAINT IF EXISTS parametros_sistema_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY core.audit_logs DROP CONSTRAINT IF EXISTS audit_logs_usuario_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.predios DROP CONSTRAINT IF EXISTS predios_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.predios DROP CONSTRAINT IF EXISTS predios_calle_secundaria_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.predios DROP CONSTRAINT IF EXISTS predios_calle_principal_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.predios DROP CONSTRAINT IF EXISTS predios_barrio_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.predios DROP CONSTRAINT IF EXISTS predios_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.medidores DROP CONSTRAINT IF EXISTS medidores_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.medidores DROP CONSTRAINT IF EXISTS medidores_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.historial_tarifa_cuenta DROP CONSTRAINT IF EXISTS historial_tarifa_cuenta_cuenta_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.historial_tarifa_cuenta DROP CONSTRAINT IF EXISTS historial_tarifa_cuenta_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.historial_tarifa_cuenta DROP CONSTRAINT IF EXISTS historial_tarifa_cuenta_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.historial_medidor_cuenta DROP CONSTRAINT IF EXISTS historial_medidor_cuenta_medidor_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.historial_medidor_cuenta DROP CONSTRAINT IF EXISTS historial_medidor_cuenta_cuenta_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.historial_medidor_cuenta DROP CONSTRAINT IF EXISTS historial_medidor_cuenta_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.historial_medidor_cuenta DROP CONSTRAINT IF EXISTS historial_medidor_cuenta_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.cuentas DROP CONSTRAINT IF EXISTS cuentas_responsable_pago_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.cuentas DROP CONSTRAINT IF EXISTS cuentas_propietario_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.cuentas DROP CONSTRAINT IF EXISTS cuentas_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.cuentas DROP CONSTRAINT IF EXISTS cuentas_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.cuentas DROP CONSTRAINT IF EXISTS cuentas_acometida_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.acometidas DROP CONSTRAINT IF EXISTS acometidas_ruta_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.acometidas DROP CONSTRAINT IF EXISTS acometidas_predio_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.acometidas DROP CONSTRAINT IF EXISTS acometidas_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY comercial.acometidas DROP CONSTRAINT IF EXISTS acometidas_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.sectores DROP CONSTRAINT IF EXISTS sectores_red_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.sectores DROP CONSTRAINT IF EXISTS sectores_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.sectores DROP CONSTRAINT IF EXISTS sectores_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.rutas DROP CONSTRAINT IF EXISTS rutas_sector_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.rutas DROP CONSTRAINT IF EXISTS rutas_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.rutas DROP CONSTRAINT IF EXISTS rutas_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.referencias_ciudadanos DROP CONSTRAINT IF EXISTS referencias_ciudadanos_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.referencias_ciudadanos DROP CONSTRAINT IF EXISTS referencias_ciudadanos_ciudadano_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.referencias_ciudadanos DROP CONSTRAINT IF EXISTS referencias_ciudadanos_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.redes DROP CONSTRAINT IF EXISTS redes_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.redes DROP CONSTRAINT IF EXISTS redes_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.ciudadanos DROP CONSTRAINT IF EXISTS ciudadanos_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.ciudadanos DROP CONSTRAINT IF EXISTS ciudadanos_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.calles DROP CONSTRAINT IF EXISTS calles_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.calles DROP CONSTRAINT IF EXISTS calles_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.barrios DROP CONSTRAINT IF EXISTS barrios_creado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY catastro.barrios DROP CONSTRAINT IF EXISTS barrios_actualizado_por_id_fkey;
ALTER TABLE IF EXISTS ONLY administracion.users DROP CONSTRAINT IF EXISTS users_role_id_fkey;
ALTER TABLE IF EXISTS ONLY administracion.role_permission DROP CONSTRAINT IF EXISTS role_permission_role_id_fkey;
ALTER TABLE IF EXISTS ONLY administracion.role_permission DROP CONSTRAINT IF EXISTS role_permission_permission_id_fkey;
DROP INDEX IF EXISTS core.ix_core_parametros_sistema_id;
DROP INDEX IF EXISTS core.ix_core_parametros_sistema_clave;
DROP INDEX IF EXISTS core.ix_core_audit_logs_tabla_afectada;
DROP INDEX IF EXISTS core.ix_core_audit_logs_registro_id;
DROP INDEX IF EXISTS core.ix_core_audit_logs_id;
DROP INDEX IF EXISTS comercial.ix_comercial_predios_id;
DROP INDEX IF EXISTS comercial.ix_comercial_predios_clave_catastral;
DROP INDEX IF EXISTS comercial.ix_comercial_medidores_serie;
DROP INDEX IF EXISTS comercial.ix_comercial_medidores_id;
DROP INDEX IF EXISTS comercial.ix_comercial_historial_tarifa_cuenta_id;
DROP INDEX IF EXISTS comercial.ix_comercial_historial_medidor_cuenta_id;
DROP INDEX IF EXISTS comercial.ix_comercial_cuentas_id;
DROP INDEX IF EXISTS comercial.ix_comercial_acometidas_id;
DROP INDEX IF EXISTS comercial.idx_predios_geometria;
DROP INDEX IF EXISTS comercial.idx_acometidas_geometria;
DROP INDEX IF EXISTS catastro.ix_catastro_sectores_id;
DROP INDEX IF EXISTS catastro.ix_catastro_sectores_codigo_sector;
DROP INDEX IF EXISTS catastro.ix_catastro_rutas_id;
DROP INDEX IF EXISTS catastro.ix_catastro_rutas_codigo_ruta;
DROP INDEX IF EXISTS catastro.ix_catastro_referencias_ciudadanos_id;
DROP INDEX IF EXISTS catastro.ix_catastro_redes_id;
DROP INDEX IF EXISTS catastro.ix_catastro_redes_codigo;
DROP INDEX IF EXISTS catastro.ix_catastro_ciudadanos_identificacion;
DROP INDEX IF EXISTS catastro.ix_catastro_ciudadanos_id;
DROP INDEX IF EXISTS catastro.ix_catastro_calles_nombre;
DROP INDEX IF EXISTS catastro.ix_catastro_calles_id;
DROP INDEX IF EXISTS catastro.ix_catastro_barrios_nombre;
DROP INDEX IF EXISTS catastro.ix_catastro_barrios_id;
DROP INDEX IF EXISTS catastro.idx_calles_geometria;
DROP INDEX IF EXISTS catastro.idx_barrios_geometria;
DROP INDEX IF EXISTS administracion.ix_administracion_users_id;
DROP INDEX IF EXISTS administracion.ix_administracion_users_correo;
DROP INDEX IF EXISTS administracion.ix_administracion_users_cedula;
DROP INDEX IF EXISTS administracion.ix_administracion_roles_nombre_rol;
DROP INDEX IF EXISTS administracion.ix_administracion_roles_id;
DROP INDEX IF EXISTS administracion.ix_administracion_permissions_nombre_permiso;
DROP INDEX IF EXISTS administracion.ix_administracion_permissions_id;
ALTER TABLE IF EXISTS ONLY public.alembic_version DROP CONSTRAINT IF EXISTS alembic_version_pkc;
ALTER TABLE IF EXISTS ONLY core.parametros_sistema DROP CONSTRAINT IF EXISTS parametros_sistema_pkey;
ALTER TABLE IF EXISTS ONLY core.audit_logs DROP CONSTRAINT IF EXISTS audit_logs_pkey;
ALTER TABLE IF EXISTS ONLY comercial.predios DROP CONSTRAINT IF EXISTS predios_pkey;
ALTER TABLE IF EXISTS ONLY comercial.medidores DROP CONSTRAINT IF EXISTS medidores_pkey;
ALTER TABLE IF EXISTS ONLY comercial.historial_tarifa_cuenta DROP CONSTRAINT IF EXISTS historial_tarifa_cuenta_pkey;
ALTER TABLE IF EXISTS ONLY comercial.historial_medidor_cuenta DROP CONSTRAINT IF EXISTS historial_medidor_cuenta_pkey;
ALTER TABLE IF EXISTS ONLY comercial.cuentas DROP CONSTRAINT IF EXISTS cuentas_pkey;
ALTER TABLE IF EXISTS ONLY comercial.acometidas DROP CONSTRAINT IF EXISTS acometidas_pkey;
ALTER TABLE IF EXISTS ONLY catastro.sectores DROP CONSTRAINT IF EXISTS sectores_pkey;
ALTER TABLE IF EXISTS ONLY catastro.rutas DROP CONSTRAINT IF EXISTS rutas_pkey;
ALTER TABLE IF EXISTS ONLY catastro.referencias_ciudadanos DROP CONSTRAINT IF EXISTS referencias_ciudadanos_pkey;
ALTER TABLE IF EXISTS ONLY catastro.redes DROP CONSTRAINT IF EXISTS redes_pkey;
ALTER TABLE IF EXISTS ONLY catastro.redes DROP CONSTRAINT IF EXISTS redes_nombre_key;
ALTER TABLE IF EXISTS ONLY catastro.ciudadanos DROP CONSTRAINT IF EXISTS ciudadanos_pkey;
ALTER TABLE IF EXISTS ONLY catastro.calles DROP CONSTRAINT IF EXISTS calles_pkey;
ALTER TABLE IF EXISTS ONLY catastro.barrios DROP CONSTRAINT IF EXISTS barrios_pkey;
ALTER TABLE IF EXISTS ONLY administracion.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY administracion.roles DROP CONSTRAINT IF EXISTS roles_pkey;
ALTER TABLE IF EXISTS ONLY administracion.role_permission DROP CONSTRAINT IF EXISTS role_permission_pkey;
ALTER TABLE IF EXISTS ONLY administracion.permissions DROP CONSTRAINT IF EXISTS permissions_pkey;
ALTER TABLE IF EXISTS core.parametros_sistema ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS core.audit_logs ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS comercial.predios ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS comercial.medidores ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS comercial.historial_tarifa_cuenta ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS comercial.historial_medidor_cuenta ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS comercial.cuentas ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS comercial.acometidas ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS catastro.sectores ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS catastro.rutas ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS catastro.referencias_ciudadanos ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS catastro.redes ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS catastro.ciudadanos ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS catastro.calles ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS catastro.barrios ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS administracion.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS administracion.roles ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS administracion.permissions ALTER COLUMN id DROP DEFAULT;
DROP TABLE IF EXISTS public.alembic_version;
DROP SEQUENCE IF EXISTS core.parametros_sistema_id_seq;
DROP TABLE IF EXISTS core.parametros_sistema;
DROP SEQUENCE IF EXISTS core.audit_logs_id_seq;
DROP TABLE IF EXISTS core.audit_logs;
DROP SEQUENCE IF EXISTS comercial.predios_id_seq;
DROP TABLE IF EXISTS comercial.predios;
DROP SEQUENCE IF EXISTS comercial.medidores_id_seq;
DROP TABLE IF EXISTS comercial.medidores;
DROP SEQUENCE IF EXISTS comercial.historial_tarifa_cuenta_id_seq;
DROP TABLE IF EXISTS comercial.historial_tarifa_cuenta;
DROP SEQUENCE IF EXISTS comercial.historial_medidor_cuenta_id_seq;
DROP TABLE IF EXISTS comercial.historial_medidor_cuenta;
DROP SEQUENCE IF EXISTS comercial.cuentas_id_seq;
DROP TABLE IF EXISTS comercial.cuentas;
DROP SEQUENCE IF EXISTS comercial.acometidas_id_seq;
DROP TABLE IF EXISTS comercial.acometidas;
DROP SEQUENCE IF EXISTS catastro.sectores_id_seq;
DROP TABLE IF EXISTS catastro.sectores;
DROP SEQUENCE IF EXISTS catastro.rutas_id_seq;
DROP TABLE IF EXISTS catastro.rutas;
DROP SEQUENCE IF EXISTS catastro.referencias_ciudadanos_id_seq;
DROP TABLE IF EXISTS catastro.referencias_ciudadanos;
DROP SEQUENCE IF EXISTS catastro.redes_id_seq;
DROP TABLE IF EXISTS catastro.redes;
DROP SEQUENCE IF EXISTS catastro.ciudadanos_id_seq;
DROP TABLE IF EXISTS catastro.ciudadanos;
DROP SEQUENCE IF EXISTS catastro.calles_id_seq;
DROP TABLE IF EXISTS catastro.calles;
DROP SEQUENCE IF EXISTS catastro.barrios_id_seq;
DROP TABLE IF EXISTS catastro.barrios;
DROP SEQUENCE IF EXISTS administracion.users_id_seq;
DROP TABLE IF EXISTS administracion.users;
DROP SEQUENCE IF EXISTS administracion.roles_id_seq;
DROP TABLE IF EXISTS administracion.roles;
DROP TABLE IF EXISTS administracion.role_permission;
DROP SEQUENCE IF EXISTS administracion.permissions_id_seq;
DROP TABLE IF EXISTS administracion.permissions;
DROP EXTENSION IF EXISTS postgis_topology;
DROP EXTENSION IF EXISTS postgis_tiger_geocoder;
DROP EXTENSION IF EXISTS postgis;
DROP EXTENSION IF EXISTS fuzzystrmatch;
DROP SCHEMA IF EXISTS topology;
DROP SCHEMA IF EXISTS tiger_data;
DROP SCHEMA IF EXISTS tiger;
DROP SCHEMA IF EXISTS core;
DROP SCHEMA IF EXISTS comercial;
DROP SCHEMA IF EXISTS catastro;
DROP SCHEMA IF EXISTS administracion;
--
-- Name: administracion; Type: SCHEMA; Schema: -; Owner: sge_admin
--

CREATE SCHEMA administracion;


ALTER SCHEMA administracion OWNER TO sge_admin;

--
-- Name: catastro; Type: SCHEMA; Schema: -; Owner: sge_admin
--

CREATE SCHEMA catastro;


ALTER SCHEMA catastro OWNER TO sge_admin;

--
-- Name: comercial; Type: SCHEMA; Schema: -; Owner: sge_admin
--

CREATE SCHEMA comercial;


ALTER SCHEMA comercial OWNER TO sge_admin;

--
-- Name: core; Type: SCHEMA; Schema: -; Owner: sge_admin
--

CREATE SCHEMA core;


ALTER SCHEMA core OWNER TO sge_admin;

--
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: sge_admin
--

CREATE SCHEMA tiger;


ALTER SCHEMA tiger OWNER TO sge_admin;

--
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: sge_admin
--

CREATE SCHEMA tiger_data;


ALTER SCHEMA tiger_data OWNER TO sge_admin;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: sge_admin
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO sge_admin;

--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: sge_admin
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: postgis_tiger_geocoder; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder WITH SCHEMA tiger;


--
-- Name: EXTENSION postgis_tiger_geocoder; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_tiger_geocoder IS 'PostGIS tiger geocoder and reverse geocoder';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: permissions; Type: TABLE; Schema: administracion; Owner: sge_admin
--

CREATE TABLE administracion.permissions (
    id integer NOT NULL,
    nombre_permiso character varying(100) NOT NULL
);


ALTER TABLE administracion.permissions OWNER TO sge_admin;

--
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: administracion; Owner: sge_admin
--

CREATE SEQUENCE administracion.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE administracion.permissions_id_seq OWNER TO sge_admin;

--
-- Name: permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: administracion; Owner: sge_admin
--

ALTER SEQUENCE administracion.permissions_id_seq OWNED BY administracion.permissions.id;


--
-- Name: role_permission; Type: TABLE; Schema: administracion; Owner: sge_admin
--

CREATE TABLE administracion.role_permission (
    role_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE administracion.role_permission OWNER TO sge_admin;

--
-- Name: roles; Type: TABLE; Schema: administracion; Owner: sge_admin
--

CREATE TABLE administracion.roles (
    id integer NOT NULL,
    nombre_rol character varying(50) NOT NULL,
    descripcion character varying(255)
);


ALTER TABLE administracion.roles OWNER TO sge_admin;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: administracion; Owner: sge_admin
--

CREATE SEQUENCE administracion.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE administracion.roles_id_seq OWNER TO sge_admin;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: administracion; Owner: sge_admin
--

ALTER SEQUENCE administracion.roles_id_seq OWNED BY administracion.roles.id;


--
-- Name: users; Type: TABLE; Schema: administracion; Owner: sge_admin
--

CREATE TABLE administracion.users (
    id integer NOT NULL,
    cedula character varying(20) NOT NULL,
    nombres character varying(100) NOT NULL,
    apellidos character varying(100) NOT NULL,
    correo character varying(100) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    is_active boolean,
    role_id integer
);


ALTER TABLE administracion.users OWNER TO sge_admin;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: administracion; Owner: sge_admin
--

CREATE SEQUENCE administracion.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE administracion.users_id_seq OWNER TO sge_admin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: administracion; Owner: sge_admin
--

ALTER SEQUENCE administracion.users_id_seq OWNED BY administracion.users.id;


--
-- Name: barrios; Type: TABLE; Schema: catastro; Owner: sge_admin
--

CREATE TABLE catastro.barrios (
    id integer NOT NULL,
    nombre character varying(150) NOT NULL,
    geometria public.geometry(MultiPolygon,4326),
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE catastro.barrios OWNER TO sge_admin;

--
-- Name: barrios_id_seq; Type: SEQUENCE; Schema: catastro; Owner: sge_admin
--

CREATE SEQUENCE catastro.barrios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE catastro.barrios_id_seq OWNER TO sge_admin;

--
-- Name: barrios_id_seq; Type: SEQUENCE OWNED BY; Schema: catastro; Owner: sge_admin
--

ALTER SEQUENCE catastro.barrios_id_seq OWNED BY catastro.barrios.id;


--
-- Name: calles; Type: TABLE; Schema: catastro; Owner: sge_admin
--

CREATE TABLE catastro.calles (
    id integer NOT NULL,
    nombre character varying(200) NOT NULL,
    tipo character varying(50) NOT NULL,
    geometria public.geometry(MultiLineString,4326),
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE catastro.calles OWNER TO sge_admin;

--
-- Name: calles_id_seq; Type: SEQUENCE; Schema: catastro; Owner: sge_admin
--

CREATE SEQUENCE catastro.calles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE catastro.calles_id_seq OWNER TO sge_admin;

--
-- Name: calles_id_seq; Type: SEQUENCE OWNED BY; Schema: catastro; Owner: sge_admin
--

ALTER SEQUENCE catastro.calles_id_seq OWNED BY catastro.calles.id;


--
-- Name: ciudadanos; Type: TABLE; Schema: catastro; Owner: sge_admin
--

CREATE TABLE catastro.ciudadanos (
    id integer NOT NULL,
    tipo_persona character varying(20) NOT NULL,
    identificacion character varying(20) NOT NULL,
    nombres character varying(100),
    apellidos character varying(100),
    razon_social character varying(200),
    correo_principal character varying(150),
    telefono_fijo character varying(20),
    celular character varying(20),
    preferencia_contacto character varying(50),
    redes_sociales jsonb,
    fecha_nacimiento date,
    nacionalidad character varying(50),
    genero character varying(20),
    estado_civil character varying(50),
    tiene_discapacidad boolean,
    porcentaje_discapacidad double precision,
    aplica_tercera_edad boolean,
    is_active boolean,
    tipo_empresa character varying(50),
    naturaleza_juridica character varying(50),
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE catastro.ciudadanos OWNER TO sge_admin;

--
-- Name: ciudadanos_id_seq; Type: SEQUENCE; Schema: catastro; Owner: sge_admin
--

CREATE SEQUENCE catastro.ciudadanos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE catastro.ciudadanos_id_seq OWNER TO sge_admin;

--
-- Name: ciudadanos_id_seq; Type: SEQUENCE OWNED BY; Schema: catastro; Owner: sge_admin
--

ALTER SEQUENCE catastro.ciudadanos_id_seq OWNED BY catastro.ciudadanos.id;


--
-- Name: redes; Type: TABLE; Schema: catastro; Owner: sge_admin
--

CREATE TABLE catastro.redes (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    codigo character varying(50) NOT NULL,
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE catastro.redes OWNER TO sge_admin;

--
-- Name: redes_id_seq; Type: SEQUENCE; Schema: catastro; Owner: sge_admin
--

CREATE SEQUENCE catastro.redes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE catastro.redes_id_seq OWNER TO sge_admin;

--
-- Name: redes_id_seq; Type: SEQUENCE OWNED BY; Schema: catastro; Owner: sge_admin
--

ALTER SEQUENCE catastro.redes_id_seq OWNED BY catastro.redes.id;


--
-- Name: referencias_ciudadanos; Type: TABLE; Schema: catastro; Owner: sge_admin
--

CREATE TABLE catastro.referencias_ciudadanos (
    id integer NOT NULL,
    ciudadano_id integer NOT NULL,
    tipo_referencia character varying(50) NOT NULL,
    nombres character varying(100) NOT NULL,
    apellidos character varying(100) NOT NULL,
    identificacion character varying(20),
    telefono character varying(20),
    correo character varying(150),
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE catastro.referencias_ciudadanos OWNER TO sge_admin;

--
-- Name: referencias_ciudadanos_id_seq; Type: SEQUENCE; Schema: catastro; Owner: sge_admin
--

CREATE SEQUENCE catastro.referencias_ciudadanos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE catastro.referencias_ciudadanos_id_seq OWNER TO sge_admin;

--
-- Name: referencias_ciudadanos_id_seq; Type: SEQUENCE OWNED BY; Schema: catastro; Owner: sge_admin
--

ALTER SEQUENCE catastro.referencias_ciudadanos_id_seq OWNED BY catastro.referencias_ciudadanos.id;


--
-- Name: rutas; Type: TABLE; Schema: catastro; Owner: sge_admin
--

CREATE TABLE catastro.rutas (
    id integer NOT NULL,
    sector_id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    codigo_ruta character varying(50) NOT NULL,
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE catastro.rutas OWNER TO sge_admin;

--
-- Name: rutas_id_seq; Type: SEQUENCE; Schema: catastro; Owner: sge_admin
--

CREATE SEQUENCE catastro.rutas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE catastro.rutas_id_seq OWNER TO sge_admin;

--
-- Name: rutas_id_seq; Type: SEQUENCE OWNED BY; Schema: catastro; Owner: sge_admin
--

ALTER SEQUENCE catastro.rutas_id_seq OWNED BY catastro.rutas.id;


--
-- Name: sectores; Type: TABLE; Schema: catastro; Owner: sge_admin
--

CREATE TABLE catastro.sectores (
    id integer NOT NULL,
    red_id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    codigo_sector character varying(50) NOT NULL,
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE catastro.sectores OWNER TO sge_admin;

--
-- Name: sectores_id_seq; Type: SEQUENCE; Schema: catastro; Owner: sge_admin
--

CREATE SEQUENCE catastro.sectores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE catastro.sectores_id_seq OWNER TO sge_admin;

--
-- Name: sectores_id_seq; Type: SEQUENCE OWNED BY; Schema: catastro; Owner: sge_admin
--

ALTER SEQUENCE catastro.sectores_id_seq OWNED BY catastro.sectores.id;


--
-- Name: acometidas; Type: TABLE; Schema: comercial; Owner: sge_admin
--

CREATE TABLE comercial.acometidas (
    id integer NOT NULL,
    predio_id integer NOT NULL,
    ruta_id integer,
    diametro double precision,
    material character varying(50),
    geometria public.geometry(Point,4326),
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE comercial.acometidas OWNER TO sge_admin;

--
-- Name: acometidas_id_seq; Type: SEQUENCE; Schema: comercial; Owner: sge_admin
--

CREATE SEQUENCE comercial.acometidas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comercial.acometidas_id_seq OWNER TO sge_admin;

--
-- Name: acometidas_id_seq; Type: SEQUENCE OWNED BY; Schema: comercial; Owner: sge_admin
--

ALTER SEQUENCE comercial.acometidas_id_seq OWNED BY comercial.acometidas.id;


--
-- Name: cuentas; Type: TABLE; Schema: comercial; Owner: sge_admin
--

CREATE TABLE comercial.cuentas (
    id integer NOT NULL,
    acometida_id integer NOT NULL,
    propietario_id integer NOT NULL,
    responsable_pago_id integer NOT NULL,
    secuencial_lectura integer,
    estado character varying(20) NOT NULL,
    tiene_alcantarillado boolean,
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE comercial.cuentas OWNER TO sge_admin;

--
-- Name: cuentas_id_seq; Type: SEQUENCE; Schema: comercial; Owner: sge_admin
--

CREATE SEQUENCE comercial.cuentas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comercial.cuentas_id_seq OWNER TO sge_admin;

--
-- Name: cuentas_id_seq; Type: SEQUENCE OWNED BY; Schema: comercial; Owner: sge_admin
--

ALTER SEQUENCE comercial.cuentas_id_seq OWNED BY comercial.cuentas.id;


--
-- Name: historial_medidor_cuenta; Type: TABLE; Schema: comercial; Owner: sge_admin
--

CREATE TABLE comercial.historial_medidor_cuenta (
    id integer NOT NULL,
    cuenta_id integer NOT NULL,
    medidor_id integer NOT NULL,
    fecha_instalacion date NOT NULL,
    fecha_retiro date,
    lectura_inicial integer NOT NULL,
    lectura_retiro integer,
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE comercial.historial_medidor_cuenta OWNER TO sge_admin;

--
-- Name: historial_medidor_cuenta_id_seq; Type: SEQUENCE; Schema: comercial; Owner: sge_admin
--

CREATE SEQUENCE comercial.historial_medidor_cuenta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comercial.historial_medidor_cuenta_id_seq OWNER TO sge_admin;

--
-- Name: historial_medidor_cuenta_id_seq; Type: SEQUENCE OWNED BY; Schema: comercial; Owner: sge_admin
--

ALTER SEQUENCE comercial.historial_medidor_cuenta_id_seq OWNED BY comercial.historial_medidor_cuenta.id;


--
-- Name: historial_tarifa_cuenta; Type: TABLE; Schema: comercial; Owner: sge_admin
--

CREATE TABLE comercial.historial_tarifa_cuenta (
    id integer NOT NULL,
    cuenta_id integer NOT NULL,
    tipo_tarifa character varying(50) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date,
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE comercial.historial_tarifa_cuenta OWNER TO sge_admin;

--
-- Name: historial_tarifa_cuenta_id_seq; Type: SEQUENCE; Schema: comercial; Owner: sge_admin
--

CREATE SEQUENCE comercial.historial_tarifa_cuenta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comercial.historial_tarifa_cuenta_id_seq OWNER TO sge_admin;

--
-- Name: historial_tarifa_cuenta_id_seq; Type: SEQUENCE OWNED BY; Schema: comercial; Owner: sge_admin
--

ALTER SEQUENCE comercial.historial_tarifa_cuenta_id_seq OWNED BY comercial.historial_tarifa_cuenta.id;


--
-- Name: medidores; Type: TABLE; Schema: comercial; Owner: sge_admin
--

CREATE TABLE comercial.medidores (
    id integer NOT NULL,
    marca character varying(50),
    serie character varying(50) NOT NULL,
    esferas integer,
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE comercial.medidores OWNER TO sge_admin;

--
-- Name: medidores_id_seq; Type: SEQUENCE; Schema: comercial; Owner: sge_admin
--

CREATE SEQUENCE comercial.medidores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comercial.medidores_id_seq OWNER TO sge_admin;

--
-- Name: medidores_id_seq; Type: SEQUENCE OWNED BY; Schema: comercial; Owner: sge_admin
--

ALTER SEQUENCE comercial.medidores_id_seq OWNED BY comercial.medidores.id;


--
-- Name: predios; Type: TABLE; Schema: comercial; Owner: sge_admin
--

CREATE TABLE comercial.predios (
    id integer NOT NULL,
    clave_catastral character varying(50) NOT NULL,
    barrio_id integer,
    calle_principal_id integer,
    calle_secundaria_id integer,
    numero_casa character varying(50),
    foto_fachada character varying(255),
    croquis character varying(255),
    geometria public.geometry(Geometry,4326),
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE comercial.predios OWNER TO sge_admin;

--
-- Name: predios_id_seq; Type: SEQUENCE; Schema: comercial; Owner: sge_admin
--

CREATE SEQUENCE comercial.predios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comercial.predios_id_seq OWNER TO sge_admin;

--
-- Name: predios_id_seq; Type: SEQUENCE OWNED BY; Schema: comercial; Owner: sge_admin
--

ALTER SEQUENCE comercial.predios_id_seq OWNED BY comercial.predios.id;


--
-- Name: audit_logs; Type: TABLE; Schema: core; Owner: sge_admin
--

CREATE TABLE core.audit_logs (
    id integer NOT NULL,
    tabla_afectada character varying(100) NOT NULL,
    registro_id integer NOT NULL,
    accion character varying(50) NOT NULL,
    valores_viejos text,
    valores_nuevos text,
    fecha_evento timestamp with time zone DEFAULT now() NOT NULL,
    usuario_id integer
);


ALTER TABLE core.audit_logs OWNER TO sge_admin;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE; Schema: core; Owner: sge_admin
--

CREATE SEQUENCE core.audit_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE core.audit_logs_id_seq OWNER TO sge_admin;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: sge_admin
--

ALTER SEQUENCE core.audit_logs_id_seq OWNED BY core.audit_logs.id;


--
-- Name: parametros_sistema; Type: TABLE; Schema: core; Owner: sge_admin
--

CREATE TABLE core.parametros_sistema (
    id integer NOT NULL,
    clave character varying(100) NOT NULL,
    valor character varying(255) NOT NULL,
    tipo_dato character varying(50) NOT NULL,
    descripcion character varying(255),
    creado_en timestamp with time zone DEFAULT now() NOT NULL,
    actualizado_en timestamp with time zone DEFAULT now() NOT NULL,
    creado_por_id integer,
    actualizado_por_id integer
);


ALTER TABLE core.parametros_sistema OWNER TO sge_admin;

--
-- Name: parametros_sistema_id_seq; Type: SEQUENCE; Schema: core; Owner: sge_admin
--

CREATE SEQUENCE core.parametros_sistema_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE core.parametros_sistema_id_seq OWNER TO sge_admin;

--
-- Name: parametros_sistema_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: sge_admin
--

ALTER SEQUENCE core.parametros_sistema_id_seq OWNED BY core.parametros_sistema.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: sge_admin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO sge_admin;

--
-- Name: permissions id; Type: DEFAULT; Schema: administracion; Owner: sge_admin
--

ALTER TABLE ONLY administracion.permissions ALTER COLUMN id SET DEFAULT nextval('administracion.permissions_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: administracion; Owner: sge_admin
--

ALTER TABLE ONLY administracion.roles ALTER COLUMN id SET DEFAULT nextval('administracion.roles_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: administracion; Owner: sge_admin
--

ALTER TABLE ONLY administracion.users ALTER COLUMN id SET DEFAULT nextval('administracion.users_id_seq'::regclass);


--
-- Name: barrios id; Type: DEFAULT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.barrios ALTER COLUMN id SET DEFAULT nextval('catastro.barrios_id_seq'::regclass);


--
-- Name: calles id; Type: DEFAULT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.calles ALTER COLUMN id SET DEFAULT nextval('catastro.calles_id_seq'::regclass);


--
-- Name: ciudadanos id; Type: DEFAULT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.ciudadanos ALTER COLUMN id SET DEFAULT nextval('catastro.ciudadanos_id_seq'::regclass);


--
-- Name: redes id; Type: DEFAULT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.redes ALTER COLUMN id SET DEFAULT nextval('catastro.redes_id_seq'::regclass);


--
-- Name: referencias_ciudadanos id; Type: DEFAULT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.referencias_ciudadanos ALTER COLUMN id SET DEFAULT nextval('catastro.referencias_ciudadanos_id_seq'::regclass);


--
-- Name: rutas id; Type: DEFAULT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.rutas ALTER COLUMN id SET DEFAULT nextval('catastro.rutas_id_seq'::regclass);


--
-- Name: sectores id; Type: DEFAULT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.sectores ALTER COLUMN id SET DEFAULT nextval('catastro.sectores_id_seq'::regclass);


--
-- Name: acometidas id; Type: DEFAULT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.acometidas ALTER COLUMN id SET DEFAULT nextval('comercial.acometidas_id_seq'::regclass);


--
-- Name: cuentas id; Type: DEFAULT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.cuentas ALTER COLUMN id SET DEFAULT nextval('comercial.cuentas_id_seq'::regclass);


--
-- Name: historial_medidor_cuenta id; Type: DEFAULT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.historial_medidor_cuenta ALTER COLUMN id SET DEFAULT nextval('comercial.historial_medidor_cuenta_id_seq'::regclass);


--
-- Name: historial_tarifa_cuenta id; Type: DEFAULT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.historial_tarifa_cuenta ALTER COLUMN id SET DEFAULT nextval('comercial.historial_tarifa_cuenta_id_seq'::regclass);


--
-- Name: medidores id; Type: DEFAULT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.medidores ALTER COLUMN id SET DEFAULT nextval('comercial.medidores_id_seq'::regclass);


--
-- Name: predios id; Type: DEFAULT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.predios ALTER COLUMN id SET DEFAULT nextval('comercial.predios_id_seq'::regclass);


--
-- Name: audit_logs id; Type: DEFAULT; Schema: core; Owner: sge_admin
--

ALTER TABLE ONLY core.audit_logs ALTER COLUMN id SET DEFAULT nextval('core.audit_logs_id_seq'::regclass);


--
-- Name: parametros_sistema id; Type: DEFAULT; Schema: core; Owner: sge_admin
--

ALTER TABLE ONLY core.parametros_sistema ALTER COLUMN id SET DEFAULT nextval('core.parametros_sistema_id_seq'::regclass);


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: administracion; Owner: sge_admin
--

COPY administracion.permissions (id, nombre_permiso) FROM stdin;
1	crear_usuario
2	editar_usuario
3	eliminar_usuario
4	gestionar_roles
5	anular_factura
6	crear_contrato
\.


--
-- Data for Name: role_permission; Type: TABLE DATA; Schema: administracion; Owner: sge_admin
--

COPY administracion.role_permission (role_id, permission_id) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: administracion; Owner: sge_admin
--

COPY administracion.roles (id, nombre_rol, descripcion) FROM stdin;
1	SuperAdmin	Administrador total del sistema
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: administracion; Owner: sge_admin
--

COPY administracion.users (id, cedula, nombres, apellidos, correo, hashed_password, is_active, role_id) FROM stdin;
1	0000000000	Admin	SGE	admin@riobambaep.gob.ec	$2b$12$9nUJzsv5MuwhJ08RJzyoAeepDicDhoaU5oOrLyGUqwMy14rXRIWua	t	1
\.


--
-- Data for Name: barrios; Type: TABLE DATA; Schema: catastro; Owner: sge_admin
--

COPY catastro.barrios (id, nombre, geometria, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: calles; Type: TABLE DATA; Schema: catastro; Owner: sge_admin
--

COPY catastro.calles (id, nombre, tipo, geometria, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: ciudadanos; Type: TABLE DATA; Schema: catastro; Owner: sge_admin
--

COPY catastro.ciudadanos (id, tipo_persona, identificacion, nombres, apellidos, razon_social, correo_principal, telefono_fijo, celular, preferencia_contacto, redes_sociales, fecha_nacimiento, nacionalidad, genero, estado_civil, tiene_discapacidad, porcentaje_discapacidad, aplica_tercera_edad, is_active, tipo_empresa, naturaleza_juridica, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: redes; Type: TABLE DATA; Schema: catastro; Owner: sge_admin
--

COPY catastro.redes (id, nombre, codigo, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: referencias_ciudadanos; Type: TABLE DATA; Schema: catastro; Owner: sge_admin
--

COPY catastro.referencias_ciudadanos (id, ciudadano_id, tipo_referencia, nombres, apellidos, identificacion, telefono, correo, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: rutas; Type: TABLE DATA; Schema: catastro; Owner: sge_admin
--

COPY catastro.rutas (id, sector_id, nombre, codigo_ruta, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: sectores; Type: TABLE DATA; Schema: catastro; Owner: sge_admin
--

COPY catastro.sectores (id, red_id, nombre, codigo_sector, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: acometidas; Type: TABLE DATA; Schema: comercial; Owner: sge_admin
--

COPY comercial.acometidas (id, predio_id, ruta_id, diametro, material, geometria, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: cuentas; Type: TABLE DATA; Schema: comercial; Owner: sge_admin
--

COPY comercial.cuentas (id, acometida_id, propietario_id, responsable_pago_id, secuencial_lectura, estado, tiene_alcantarillado, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: historial_medidor_cuenta; Type: TABLE DATA; Schema: comercial; Owner: sge_admin
--

COPY comercial.historial_medidor_cuenta (id, cuenta_id, medidor_id, fecha_instalacion, fecha_retiro, lectura_inicial, lectura_retiro, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: historial_tarifa_cuenta; Type: TABLE DATA; Schema: comercial; Owner: sge_admin
--

COPY comercial.historial_tarifa_cuenta (id, cuenta_id, tipo_tarifa, fecha_inicio, fecha_fin, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: medidores; Type: TABLE DATA; Schema: comercial; Owner: sge_admin
--

COPY comercial.medidores (id, marca, serie, esferas, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: predios; Type: TABLE DATA; Schema: comercial; Owner: sge_admin
--

COPY comercial.predios (id, clave_catastral, barrio_id, calle_principal_id, calle_secundaria_id, numero_casa, foto_fachada, croquis, geometria, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: core; Owner: sge_admin
--

COPY core.audit_logs (id, tabla_afectada, registro_id, accion, valores_viejos, valores_nuevos, fecha_evento, usuario_id) FROM stdin;
\.


--
-- Data for Name: parametros_sistema; Type: TABLE DATA; Schema: core; Owner: sge_admin
--

COPY core.parametros_sistema (id, clave, valor, tipo_dato, descripcion, creado_en, actualizado_en, creado_por_id, actualizado_por_id) FROM stdin;
1	SRID_LOCAL	32717	int	SRID para proyecciones metricas locales (Ej. UTM Zona 17S)	2026-03-05 17:21:16.578223+00	2026-03-05 17:21:16.578223+00	\N	\N
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: sge_admin
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: sge_admin
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: geocode_settings; Type: TABLE DATA; Schema: tiger; Owner: sge_admin
--

COPY tiger.geocode_settings (name, setting, unit, category, short_desc) FROM stdin;
\.


--
-- Data for Name: pagc_gaz; Type: TABLE DATA; Schema: tiger; Owner: sge_admin
--

COPY tiger.pagc_gaz (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_lex; Type: TABLE DATA; Schema: tiger; Owner: sge_admin
--

COPY tiger.pagc_lex (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_rules; Type: TABLE DATA; Schema: tiger; Owner: sge_admin
--

COPY tiger.pagc_rules (id, rule, is_custom) FROM stdin;
\.


--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: sge_admin
--

COPY topology.topology (id, name, srid, "precision", hasz) FROM stdin;
\.


--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: sge_admin
--

COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- Name: permissions_id_seq; Type: SEQUENCE SET; Schema: administracion; Owner: sge_admin
--

SELECT pg_catalog.setval('administracion.permissions_id_seq', 6, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: administracion; Owner: sge_admin
--

SELECT pg_catalog.setval('administracion.roles_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: administracion; Owner: sge_admin
--

SELECT pg_catalog.setval('administracion.users_id_seq', 1, true);


--
-- Name: barrios_id_seq; Type: SEQUENCE SET; Schema: catastro; Owner: sge_admin
--

SELECT pg_catalog.setval('catastro.barrios_id_seq', 1, false);


--
-- Name: calles_id_seq; Type: SEQUENCE SET; Schema: catastro; Owner: sge_admin
--

SELECT pg_catalog.setval('catastro.calles_id_seq', 1, false);


--
-- Name: ciudadanos_id_seq; Type: SEQUENCE SET; Schema: catastro; Owner: sge_admin
--

SELECT pg_catalog.setval('catastro.ciudadanos_id_seq', 1, false);


--
-- Name: redes_id_seq; Type: SEQUENCE SET; Schema: catastro; Owner: sge_admin
--

SELECT pg_catalog.setval('catastro.redes_id_seq', 1, false);


--
-- Name: referencias_ciudadanos_id_seq; Type: SEQUENCE SET; Schema: catastro; Owner: sge_admin
--

SELECT pg_catalog.setval('catastro.referencias_ciudadanos_id_seq', 1, false);


--
-- Name: rutas_id_seq; Type: SEQUENCE SET; Schema: catastro; Owner: sge_admin
--

SELECT pg_catalog.setval('catastro.rutas_id_seq', 1, false);


--
-- Name: sectores_id_seq; Type: SEQUENCE SET; Schema: catastro; Owner: sge_admin
--

SELECT pg_catalog.setval('catastro.sectores_id_seq', 1, false);


--
-- Name: acometidas_id_seq; Type: SEQUENCE SET; Schema: comercial; Owner: sge_admin
--

SELECT pg_catalog.setval('comercial.acometidas_id_seq', 1, false);


--
-- Name: cuentas_id_seq; Type: SEQUENCE SET; Schema: comercial; Owner: sge_admin
--

SELECT pg_catalog.setval('comercial.cuentas_id_seq', 1, false);


--
-- Name: historial_medidor_cuenta_id_seq; Type: SEQUENCE SET; Schema: comercial; Owner: sge_admin
--

SELECT pg_catalog.setval('comercial.historial_medidor_cuenta_id_seq', 1, false);


--
-- Name: historial_tarifa_cuenta_id_seq; Type: SEQUENCE SET; Schema: comercial; Owner: sge_admin
--

SELECT pg_catalog.setval('comercial.historial_tarifa_cuenta_id_seq', 1, false);


--
-- Name: medidores_id_seq; Type: SEQUENCE SET; Schema: comercial; Owner: sge_admin
--

SELECT pg_catalog.setval('comercial.medidores_id_seq', 1, false);


--
-- Name: predios_id_seq; Type: SEQUENCE SET; Schema: comercial; Owner: sge_admin
--

SELECT pg_catalog.setval('comercial.predios_id_seq', 1, false);


--
-- Name: audit_logs_id_seq; Type: SEQUENCE SET; Schema: core; Owner: sge_admin
--

SELECT pg_catalog.setval('core.audit_logs_id_seq', 1, false);


--
-- Name: parametros_sistema_id_seq; Type: SEQUENCE SET; Schema: core; Owner: sge_admin
--

SELECT pg_catalog.setval('core.parametros_sistema_id_seq', 1, true);


--
-- Name: topology_id_seq; Type: SEQUENCE SET; Schema: topology; Owner: sge_admin
--

SELECT pg_catalog.setval('topology.topology_id_seq', 1, false);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: administracion; Owner: sge_admin
--

ALTER TABLE ONLY administracion.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: role_permission role_permission_pkey; Type: CONSTRAINT; Schema: administracion; Owner: sge_admin
--

ALTER TABLE ONLY administracion.role_permission
    ADD CONSTRAINT role_permission_pkey PRIMARY KEY (role_id, permission_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: administracion; Owner: sge_admin
--

ALTER TABLE ONLY administracion.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: administracion; Owner: sge_admin
--

ALTER TABLE ONLY administracion.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: barrios barrios_pkey; Type: CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.barrios
    ADD CONSTRAINT barrios_pkey PRIMARY KEY (id);


--
-- Name: calles calles_pkey; Type: CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.calles
    ADD CONSTRAINT calles_pkey PRIMARY KEY (id);


--
-- Name: ciudadanos ciudadanos_pkey; Type: CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.ciudadanos
    ADD CONSTRAINT ciudadanos_pkey PRIMARY KEY (id);


--
-- Name: redes redes_nombre_key; Type: CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.redes
    ADD CONSTRAINT redes_nombre_key UNIQUE (nombre);


--
-- Name: redes redes_pkey; Type: CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.redes
    ADD CONSTRAINT redes_pkey PRIMARY KEY (id);


--
-- Name: referencias_ciudadanos referencias_ciudadanos_pkey; Type: CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.referencias_ciudadanos
    ADD CONSTRAINT referencias_ciudadanos_pkey PRIMARY KEY (id);


--
-- Name: rutas rutas_pkey; Type: CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.rutas
    ADD CONSTRAINT rutas_pkey PRIMARY KEY (id);


--
-- Name: sectores sectores_pkey; Type: CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.sectores
    ADD CONSTRAINT sectores_pkey PRIMARY KEY (id);


--
-- Name: acometidas acometidas_pkey; Type: CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.acometidas
    ADD CONSTRAINT acometidas_pkey PRIMARY KEY (id);


--
-- Name: cuentas cuentas_pkey; Type: CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.cuentas
    ADD CONSTRAINT cuentas_pkey PRIMARY KEY (id);


--
-- Name: historial_medidor_cuenta historial_medidor_cuenta_pkey; Type: CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.historial_medidor_cuenta
    ADD CONSTRAINT historial_medidor_cuenta_pkey PRIMARY KEY (id);


--
-- Name: historial_tarifa_cuenta historial_tarifa_cuenta_pkey; Type: CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.historial_tarifa_cuenta
    ADD CONSTRAINT historial_tarifa_cuenta_pkey PRIMARY KEY (id);


--
-- Name: medidores medidores_pkey; Type: CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.medidores
    ADD CONSTRAINT medidores_pkey PRIMARY KEY (id);


--
-- Name: predios predios_pkey; Type: CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.predios
    ADD CONSTRAINT predios_pkey PRIMARY KEY (id);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: core; Owner: sge_admin
--

ALTER TABLE ONLY core.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: parametros_sistema parametros_sistema_pkey; Type: CONSTRAINT; Schema: core; Owner: sge_admin
--

ALTER TABLE ONLY core.parametros_sistema
    ADD CONSTRAINT parametros_sistema_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: sge_admin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: ix_administracion_permissions_id; Type: INDEX; Schema: administracion; Owner: sge_admin
--

CREATE INDEX ix_administracion_permissions_id ON administracion.permissions USING btree (id);


--
-- Name: ix_administracion_permissions_nombre_permiso; Type: INDEX; Schema: administracion; Owner: sge_admin
--

CREATE UNIQUE INDEX ix_administracion_permissions_nombre_permiso ON administracion.permissions USING btree (nombre_permiso);


--
-- Name: ix_administracion_roles_id; Type: INDEX; Schema: administracion; Owner: sge_admin
--

CREATE INDEX ix_administracion_roles_id ON administracion.roles USING btree (id);


--
-- Name: ix_administracion_roles_nombre_rol; Type: INDEX; Schema: administracion; Owner: sge_admin
--

CREATE UNIQUE INDEX ix_administracion_roles_nombre_rol ON administracion.roles USING btree (nombre_rol);


--
-- Name: ix_administracion_users_cedula; Type: INDEX; Schema: administracion; Owner: sge_admin
--

CREATE UNIQUE INDEX ix_administracion_users_cedula ON administracion.users USING btree (cedula);


--
-- Name: ix_administracion_users_correo; Type: INDEX; Schema: administracion; Owner: sge_admin
--

CREATE UNIQUE INDEX ix_administracion_users_correo ON administracion.users USING btree (correo);


--
-- Name: ix_administracion_users_id; Type: INDEX; Schema: administracion; Owner: sge_admin
--

CREATE INDEX ix_administracion_users_id ON administracion.users USING btree (id);


--
-- Name: idx_barrios_geometria; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE INDEX idx_barrios_geometria ON catastro.barrios USING gist (geometria);


--
-- Name: idx_calles_geometria; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE INDEX idx_calles_geometria ON catastro.calles USING gist (geometria);


--
-- Name: ix_catastro_barrios_id; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE INDEX ix_catastro_barrios_id ON catastro.barrios USING btree (id);


--
-- Name: ix_catastro_barrios_nombre; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE INDEX ix_catastro_barrios_nombre ON catastro.barrios USING btree (nombre);


--
-- Name: ix_catastro_calles_id; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE INDEX ix_catastro_calles_id ON catastro.calles USING btree (id);


--
-- Name: ix_catastro_calles_nombre; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE INDEX ix_catastro_calles_nombre ON catastro.calles USING btree (nombre);


--
-- Name: ix_catastro_ciudadanos_id; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE INDEX ix_catastro_ciudadanos_id ON catastro.ciudadanos USING btree (id);


--
-- Name: ix_catastro_ciudadanos_identificacion; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE UNIQUE INDEX ix_catastro_ciudadanos_identificacion ON catastro.ciudadanos USING btree (identificacion);


--
-- Name: ix_catastro_redes_codigo; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE UNIQUE INDEX ix_catastro_redes_codigo ON catastro.redes USING btree (codigo);


--
-- Name: ix_catastro_redes_id; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE INDEX ix_catastro_redes_id ON catastro.redes USING btree (id);


--
-- Name: ix_catastro_referencias_ciudadanos_id; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE INDEX ix_catastro_referencias_ciudadanos_id ON catastro.referencias_ciudadanos USING btree (id);


--
-- Name: ix_catastro_rutas_codigo_ruta; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE UNIQUE INDEX ix_catastro_rutas_codigo_ruta ON catastro.rutas USING btree (codigo_ruta);


--
-- Name: ix_catastro_rutas_id; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE INDEX ix_catastro_rutas_id ON catastro.rutas USING btree (id);


--
-- Name: ix_catastro_sectores_codigo_sector; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE UNIQUE INDEX ix_catastro_sectores_codigo_sector ON catastro.sectores USING btree (codigo_sector);


--
-- Name: ix_catastro_sectores_id; Type: INDEX; Schema: catastro; Owner: sge_admin
--

CREATE INDEX ix_catastro_sectores_id ON catastro.sectores USING btree (id);


--
-- Name: idx_acometidas_geometria; Type: INDEX; Schema: comercial; Owner: sge_admin
--

CREATE INDEX idx_acometidas_geometria ON comercial.acometidas USING gist (geometria);


--
-- Name: idx_predios_geometria; Type: INDEX; Schema: comercial; Owner: sge_admin
--

CREATE INDEX idx_predios_geometria ON comercial.predios USING gist (geometria);


--
-- Name: ix_comercial_acometidas_id; Type: INDEX; Schema: comercial; Owner: sge_admin
--

CREATE INDEX ix_comercial_acometidas_id ON comercial.acometidas USING btree (id);


--
-- Name: ix_comercial_cuentas_id; Type: INDEX; Schema: comercial; Owner: sge_admin
--

CREATE INDEX ix_comercial_cuentas_id ON comercial.cuentas USING btree (id);


--
-- Name: ix_comercial_historial_medidor_cuenta_id; Type: INDEX; Schema: comercial; Owner: sge_admin
--

CREATE INDEX ix_comercial_historial_medidor_cuenta_id ON comercial.historial_medidor_cuenta USING btree (id);


--
-- Name: ix_comercial_historial_tarifa_cuenta_id; Type: INDEX; Schema: comercial; Owner: sge_admin
--

CREATE INDEX ix_comercial_historial_tarifa_cuenta_id ON comercial.historial_tarifa_cuenta USING btree (id);


--
-- Name: ix_comercial_medidores_id; Type: INDEX; Schema: comercial; Owner: sge_admin
--

CREATE INDEX ix_comercial_medidores_id ON comercial.medidores USING btree (id);


--
-- Name: ix_comercial_medidores_serie; Type: INDEX; Schema: comercial; Owner: sge_admin
--

CREATE UNIQUE INDEX ix_comercial_medidores_serie ON comercial.medidores USING btree (serie);


--
-- Name: ix_comercial_predios_clave_catastral; Type: INDEX; Schema: comercial; Owner: sge_admin
--

CREATE UNIQUE INDEX ix_comercial_predios_clave_catastral ON comercial.predios USING btree (clave_catastral);


--
-- Name: ix_comercial_predios_id; Type: INDEX; Schema: comercial; Owner: sge_admin
--

CREATE INDEX ix_comercial_predios_id ON comercial.predios USING btree (id);


--
-- Name: ix_core_audit_logs_id; Type: INDEX; Schema: core; Owner: sge_admin
--

CREATE INDEX ix_core_audit_logs_id ON core.audit_logs USING btree (id);


--
-- Name: ix_core_audit_logs_registro_id; Type: INDEX; Schema: core; Owner: sge_admin
--

CREATE INDEX ix_core_audit_logs_registro_id ON core.audit_logs USING btree (registro_id);


--
-- Name: ix_core_audit_logs_tabla_afectada; Type: INDEX; Schema: core; Owner: sge_admin
--

CREATE INDEX ix_core_audit_logs_tabla_afectada ON core.audit_logs USING btree (tabla_afectada);


--
-- Name: ix_core_parametros_sistema_clave; Type: INDEX; Schema: core; Owner: sge_admin
--

CREATE UNIQUE INDEX ix_core_parametros_sistema_clave ON core.parametros_sistema USING btree (clave);


--
-- Name: ix_core_parametros_sistema_id; Type: INDEX; Schema: core; Owner: sge_admin
--

CREATE INDEX ix_core_parametros_sistema_id ON core.parametros_sistema USING btree (id);


--
-- Name: role_permission role_permission_permission_id_fkey; Type: FK CONSTRAINT; Schema: administracion; Owner: sge_admin
--

ALTER TABLE ONLY administracion.role_permission
    ADD CONSTRAINT role_permission_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES administracion.permissions(id) ON DELETE CASCADE;


--
-- Name: role_permission role_permission_role_id_fkey; Type: FK CONSTRAINT; Schema: administracion; Owner: sge_admin
--

ALTER TABLE ONLY administracion.role_permission
    ADD CONSTRAINT role_permission_role_id_fkey FOREIGN KEY (role_id) REFERENCES administracion.roles(id) ON DELETE CASCADE;


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: administracion; Owner: sge_admin
--

ALTER TABLE ONLY administracion.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES administracion.roles(id) ON DELETE SET NULL;


--
-- Name: barrios barrios_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.barrios
    ADD CONSTRAINT barrios_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: barrios barrios_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.barrios
    ADD CONSTRAINT barrios_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: calles calles_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.calles
    ADD CONSTRAINT calles_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: calles calles_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.calles
    ADD CONSTRAINT calles_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: ciudadanos ciudadanos_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.ciudadanos
    ADD CONSTRAINT ciudadanos_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: ciudadanos ciudadanos_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.ciudadanos
    ADD CONSTRAINT ciudadanos_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: redes redes_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.redes
    ADD CONSTRAINT redes_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: redes redes_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.redes
    ADD CONSTRAINT redes_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: referencias_ciudadanos referencias_ciudadanos_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.referencias_ciudadanos
    ADD CONSTRAINT referencias_ciudadanos_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: referencias_ciudadanos referencias_ciudadanos_ciudadano_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.referencias_ciudadanos
    ADD CONSTRAINT referencias_ciudadanos_ciudadano_id_fkey FOREIGN KEY (ciudadano_id) REFERENCES catastro.ciudadanos(id) ON DELETE CASCADE;


--
-- Name: referencias_ciudadanos referencias_ciudadanos_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.referencias_ciudadanos
    ADD CONSTRAINT referencias_ciudadanos_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: rutas rutas_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.rutas
    ADD CONSTRAINT rutas_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: rutas rutas_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.rutas
    ADD CONSTRAINT rutas_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: rutas rutas_sector_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.rutas
    ADD CONSTRAINT rutas_sector_id_fkey FOREIGN KEY (sector_id) REFERENCES catastro.sectores(id) ON DELETE CASCADE;


--
-- Name: sectores sectores_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.sectores
    ADD CONSTRAINT sectores_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: sectores sectores_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.sectores
    ADD CONSTRAINT sectores_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: sectores sectores_red_id_fkey; Type: FK CONSTRAINT; Schema: catastro; Owner: sge_admin
--

ALTER TABLE ONLY catastro.sectores
    ADD CONSTRAINT sectores_red_id_fkey FOREIGN KEY (red_id) REFERENCES catastro.redes(id) ON DELETE CASCADE;


--
-- Name: acometidas acometidas_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.acometidas
    ADD CONSTRAINT acometidas_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: acometidas acometidas_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.acometidas
    ADD CONSTRAINT acometidas_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: acometidas acometidas_predio_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.acometidas
    ADD CONSTRAINT acometidas_predio_id_fkey FOREIGN KEY (predio_id) REFERENCES comercial.predios(id) ON DELETE CASCADE;


--
-- Name: acometidas acometidas_ruta_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.acometidas
    ADD CONSTRAINT acometidas_ruta_id_fkey FOREIGN KEY (ruta_id) REFERENCES catastro.rutas(id) ON DELETE RESTRICT;


--
-- Name: cuentas cuentas_acometida_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.cuentas
    ADD CONSTRAINT cuentas_acometida_id_fkey FOREIGN KEY (acometida_id) REFERENCES comercial.acometidas(id) ON DELETE RESTRICT;


--
-- Name: cuentas cuentas_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.cuentas
    ADD CONSTRAINT cuentas_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: cuentas cuentas_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.cuentas
    ADD CONSTRAINT cuentas_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: cuentas cuentas_propietario_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.cuentas
    ADD CONSTRAINT cuentas_propietario_id_fkey FOREIGN KEY (propietario_id) REFERENCES catastro.ciudadanos(id) ON DELETE RESTRICT;


--
-- Name: cuentas cuentas_responsable_pago_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.cuentas
    ADD CONSTRAINT cuentas_responsable_pago_id_fkey FOREIGN KEY (responsable_pago_id) REFERENCES catastro.ciudadanos(id) ON DELETE RESTRICT;


--
-- Name: historial_medidor_cuenta historial_medidor_cuenta_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.historial_medidor_cuenta
    ADD CONSTRAINT historial_medidor_cuenta_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: historial_medidor_cuenta historial_medidor_cuenta_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.historial_medidor_cuenta
    ADD CONSTRAINT historial_medidor_cuenta_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: historial_medidor_cuenta historial_medidor_cuenta_cuenta_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.historial_medidor_cuenta
    ADD CONSTRAINT historial_medidor_cuenta_cuenta_id_fkey FOREIGN KEY (cuenta_id) REFERENCES comercial.cuentas(id) ON DELETE CASCADE;


--
-- Name: historial_medidor_cuenta historial_medidor_cuenta_medidor_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.historial_medidor_cuenta
    ADD CONSTRAINT historial_medidor_cuenta_medidor_id_fkey FOREIGN KEY (medidor_id) REFERENCES comercial.medidores(id) ON DELETE RESTRICT;


--
-- Name: historial_tarifa_cuenta historial_tarifa_cuenta_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.historial_tarifa_cuenta
    ADD CONSTRAINT historial_tarifa_cuenta_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: historial_tarifa_cuenta historial_tarifa_cuenta_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.historial_tarifa_cuenta
    ADD CONSTRAINT historial_tarifa_cuenta_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: historial_tarifa_cuenta historial_tarifa_cuenta_cuenta_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.historial_tarifa_cuenta
    ADD CONSTRAINT historial_tarifa_cuenta_cuenta_id_fkey FOREIGN KEY (cuenta_id) REFERENCES comercial.cuentas(id) ON DELETE CASCADE;


--
-- Name: medidores medidores_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.medidores
    ADD CONSTRAINT medidores_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: medidores medidores_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.medidores
    ADD CONSTRAINT medidores_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: predios predios_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.predios
    ADD CONSTRAINT predios_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: predios predios_barrio_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.predios
    ADD CONSTRAINT predios_barrio_id_fkey FOREIGN KEY (barrio_id) REFERENCES catastro.barrios(id) ON DELETE SET NULL;


--
-- Name: predios predios_calle_principal_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.predios
    ADD CONSTRAINT predios_calle_principal_id_fkey FOREIGN KEY (calle_principal_id) REFERENCES catastro.calles(id) ON DELETE SET NULL;


--
-- Name: predios predios_calle_secundaria_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.predios
    ADD CONSTRAINT predios_calle_secundaria_id_fkey FOREIGN KEY (calle_secundaria_id) REFERENCES catastro.calles(id) ON DELETE SET NULL;


--
-- Name: predios predios_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: comercial; Owner: sge_admin
--

ALTER TABLE ONLY comercial.predios
    ADD CONSTRAINT predios_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: audit_logs audit_logs_usuario_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: sge_admin
--

ALTER TABLE ONLY core.audit_logs
    ADD CONSTRAINT audit_logs_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: parametros_sistema parametros_sistema_actualizado_por_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: sge_admin
--

ALTER TABLE ONLY core.parametros_sistema
    ADD CONSTRAINT parametros_sistema_actualizado_por_id_fkey FOREIGN KEY (actualizado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- Name: parametros_sistema parametros_sistema_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: sge_admin
--

ALTER TABLE ONLY core.parametros_sistema
    ADD CONSTRAINT parametros_sistema_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES administracion.users(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

