# Guía de Despliegue - Entorno de Desarrollo SGE

Este documento contiene las instrucciones precisas para replicar el entorno de desarrollo del Sistema de Gestión Empresarial (SGE) desde cero en un nuevo servidor o máquina local.

## 1. Clonar el Repositorio
```bash
git clone https://github.com/ayepezvv/sge-riobamba.git
cd sge-riobamba
```

## 2. Variables de Entorno
Crea los archivos de configuración a partir del ejemplo:
```bash
cp .env.example .env
```
*Edita el `.env` para asignar contraseñas seguras y definir la IP de tu nuevo servidor.*

Dentro de la carpeta `frontend/`, asegúrate de crear el archivo `.env.local` apuntando al backend:
```bash
echo "NEXT_PUBLIC_API_URL=http://<IP_DEL_SERVIDOR>:8000" > frontend/.env.local
```

## 3. Base de Datos (Docker + PostGIS)
El sistema requiere **PostgreSQL 15 + PostGIS 3.4**. Levanta el contenedor usando Docker Compose:
```bash
docker compose up -d
```
*Nota: El puerto por defecto expuesto es el `5433` para evitar conflictos con otras instalaciones locales.*

### 3.1. Restauración del Snapshot (Dump)
Para no tener que correr las migraciones y los seeds manualmente, restaura la base de datos con el Snapshot oficial que incluye la estructura completa (esquemas) y el usuario semilla (`admin@riobambaep.gob.ec` / `Admin123*`):
```bash
cat db_backups/sge_replica_inicial.sql | docker exec -i sge_postgres_db psql -U sge_admin -d sge_db
```

*(Alternativa manual: Si no usas el dump, deberás crear los esquemas manualmente, correr `alembic upgrade head` y luego `python backend/seed_*.py`)*

## 4. Instalación del Backend (FastAPI)
Requiere Python 3.12+.
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Levantar el servidor Backend:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 5. Instalación del Frontend (Next.js / Berry)
Requiere Node.js 18+.
```bash
cd frontend
# Es CRÍTICO usar --legacy-peer-deps para la plantilla Berry
npm install --legacy-peer-deps
```

Levantar el servidor Frontend:
```bash
npm run dev -- -H 0.0.0.0
```

## 6. Verificación (Prueba de Humo)
1. Accede a `http://<IP_DEL_SERVIDOR>:3000` en tu navegador.
2. Inicia sesión con `admin@riobambaep.gob.ec` y tu contraseña semilla.
3. Navega al "Padrón de Ciudadanos" y "Gestión de Predios" (Mapa) para verificar la correcta comunicación con PostGIS y la API.
