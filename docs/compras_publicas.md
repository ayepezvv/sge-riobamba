# Manual de Usuario — Módulo Compras Públicas

**Sistema de Gestión Empresarial (SGE) — Unidad de Tecnologías de Riobamba EP**
**Versión:** 1.0 | **Fecha:** Abril 2026 | **Prefijo API:** `/api/compras`
**Roles habilitados:** `SuperAdmin`, `Compras`

---

## 1. Descripción General

El módulo de **Compras Públicas** gestiona los procesos de contratación pública siguiendo la normativa del SERCOP (Servicio Nacional de Contratación Pública) y el PAC (Plan Anual de Contratación) del Ecuador.

---

## 2. Carpetas Anuales (PAC)

Las carpetas anuales organizan todos los procesos de contratación de un año fiscal, correspondiendo al **Plan Anual de Contratación (PAC)** institucional.

| Campo | Descripción |
|-------|-------------|
| `anio` | Año fiscal |
| `descripcion` | Descripción de la carpeta |
| `estado` | `ACTIVA` / `CERRADA` |

> Solo puede haber una carpeta activa por año. Al crear la carpeta del nuevo año, se deben planificar los procesos que se ejecutarán.

---

## 3. Procesos de Contratación

Cada proceso representa un procedimiento de contratación pública (cotización, subasta inversa, menor cuantía, etc.).

### 3.1 Crear un proceso

| Campo | Descripción |
|-------|-------------|
| `id_carpeta` | Carpeta anual (PAC) a la que pertenece |
| `codigo_proceso` | Código único del proceso |
| `tipo_proceso` | Tipo de contratación (ver tabla abajo) |
| `descripcion` | Objeto de contratación |
| `presupuesto_referencial` | Monto referencial en USD |
| `fecha_publicacion` | Fecha de publicación en SERCOP |
| `estado` | Estado actual del proceso |

### 3.2 Tipos de proceso (según SERCOP)

| Tipo | Descripción | Umbral aproximado |
|------|-------------|-------------------|
| `CATALOGO_ELECTRONICO` | Compra por catálogo del SERCOP | Sin umbral |
| `MENOR_CUANTIA_BIENES` | Menor cuantía bienes/servicios | Hasta $7.263 |
| `MENOR_CUANTIA_OBRAS` | Menor cuantía obras | Hasta $72.630 |
| `COTIZACION` | Cotización | $7.263 – $72.630 |
| `LICITACION` | Licitación | Sobre $72.630 |
| `SUBASTA_INVERSA` | Subasta inversa electrónica | Variable |
| `LISTA_CORTA` | Consultoría lista corta | Variable |
| `CONCURSO_PUBLICO` | Consultoría concurso público | Sobre $73.000 |
| `CONTRATACION_DIRECTA` | Contratación directa | Casos especiales |
| `EMERGENCIA` | Contratación de emergencia | Casos de emergencia |

### 3.3 Estados del proceso

| Estado | Descripción |
|--------|-------------|
| `PLANIFICADO` | En el PAC, pendiente de inicio |
| `EN_PROCESO` | Publicado en SERCOP, en curso |
| `ADJUDICADO` | Proveedor seleccionado |
| `CONTRATADO` | Contrato suscrito |
| `FINALIZADO` | Proceso completado |
| `DESIERTO` | Sin ofertas válidas |
| `CANCELADO` | Proceso cancelado |

---

## 4. Seguimiento del Proceso

El seguimiento registra el avance del proceso de contratación.

| Campo | Descripción |
|-------|-------------|
| `proveedor_adjudicado` | Nombre del proveedor ganador |
| `ruc_proveedor` | RUC del proveedor |
| `valor_adjudicado` | Monto adjudicado |
| `numero_contrato` | Número del contrato suscrito |
| `fecha_adjudicacion` | Fecha de adjudicación |
| `observaciones` | Notas del proceso |

---

## 5. Plazos del Proceso

Registra las fechas clave de cada etapa del proceso de contratación.

| Campo | Descripción |
|-------|-------------|
| `etapa` | Nombre de la etapa (ej. "Recepción de ofertas") |
| `fecha_inicio` | Inicio de la etapa |
| `fecha_fin` | Fin de la etapa |
| `completada` | Indica si la etapa fue completada |

**Etapas típicas de un proceso:**
1. Elaboración de pliegos
2. Publicación en SERCOP
3. Preguntas y respuestas
4. Recepción de ofertas
5. Calificación
6. Adjudicación
7. Suscripción del contrato

---

## 6. Checklist Documental

Cada proceso tiene un checklist de documentos requeridos según el tipo de contratación.

| Campo | Descripción |
|-------|-------------|
| `nombre_documento` | Nombre del documento requerido |
| `obligatorio` | Indica si es obligatorio |
| `cargado` | Indica si fue subido al sistema |
| `observacion` | Notas sobre el documento |

**Documentos comunes:**
- Estudio de mercado / presupuesto referencial
- Especificaciones técnicas / términos de referencia
- Resolución de inicio
- Pliegos aprobados
- Acta de adjudicación
- Contrato suscrito
- Garantías

---

## 7. Dashboard de Compras

El dashboard muestra un resumen ejecutivo del estado de los procesos de contratación:

- Total de procesos por estado
- Monto total adjudicado
- Procesos en riesgo (plazos vencidos)
- Ejecución del PAC (% completado)

---

## 8. Preguntas Frecuentes

**¿El módulo publica automáticamente en el portal SERCOP?**
No. El módulo registra y da seguimiento a los procesos internamente. La publicación en el portal del SERCOP se realiza directamente en el sistema SOCE del SERCOP. Los datos deben ingresarse en ambos sistemas.

**¿Puedo registrar un proceso no planificado en el PAC?**
Sí, mediante una **reforma al PAC**. Actualice la carpeta anual para incluir el nuevo proceso antes de iniciarlo.

**¿Qué pasa si declaro desierto un proceso?**
El proceso pasa a estado `DESIERTO`. Puede iniciar un nuevo proceso con el mismo objeto de contratación si las condiciones lo permiten.

**¿Cómo vinculo un proceso con el presupuesto?**
El compromiso presupuestario se crea en el módulo de Presupuesto referenciando el número de contrato del proceso adjudicado.
