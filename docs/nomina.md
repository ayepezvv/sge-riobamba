# Manual de Usuario — Módulo Nómina / Rol de Pagos

**Sistema de Gestión Empresarial (SGE) — Unidad de Tecnologías de Riobamba EP**
**Versión:** 1.0 | **Fecha:** Abril 2026 | **Prefijo API:** `/api/rrhh/nomina`
**Roles habilitados:** `SuperAdmin`, `RRHH`

---

## 1. Descripción General

El módulo de **Nómina / Rol de Pagos** permite gestionar el proceso completo de pago de remuneraciones del personal: desde la configuración de rubros hasta la generación del archivo SPI para pagos masivos al Banco Central del Ecuador (BCE).

### Flujo principal del Rol de Pagos

```
BORRADOR → CALCULADO → APROBADO → CERRADO
              ↑
         (recalcular)
              
Desde cualquier estado (excepto CERRADO) → ANULADO (solo SuperAdmin)
```

---

## 2. Rubros de Nómina

Los **rubros de nómina** son el catálogo de conceptos de ingreso y descuento que se aplican al calcular el rol de pagos (ej. sueldo básico, décimo tercero, IESS personal, impuesto a la renta, etc.).

### 2.1 Listar rubros

| Campo | Descripción |
|-------|-------------|
| `codigo_rubro` | Código único del rubro |
| `nombre` | Nombre descriptivo |
| `tipo` | `INGRESO` o `DESCUENTO` |
| `orden_ejecucion` | Orden de cálculo (menor = primero) |

**Acceso:** Todos los usuarios autenticados pueden consultar el catálogo.

### 2.2 Crear o modificar un rubro

Solo usuarios con rol **RRHH** o **SuperAdmin** pueden crear o modificar rubros.

> **Importante:** El código de rubro debe ser único en el sistema. Si intenta crear un rubro con un código ya existente, el sistema rechazará la operación con un error.

---

## 3. Proceso de Generación del Rol de Pagos

### Paso 1 — Crear el Rol (estado: BORRADOR)

Se crea la cabecera del rol indicando:

| Campo | Descripción |
|-------|-------------|
| `periodo_anio` | Año del período (ej. 2026) |
| `periodo_mes` | Mes del período (1–12) |
| `tipo_rol` | Tipo de rol (ej. `MENSUAL`, `DECIMO_TERCERO`, `DECIMO_CUARTO`) |

> El sistema valida que no exista ya un rol del mismo tipo y período. Si ya existe, rechaza la creación.

### Paso 2 — Calcular el Rol (estado: CALCULADO)

Al ejecutar el cálculo, el motor de nómina:
- Procesa todos los empleados activos con contratos vigentes para el período
- Aplica los rubros en orden de ejecución (ingresos primero, descuentos después)
- Genera una **línea** por empleado con el desglose de su remuneración
- Calcula totales consolidados del rol

> Se puede recalcular un rol ya en estado `CALCULADO` (vuelve a `CALCULADO` con nuevos valores).

### Paso 3 — Aprobar el Rol (estado: APROBADO)

La aprobación confirma los valores calculados. Solo se puede aprobar un rol en estado `CALCULADO`.

> Registra la fecha de aprobación y el usuario que aprobó.

### Paso 4 — Cerrar el Rol (estado: CERRADO)

El cierre realiza dos acciones:
1. Marca el rol como `CERRADO` (no se puede modificar)
2. **Genera automáticamente el asiento contable** de nómina en el módulo de Contabilidad

> Solo se pueden cerrar roles en estado `APROBADO`.

### Anulación

Un **SuperAdmin** puede anular un rol en cualquier estado **excepto** `CERRADO`. Un rol cerrado no puede anularse.

---

## 4. Consulta de Líneas del Rol

Cada línea del rol corresponde a un empleado e incluye:
- Datos del empleado (nombre, cédula, cargo)
- Subtotal de ingresos
- Subtotal de descuentos
- **Valor neto a pagar**
- Datos bancarios (para transferencia SPI)
- Detalle por rubro

Para actualizar los datos bancarios de un empleado en el rol (número de cuenta, banco destino), use la opción de actualización de línea antes de generar el archivo SPI.

---

## 5. Exportación SPI — Pagos Masivos BCE

El archivo **SPI** (Sistema de Pagos Interbancarios) es el formato requerido por el Banco Central del Ecuador para ejecutar pagos masivos de nómina.

### Requisitos previos
- El rol debe estar en estado `APROBADO` o `CERRADO`
- Cada línea debe tener datos bancarios completos del empleado

### Parámetros de generación

| Parámetro | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `ruc_empresa` | RUC de la entidad pagadora | `1760001340001` |
| `cuenta_empresa` | Cuenta origen de la transferencia | — |

### Resultado
Se descarga un archivo `.txt` con nombre `SPI_{tipo_rol}_{año}{mes}.txt` listo para cargar en el portal del BCE.

---

## 6. Preguntas Frecuentes

**¿Puedo recalcular un rol ya aprobado?**
No. Solo se puede recalcular un rol en estado `BORRADOR` o `CALCULADO`. Para corregir un rol aprobado, un SuperAdmin debe anularlo y crear uno nuevo.

**¿El cierre del rol afecta la contabilidad?**
Sí. Al cerrar un rol se genera automáticamente el asiento contable de nómina. Verifique que los parámetros contables estén configurados antes de cerrar.

**¿Qué ocurre si un empleado no tiene datos bancarios?**
El archivo SPI no se generará correctamente. Actualice los datos bancarios de la línea antes de exportar.

**¿Se puede eliminar un rol?**
No se elimina. Se anula (SuperAdmin). Los roles anulados quedan en el historial.
