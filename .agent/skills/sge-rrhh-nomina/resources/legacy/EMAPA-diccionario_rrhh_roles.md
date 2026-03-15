# Diccionario de Datos: Módulo RRHH y Nómina (Roles)

Este documento consolida las tablas identificadas en los diagramas **DIAGRAMA RRHH** y **DIAGRAMA ROLES** de la base de datos `emapa_r_pro`.

## 1. Listado de Tablas

- [`TBL_AD_ROL`](#tbladrol)
- [`TBL_AD_ROL_ANTICIPO_PAGO`](#tbladrolanticipopago)
- [`TBL_AD_ROL_ANTICIPO_PRESTAMO`](#tbladrolanticipoprestamo)
- [`TBL_AD_ROL_APLICACION`](#tbladrolaplicacion)
- [`TBL_AD_ROL_DEFINITIVO`](#tbladroldefinitivo)
- [`TBL_AD_ROL_ESCALA_SALARIAL`](#tbladrolescalasalarial)
- [`TBL_AD_ROL_METODOLOGIA`](#tbladrolmetodologia)
- [`TBL_AD_ROL_NOVEDAD`](#tbladrolnovedad)
- [`TBL_AD_ROL_PENDIENTE`](#tbladrolpendiente)
- [`TBL_AD_ROL_PERIODO`](#tbladrolperiodo)
- [`TBL_AD_ROL_PRESTAMO_ANTICIPO`](#tbladrolprestamoanticipo)
- [`TBL_AD_ROL_PROVISIONAL`](#tbladrolprovisional)
- [`TBL_AD_ROL_RUBRO`](#tbladrolrubro)
- [`TBL_AD_ROL_RUBRO_DET`](#tbladrolrubrodet)
- [`TBL_AD_ROL_TIPO_RUBRO`](#tbladroltiporubro)
- [`TBL_AD_RRHH_ACCIDENTE`](#tbladrrhhaccidente)
- [`TBL_AD_RRHH_BENEFICIO`](#tbladrrhhbeneficio)
- [`TBL_AD_RRHH_CARGO`](#tbladrrhhcargo)
- [`TBL_AD_RRHH_CARGOS`](#tbladrrhhcargos)
- [`TBL_AD_RRHH_CONTRATO`](#tbladrrhhcontrato)
- [`TBL_AD_RRHH_CONTRATO_CATALOGO`](#tbladrrhhcontratocatalogo)
- [`TBL_AD_RRHH_CURRICULUM`](#tbladrrhhcurriculum)
- [`TBL_AD_RRHH_CURSO`](#tbladrrhhcurso)
- [`TBL_AD_RRHH_DATOS`](#tbladrrhhdatos)
- [`TBL_AD_RRHH_DEPARTAMENTO`](#tbladrrhhdepartamento)
- [`TBL_AD_RRHH_DIVISION`](#tbladrrhhdivision)
- [`TBL_AD_RRHH_FAMILIA`](#tbladrrhhfamilia)
- [`TBL_AD_RRHH_IDIOMA`](#tbladrrhhidioma)
- [`TBL_AD_RRHH_INCENTIVO`](#tbladrrhhincentivo)
- [`TBL_AD_RRHH_LABORAL`](#tbladrrhhlaboral)
- [`TBL_AD_RRHH_MULTA`](#tbladrrhhmulta)
- [`TBL_AD_RRHH_PRESTAMO`](#tbladrrhhprestamo)
- [`TBL_AD_RRHH_RET_JUDICIAL`](#tbladrrhhretjudicial)
- [`TBL_AD_RRHH_SELECCION`](#tbladrrhhseleccion)
- [`TBL_AD_RRHH_TIPO_EMPLEADO`](#tbladrrhhtipoempleado)
- [`TBL_AD_RRHH_TRB_SOCIAL`](#tbladrrhhtrbsocial)
- [`TBL_AD_RRHH_UNIDAD`](#tbladrrhhunidad)
- [`TBL_AD_RRHH_VACACION`](#tbladrrhhvacacion)
- [`TBL_AD_RRHH_VACACION_DET`](#tbladrrhhvacaciondet)
- [`TBL_MIS_CLIENTE_EXTERNO`](#tblmisclienteexterno)
- [`TBL_TE_CAL_PAR`](#tbltecalpar)

## 2. Estructura de Tablas

### TBL_AD_ROL

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RRB_ID | smallint | 2 | No | No |
| RPE_ANIO | smallint | 2 | No | No |
| RPE_MES | smallint | 2 | No | No |
| CLE_CI_RUC | varchar | 15 | No | No |
| ROL_VALOR | float | 8 | Sí | No |
| ROL_PAGADO | bit | 1 | No | No |
| ROL_TIPO | varchar | 5 | No | No |
| ROL_CALCULADO | bit | 1 | No | No |
| ROL_FACTOR | smallint | 2 | Sí | No |

### TBL_AD_ROL_ANTICIPO_PAGO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RPG_ID | bigint | 8 | No | Sí |
| RAN_ID | int | 4 | No | No |
| RPG_FECHA | smalldatetime | 4 | No | No |
| RPG_MONTO | float | 8 | No | No |
| RPG_PAGADO | bit | 1 | No | No |

### TBL_AD_ROL_ANTICIPO_PRESTAMO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RAN_ID | int | 4 | No | Sí |
| RRB_ID | smallint | 2 | No | No |
| CLE_CI_RUC | varchar | 15 | No | No |
| RAN_FECHA | smalldatetime | 4 | No | No |
| RAN_MONTO | float | 8 | No | No |
| RAN_REGISTRADO | bit | 1 | No | No |

### TBL_AD_ROL_APLICACION

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RRB_ID | smallint | 2 | No | No |
| RHT_ID | varchar | 10 | No | No |
| RRB_VALOR | real | 4 | Sí | No |
| RRB_ID_REF | smallint | 2 | Sí | No |

### TBL_AD_ROL_DEFINITIVO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RDE_ID | int | 4 | No | No |
| RRB_ID | smallint | 2 | Sí | No |

### TBL_AD_ROL_ESCALA_SALARIAL

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RES_ID | int | 4 | No | Sí |
| RES_NOMBRE | varchar | 50 | No | No |
| RES_SUELDO_NOMINAL | float | 8 | No | No |

### TBL_AD_ROL_METODOLOGIA

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RRB_ID | smallint | 2 | No | No |
| RRB_BASE | int | 4 | No | No |
| RRB_UNIDAD | varchar | 10 | Sí | No |
| RRB_VALOR | real | 4 | No | No |
| RRB_ID_REF | smallint | 2 | Sí | No |
| RRB_CALCULO | bit | 1 | Sí | No |
| RRB_FIJ_POR | smallint | 2 | Sí | No |
| RRB_PARAMETRO | varchar | 50 | Sí | No |

### TBL_AD_ROL_NOVEDAD

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RRB_ID | smallint | 2 | No | No |
| RPE_ANIO | smallint | 2 | No | No |
| RPE_MES | smallint | 2 | No | No |
| CLE_CI_RUC | varchar | 15 | No | No |
| RNO_CANTIDAD | float | 8 | No | No |

### TBL_AD_ROL_PENDIENTE

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RRB_ID | smallint | 2 | No | No |
| RPE_ANIO | smallint | 2 | No | No |
| RPE_MES | smallint | 2 | No | No |
| CLE_CI_RUC | varchar | 15 | No | No |
| RPE_VALOR | real | 4 | Sí | No |
| RPE_MESES | tinyint | 1 | Sí | No |
| RPE_CALCULADO | bit | 1 | Sí | No |
| RPE_TIPO | char | 5 | Sí | No |
| RPE_FACTOR | smallint | 2 | Sí | No |

### TBL_AD_ROL_PERIODO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RPE_ANIO | smallint | 2 | No | No |
| RPE_MES | smallint | 2 | No | No |
| RPE_ACTUAL | bit | 1 | No | No |

### TBL_AD_ROL_PRESTAMO_ANTICIPO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RPA_ID | numeric | 9 | No | Sí |
| RRB_ID | smallint | 2 | Sí | No |

### TBL_AD_ROL_PROVISIONAL

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RPR_ID | int | 4 | No | No |
| RRB_ID | smallint | 2 | Sí | No |

### TBL_AD_ROL_RUBRO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RRB_ID | smallint | 2 | No | Sí |
| RRB_NOMBRE | varchar | 50 | No | No |
| RRB_DESCRIPCION | varchar | 255 | Sí | No |
| RRB_PARAMETRO | varchar | 50 | Sí | No |
| RTR_TIPO_ID | varchar | 5 | No | No |
| RRB_FACTOR | smallint | 2 | No | No |
| RRB_DESCONTABLE | bit | 1 | No | No |
| RRB_USER | varchar | 20 | Sí | No |
| RRB_FECHA | smalldatetime | 4 | Sí | No |

### TBL_AD_ROL_RUBRO_DET

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RRB_ID_PADRE | smallint | 2 | No | No |
| RRB_ID_HIJO | smallint | 2 | No | No |

### TBL_AD_ROL_TIPO_RUBRO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RTR_TIPO_ID | varchar | 5 | No | No |
| RTR_TIPO_DESC | varchar | 50 | No | No |

### TBL_AD_RRHH_ACCIDENTE

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RHA_ID | int | 4 | No | Sí |
| RHA_FECHA | varchar | 15 | Sí | No |
| RHA_MOTIVO | varchar | 30 | Sí | No |
| RHA_OBSERVACION | varchar | 255 | Sí | No |
| CLE_CI_RUC | varchar | 15 | No | No |
| RHA_DIAGNOSTICO | varchar | 255 | Sí | No |
| RHA_CENTRO | varchar | 100 | Sí | No |
| RHA_MEDICO | varchar | 100 | Sí | No |
| RHA_TIPO | varchar | 20 | Sí | No |
| RH_SG_SEGUROS_ID | int | 4 | Sí | No |
| RH_SG_Estado | char | 20 | Sí | No |
| Reg | bit | 1 | Sí | No |
| COM_USER | varchar | 15 | Sí | No |

### TBL_AD_RRHH_BENEFICIO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RBE_ID | int | 4 | No | Sí |
| RBE_TIPO | numeric | 9 | Sí | No |
| RBE_MOTIVO | varchar | 100 | Sí | No |
| RBE_FPAGO | smalldatetime | 4 | Sí | No |
| RBE_VPAGADO | float | 8 | Sí | No |
| RBE_FATENCION | smalldatetime | 4 | Sí | No |
| RBE_VRECLAMADO | float | 8 | Sí | No |
| RBE_VREEMBOLSO | float | 8 | Sí | No |
| CLE_CI_RUC | varchar | 15 | No | No |
| RBE_USER | varchar | 20 | Sí | No |

### TBL_AD_RRHH_CARGO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| CRG_ID | int | 4 | No | Sí |
| CRG_CARGO_WNET | varchar | 100 | Sí | No |
| CRG_SUELDO_WNET | float | 8 | Sí | No |
| CRG_CARGO_LEY | varchar | 50 | Sí | No |
| CRG_SUELDO_LEY | float | 8 | Sí | No |
| CRG_CANTIDAD | int | 4 | Sí | No |

### TBL_AD_RRHH_CARGOS

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RHC_ID | int | 4 | No | Sí |
| RHC_CARGO | varchar | 50 | Sí | No |
| RHC_FECHA | varchar | 50 | Sí | No |
| RHC_SUELDO | varchar | 10 | Sí | No |
| RHC_OBSERVACION | varchar | 50 | Sí | No |
| RHC_TIPOCONTRATO | varchar | 30 | Sí | No |
| RHC_TIPO | varchar | 30 | Sí | No |
| RHC_TIEMPO | varchar | 15 | Sí | No |
| RHC_FECHA_FIN | smalldatetime | 4 | Sí | No |
| CLE_CI_RUC | varchar | 15 | No | No |

### TBL_AD_RRHH_CONTRATO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RCN_ID | int | 4 | No | Sí |
| CLE_CI_RUC | varchar | 15 | No | No |
| RCN_DESDE | smalldatetime | 4 | Sí | No |
| RCN_HASTA | smalldatetime | 4 | Sí | No |
| RCN_VIGENTE | bit | 1 | Sí | No |
| RCN_DOCUMENTO | varchar | 80 | Sí | No |
| RCN_USER | varchar | 20 | Sí | No |
| RCN_TIPO | int | 4 | Sí | No |
| RCN_TIEMPO | int | 4 | Sí | No |
| RCN_FECHA | smalldatetime | 4 | Sí | No |
| RCN_OBSERVACION | varchar | 255 | Sí | No |

### TBL_AD_RRHH_CONTRATO_CATALOGO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RCO_ID | int | 4 | No | Sí |
| RCO_DESCRIPCION | varchar | 50 | Sí | No |
| RCO_TIEMPO | int | 4 | Sí | No |
| RCO_SUELDO | float | 8 | Sí | No |
| RCO_DOCUMENTO | varchar | 80 | Sí | No |
| RCO_OBSERVACION | varchar | 150 | Sí | No |
| RCO_USER | varchar | 20 | Sí | No |

### TBL_AD_RRHH_CURRICULUM

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| CLE_CI_RUC | varchar | 15 | No | No |
| RHU_ID | int | 4 | No | Sí |
| RHU_TIPO | tinyint | 1 | Sí | No |
| RHU_INSTITUCION | varchar | 130 | Sí | No |
| RHU_ANIO | varchar | 15 | Sí | No |
| RHU_TITULO | varchar | 80 | Sí | No |
| RHU_LUGAR | varchar | 30 | Sí | No |
| RHU_DURACION | varchar | 30 | Sí | No |
| RHU_OBSERVACION | varchar | 30 | Sí | No |

### TBL_AD_RRHH_CURSO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| CLE_CI_RUC | varchar | 15 | No | No |
| RHC_ID | int | 4 | No | Sí |
| RHC_CURSO | varchar | 200 | Sí | No |
| RHC_INSTITUCION | varchar | 200 | Sí | No |
| RHC_DURACION | varchar | 15 | Sí | No |
| RHC_PAIS | varchar | 30 | Sí | No |
| RHC_ANIO | int | 4 | Sí | No |
| RHC_OBSERVACION | varchar | 50 | Sí | No |

### TBL_AD_RRHH_DATOS

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| CLE_CI_RUC | varchar | 15 | No | No |
| RES_ID | int | 4 | No | Sí |
| RHD_ESTADO_CIVIL | varchar | 10 | Sí | No |
| RHD_FECHA_NAC | smalldatetime | 4 | Sí | No |
| RHD_LUGAR_NAC | varchar | 20 | Sí | No |
| RHD_NUM_HIJOS | tinyint | 1 | Sí | No |
| RHD_BANCO_NOMBRE | varchar | 30 | Sí | No |
| RHD_BANCO_CTA | varchar | 50 | Sí | No |
| RHD_ACTIVO | bit | 1 | Sí | No |
| RHT_ID | varchar | 10 | Sí | No |
| RHD_POLIZA | varchar | 50 | Sí | No |
| RHD_GRUPO | numeric | 9 | Sí | No |
| RHD_CALIFICACION | int | 4 | Sí | No |
| RHD_DIVISION | int | 4 | Sí | No |
| RHD_DEPARTAMENTO | varchar | 50 | Sí | No |
| RHD_UNIDAD | int | 4 | Sí | No |
| RHD_GRADO | numeric | 9 | Sí | No |
| RHD_SUELDO | float | 8 | Sí | No |
| RHD_PUESTO_AC | char | 100 | Sí | No |
| RHD_PARTIDA_PRES | char | 30 | Sí | No |
| RHD_LUGART_AC | char | 80 | Sí | No |
| RHD_TIPOCONTRATO | char | 20 | Sí | No |
| RHD_SUELDO_base | float | 8 | Sí | No |
| RRD_Contrato | bit | 1 | Sí | No |
| RRD_idCentroCosto | int | 4 | Sí | No |
| RRD_SComponente | float | 8 | Sí | No |
| RHD_FECHA_INGRESO | smalldatetime | 4 | Sí | No |
| RH_GR_ID | int | 4 | Sí | No |
| RHD_Admi | bit | 1 | Sí | No |
| RHD_Programa | int | 4 | Sí | No |
| RHD_DEP_ID | int | 4 | Sí | No |
| RHD_GREMIO | char | 1 | Sí | No |
| RHD_BASE_CESANTIA | float | 8 | Sí | No |
| RHD_FOTO | varchar | 100 | Sí | No |

### TBL_AD_RRHH_DEPARTAMENTO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| ADI_ID | int | 4 | No | No |
| ADE_ID | int | 4 | No | No |
| ADE_DESCRIPCION | varchar | 50 | Sí | No |
| ADE_OBSERVACION | varchar | 100 | Sí | No |

### TBL_AD_RRHH_DIVISION

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| ADI_ID | int | 4 | No | No |
| ADI_DESCRIPCION | varchar | 30 | Sí | No |
| ADI_OBSERVACION | varchar | 100 | Sí | No |

### TBL_AD_RRHH_FAMILIA

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RHF_ID | int | 4 | No | Sí |
| RHF_RELACION | tinyint | 1 | Sí | No |
| RHF_NOMBRE | varchar | 50 | Sí | No |
| RHF_FECHA_NAC | varchar | 20 | Sí | No |
| RHF_INGRESO | varchar | 50 | Sí | No |
| RHF_EDAD | varchar | 3 | Sí | No |
| RHF_OCUPACION | varchar | 20 | Sí | No |
| RHF_NACIONALIDAD | varchar | 50 | Sí | No |
| RHF_VIVE | varchar | 2 | Sí | No |
| RHF_CARGAS | varchar | 2 | Sí | No |
| CLE_CI_RUC | varchar | 15 | No | No |

### TBL_AD_RRHH_IDIOMA

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| CLE_CI_RUC | varchar | 15 | No | No |
| RHD_ID | int | 4 | No | Sí |
| RHD_IDIOMA | varchar | 20 | Sí | No |
| RHD_LEE | int | 4 | Sí | No |
| RHD_ESCRIBE | int | 4 | Sí | No |
| RHD_HABLA | int | 4 | Sí | No |

### TBL_AD_RRHH_INCENTIVO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| CLE_CI_RUC | varchar | 15 | No | No |
| RHI_ID | int | 4 | No | Sí |
| RHI_TIPO | numeric | 9 | Sí | No |
| RHI_DESDE | smalldatetime | 4 | Sí | No |
| RHI_HASTA | smalldatetime | 4 | Sí | No |
| RHI_INSTITUCION | varchar | 80 | Sí | No |
| RHI_HORAS | int | 4 | Sí | No |
| RHI_CURSO | varchar | 100 | Sí | No |
| RHI_PAIS | varchar | 30 | Sí | No |
| RHI_CIUDAD | varchar | 30 | Sí | No |
| RHI_COSTO | float | 8 | Sí | No |

### TBL_AD_RRHH_LABORAL

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| CLE_CI_RUC | varchar | 15 | No | No |
| RHE_ID | int | 4 | No | Sí |
| RHE_EMPRESA | varchar | 100 | Sí | No |
| RHE_FUNCION | varchar | 80 | Sí | No |
| RHE_TIEMPO | varchar | 15 | Sí | No |
| RHE_PAIS | varchar | 30 | Sí | No |
| RHE_TELEFONO | varchar | 20 | Sí | No |
| RHE_ANIO | int | 4 | Sí | No |

### TBL_AD_RRHH_MULTA

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RMU_ID | int | 4 | No | Sí |
| RMU_TIPO | numeric | 9 | Sí | No |
| RMU_MOTIVO | varchar | 150 | Sí | No |
| RMU_REGISTRA | varchar | 20 | Sí | No |
| RMU_DOCUMENTO | varchar | 80 | Sí | No |
| RMU_SANCION | float | 8 | Sí | No |
| CLE_CI_RUC | varchar | 15 | No | No |
| RMU_FSANCION | smalldatetime | 4 | Sí | No |

### TBL_AD_RRHH_PRESTAMO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RHP_ID | int | 4 | No | Sí |
| RHP_ENTIDAD | varchar | 30 | Sí | No |
| RHP_VALOR | varchar | 10 | Sí | No |
| RHP_MOTIVO | varchar | 50 | Sí | No |
| RHP_FECHA | varchar | 20 | Sí | No |
| RHP_CANCELA | varchar | 20 | Sí | No |
| RHP_TIP_PRESTAMO | varchar | 30 | Sí | No |
| RHP_OBSERVACION | varchar | 50 | Sí | No |
| CLE_CI_RUC | varchar | 15 | No | No |

### TBL_AD_RRHH_RET_JUDICIAL

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RHJ_ID | int | 4 | No | Sí |
| RHJ_RETENCION | varchar | 30 | Sí | No |
| RHJ_OBSERVACION | varchar | 50 | Sí | No |
| CLE_CI_RUC | varchar | 15 | No | No |
| RHJ_FECHA | varchar | 15 | No | No |

### TBL_AD_RRHH_SELECCION

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RHS_ID | int | 4 | No | Sí |
| RHS_ASP_PERSONAL | varchar | 50 | Sí | No |
| RHS_ASP_FAMILIAR | varchar | 50 | Sí | No |
| RHS_ASP_LABORAL | varchar | 50 | Sí | No |
| RHS_PRO_COMENTARIO | varchar | 50 | Sí | No |
| RHS_TIE_EMPRESA | varchar | 3 | Sí | No |
| RHS_MES_EMPRESA | char | 2 | Sí | No |
| RHS_FEC_INGRESO | varchar | 15 | Sí | No |
| RHS_SUE_INGRESO | varchar | 50 | Sí | No |
| RHS_SUE_ACTUAL | varchar | 50 | Sí | No |
| RHS_ARE_TRABAJA | varchar | 50 | Sí | No |
| CLE_CI_RUC | varchar | 15 | No | No |

### TBL_AD_RRHH_TIPO_EMPLEADO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RHT_ID | varchar | 10 | No | No |
| RHT_DESC | varchar | 50 | Sí | No |
| RHT_UNIFICADO | bit | 1 | Sí | No |
| RHT_APORTE | char | 2 | Sí | No |

### TBL_AD_RRHH_TRB_SOCIAL

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RHS_ID | int | 4 | No | Sí |
| RHS_FECHA | varchar | 15 | Sí | No |
| RHS_MOTIVO | varchar | 50 | Sí | No |
| RHS_NOM_VISITANTE | varchar | 30 | Sí | No |
| RHS_OBSERVACION | varchar | 50 | Sí | No |
| CLE_CI_RUC | varchar | 15 | No | No |

### TBL_AD_RRHH_UNIDAD

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| ADE_ID | int | 4 | No | No |
| AUN_ID | int | 4 | No | No |
| AUN_DESCRIPCION | varchar | 30 | Sí | No |
| AUN_OBSERVACION | varchar | 100 | Sí | No |

### TBL_AD_RRHH_VACACION

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RVA_ID | int | 4 | No | Sí |
| RVA_TIPO | numeric | 9 | Sí | No |
| RVA_MOTIVO | varchar | 200 | Sí | No |
| RVA_FDESDE | smalldatetime | 4 | Sí | No |
| RVA_FHASTA | smalldatetime | 4 | Sí | No |
| RVA_DIAS | int | 4 | Sí | No |
| RVA_HDESDE | smalldatetime | 4 | Sí | No |
| RVA_HHASTA | smalldatetime | 4 | Sí | No |
| RVA_HORAS | int | 4 | Sí | No |
| RVA_AUTORIZADO | bit | 1 | Sí | No |
| CLE_CI_RUC | varchar | 15 | No | No |
| COM_USER | varchar | 15 | Sí | No |
| RVA_FDESDE_REC | smalldatetime | 4 | Sí | No |
| RVA_FHASTA_REC | smalldatetime | 4 | Sí | No |
| RVA_HDESDE_REC | smalldatetime | 4 | Sí | No |
| RVA_HHASTA_REC | varchar | 5 | Sí | No |
| RVA_OBSERVACION | varchar | 10 | Sí | No |
| RVA_PERIODO | varchar | 6 | Sí | No |
| RH_FechaCrea | smalldatetime | 4 | Sí | No |
| RH_Oficial | bit | 1 | Sí | No |
| RH_Remunerado | bit | 1 | Sí | No |
| RH_Remplazo | char | 25 | Sí | No |
| RH_Puesto | char | 30 | Sí | No |
| Registrado | bit | 1 | Sí | No |
| RVA_MINUTOS | int | 4 | Sí | No |

### TBL_AD_RRHH_VACACION_DET

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RVA_ID | int | 4 | No | No |
| VAD_ID | int | 4 | No | No |
| VAD_DIADESDE | smalldatetime | 4 | Sí | No |
| VAD_DIAHASTA | smalldatetime | 4 | Sí | No |
| VAD_HORADESDE | varchar | 5 | Sí | No |
| VAD_HORAHASTA | varchar | 5 | Sí | No |
| VAD_DIAS | int | 4 | Sí | No |
| VAD_HORAS | int | 4 | Sí | No |
| VAD_USER | varchar | 20 | Sí | No |

### TBL_MIS_CLIENTE_EXTERNO

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| RES_ID | int | 4 | Sí | No |
| CLE_CI_RUC | varchar | 15 | No | No |
| TCL_ID | int | 4 | Sí | No |
| CLE_APELLIDOS | varchar | 50 | No | No |
| CLE_NOMBRES | varchar | 49 | No | No |
| CLE_NOMBRE_EMPRESA | varchar | 100 | Sí | No |
| CLE_CALLEP | varchar | 75 | Sí | No |
| CLE_NUMERODIR | varchar | 10 | Sí | No |
| CLE_CALLES | varchar | 75 | Sí | No |
| CLE_TELEFONO | varchar | 30 | Sí | No |
| CLE_EMAIL | varchar | 100 | Sí | No |
| CLE_LUGAR_TRABAJO | varchar | 20 | Sí | No |
| CLE_TELF_TRAB | varchar | 12 | Sí | No |
| CLE_EXTENSION | varchar | 3 | Sí | No |
| CLE_PROFESION | varchar | 50 | Sí | No |
| CLE_ARTESANAL | bit | 1 | Sí | No |
| CLE_ESPECIAL | bit | 1 | Sí | No |
| CLE_LINEA | varchar | 100 | Sí | No |
| CLE_NIVEL_INSTRUCCION | varchar | 3 | Sí | No |
| CLE_FAX | varchar | 20 | Sí | No |
| CLE_CIUDAD | varchar | 50 | Sí | No |
| CLE_FECHA_NACIMIENTO | smalldatetime | 4 | Sí | No |
| CLE_FECHA | smalldatetime | 4 | Sí | No |
| CLE_USER | varchar | 20 | Sí | No |
| CLE_DOC_TIPO | varchar | 50 | Sí | No |
| CLE_SRI_SERIE | varchar | 10 | Sí | No |
| CLE_SRI_AUTORIZ | varchar | 15 | Sí | No |
| CLE_SRI_DEVOL_IVA | bit | 1 | Sí | No |
| CLE_SRI_FECHA_VALIDEZ1 | smalldatetime | 4 | Sí | No |
| CLE_SRI_IVA_RET | numeric | 5 | Sí | No |
| CLE_SRI_IVA_COD_RET | tinyint | 1 | Sí | No |
| CLE_SRI_FUENTE_RET | numeric | 5 | Sí | No |
| CLE_NACIONALIDAD | varchar | 50 | Sí | No |
| CLE_EST_CIVIL | varchar | 15 | Sí | No |
| CLE_SEXO | varchar | 15 | Sí | No |
| CLE_SECTOR | varchar | 75 | Sí | No |
| CLE_DIRECCION | varchar | 150 | Sí | No |
| CLE_CELULAR | varchar | 15 | Sí | No |
| CLE_HIJOS | tinyint | 1 | Sí | No |
| CLE_IESS | varchar | 20 | Sí | No |
| CLE_RECORD_POL | varchar | 80 | Sí | No |
| CLE_LIBRETA_MIL | varchar | 20 | Sí | No |
| CRG_ID | int | 4 | Sí | No |
| CLE_LICENCIA | varchar | 2 | Sí | No |
| CLE_TIP_SANGRE | varchar | 10 | Sí | No |
| CLE_VIVIENDA | varchar | 20 | Sí | No |
| CLE_TIP_VIVIENDA | varchar | 20 | Sí | No |
| CLE_AGUA | varchar | 2 | Sí | No |
| CLE_LUZ | varchar | 2 | Sí | No |
| CLE_ALCANTARILLADO | varchar | 2 | Sí | No |
| CLE_SER_HIGIENICO | varchar | 2 | Sí | No |
| CLE_BANCO_CUENTA | varchar | 50 | Sí | No |
| CLE_BANCO_TIPO_CUENTA | int | 4 | Sí | No |
| CLE_BANCO | varchar | 50 | Sí | No |
| CLE_SRI_SERIE_ESTABLECIMIENTO | varchar | 3 | Sí | No |
| CLE_SRI_SERIE_PUNTO_EMISION | varchar | 3 | Sí | No |
| CLE_SRI_AUTORIZACION | varchar | 15 | Sí | No |
| CLE_SRI_FECHA_VALIDEZ | varchar | 7 | Sí | No |
| CLE_SRI_RET_IVA_PORC_SERV | tinyint | 1 | Sí | No |
| CLE_SRI_RET_IVA_COD_SERV | char | 1 | Sí | No |
| CLE_SRI_RET_IVA_PORC_BIEN | tinyint | 1 | Sí | No |
| CLE_SRI_RET_IVA_COD_BIEN | char | 1 | Sí | No |
| CLE_SRI_RET_RENTA_SERV | tinyint | 1 | Sí | No |
| CLE_SRI_RET_RENTA_BIEN | tinyint | 1 | Sí | No |
| CLE_FACTURA_DESDE | int | 4 | Sí | No |
| CLE_FACTURA_HASTA | int | 4 | Sí | No |
| CLE_REPRESENTANTE | varchar | 255 | Sí | No |
| CLE_LINEA_DESCRIPCION | varchar | 255 | Sí | No |
| CLE_TIPO_CONTRIBUYENTE | varchar | 150 | Sí | No |
| CLE_EVENTUAL | tinyint | 1 | Sí | No |
| CLE_CORREO | varchar | 255 | Sí | No |
| CLE_CODIGO_BANCO | varchar | 10 | Sí | No |
| CLE_CI_ALTERNATIVO | varchar | 15 | Sí | No |
| CLE_FALLECIDO | bit | 1 | Sí | No |

### TBL_TE_CAL_PAR

| Columna | Tipo de Dato | Longitud | Permite Nulos | Identity |
|---|---|---|---|---|
| TCC_ID | numeric | 9 | No | Sí |
| CDE_ID | int | 4 | Sí | No |
| TPR_DESCRIPCION | varchar | 100 | Sí | No |
| TCC_CANTIDAD | float | 8 | Sí | No |
| TPR_UNIDAD | varchar | 50 | Sí | No |
| TPR_ID | numeric | 9 | Sí | No |

## 3. Relaciones (Claves Foráneas)

| Nombre FK | Tabla | Columna FK | Referencia A | Columna Ref |
|---|---|---|---|---|
| FK_TBL_AD_ACT_SALVO_CLIENTE_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_ACT_SALVO_CLIENTE | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_ROL_TBL_AD_ROL_PERIODO | TBL_AD_ROL | RPE_ANIO | TBL_AD_ROL_PERIODO | RPE_ANIO |
| FK_TBL_AD_ROL_TBL_AD_ROL_PERIODO | TBL_AD_ROL | RPE_MES | TBL_AD_ROL_PERIODO | RPE_MES |
| FK_TBL_AD_ROL_TBL_AD_ROL_RUBRO | TBL_AD_ROL | RRB_ID | TBL_AD_ROL_RUBRO | RRB_ID |
| FK_TBL_AD_ROL_ANTICIPO_PAGO_TBL_AD_ROL_ANTICIPO_PRESTAMO | TBL_AD_ROL_ANTICIPO_PAGO | RAN_ID | TBL_AD_ROL_ANTICIPO_PRESTAMO | RAN_ID |
| FK_TBL_AD_ROL_ANTICIPO_PRESTAMO_TBL_AD_ROL_RUBRO | TBL_AD_ROL_ANTICIPO_PRESTAMO | RRB_ID | TBL_AD_ROL_RUBRO | RRB_ID |
| FK_TBL_AD_ROL_ANTICIPO_PRESTAMO_TBL_AD_RRHH_DATOS | TBL_AD_ROL_ANTICIPO_PRESTAMO | CLE_CI_RUC | TBL_AD_RRHH_DATOS | CLE_CI_RUC |
| FK_TBL_AD_ROL_ANTICIPO_PRESTAMO_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_ROL_ANTICIPO_PRESTAMO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_ROL_APLICACION_TBL_AD_ROL_METODOLOGIA | TBL_AD_ROL_APLICACION | RRB_ID | TBL_AD_ROL_METODOLOGIA | RRB_ID |
| CNS_RRB_RDE | TBL_AD_ROL_DEFINITIVO | RRB_ID | TBL_AD_ROL_RUBRO | RRB_ID |
| CNS_RRB_RMD2 | TBL_AD_ROL_METODOLOGIA | RRB_ID | TBL_AD_ROL_RUBRO | RRB_ID |
| FK_TBL_AD_ROL_METODOLOGIA_TBL_AD_ROL_RUBRO | TBL_AD_ROL_METODOLOGIA | RRB_ID_REF | TBL_AD_ROL_RUBRO | RRB_ID |
| FK_TBL_AD_ROL_NOVEDAD_TBL_AD_ROL_PERIODO | TBL_AD_ROL_NOVEDAD | RPE_ANIO | TBL_AD_ROL_PERIODO | RPE_ANIO |
| FK_TBL_AD_ROL_NOVEDAD_TBL_AD_ROL_PERIODO | TBL_AD_ROL_NOVEDAD | RPE_MES | TBL_AD_ROL_PERIODO | RPE_MES |
| FK_TBL_AD_ROL_NOVEDAD_TBL_AD_ROL_RUBRO | TBL_AD_ROL_NOVEDAD | RRB_ID | TBL_AD_ROL_RUBRO | RRB_ID |
| FK_TBL_AD_ROL_NOVEDAD_TBL_AD_RRHH_DATOS | TBL_AD_ROL_NOVEDAD | CLE_CI_RUC | TBL_AD_RRHH_DATOS | CLE_CI_RUC |
| FK_TBL_AD_ROL_NOVEDAD_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_ROL_NOVEDAD | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_ROL_PENDIENTE_TBL_AD_ROL_PERIODO | TBL_AD_ROL_PENDIENTE | RPE_ANIO | TBL_AD_ROL_PERIODO | RPE_ANIO |
| FK_TBL_AD_ROL_PENDIENTE_TBL_AD_ROL_PERIODO | TBL_AD_ROL_PENDIENTE | RPE_MES | TBL_AD_ROL_PERIODO | RPE_MES |
| FK_TBL_AD_ROL_PENDIENTE_TBL_AD_ROL_RUBRO | TBL_AD_ROL_PENDIENTE | RRB_ID | TBL_AD_ROL_RUBRO | RRB_ID |
| FK_TBL_AD_ROL_PENDIENTE_TBL_AD_RRHH_DATOS | TBL_AD_ROL_PENDIENTE | CLE_CI_RUC | TBL_AD_RRHH_DATOS | CLE_CI_RUC |
| FK_TBL_AD_ROL_PENDIENTE_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_ROL_PENDIENTE | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_RRB_RPA | TBL_AD_ROL_PRESTAMO_ANTICIPO | RRB_ID | TBL_AD_ROL_RUBRO | RRB_ID |
| CNS_RRB_RPO | TBL_AD_ROL_PROVISIONAL | RRB_ID | TBL_AD_ROL_RUBRO | RRB_ID |
| FK_TBL_AD_ROL_RUBRO_TBL_AD_ROL_TIPO_RUBRO | TBL_AD_ROL_RUBRO | RTR_TIPO_ID | TBL_AD_ROL_TIPO_RUBRO | RTR_TIPO_ID |
| FK_TBL_AD_ROL_RUBRO_DET_TBL_AD_ROL_RUBRO | TBL_AD_ROL_RUBRO_DET | RRB_ID_HIJO | TBL_AD_ROL_RUBRO | RRB_ID |
| FK_TBL_AD_ROL_RUBRO_DET_TBL_AD_ROL_RUBRO1 | TBL_AD_ROL_RUBRO_DET | RRB_ID_PADRE | TBL_AD_ROL_RUBRO | RRB_ID |
| FK_TBL_AD_RRHH_ACCIDENTE_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_ACCIDENTE | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_BENEFICIO_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_BENEFICIO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_CARGOS_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_CARGOS | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_CONTRATO_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_CONTRATO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_CURRICULUM_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_CURRICULUM | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_CURSO_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_CURSO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_DATOS_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_DATOS | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_FAMILIA_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_FAMILIA | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_IDIOMA_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_IDIOMA | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_INCENTIVO_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_INCENTIVO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_LABORAL_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_LABORAL | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_MULTA_TBL_AD_PARAMETRO | TBL_AD_RRHH_MULTA | RMU_TIPO | TBL_AD_PARAMETRO | APR_ID |
| FK_TBL_AD_RRHH_MULTA_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_MULTA | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_PRESTAMO_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_PRESTAMO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_RET_JUDICIAL_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_RET_JUDICIAL | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_SELECCION_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_SELECCION | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_RRHH_TRB_SOCIAL_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_RRHH_TRB_SOCIAL | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_AD_SOLICITUD_SERVICIOS_TBL_MIS_CLIENTE_EXTERNO | TBL_AD_SOLICITUD_SERVICIOS | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_FI_ACT_USUARIO_TBL_MIS_CLIENTE_EXTERNO | TBL_FI_ACT_USUARIO | USR_CI | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_CLE_COM | TBL_FI_ADQ_COMPRA | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_FI_ADQ_CONTRATO_TBL_MIS_CLIENTE_EXTERNO | TBL_FI_ADQ_CONTRATO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_FI_ADQ_REQUERIMIENTO_TBL_MIS_CLIENTE_EXTERNO | TBL_FI_ADQ_REQUERIMIENTO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_FI_ADQ_SOLICITUD_TBL_MIS_CLIENTE_EXTERNO | TBL_FI_ADQ_SOLICITUD | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_MIS_CLIENTE_EXTERNO | TBL_FI_BOD_ACTIVOS_EMPLEADO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_FI_BOD_DEVOLUCION_TBL_MIS_CLIENTE_EXTERNO | TBL_FI_BOD_DEVOLUCION | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_CLE_EGB | TBL_FI_BOD_EGRESO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_CLE_CMP | TBL_FI_CON_COMPROBANTE | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_CLE_CXC | TBL_FI_CXC | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_CLE_CCP | TBL_FI_CXC_PAGO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_CLE_CXP | TBL_FI_CXP | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_CLE_CPP | TBL_FI_CXP_PAGO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_CLE_TGA | TBL_FI_TES_GARANTIA | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_CLE_TGA_1 | TBL_FI_TES_GARANTIA | CLE_CI_RUC2 | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_MIS_CLIENTE_EXTERNO_TBL_AD_ROL_ESCALA_SALARIAL | TBL_MIS_CLIENTE_EXTERNO | RES_ID | TBL_AD_ROL_ESCALA_SALARIAL | RES_ID |
| FK_TBL_MIS_CLIENTE_EXTERNO_REFERENCIA_TBL_MIS_CLIENTE_EXTERNO | TBL_MIS_CLIENTE_EXTERNO_REFERENCIA | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| FK_TBL_MIS_CLIENTE_EXTERNO_RELACION_TBL_MIS_CLIENTE_EXTERNO | TBL_MIS_CLIENTE_EXTERNO_RELACION | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_CLE_PRY | TBL_PL_PRE_PROYECTO | CLE_CI_RUC | TBL_MIS_CLIENTE_EXTERNO | CLE_CI_RUC |
| CNS_CDE_TCC | TBL_TE_CAL_PAR | CDE_ID | TBL_TE_CAL_DET | CDE_ID |

---
*Generado automáticamente por Antigravity.*
