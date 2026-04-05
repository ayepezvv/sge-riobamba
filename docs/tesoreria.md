# Manual de Usuario — Módulo Tesorería y Pagos

**Sistema de Gestión Empresarial (SGE) — Unidad de Tecnologías de Riobamba EP**
**Versión:** 1.0 | **Fecha:** Abril 2026 | **Prefijo API:** `/api/tesoreria`
**Roles habilitados:** `SuperAdmin`, `Tesorería`

---

## 1. Descripción General

El módulo de **Tesorería y Pagos** gestiona las cuentas bancarias institucionales, los extractos bancarios, la conciliación bancaria, la caja chica y los pagos masivos al Banco Central del Ecuador a través del sistema SPI.

---

## 2. Entidades Bancarias

Catálogo de bancos e instituciones financieras con las que opera la institución.

| Campo | Descripción |
|-------|-------------|
| `codigo` | Código del banco |
| `nombre` | Nombre de la entidad bancaria |
| `tipo` | Tipo (BCE, banco privado, cooperativa, etc.) |
| `estado` | `ACTIVO` / `INACTIVO` |

---

## 3. Cuentas Bancarias

Registro de las cuentas bancarias institucionales.

| Campo | Descripción |
|-------|-------------|
| `numero_cuenta` | Número de cuenta |
| `id_entidad_bancaria` | Banco donde está la cuenta |
| `tipo_cuenta` | `CORRIENTE`, `AHORROS`, etc. |
| `moneda` | Moneda (USD por defecto) |
| `saldo_inicial` | Saldo de apertura |
| `estado` | `ACTIVA` / `INACTIVA` |

---

## 4. Extractos Bancarios

Los extractos reflejan los movimientos bancarios recibidos del banco.

### 4.1 Flujo de estados del extracto

```
PENDIENTE → CONFIRMADO
```

### 4.2 Registrar un extracto

Al crear un extracto se deben ingresar sus líneas (movimientos):

| Campo de línea | Descripción |
|----------------|-------------|
| `fecha_movimiento` | Fecha del movimiento |
| `tipo` | `CREDITO` o `DEBITO` |
| `valor` | Monto del movimiento |
| `concepto` | Descripción del movimiento |
| `referencia` | Número de referencia bancaria |

### 4.3 Confirmar un extracto

Al confirmar, el extracto queda disponible para el proceso de conciliación bancaria.

---

## 5. Conciliación Bancaria

La conciliación cruza los movimientos del extracto bancario contra los registros contables del sistema.

### 5.1 Proceso de conciliación

**Paso 1 — Crear la conciliación**

| Campo | Descripción |
|-------|-------------|
| `id_cuenta_bancaria` | Cuenta a conciliar |
| `periodo` | Período de la conciliación |
| `saldo_banco` | Saldo según extracto bancario |
| `saldo_contable` | Saldo según libros contables |

**Paso 2 — Marcar movimientos**

Se cruzan las líneas del extracto con los asientos contables. Cada marca indica que un movimiento bancario corresponde a un registro contable.

**Paso 3 — Cerrar la conciliación**

Una vez que la diferencia entre saldo bancario y saldo contable sea cero (o dentro del margen aceptable), se cierra la conciliación.

### 5.2 Estados de la conciliación

| Estado | Descripción |
|--------|-------------|
| `ABIERTA` | En proceso |
| `CERRADA` | Conciliación completada |

---

## 6. Caja Chica

Gestión del fondo de caja chica para gastos menores.

### 6.1 Crear una caja chica

| Campo | Descripción |
|-------|-------------|
| `nombre` | Nombre de la caja (ej. "Caja Chica Administrativa") |
| `monto_fondo` | Monto del fondo asignado |
| `responsable_id` | Usuario responsable |
| `estado` | `ACTIVA` / `INACTIVA` |

### 6.2 Registrar movimientos de caja

| Campo | Descripción |
|-------|-------------|
| `tipo` | `EGRESO` (gasto) o `REPOSICION` (recarga del fondo) |
| `valor` | Monto del movimiento |
| `concepto` | Descripción del gasto |
| `fecha` | Fecha del movimiento |
| `numero_documento` | Factura o comprobante |

> Los egresos reducen el saldo disponible. Las reposiciones reponen el fondo hasta su monto máximo.

---

## 7. SPI — Sistema de Pagos Interbancarios (BCE)

El SPI permite realizar pagos masivos a través del Banco Central del Ecuador.

### 7.1 Lotes SPI

Un **lote SPI** agrupa múltiples órdenes de pago en un solo archivo para procesar en el BCE.

**Crear un lote:**

| Campo | Descripción |
|-------|-------------|
| `descripcion` | Descripción del lote |
| `id_cuenta_origen` | Cuenta bancaria institucional origen |
| `fecha_proceso` | Fecha programada para el débito |

**Agregar órdenes de pago al lote:**

| Campo | Descripción |
|-------|-------------|
| `beneficiario_nombre` | Nombre del beneficiario |
| `beneficiario_ruc_cedula` | RUC o cédula del beneficiario |
| `banco_destino` | Código del banco destino |
| `cuenta_destino` | Número de cuenta destino |
| `tipo_cuenta_destino` | `AHO` (ahorros) o `CTE` (corriente) |
| `valor` | Monto a transferir |
| `concepto` | Descripción del pago |

### 7.2 Flujo del lote SPI

```
BORRADOR → [generar-archivo] → GENERADO → [marcar-enviado] → ENVIADO
```

| Paso | Acción | Descripción |
|------|--------|-------------|
| 1 | Crear lote | Se agregan las órdenes de pago |
| 2 | Generar archivo | Produce el archivo `.txt` en formato BCE |
| 3 | Descargar y cargar en BCE | Manual: el usuario sube el archivo al portal del BCE |
| 4 | Marcar como enviado | Confirma en el sistema que el archivo fue transmitido |

### 7.3 Generación del archivo SPI

El archivo generado sigue el formato estándar del BCE. Se descarga desde el sistema y se carga manualmente en el portal de Pagos Masivos del BCE.

> **Nota:** El módulo de Nómina genera automáticamente el archivo SPI del rol de pagos. Para pagos de otros conceptos, use los lotes SPI manuales.

---

## 8. Preguntas Frecuentes

**¿Puedo modificar un lote SPI después de generar el archivo?**
No se recomienda. Una vez generado el archivo, el lote debe marcarse como enviado. Si hay correcciones, anule el lote y cree uno nuevo.

**¿La conciliación bancaria afecta los saldos contables?**
La conciliación es un proceso de verificación, no modifica asientos. Los asientos deben corregirse por separado en el módulo de Contabilidad si hay discrepancias.

**¿Cuántas cajas chicas puede tener la institución?**
El sistema permite múltiples cajas chicas. Cada una tiene su propio responsable, fondo y registro de movimientos.

**¿Puedo ver el historial de movimientos de una caja?**
Sí. Consulte los movimientos de la caja usando el endpoint de movimientos filtrando por caja y rango de fechas.
