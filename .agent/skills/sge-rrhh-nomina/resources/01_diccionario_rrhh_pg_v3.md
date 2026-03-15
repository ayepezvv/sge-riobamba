# Diccionario de Datos: Esquema `rrhh` (SGE Riobamba EP)

## Tablas Maestras
* **`rrhh.empleado`**: Datos personales. Clave primaria `id_empleado`. Incluye `identificacion` (única), `fecha_nacimiento`, `porcentaje_discapacidad`, `aplica_iess`, `estado_empleado` ('ACTIVO', 'DESVINCULADO'). Usa borrado lógico (`eliminado_en`).
* **`rrhh.empleado_carga_familiar`**: Hijos y cónyuges. Fundamental para cálculo de utilidades e Impuesto a la Renta. Relacionado con `id_empleado`.
* **`rrhh.area_organizacional`**: Estructura tipo árbol. Clave `id_area`, recursividad con `id_area_padre`.
* **`rrhh.escala_salarial`**: Catálogo legal de salarios (Ej. SP1, CT1).
* **`rrhh.cargo`**: Catálogo de puestos, atado a `id_escala_salarial`.

## Tablas Transaccionales
* **`rrhh.historial_laboral`**: Une al empleado, área y cargo. Usa `fecha_inicio` y `fecha_fin` para control temporal.
* **`rrhh.parametro_calculo`**: Valores anuales variables (SBU, % IESS). Claves: `anio_vigencia`, `codigo_parametro`.
* **`rrhh.impuesto_renta_escala`**: Tabla progresiva del SRI por año.
* **`rrhh.rubro_nomina`**: Catálogo de ingresos/descuentos. Clave `codigo_rubro`. Tiene `formula_calculo` y `orden_ejecucion`.
* **`rrhh.rol_pago_cabecera`**: Contenedor mensual. Estados: BORRADOR, APROBADO_RRHH, CONTABILIZADO.
* **`rrhh.rol_pago_empleado`**: Detalle neto a pagar por trabajador.