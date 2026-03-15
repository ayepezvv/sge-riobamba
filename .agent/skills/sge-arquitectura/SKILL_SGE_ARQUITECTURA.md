# 🧠 SKILL BASE: ARQUITECTURA DEL SISTEMA DE GESTIÓN EMPRESARIAL (SGE)
**Empresa Pública Riobamba EP**

## 🎯 1. CONTEXTO Y MISIÓN
Eres un Arquitecto de Software Senior. Estás desarrollando un ERP a medida (SGE) para una empresa pública en Ecuador. El sistema es robusto, transaccional, altamente relacional y cuenta con una interfaz de usuario premium. 

## 🛠️ 2. STACK TECNOLÓGICO OFICIAL
* **Backend:** Python 3.12+, FastAPI, Uvicorn (Puerto 8000).
* **ORM y Base de Datos:** SQLAlchemy 2.0+, Alembic (Migraciones), PostgreSQL (Navicat como cliente GUI).
* **Frontend:** React, Next.js (App Router / Turbopack), TypeScript.
* **Plantilla UI:** Berry Material-UI (Premium).
* **Gestor de Paquetes:** `npm` (Frontend), `pip` / `venv` (Backend).

---

## 🗄️ 3. ARQUITECTURA DE BASE DE DATOS (POSTGRESQL + SQLALCHEMY)

### 3.1. Separación Física por Esquemas (Multi-Schema)
Prohibido usar el esquema `public` para lógica de negocio. El sistema se divide estrictamente en esquemas físicos:
* `configuracion`: Core del sistema (usuarios, roles, permisos en español).
* `administracion`: Módulo de RRHH (personal, puestos, direcciones, unidades).
* `contratacion`: Módulo de Compras (pac_anual, item_pac, procesos, link M:M).
* `informatica`: Módulo de IT (segmentos_red, ips_asignadas).
* **Regla de Modelado:** Toda clase SQLAlchemy debe incluir `__table_args__ = {'schema': 'nombre_esquema'}`.
* **Regla de Foreign Keys:** Usar rutas absolutas cruzadas: `ForeignKey('configuracion.usuarios.id')`.

### 3.2. Alembic (Migraciones)
* Configurado en `env.py` con `include_schemas=True`.
* El `include_object` está configurado para permitir todas las tablas, ignorando únicamente extensiones de PostGIS (`topology`, `tiger`).

### 3.3. Relaciones Cruzadas (Cross-Schema Constraints)
* El sistema es altamente interconectado. Existen dependencias duras entre esquemas.
* **Regla de Refactorización:** NUNCA elimines una tabla con `DROP TABLE ... CASCADE` si rompe la integridad de otro módulo.
* **Integración RRHH - Informática:** El módulo de Informática (`informatica.direccion_ip_asignada`) depende OBLIGATORIAMENTE del catálogo de empleados. Si se refactoriza RRHH (hacia el esquema `rrhh`), el modelo de IPs debe actualizar su Foreign Key para apuntar estrictamente a `rrhh.empleado.id_empleado`.

### 3.4. Migración de Esquemas (Refactorización)
* **Contexto:** El módulo de RRHH está migrando del esquema `administracion` al nuevo esquema `rrhh`.
* **Impacto:** Las tablas `empleado`, `historial_laboral`, `cargo`, `escala_salarial`, `area_organizacional`, `empleado_carga_familiar`, `parametro_calculo`, `impuesto_renta_escala`, `rubro_nomina`, `rol_pago_cabecera`, `rol_pago_empleado` y `novedad_nomina` se moverán.
* **Acción Requerida:** Al actualizar los modelos en SQLAlchemy, DEBES actualizar todas las `ForeignKey` y `relationship` que apunten a estas tablas para que reflejen el nuevo esquema `rrhh`.

---

## ⚙️ 4. ARQUITECTURA BACKEND (FASTAPI)

### 4.1. Estructura de Directorios
* `app/api/routes/`: Controladores agrupados por módulo (`auth.py`, `contratacion.py`, `informatica.py`). Registrados en `app/main.py`.
* `app/models/`: Clases de SQLAlchemy.
* `app/schemas/`: Modelos Pydantic para validación de entrada/salida.

### 4.2. Reglas de Pydantic y Python
* **Prevención de NameError:** Los esquemas base y de tablas intermedias (ej. `ProcesoItemPacLinkCreate`) DEBEN definirse estrictamente ARRIBA de las clases padre que los consumen (ej. `ProcesoContratacionCreate`).
* **Procesamiento Masivo:** Para carga de Excels/CSVs, se usa `pandas`. Obligatorio sanitizar datos nulos antes de insertar a BD (`df.replace({np.nan: None})`) y traducir nombres de columnas del CSV al modelo DB usando diccionarios de mapeo.

---

## 🖥️ 5. ARQUITECTURA FRONTEND (NEXT.JS + BERRY MUI)

### 5.1. Construcción del Menú Lateral (`src/menu-items/`)
* Jerarquía estricta de 3 niveles: `type: 'group'` -> `type: 'collapse'` -> `type: 'item'`.
* **Prohibición de i18n (`<FormattedMessage>`):** El sistema es 100% en español nativo. Se eliminó la dependencia de `<FormattedMessage>` en el motor de renderizado del menú (`NavGroup`, `NavItem`). Usar strings directos: `title: 'Administración'`.
* **Íconos:** Importación directa de componentes puros desde `@tabler/icons-react` (ej. `icon: IconUsers`). NUNCA pasar objetos literales, usar la referencia al componente.
* **Consolidación:** En `index.tsx`, todos los módulos deben ser importados explícitamente en la cabecera antes de ensamblar el array `menuItems`.

### 5.2. Componentes UI y Experiencia de Usuario (UX)
* **Tablas (DataGrid):** Se usa `@mui/x-data-grid`. 
    * **Regla de Oro:** Todo array mapeado al estado de un DataGrid DEBE contener una propiedad `id`.
    * Para vistas maestras y exploradores, inyectar OBLIGATORIAMENTE `slots={{ toolbar: GridToolbar }}` para activar filtros avanzados y exportación.
* **Formularios Complejos:** Usar Steppers (`MUI Stepper`) para flujos por pasos (ej. Asistente de Contratación).
* **Relaciones M:M:** Usar `Autocomplete` con `multiple={true}`.
* **Estética Berry:** Envolver vistas en `MainCard`. Usar `Chip` de MUI para estados (Activo=Verde, Eliminado=Rojo). Renderizar Modales (`Dialog`) con `maxWidth="xl"` para tablas de detalle.

### 5.3. Fetching de Datos
* Llamadas a API manejadas en `useEffect` o mediante eventos asíncronos (`onClick`).
* **Manejo de Errores Frontend:** Prohibido mostrar errores genéricos. Extraer el detalle del backend: `const msg = err.response?.data?.detail || "Error"`.

---

## 🚫 6. ANTIPATRONES (LO QUE NO DEBES HACER)
1.  **No crear modelos sin esquema:** Toda tabla nueva necesita pertenecer a una jurisdicción (esquema).
2.  **No dejes relaciones huérfanas:** Si creas una relación `Many-to-Many` o `One-to-Many`, asegúrate de que el `back_populates` esté definido simétricamente en **ambas** clases SQLAlchemy.
3.  **No usar inglés en la UI:** Etiquetas, alertas y menús van estrictamente en español.
4.  **No matar puertos en silencio:** Si tu código backend lanza excepciones no controladas y deja el puerto 8000 tomado (`[Errno 98]`), debes alertar al usuario para que ejecute `pkill -f uvicorn`.