# Glosario Técnico — Sistema de Gestión Empresarial (SGE)

**Unidad de Tecnologías de Riobamba EP**
Versión: 1.0 | Fecha: 2026-04-04

---

## A

**Alembic**
Herramienta de migración de base de datos para SQLAlchemy. El SGE utiliza Alembic para gestionar los cambios de esquema de PostgreSQL de forma controlada y versionada.

**API REST**
Interfaz de Programación de Aplicaciones basada en el estilo arquitectónico REST (Representational State Transfer). El backend del SGE expone endpoints REST para la comunicación con el frontend.

**Asiento Contable**
Registro formal en el libro diario que refleja una transacción financiera. En el SGE, un asiento contable se registra en el módulo de Contabilidad y afecta al menos dos cuentas del Plan de Cuentas.

**Autenticación JWT**
JSON Web Token. Mecanismo de autenticación sin estado utilizado por el SGE. El token se genera al iniciar sesión y debe incluirse en el encabezado `Authorization: Bearer <token>` de cada solicitud a la API.

---

## B

**Backend**
Componente servidor del SGE. Desarrollado con FastAPI (Python). Gestiona la lógica de negocio, acceso a base de datos y exposición de la API REST.

**Berry UI**
Plantilla de interfaz de usuario basada en React + Material-UI utilizada como base para el frontend del SGE.

---

## C

**Catastro**
Módulo del SGE que gestiona el inventario de bienes inmuebles y predios del municipio. Incluye registro de propietarios, avalúos y características de predios.

**CRM (Customer Relationship Management)**
Módulo del SGE orientado a la gestión de ciudadanos/clientes. Registra datos de contacto, historial de interacciones y categorización de usuarios del servicio.

**Contratación Pública**
Módulo del SGE que gestiona los procesos de contratación conforme a la Ley Orgánica del Sistema Nacional de Contratación Pública (LOSNCP) del Ecuador. Incluye tipos de proceso (subasta inversa, cotización, menor cuantía, etc.).

---

## D

**Docker Compose**
Herramienta para definir y ejecutar aplicaciones multi-contenedor. El SGE utiliza `docker-compose.yml` para orquestar los servicios de backend, frontend y base de datos PostgreSQL.

**DOCX Template (docxtpl)**
Biblioteca Python utilizada para generar documentos Word a partir de plantillas. El SGE la emplea en el módulo de Contratación para generar contratos y resoluciones.

---

## E

**Endpoint**
URL específica de la API REST del SGE que acepta solicitudes HTTP (GET, POST, PUT, PATCH, DELETE). Ejemplo: `POST /api/v1/contratacion/procesos/`.

**Esquema (Schema)**
En el contexto de PostgreSQL, un esquema es un espacio de nombres que contiene objetos de base de datos (tablas, vistas, funciones). El SGE utiliza múltiples esquemas para separar módulos: `contratacion`, `catastro`, `crm`, etc.

**Esquema Pydantic**
Modelo de validación de datos utilizado por FastAPI para definir la estructura de las solicitudes y respuestas de la API. En el SGE se ubican en `backend/app/schemas/`.

---

## F

**FastAPI**
Framework web moderno de Python para construir APIs. El backend del SGE está construido con FastAPI, aprovechando su soporte automático de documentación OpenAPI (Swagger).

**Frontend**
Componente cliente del SGE. Desarrollado con Next.js (React + TypeScript). Proporciona la interfaz gráfica de usuario accesible desde el navegador web.

---

## G

**Gestión de Predios**
Funcionalidad del módulo Catastro que permite registrar, actualizar y consultar información de predios urbanos y rurales, incluyendo avalúos y propietarios.

---

## H

**HTTP Status Code**
Código numérico que indica el resultado de una solicitud HTTP. Códigos comunes en el SGE:
- `200 OK`: solicitud exitosa
- `201 Created`: recurso creado
- `400 Bad Request`: datos inválidos
- `401 Unauthorized`: no autenticado
- `403 Forbidden`: sin permisos
- `404 Not Found`: recurso no encontrado
- `422 Unprocessable Entity`: error de validación Pydantic
- `500 Internal Server Error`: error del servidor

---

## I

**Internacionalización (i18n)**
Proceso de adaptar el software para distintos idiomas. El frontend del SGE utiliza archivos de traducción para soportar el idioma español en toda la interfaz.

---

## J

**JWT (JSON Web Token)**
Ver *Autenticación JWT*.

---

## L

**LOSNCP**
Ley Orgánica del Sistema Nacional de Contratación Pública del Ecuador. Marco legal que regula los procesos de contratación pública implementados en el módulo de Contratación del SGE.

---

## M

**Migración de Base de Datos**
Cambio controlado en la estructura de la base de datos (agregar tablas, modificar columnas, etc.). El SGE gestiona migraciones mediante Alembic con archivos versionados en `backend/alembic/versions/`.

**Modelo SQLAlchemy**
Clase Python que mapea a una tabla de base de datos. Los modelos del SGE se ubican en `backend/app/models/` y definen la estructura de datos persistida en PostgreSQL.

**Módulo**
Unidad funcional del SGE que agrupa un conjunto de funcionalidades relacionadas. Ejemplos: Contratación, Catastro, CRM, Administración.

---

## N

**Next.js**
Framework React para aplicaciones web con soporte de renderizado del lado del servidor (SSR). El frontend del SGE está desarrollado con Next.js.

---

## P

**PAC (Plan Anual de Contratación)**
Instrumento de planificación que define los procesos de contratación que una entidad pública ejecutará en el año fiscal. El SGE incluye gestión de PAC en el módulo de Contratación.

**Paginación**
Técnica para dividir grandes conjuntos de resultados en páginas. Los endpoints del SGE que retornan listas utilizan parámetros `skip` y `limit` para la paginación.

**Plan de Cuentas**
Catálogo estructurado de cuentas contables utilizado en el módulo de Contabilidad del SGE. Sigue la estructura del Clasificador de Ingresos y Gastos del sector público ecuatoriano.

**PostgreSQL**
Sistema de gestión de base de datos relacional utilizado por el SGE. Versión recomendada: 14 o superior.

**Predio**
Bien inmueble (terreno, edificación) registrado en el módulo de Catastro. Identificado por un código catastral único.

**Proceso de Contratación**
Procedimiento formal para adquirir bienes, servicios u obras según la LOSNCP. En el SGE, un proceso tiene etapas: planificación, convocatoria, oferta, adjudicación, contrato.

---

## R

**Resolución**
Documento administrativo formal emitido durante un proceso de contratación (ej: resolución de adjudicación). El SGE genera resoluciones en formato DOCX mediante plantillas.

**Rol (Role)**
Perfil de permisos asignado a un usuario del SGE. Los roles controlan qué módulos y funcionalidades puede acceder cada usuario. Roles típicos: `admin`, `contador`, `tesorero`, `tecnico_catastro`.

**Router (FastAPI)**
Componente de FastAPI que agrupa endpoints relacionados. En el SGE, cada módulo tiene su propio router en `backend/app/api/`.

---

## S

**SGE (Sistema de Gestión Empresarial)**
Sistema integrado de gestión desarrollado por la Unidad de Tecnologías de Riobamba EP. Centraliza la gestión de contratación pública, catastro, CRM y otros procesos administrativos municipales.

**SQLAlchemy**
ORM (Object-Relational Mapper) de Python utilizado por el SGE para interactuar con la base de datos PostgreSQL de forma orientada a objetos.

**Subasta Inversa Electrónica**
Modalidad de contratación pública en la que los proveedores compiten ofertando precios decrecientes. Implementada en el módulo de Contratación del SGE.

**Swagger UI**
Interfaz web automáticamente generada por FastAPI para documentar y probar los endpoints de la API. Accesible en `/docs` del servidor backend.

---

## T

**Token de Acceso**
Ver *Autenticación JWT*. El token tiene una vigencia definida y debe renovarse mediante el endpoint de refresh.

**TypeScript**
Superconjunto tipado de JavaScript utilizado en el frontend del SGE (Next.js). Mejora la detección de errores en tiempo de desarrollo.

---

## U

**UUID**
Universally Unique Identifier. Identificador único de 128 bits utilizado como clave primaria en la mayoría de las tablas del SGE. Formato: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.

---

## V

**Venv (Virtual Environment)**
Entorno virtual de Python que aísla las dependencias del proyecto. El backend del SGE requiere activar el venv antes de ejecutar el servidor.

---

## W

**Workspace**
Directorio de trabajo del proyecto SGE en el servidor. Ruta estándar: `/home/ayepez/.openclaw/workspace/sge/`.

---

*Documento mantenido por DocWriter-SGE. Para sugerencias o correcciones, contactar al equipo de documentación.*
