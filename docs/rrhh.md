# Manual de Usuario — Módulo Talento Humano (RRHH)

**Sistema de Gestión Empresarial (SGE) — Unidad de Tecnologías de Riobamba EP**
**Versión:** 1.0 | **Fecha:** Abril 2026 | **Prefijo API:** `/api/rrhh`
**Roles habilitados:** `SuperAdmin`, `RRHH`

---

## 1. Descripción General

El módulo de **Talento Humano** gestiona la información del personal de la institución: estructura organizacional, cargos, escalas salariales, empleados, cargas familiares, historial laboral, contratos y parámetros de cálculo de nómina.

---

## 2. Estructura Organizacional

### 2.1 Áreas Organizacionales

Definen la jerarquía departamental de la institución.

| Campo | Descripción |
|-------|-------------|
| `nombre` | Nombre del área (ej. "Dirección Financiera") |
| `codigo` | Código único del área |
| `area_padre_id` | ID del área superior (para estructura jerárquica) |
| `estado` | `ACTIVO` / `INACTIVO` |

Solo se listan áreas en estado `ACTIVO`. Para desactivar un área, actualice su estado a `INACTIVO`.

### 2.2 Escala Salarial

Define las bandas salariales aplicables a los cargos.

| Campo | Descripción |
|-------|-------------|
| `codigo_escala` | Código único (ej. `NJS-1`) |
| `nivel` | Nivel jerárquico |
| `remuneracion_mensual` | Sueldo base mensual |
| `descripcion` | Descripción del nivel |

### 2.3 Cargos

Los cargos vinculan un puesto de trabajo con su escala salarial y área organizacional.

| Campo | Descripción |
|-------|-------------|
| `nombre_cargo` | Denominación del cargo |
| `codigo_cargo` | Código único |
| `id_escala` | Escala salarial asignada |
| `id_area` | Área organizacional |
| `estado` | `ACTIVO` / `INACTIVO` |

> El listado de cargos incluye la información de la escala salarial vinculada.

---

## 3. Empleados

### 3.1 Registro de Empleados

| Campo | Descripción |
|-------|-------------|
| `cedula` | Cédula de identidad (único) |
| `nombres` | Nombres completos |
| `apellidos` | Apellidos completos |
| `fecha_nacimiento` | Fecha de nacimiento |
| `correo_institucional` | Correo corporativo |
| `telefono` | Teléfono de contacto |
| `estado` | `ACTIVO` / `INACTIVO` / `LICENCIA` |
| `id_cargo` | Cargo asignado |
| `cuenta_bancaria` | Número de cuenta para transferencias |
| `banco` | Banco del empleado |

> La cédula es el identificador único del empleado. No puede registrarse dos empleados con la misma cédula.

### 3.2 Cargas Familiares

Cada empleado puede tener registradas sus cargas familiares para efectos de cálculo del impuesto a la renta y beneficios.

| Campo | Descripción |
|-------|-------------|
| `nombres` | Nombres de la carga familiar |
| `parentesco` | Relación (cónyuge, hijo/a, etc.) |
| `fecha_nacimiento` | Fecha de nacimiento |
| `discapacidad` | Indica si tiene discapacidad |

### 3.3 Historial Laboral

Registra los movimientos de personal del empleado (ingresos, ascensos, traspasos, salidas).

| Campo | Descripción |
|-------|-------------|
| `tipo_movimiento` | Tipo (INGRESO, ASCENSO, TRASPASO, SALIDA, etc.) |
| `fecha_movimiento` | Fecha del evento |
| `id_cargo_anterior` | Cargo previo al movimiento |
| `id_cargo_nuevo` | Cargo posterior al movimiento |
| `observaciones` | Notas adicionales |

---

## 4. Contratos

El módulo gestiona los contratos de trabajo del personal.

| Campo | Descripción |
|-------|-------------|
| `id_empleado` | Empleado al que pertenece el contrato |
| `tipo_contrato` | Tipo (NOMBRAMIENTO, CONTRATO_PLAZO_FIJO, etc.) |
| `fecha_inicio` | Fecha de inicio del contrato |
| `fecha_fin` | Fecha de fin (vacío = indefinido) |
| `sueldo_mensual` | Remuneración pactada |
| `horas_semanales` | Horas de trabajo semanales |
| `estado` | `ACTIVO` / `TERMINADO` / `SUSPENDIDO` |

> El motor de nómina utiliza los contratos **activos** para calcular el rol de pagos. Un empleado sin contrato activo no genera línea en el rol.

---

## 5. Parámetros de Cálculo

Configuran los valores globales usados por el motor de nómina (porcentajes IESS, décimos, etc.).

| Campo | Descripción |
|-------|-------------|
| `clave` | Identificador del parámetro |
| `valor` | Valor numérico |
| `descripcion` | Descripción del parámetro |
| `anio_vigencia` | Año al que aplica |

> Ejemplos de parámetros: `IESS_PERSONAL` (9.45%), `IESS_PATRONAL` (12.15%), `SBU` (salario básico unificado vigente).

---

## 6. Relación con otros módulos

| Módulo | Relación |
|--------|----------|
| **Nómina** | Usa empleados, contratos y parámetros para calcular el rol de pagos |
| **Contabilidad** | El cierre de nómina genera asientos contables automáticos |
| **Tesorería** | El archivo SPI de nómina se gestiona desde Tesorería (lotes SPI) |

---

## 7. Preguntas Frecuentes

**¿Puedo tener un empleado con dos contratos activos simultáneos?**
El motor de nómina procesa el contrato activo vigente para el período. Si hay ambigüedad, se recomienda verificar que solo un contrato esté en estado `ACTIVO` por empleado.

**¿Qué pasa si cambio el cargo de un empleado?**
Registre un movimiento en el Historial Laboral con tipo `ASCENSO` o `TRASPASO`, actualice el contrato y el cargo del empleado.

**¿Cómo inactivo un empleado que se desvincula?**
Cambie el estado del empleado a `INACTIVO`, termine su contrato (estado `TERMINADO`) y registre un movimiento de `SALIDA` en el historial laboral.
