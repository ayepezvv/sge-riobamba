# Manual de Usuario — Módulo Contabilidad

**Sistema de Gestión Empresarial (SGE) — Unidad de Tecnologías de Riobamba EP**
**Versión:** 1.0 | **Fecha:** Abril 2026 | **Prefijo API:** `/api/contabilidad`
**Roles habilitados:** `SuperAdmin`, `Contabilidad`

---

## 1. Descripción General

El módulo de **Contabilidad** implementa la contabilidad por partida doble del sector público ecuatoriano. Gestiona el plan de cuentas, los diarios contables, los períodos y los asientos contables.

---

## 2. Tipos de Cuenta

Los tipos de cuenta clasifican las cuentas del plan contable (Activo, Pasivo, Patrimonio, Ingresos, Gastos).

| Campo | Descripción |
|-------|-------------|
| `codigo` | Código numérico del tipo |
| `nombre` | Nombre del tipo de cuenta |
| `naturaleza` | `DEUDORA` o `ACREEDORA` |

---

## 3. Plan de Cuentas

### 3.1 Estructura

El plan de cuentas es **jerárquico**. Cada cuenta puede tener una cuenta padre, formando un árbol contable.

| Campo | Descripción |
|-------|-------------|
| `codigo_cuenta` | Código contable (ej. `1.1.1.01`) |
| `nombre` | Nombre de la cuenta |
| `id_tipo_cuenta` | Tipo de cuenta asociado |
| `id_cuenta_padre` | Cuenta padre (vacío = cuenta raíz) |
| `acepta_movimientos` | `true` = cuenta de detalle / `false` = cuenta de grupo |
| `estado` | `ACTIVO` / `INACTIVO` |

### 3.2 Árbol de Cuentas

Use el endpoint `/api/contabilidad/cuentas/arbol` para obtener el plan de cuentas en estructura jerárquica completa.

### 3.3 Saldo de una Cuenta

El endpoint `/api/contabilidad/cuentas/{id}/saldo` devuelve:
- Total débitos
- Total créditos
- Saldo actual (según naturaleza de la cuenta)

> Solo las cuentas con `acepta_movimientos = true` pueden recibir líneas de asiento.

---

## 4. Diarios Contables

Los diarios agrupan asientos por tipo de operación.

| Campo | Descripción |
|-------|-------------|
| `codigo` | Código único del diario |
| `nombre` | Nombre descriptivo (ej. "Diario de Nómina") |
| `tipo` | Tipo de diario |
| `secuencia_prefijo` | Prefijo para la numeración automática |

**Ejemplos de diarios comunes:**
- `NOMINA` — Asientos de rol de pagos
- `BANCO` — Movimientos bancarios
- `VARIOS` — Asientos generales

---

## 5. Períodos Contables

Los períodos controlan qué fechas están abiertas para registro contable.

| Estado | Descripción |
|--------|-------------|
| `ABIERTO` | Permite registrar y modificar asientos |
| `CERRADO` | No se pueden registrar nuevos asientos |
| `BLOQUEADO` | Solo lectura, sin modificaciones |

> Antes de registrar asientos, verifique que el período correspondiente esté en estado `ABIERTO`.

### Cambio de estado de un período

Solo **SuperAdmin** puede cambiar el estado de un período.

---

## 6. Asientos Contables

### 6.1 Flujo de estados

```
BORRADOR → PUBLICADO → ANULADO
```

| Estado | Descripción |
|--------|-------------|
| `BORRADOR` | Asiento en elaboración, no afecta saldos |
| `PUBLICADO` | Afecta saldos contables |
| `ANULADO` | Reversado, no afecta saldos |

### 6.2 Crear un asiento

Al crear un asiento se deben incluir sus **líneas** (partidas). Cada línea requiere:

| Campo | Descripción |
|-------|-------------|
| `id_cuenta` | Cuenta contable |
| `descripcion` | Concepto de la línea |
| `debe` | Valor al debe (0 si es crédito) |
| `haber` | Valor al haber (0 si es débito) |

> **Regla de partida doble:** La suma de débitos debe ser igual a la suma de créditos. El sistema rechaza asientos desbalanceados.

### 6.3 Publicar un asiento

Al publicar, el asiento pasa de `BORRADOR` a `PUBLICADO` y sus valores afectan los saldos de las cuentas. Se requiere que:
- El asiento esté balanceado (debe = haber)
- El período contable esté `ABIERTO`

### 6.4 Anular un asiento

Se puede anular un asiento `PUBLICADO`. La anulación genera un asiento de reversión automático.

---

## 7. Parámetros Contables

Configuran cuentas y valores por defecto usados por los módulos integrados (ej. cuentas de nómina, cuentas de bancos).

| Campo | Descripción |
|-------|-------------|
| `clave` | Identificador del parámetro |
| `valor` | Valor (código de cuenta u otro) |
| `descripcion` | Descripción del parámetro |

**Parámetros importantes para la integración con Nómina:**
- `CUENTA_GASTO_NOMINA` — Cuenta de gasto de remuneraciones
- `CUENTA_IESS_PATRONAL` — Cuenta de aporte patronal IESS
- `CUENTA_IESS_PERSONAL` — Cuenta de descuento IESS personal

---

## 8. Preguntas Frecuentes

**¿Puedo editar un asiento publicado?**
No. Un asiento publicado no se puede editar. Si hay un error, debe anularlo y crear uno nuevo.

**¿Puedo registrar asientos en un período cerrado?**
No. Debe abrir el período (solo SuperAdmin) o usar el período correcto.

**¿Los asientos de nómina se crean automáticamente?**
Sí. Al cerrar un Rol de Pagos en el módulo de Nómina, el sistema genera automáticamente el asiento contable correspondiente usando los parámetros contables configurados.

**¿Cómo veo el saldo de una cuenta en un período específico?**
Use el endpoint de saldo de cuenta filtrando por período.
