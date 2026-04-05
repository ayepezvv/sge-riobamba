# Manual de Usuario — Módulo Presupuesto

**Sistema de Gestión Empresarial (SGE) — Unidad de Tecnologías de Riobamba EP**
**Versión:** 1.0 | **Fecha:** Abril 2026 | **Prefijo API:** `/api/presupuesto`
**Roles habilitados:** `SuperAdmin`, `Presupuesto`

---

## 1. Descripción General

El módulo de **Presupuesto** implementa el ciclo presupuestario del sector público ecuatoriano: partidas presupuestarias, presupuesto anual, certificaciones, reformas, compromisos y devengados.

### Ciclo presupuestario

```
Partidas → Presupuesto Anual → Certificación → Compromiso → Devengado
```

---

## 2. Partidas Presupuestarias

Las partidas son los ítems del clasificador presupuestario del sector público.

| Campo | Descripción |
|-------|-------------|
| `codigo_partida` | Código del clasificador (ej. `5.1.01.05`) |
| `nombre` | Nombre de la partida |
| `tipo` | `INGRESO` o `GASTO` |
| `grupo` | Grupo presupuestario |

> El código de partida sigue el **Clasificador Presupuestario de Ingresos y Gastos** del Ministerio de Finanzas del Ecuador.

---

## 3. Presupuesto Anual

El presupuesto anual asigna montos a las partidas presupuestarias para cada año fiscal.

### 3.1 Crear el presupuesto anual

| Campo | Descripción |
|-------|-------------|
| `anio` | Año fiscal |
| `estado` | Estado del presupuesto |

### 3.2 Ítems del presupuesto

Cada ítem vincula una partida con su monto asignado:

| Campo | Descripción |
|-------|-------------|
| `id_partida` | Partida presupuestaria |
| `monto_aprobado` | Monto inicial aprobado |
| `monto_codificado` | Monto actual (incluye reformas) |

### 3.3 Estados del presupuesto

| Estado | Descripción |
|--------|-------------|
| `ELABORACION` | En preparación |
| `APROBADO` | Aprobado por autoridad competente |
| `EN_EJECUCION` | Período fiscal activo |
| `CERRADO` | Año fiscal concluido |

---

## 4. Reformas Presupuestarias

Las reformas modifican el monto codificado de las partidas durante el período de ejecución.

| Campo | Descripción |
|-------|-------------|
| `id_item_origen` | Partida que libera recursos |
| `id_item_destino` | Partida que recibe recursos |
| `monto` | Monto de la reforma |
| `justificacion` | Razón de la reforma |
| `numero_resolucion` | Número del acto administrativo que autoriza |

> Las reformas deben estar autorizadas por el funcionario competente. El monto codificado se actualiza automáticamente.

---

## 5. Certificaciones Presupuestarias

La certificación presupuestaria reserva fondos para un proceso de contratación o gasto antes de comprometerse.

### 5.1 Proceso

| Paso | Descripción |
|------|-------------|
| Solicitar certificación | Se indica la partida y el monto a certificar |
| Aprobar | La autoridad presupuestaria aprueba la reserva |
| Usar en compromiso | La certificación aprobada habilita la creación del compromiso |

### 5.2 Estados de la certificación

| Estado | Descripción |
|--------|-------------|
| `SOLICITADA` | Pendiente de aprobación |
| `APROBADA` | Fondos reservados |
| `UTILIZADA` | Ya fue aplicada a un compromiso |
| `ANULADA` | Cancelada sin uso |

---

## 6. Compromisos

El compromiso es el acto por el cual se afecta preventivamente el presupuesto al suscribir un contrato u obligación.

| Campo | Descripción |
|-------|-------------|
| `id_certificacion` | Certificación que respalda el compromiso |
| `descripcion` | Descripción del compromiso |
| `numero_contrato` | Número de contrato o documento |
| `valor` | Monto comprometido |
| `fecha_compromiso` | Fecha del compromiso |
| `proveedor` | Nombre del proveedor o beneficiario |

### Estados del compromiso

| Estado | Descripción |
|--------|-------------|
| `ACTIVO` | Compromiso vigente |
| `ANULADO` | Compromiso cancelado (libera el saldo) |

---

## 7. Devengados

El devengado registra la obligación de pago cuando se recibe el bien o servicio.

| Campo | Descripción |
|-------|-------------|
| `id_compromiso` | Compromiso al que pertenece |
| `valor_devengado` | Monto efectivamente devengado |
| `fecha_devengado` | Fecha de recepción del bien/servicio |
| `numero_factura` | Número de factura o comprobante |

> El devengado no puede superar el monto comprometido. Se pueden crear múltiples devengados contra un mismo compromiso (entregas parciales).

---

## 8. Saldos Disponibles

El sistema calcula automáticamente los saldos en cada nivel:

```
Saldo disponible = Monto codificado − Certificaciones aprobadas − Compromisos activos
```

| Concepto | Descripción |
|----------|-------------|
| `monto_codificado` | Presupuesto vigente (inicial + reformas) |
| `comprometido` | Total de compromisos activos |
| `devengado` | Total devengado |
| `pagado` | Total pagado |
| `disponible` | Saldo libre para nueva certificación |

---

## 9. Preguntas Frecuentes

**¿Puedo comprometer sin certificación?**
No. El flujo obligatorio es: certificación aprobada → compromiso. No se pueden crear compromisos sin certificación previa.

**¿Una reforma puede ser negativa?**
Sí. Una reforma puede reducir una partida para aumentar otra (traspaso de crédito). El sistema valida que el monto codificado resultante no sea negativo.

**¿Cuándo se cierra el presupuesto anual?**
Al cierre del año fiscal, el presupuesto pasa a estado `CERRADO`. Los saldos no comprometidos se liberan. Contacte al administrador del sistema para ejecutar el cierre.

**¿El devengado genera asiento contable?**
Depende de la configuración. En integraciones completas, el devengado puede generar automáticamente el asiento en Contabilidad.
