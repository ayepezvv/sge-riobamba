# Documento de Arquitectura del Sistema — SGE

**Sistema de Gestión Empresarial (SGE) — Unidad de Tecnologías de Riobamba EP**
**Versión:** 1.0 | **Fecha:** Abril 2026

---

## 1. Visión General

El SGE es un sistema web modular para la gestión financiera, administrativa y de talento humano de la Unidad de Tecnologías de Riobamba EP. Está construido sobre una arquitectura **cliente-servidor** con API REST.

```
┌─────────────────────────────────────────┐
│           FRONTEND (Berry UI)           │
│         React + Material UI             │
│        http://192.168.1.15:3000         │
└────────────────────┬────────────────────┘
                     │ HTTP/REST (JSON)
┌────────────────────▼────────────────────┐
│           BACKEND (FastAPI)             │
│           Python 3.x + SQLAlchemy       │
│        http://192.168.1.15:8000         │
└────────────────────┬────────────────────┘
                     │ SQL
┌────────────────────▼────────────────────┐
│           BASE DE DATOS                 │
│              PostgreSQL                 │
│          (multi-esquema)                │
└─────────────────────────────────────────┘
```

---

## 2. Stack Tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Frontend | React + Berry Admin UI | — |
| Backend | FastAPI (Python) | — |
| ORM | SQLAlchemy + Alembic | — |
| Base de datos | PostgreSQL | — |
| Autenticación | JWT (Bearer Token) | — |
| Contenedores | Docker / docker-compose | — |

---

## 3. Módulos del Backend

Todos los módulos son routers FastAPI registrados en `backend/app/main.py`.

| Módulo | Prefijo API | Descripción |
|--------|------------|-------------|
| Autenticación | `/api/auth` | Login, refresh token, logout |
| Usuarios | `/api/users` | Gestión de usuarios del sistema |
| Roles | `/api/roles` | Definición de roles de acceso |
| Permisos | `/api/permissions` | Permisos granulares |
| Parámetros | `/api/parametros` | Parámetros globales del sistema |
| Territorio | `/api/territorio` | Provincias, cantones, parroquias |
| Ciudadanos | `/api/ciudadanos` | Registro de ciudadanos |
| Comercial | `/api/comercial` | Gestión comercial |
| Contratación | `/api/contratacion` | Procesos contractuales |
| Administrativo | `/api/administrativo` | Gestión administrativa |
| Informática | `/api/informatica` | Activos TIC y soporte |
| RRHH | `/api/rrhh` | Talento Humano (áreas, cargos, empleados, contratos) |
| Nómina | `/api/rrhh/nomina` | Rol de pagos y SPI |
| Bodega | `/api/bodega` | Control de inventario físico |
| Contabilidad | `/api/contabilidad` | Plan de cuentas, diarios, asientos |
| Tesorería | `/api/tesoreria` | Cuentas bancarias, caja chica, SPI |
| Financiero | `/api/financiero` | Informes y análisis financiero |
| Presupuesto | `/api/presupuesto` | Partidas, certificaciones, compromisos |
| Compras Públicas | `/api/compras` | Procesos SERCOP / PAC |

---

## 4. Estructura del Repositorio

```
sge/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py          # Dependencias (auth, db, roles)
│   │   │   └── routes/          # Un archivo .py por módulo
│   │   ├── core/                # Configuración central (JWT, settings)
│   │   ├── db/                  # Sesión de base de datos
│   │   ├── models/              # Modelos SQLAlchemy
│   │   ├── schemas/             # Esquemas Pydantic (request/response)
│   │   ├── services/            # Lógica de negocio compleja
│   │   └── main.py              # Punto de entrada FastAPI
│   ├── alembic/                 # Migraciones de base de datos
│   └── requirements.txt
├── frontend/                    # Aplicación React (Berry Admin)
├── docs/                        # Documentación (este directorio)
├── db_backups/                  # Respaldos de base de datos
├── docker-compose.yml
└── .env.example
```

---

## 5. Arquitectura de la Base de Datos (Multi-Esquema)

PostgreSQL se organiza en **esquemas separados** por dominio funcional para aislar datos y facilitar migraciones independientes:

| Esquema | Módulos |
|---------|---------|
| `public` | Usuarios, roles, permisos, parámetros, territorio |
| `rrhh` | Empleados, contratos, nómina, rol de pagos |
| `contabilidad` | Plan de cuentas, diarios, asientos, períodos |
| `tesoreria` | Cuentas bancarias, extractos, conciliaciones, SPI |
| `presupuesto` | Partidas presupuestarias, certificaciones, compromisos |
| `compras` | Carpetas anuales, procesos de contratación pública |
| `comercial` | Gestión comercial |
| `contratacion` | Contratos institucionales |

---

## 6. Autenticación y Autorización

### Autenticación
- **JWT Bearer Token**: Se obtiene en `/api/auth/login` con usuario y contraseña
- El token debe incluirse en el header `Authorization: Bearer <token>` en todas las peticiones

### Roles del Sistema

| Rol | Descripción |
|-----|-------------|
| `SuperAdmin` | Acceso total a todos los módulos |
| `RRHH` | Gestión de talento humano y nómina |
| `Contabilidad` | Módulos contables y financieros |
| `Tesorería` | Cuentas bancarias, pagos y SPI |
| `Presupuesto` | Gestión presupuestaria |
| `Compras` | Procesos de compras públicas |

---

## 7. Integración entre Módulos

Los módulos financieros están integrados con generación automática de asientos:

```
Nómina (cerrar rol)
    └──→ genera asiento en Contabilidad

Tesorería (SPI)
    └──→ puede generar salida en Contabilidad

Presupuesto (compromiso/devengado)
    └──→ vinculado a partidas presupuestarias
```

---

## 8. Configuración e Instalación

### Variables de entorno (`.env`)

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/sge
SECRET_KEY=<clave-secreta-jwt>
SGE_CORS_ORIGIN=http://192.168.1.15:3000
```

### Levantar con Docker

```bash
docker-compose up -d
```

### Migraciones de base de datos

```bash
cd backend
alembic upgrade head
```

---

## 9. Health Check

```
GET /health
```

Responde `{"status": "ok", "message": "Servidor SGE activo y funcionando."}` cuando el backend está operativo.

---

## 10. Documentación Interactiva de la API

FastAPI genera automáticamente documentación interactiva disponible en:

- **Swagger UI:** `http://<host>:8000/docs`
- **ReDoc:** `http://<host>:8000/redoc`
