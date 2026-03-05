# Sistema de Gestión Empresarial (SGE) - Riobamba EP

Arquitectura modular para la gestión comercial y catastral, construida con herramientas modernas y escalables.

## Stack Tecnológico
* **Base de Datos:** PostgreSQL 15 + PostGIS 3.4 (Contenedorizado)
* **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (ORM), Alembic, Pydantic, GeoAlchemy2.
* **Frontend:** Next.js 14, React 18, TypeScript, Material-UI (Plantilla Berry React).

---

## 🚀 Accesos de Desarrollo

Para facilitar la incorporación de nuevos desarrolladores o pruebas de TIC, aquí están los datos clave del entorno base:

### 1. Base de Datos (Navicat / DBeaver)
* **Host:** `localhost` (o la IP del servidor en la red local)
* **Puerto:** `5433` *(Configurado así para evitar colisión con el puerto 5432 estándar)*
* **Base de Datos:** `sge_db`
* **Usuario:** `sge_admin`
* **Contraseña:** *(Revisar tu archivo `.env` o preguntar al Administrador)*
* **Nota Arquitectónica:** El sistema utiliza esquemas físicos para separar contextos (`administracion`, `catastro`, `comercial`, `core`). Los esquemas `tiger` y `tiger_data` son autogenerados por PostGIS y pueden ser ignorados.

### 2. Frontend y Usuario Semilla
* **Frontend Port:** `3000` (Ej. `http://192.168.1.15:3000`)
* Al levantar la base de datos y correr el script de semilla (`backend/seed_admin.py`), se inyecta un superusuario para pruebas:
  * **Usuario:** `admin@riobambaep.gob.ec`
  * **Contraseña:** *(Configurada en el script semilla o `.env`)*

---

## Levantamiento del Entorno

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm run dev -- -H 0.0.0.0
```
