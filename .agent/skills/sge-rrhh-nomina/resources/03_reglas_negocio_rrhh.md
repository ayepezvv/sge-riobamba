# Análisis y Recomendaciones: Módulo RRHH y Nómina (SGE) - Versión Postgres

El análisis de la nueva estructura del esquema `rrhh` en PostgreSQL revela una arquitectura modernizada, diseñada para la escalabilidad, la auditoría y el cumplimiento normativo para el talento humano de la empresa pública.

## 1. Estructura Orgánica Dinámica (Nuevo Enfoque)

Se ha reemplazado la rígida estructura de tres niveles (División -> Departamento -> Unidad) por un **Árbol Organizacional Recursivo**:

* **`rrhh.area_organizacional`**: A través del campo `id_area_padre`, la empresa puede dibujar un organigrama de *N* niveles de profundidad. Si mañana se crea una "Sub-gerencia" debajo de una "Gerencia" y encima de un "Departamento", el sistema lo soporta sin crear nuevas tablas.

### El Historial del Empleado (Effective Dating)
* **`rrhh.historial_laboral`**: Es el corazón del sistema. En lugar de actualizar el cargo del empleado en su tabla maestra, se inserta un nuevo registro aquí. El uso estricto de `fecha_inicio` y `fecha_fin` garantiza que RRHH pueda responder la pregunta: *"¿En qué departamento estaba Juan Pérez en mayo de 2021 y cuánto ganaba?"* de forma instantánea.

## 2. El Módulo de Nómina (Flujo Transaccional)

El motor de pago se ha simplificado y robustecido:
* **`rrhh.rubro_nomina`**: Consolida los tipos y los rubros. El campo `es_imponible` es crítico para los cálculos automáticos de retenciones legales.
* **`rrhh.rol_pago_cabecera`**: Actúa como el contenedor mensual. Su campo `estado_flujo` (Borrador -> Aprobado RRHH -> Aprobado Gerencia -> Contabilizado) reemplaza a las múltiples tablas antiguas (`TBL_AD_ROL_PROVISIONAL`, `DEFINITIVO`, etc.), utilizando una máquina de estados mucho más limpia.

## 3. Recomendaciones Tecnológicas Actualizadas

### A. Trazabilidad Estándar
Todas las tablas maestras y transaccionales ahora incluyen `creado_en` y `actualizado_en`. Se recomienda que el Backend actualice estos campos automáticamente en cada petición PUT/PATCH.

### B. Borrado Lógico (Soft Deletes)
Para empleados y configuraciones, no se debe usar la instrucción `DELETE` de SQL. Se ha implementado el campo `eliminado_en`. Si este campo es nulo, el registro está activo. Esto protege la integridad referencial de la historia de la nómina.

### C. Desacoplamiento Hacia Contabilidad
El estado `CONTABILIZADO` en la tabla `rrhh.rol_pago_cabecera` es el disparador. Cuando RRHH aprueba el rol, el Backend debe agrupar todos los registros de `rol_pago_empleado` y enviar un único asiento contable al esquema financiero, afectando el Gasto de Nómina y el Pasivo (Nómina por Pagar).