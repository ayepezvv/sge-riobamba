# Preguntas Frecuentes (FAQ) — Sistema de Gestión Empresarial (SGE)

**Unidad de Tecnologías de Riobamba EP**
Versión: 1.0 | Fecha: 2026-04-04

---

## Instalación y Configuración

### ¿Cómo instalo el SGE en un nuevo servidor?

1. Clonar el repositorio en `/home/ayepez/.openclaw/workspace/sge/`
2. Configurar las variables de entorno copiando `.env.example` a `.env` y completando los valores
3. Ejecutar `docker-compose up -d` para levantar PostgreSQL
4. En el directorio `backend/`, activar el entorno virtual: `source venv/bin/activate`
5. Instalar dependencias: `pip install -r requirements.txt`
6. Ejecutar migraciones: `alembic upgrade head`
7. Sembrar datos iniciales: `python seed_admin.py`
8. Iniciar el backend: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
9. En el directorio `frontend/`, instalar dependencias: `yarn install`
10. Iniciar el frontend: `yarn dev` (desarrollo) o `yarn build && yarn start` (producción)

---

### ¿Cuáles son los requisitos mínimos del sistema?

| Componente | Requisito mínimo |
|------------|------------------|
| Sistema Operativo | Ubuntu 20.04 LTS o superior |
| Python | 3.10 o superior |
| Node.js | 18 LTS o superior |
| PostgreSQL | 14 o superior |
| RAM | 4 GB mínimo (8 GB recomendado) |
| Almacenamiento | 20 GB mínimo |

---

### ¿Cómo configuro las variables de entorno del backend?

El archivo `.env` en el directorio `backend/` debe contener:

```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/sge_db
SECRET_KEY=clave-secreta-larga-y-aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Consulte `.env.example` para ver todas las variables disponibles.

---

## Autenticación y Usuarios

### ¿Cómo inicio sesión en el SGE?

1. Acceder a la URL del frontend (ej: `http://localhost:3000`)
2. Ingresar el correo electrónico y contraseña
3. Hacer clic en "Iniciar Sesión"

El sistema genera un token JWT válido por 30 minutos (configurable).

---

### ¿Qué hago si olvidé mi contraseña?

Contactar al administrador del sistema para que restablezca la contraseña mediante el panel de administración (`/admin/usuarios`). Los administradores pueden cambiar contraseñas directamente desde la interfaz.

---

### ¿Cómo creo un nuevo usuario?

Solo los usuarios con rol `admin` pueden crear nuevos usuarios:

1. Ir al menú **Administración > Usuarios**
2. Hacer clic en **Nuevo Usuario**
3. Completar: nombre, apellido, correo, contraseña temporal y rol
4. Hacer clic en **Guardar**

El usuario debe cambiar su contraseña en el primer inicio de sesión.

---

### ¿Qué roles existen en el SGE?

| Rol | Descripción |
|-----|-------------|
| `admin` | Acceso completo a todos los módulos y configuración del sistema |
| `contador` | Acceso al módulo de Contabilidad y reportes financieros |
| `tesorero` | Acceso al módulo de Tesorería y gestión de pagos |
| `tecnico_catastro` | Acceso al módulo de Catastro y gestión de predios |
| `tecnico_contratacion` | Acceso al módulo de Contratación Pública |
| `viewer` | Acceso de solo lectura a módulos autorizados |

---

## Módulo de Contratación Pública

### ¿Cómo registro un nuevo proceso de contratación?

1. Ir al menú **Contratación > Procesos**
2. Hacer clic en **Nuevo Proceso**
3. Seleccionar el tipo de proceso (subasta inversa, cotización, menor cuantía, etc.)
4. Completar los datos requeridos: descripción del objeto, presupuesto referencial, cronograma
5. Adjuntar los documentos precontractuales
6. Hacer clic en **Guardar y Publicar**

---

### ¿Cómo genero una resolución de adjudicación?

1. Abrir el proceso de contratación correspondiente
2. Verificar que el proceso está en estado **Adjudicado**
3. Ir a la pestaña **Documentos**
4. Hacer clic en **Generar Resolución**
5. El sistema descargará el documento en formato DOCX con los datos del proceso y el proveedor adjudicado

---

### ¿Cómo registro el PAC (Plan Anual de Contratación)?

1. Ir al menú **Contratación > PAC**
2. Seleccionar el año fiscal
3. Hacer clic en **Nuevo Ítem PAC**
4. Completar: descripción, código CPC, presupuesto, tipo de proceso
5. Guardar. El ítem quedará en estado **Planificado** hasta que se inicie el proceso

---

### ¿Qué tipos de proceso de contratación están disponibles?

El SGE implementa los tipos definidos en la LOSNCP:

- **Subasta Inversa Electrónica (SIE)**
- **Cotización**
- **Menor Cuantía (Bienes/Servicios)**
- **Menor Cuantía (Consultoría)**
- **Lista Corta**
- **Concurso Público**
- **Licitación**
- **Contratación Directa**
- **Régimen Especial**

---

## Módulo de Catastro

### ¿Cómo busco un predio por código catastral?

1. Ir al menú **Catastro > Predios**
2. En el campo de búsqueda, ingresar el código catastral (formato: `XX-XXX-XXXXXX`)
3. Presionar Enter o hacer clic en el ícono de búsqueda
4. El sistema mostrará el predio con todos sus atributos

---

### ¿Cómo actualizo el avalúo de un predio?

1. Buscar el predio por código catastral
2. Hacer clic en **Editar**
3. Ir a la pestaña **Avalúo**
4. Actualizar el valor del terreno y/o construcción
5. Ingresar la fecha de vigencia del nuevo avalúo
6. Hacer clic en **Guardar**

> **Nota:** Solo usuarios con rol `admin` o `tecnico_catastro` pueden modificar avalúos.

---

### ¿Cómo registro un nuevo propietario para un predio?

1. Abrir el predio en el módulo de Catastro
2. Ir a la pestaña **Propietarios**
3. Hacer clic en **Agregar Propietario**
4. Buscar al ciudadano por número de cédula o nombre
5. Especificar el porcentaje de participación
6. Guardar el registro

---

## Módulo CRM (Ciudadanos)

### ¿Cómo registro un nuevo ciudadano?

1. Ir al menú **CRM > Ciudadanos**
2. Hacer clic en **Nuevo Ciudadano**
3. Completar los datos: cédula, nombres, apellidos, dirección, teléfono, correo
4. Hacer clic en **Guardar**

---

### ¿Cómo consulto el historial de un ciudadano?

1. Buscar al ciudadano por cédula o nombre
2. Hacer clic en el nombre para abrir su ficha
3. Ir a la pestaña **Historial**
4. Se mostrarán todos los trámites y procesos vinculados al ciudadano

---

## API y Desarrollo

### ¿Dónde puedo ver la documentación de la API?

La documentación interactiva de la API (Swagger UI) está disponible en:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

Requiere que el servidor backend esté corriendo.

---

### ¿Cómo ejecuto las migraciones de base de datos?

```bash
# Activar entorno virtual
cd /home/ayepez/.openclaw/workspace/sge/backend
source venv/bin/activate

# Aplicar todas las migraciones pendientes
alembic upgrade head

# Verificar el estado actual
alembic current

# Ver historial de migraciones
alembic history
```

---

### ¿Cómo ejecuto las pruebas del backend?

```bash
cd /home/ayepez/.openclaw/workspace/sge/backend
source venv/bin/activate
pytest tests/ -v
```

---

### ¿Cómo genero una nueva migración de Alembic?

```bash
cd /home/ayepez/.openclaw/workspace/sge/backend
source venv/bin/activate
alembic revision --autogenerate -m "descripcion_del_cambio"
```

Revisar siempre el archivo generado antes de aplicarlo con `alembic upgrade head`.

---

## Problemas Comunes

### El backend no inicia y muestra "Connection refused" a la base de datos

**Causa:** PostgreSQL no está corriendo o las credenciales son incorrectas.

**Solución:**
1. Verificar que Docker está activo: `docker ps`
2. Si el contenedor no está corriendo: `docker-compose up -d postgres`
3. Verificar las credenciales en el archivo `.env`
4. Probar la conexión: `psql -h localhost -U usuario -d sge_db`

---

### El frontend muestra "Network Error" al intentar conectarse

**Causa:** El backend no está disponible en la URL configurada.

**Solución:**
1. Verificar que el backend está corriendo en el puerto correcto (por defecto 8000)
2. Revisar la variable `NEXT_PUBLIC_API_URL` en el archivo `.env.local` del frontend
3. Verificar que no hay problemas de CORS en la configuración del backend

---

### Al iniciar sesión recibo "401 Unauthorized"

**Causa:** Credenciales incorrectas o token expirado.

**Solución:**
1. Verificar el correo y contraseña ingresados
2. Si el token expiró, cerrar sesión y volver a iniciar
3. Si el problema persiste, contactar al administrador para verificar que la cuenta está activa

---

### Las migraciones de Alembic fallan con "Table already exists"

**Causa:** El estado de Alembic no coincide con el estado real de la base de datos.

**Solución:**
```bash
# Verificar el estado actual
alembic current

# Si es necesario, establecer la revisión manualmente
alembic stamp head
```

---

### No puedo generar documentos DOCX

**Causa:** La biblioteca `docxtpl` no está instalada o las plantillas no están en la ruta correcta.

**Solución:**
1. Verificar que `docxtpl` está en `requirements.txt` e instalado: `pip show docxtpl`
2. Verificar que las plantillas están en `backend/templates/`
3. Revisar los logs del backend para el mensaje de error específico

---

## Soporte

### ¿Con quién me comunico si tengo un problema técnico?

Contactar al equipo de la **Unidad de Tecnologías de Riobamba EP**:

- **Administrador del sistema:** ayepez
- **Canal de soporte:** sistema de tickets interno

Para reportar bugs o solicitar nuevas funcionalidades, crear una tarea en el sistema de gestión de proyectos del equipo.

---

*Documento mantenido por DocWriter-SGE. Para sugerencias o correcciones, contactar al equipo de documentación.*
