"""
Router — Módulo Compras Públicas
Prefijo: /api/compras
Esquema DB: compras_publicas
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Optional
from decimal import Decimal

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.compras_publicas import (
    CarpetaAnual,
    ProcesoCompra,
    SeguimientoProceso,
    PlazoProceso,
    ChecklistDocumental,
)
from app.schemas.compras_publicas import (
    CarpetaAnualCrear,
    CarpetaAnualActualizar,
    CarpetaAnualRespuesta,
    ProcesoCompraCrear,
    ProcesoCompraActualizar,
    ProcesoCompraRespuesta,
    ProcesoCompraDetalle,
    SeguimientoProcesoCrear,
    SeguimientoProcesoActualizar,
    SeguimientoProcesosRespuesta,
    PlazoProcesoCrear,
    PlazoProcesoActualizar,
    PlazoProcesosRespuesta,
    ChecklistDocumentalCrear,
    ChecklistDocumentalActualizar,
    ChecklistDocumentalRespuesta,
    DashboardRespuesta,
    DashboardKPIs,
)

router = APIRouter()


# ===========================================================================
# CARPETAS ANUALES
# ===========================================================================

@router.get("/carpetas-anuales", response_model=List[CarpetaAnualRespuesta])
def listar_carpetas_anuales(
    anio: Optional[int] = Query(None, description="Filtrar por año"),
    tipo_area: Optional[str] = Query(None, description="DIRECCION o UNIDAD"),
    activa: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Listar carpetas anuales de contratación pública."""
    query = db.query(CarpetaAnual)
    if anio is not None:
        query = query.filter(CarpetaAnual.anio == anio)
    if tipo_area is not None:
        query = query.filter(CarpetaAnual.tipo_area == tipo_area)
    if activa is not None:
        query = query.filter(CarpetaAnual.activa == activa)

    carpetas = query.order_by(CarpetaAnual.anio.desc(), CarpetaAnual.nombre_area).offset(skip).limit(limit).all()

    resultado = []
    for c in carpetas:
        total = db.query(func.count(ProcesoCompra.id)).filter(ProcesoCompra.carpeta_anual_id == c.id).scalar()
        r = CarpetaAnualRespuesta.model_validate(c)
        r.total_procesos = total or 0
        resultado.append(r)
    return resultado


@router.post("/carpetas-anuales", response_model=CarpetaAnualRespuesta, status_code=status.HTTP_201_CREATED)
def crear_carpeta_anual(
    datos: CarpetaAnualCrear,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Crear una nueva carpeta anual."""
    existente = db.query(CarpetaAnual).filter(
        CarpetaAnual.anio == datos.anio,
        CarpetaAnual.nombre_area == datos.nombre_area,
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una carpeta para esa área y año")

    carpeta = CarpetaAnual(**datos.model_dump(), creada_por_id=current_user.id)
    db.add(carpeta)
    db.commit()
    db.refresh(carpeta)
    resultado = CarpetaAnualRespuesta.model_validate(carpeta)
    resultado.total_procesos = 0
    return resultado


@router.get("/carpetas-anuales/{carpeta_id}", response_model=CarpetaAnualRespuesta)
def obtener_carpeta_anual(
    carpeta_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    carpeta = db.query(CarpetaAnual).filter(CarpetaAnual.id == carpeta_id).first()
    if not carpeta:
        raise HTTPException(status_code=404, detail="Carpeta anual no encontrada")
    total = db.query(func.count(ProcesoCompra.id)).filter(ProcesoCompra.carpeta_anual_id == carpeta_id).scalar()
    resultado = CarpetaAnualRespuesta.model_validate(carpeta)
    resultado.total_procesos = total or 0
    return resultado


@router.patch("/carpetas-anuales/{carpeta_id}", response_model=CarpetaAnualRespuesta)
def actualizar_carpeta_anual(
    carpeta_id: int,
    datos: CarpetaAnualActualizar,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    carpeta = db.query(CarpetaAnual).filter(CarpetaAnual.id == carpeta_id).first()
    if not carpeta:
        raise HTTPException(status_code=404, detail="Carpeta anual no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(carpeta, campo, valor)
    db.commit()
    db.refresh(carpeta)
    total = db.query(func.count(ProcesoCompra.id)).filter(ProcesoCompra.carpeta_anual_id == carpeta_id).scalar()
    resultado = CarpetaAnualRespuesta.model_validate(carpeta)
    resultado.total_procesos = total or 0
    return resultado


@router.delete("/carpetas-anuales/{carpeta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_carpeta_anual(
    carpeta_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    carpeta = db.query(CarpetaAnual).filter(CarpetaAnual.id == carpeta_id).first()
    if not carpeta:
        raise HTTPException(status_code=404, detail="Carpeta anual no encontrada")
    total = db.query(func.count(ProcesoCompra.id)).filter(ProcesoCompra.carpeta_anual_id == carpeta_id).scalar()
    if total and total > 0:
        raise HTTPException(status_code=400, detail="No se puede eliminar una carpeta con procesos asociados")
    db.delete(carpeta)
    db.commit()


# ===========================================================================
# PROCESOS DE COMPRA
# ===========================================================================

@router.get("/procesos", response_model=List[ProcesoCompraRespuesta])
def listar_procesos(
    carpeta_anual_id: Optional[int] = Query(None),
    estado: Optional[str] = Query(None, pattern="^(ACTIVO|ANULADO|FINALIZADO)$"),
    etapa_actual: Optional[str] = Query(None),
    tipo_contratacion: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Listar procesos de contratación pública."""
    query = db.query(ProcesoCompra)
    if carpeta_anual_id is not None:
        query = query.filter(ProcesoCompra.carpeta_anual_id == carpeta_anual_id)
    if estado is not None:
        query = query.filter(ProcesoCompra.estado == estado)
    if etapa_actual is not None:
        query = query.filter(ProcesoCompra.etapa_actual == etapa_actual)
    if tipo_contratacion is not None:
        query = query.filter(ProcesoCompra.tipo_contratacion.ilike(f"%{tipo_contratacion}%"))

    return query.order_by(ProcesoCompra.creado_en.desc()).offset(skip).limit(limit).all()


@router.post("/procesos", response_model=ProcesoCompraRespuesta, status_code=status.HTTP_201_CREATED)
def crear_proceso(
    datos: ProcesoCompraCrear,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Crear un nuevo proceso de contratación pública."""
    carpeta = db.query(CarpetaAnual).filter(CarpetaAnual.id == datos.carpeta_anual_id).first()
    if not carpeta:
        raise HTTPException(status_code=404, detail="Carpeta anual no encontrada")
    if not carpeta.activa:
        raise HTTPException(status_code=400, detail="La carpeta anual está inactiva")

    proceso = ProcesoCompra(**datos.model_dump(), creado_por_id=current_user.id)
    db.add(proceso)
    db.flush()

    # Crear seguimiento vacío automáticamente
    seguimiento = SeguimientoProceso(proceso_id=proceso.id, actualizado_por_id=current_user.id)
    db.add(seguimiento)

    db.commit()
    db.refresh(proceso)
    return proceso


@router.get("/procesos/{proceso_id}", response_model=ProcesoCompraDetalle)
def obtener_proceso(
    proceso_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtener un proceso con todo su detalle (seguimiento, plazos, documentos)."""
    proceso = db.query(ProcesoCompra).filter(ProcesoCompra.id == proceso_id).first()
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    return proceso


@router.patch("/procesos/{proceso_id}", response_model=ProcesoCompraRespuesta)
def actualizar_proceso(
    proceso_id: int,
    datos: ProcesoCompraActualizar,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    proceso = db.query(ProcesoCompra).filter(ProcesoCompra.id == proceso_id).first()
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(proceso, campo, valor)
    db.commit()
    db.refresh(proceso)
    return proceso


@router.delete("/procesos/{proceso_id}", status_code=status.HTTP_204_NO_CONTENT)
def anular_proceso(
    proceso_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Anular (soft-delete) un proceso de contratación."""
    proceso = db.query(ProcesoCompra).filter(ProcesoCompra.id == proceso_id).first()
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    proceso.estado = "ANULADO"
    db.commit()


# ===========================================================================
# SEGUIMIENTO DE PROCESOS
# ===========================================================================

@router.get("/procesos/{proceso_id}/seguimiento", response_model=SeguimientoProcesosRespuesta)
def obtener_seguimiento(
    proceso_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    seguimiento = db.query(SeguimientoProceso).filter(SeguimientoProceso.proceso_id == proceso_id).first()
    if not seguimiento:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado para este proceso")
    return seguimiento


@router.patch("/procesos/{proceso_id}/seguimiento", response_model=SeguimientoProcesosRespuesta)
def actualizar_seguimiento(
    proceso_id: int,
    datos: SeguimientoProcesoActualizar,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Actualizar avance físico y financiero de un proceso."""
    seguimiento = db.query(SeguimientoProceso).filter(SeguimientoProceso.proceso_id == proceso_id).first()
    if not seguimiento:
        # Si no existe, crear
        seguimiento = SeguimientoProceso(proceso_id=proceso_id, actualizado_por_id=current_user.id)
        db.add(seguimiento)

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(seguimiento, campo, valor)
    seguimiento.actualizado_por_id = current_user.id
    db.commit()
    db.refresh(seguimiento)
    return seguimiento


# ===========================================================================
# PLAZOS POR ETAPA
# ===========================================================================

@router.get("/procesos/{proceso_id}/plazos", response_model=List[PlazoProcesosRespuesta])
def listar_plazos(
    proceso_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(PlazoProceso).filter(PlazoProceso.proceso_id == proceso_id).order_by(PlazoProceso.etapa).all()


@router.post("/procesos/{proceso_id}/plazos", response_model=PlazoProcesosRespuesta, status_code=status.HTTP_201_CREATED)
def crear_plazo(
    proceso_id: int,
    datos: PlazoProcesoCrear,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if datos.proceso_id != proceso_id:
        raise HTTPException(status_code=400, detail="proceso_id no coincide con el de la URL")
    proceso = db.query(ProcesoCompra).filter(ProcesoCompra.id == proceso_id).first()
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    plazo = PlazoProceso(**datos.model_dump())
    db.add(plazo)
    db.commit()
    db.refresh(plazo)
    return plazo


@router.patch("/plazos/{plazo_id}", response_model=PlazoProcesosRespuesta)
def actualizar_plazo(
    plazo_id: int,
    datos: PlazoProcesoActualizar,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plazo = db.query(PlazoProceso).filter(PlazoProceso.id == plazo_id).first()
    if not plazo:
        raise HTTPException(status_code=404, detail="Plazo no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(plazo, campo, valor)
    db.commit()
    db.refresh(plazo)
    return plazo


@router.delete("/plazos/{plazo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_plazo(
    plazo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plazo = db.query(PlazoProceso).filter(PlazoProceso.id == plazo_id).first()
    if not plazo:
        raise HTTPException(status_code=404, detail="Plazo no encontrado")
    db.delete(plazo)
    db.commit()


# ===========================================================================
# CHECKLIST DOCUMENTAL
# ===========================================================================

@router.get("/procesos/{proceso_id}/documentos", response_model=List[ChecklistDocumentalRespuesta])
def listar_documentos(
    proceso_id: int,
    estado: Optional[str] = Query(None, pattern="^(PENDIENTE|PRESENTADO|APROBADO|RECHAZADO)$"),
    etapa: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(ChecklistDocumental).filter(ChecklistDocumental.proceso_id == proceso_id)
    if estado:
        query = query.filter(ChecklistDocumental.estado == estado)
    if etapa:
        query = query.filter(ChecklistDocumental.etapa == etapa)
    return query.order_by(ChecklistDocumental.etapa, ChecklistDocumental.nombre_documento).all()


@router.post("/procesos/{proceso_id}/documentos", response_model=ChecklistDocumentalRespuesta, status_code=status.HTTP_201_CREATED)
def crear_documento(
    proceso_id: int,
    datos: ChecklistDocumentalCrear,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if datos.proceso_id != proceso_id:
        raise HTTPException(status_code=400, detail="proceso_id no coincide con el de la URL")
    proceso = db.query(ProcesoCompra).filter(ProcesoCompra.id == proceso_id).first()
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    doc = ChecklistDocumental(**datos.model_dump())
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.patch("/documentos/{doc_id}", response_model=ChecklistDocumentalRespuesta)
def actualizar_documento(
    doc_id: int,
    datos: ChecklistDocumentalActualizar,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doc = db.query(ChecklistDocumental).filter(ChecklistDocumental.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(doc, campo, valor)
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/documentos/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_documento(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doc = db.query(ChecklistDocumental).filter(ChecklistDocumental.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    db.delete(doc)
    db.commit()


# ===========================================================================
# DASHBOARD
# ===========================================================================

@router.get("/dashboard", response_model=DashboardRespuesta)
def obtener_dashboard(
    anio: Optional[int] = Query(None, description="Filtrar por año"),
    carpeta_anual_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """KPIs y estadísticas del módulo de compras públicas."""
    query_base = db.query(ProcesoCompra)
    if anio is not None:
        query_base = query_base.join(CarpetaAnual).filter(CarpetaAnual.anio == anio)
    if carpeta_anual_id is not None:
        query_base = query_base.filter(ProcesoCompra.carpeta_anual_id == carpeta_anual_id)

    total = query_base.count()
    activos = query_base.filter(ProcesoCompra.estado == "ACTIVO").count()
    finalizados = query_base.filter(ProcesoCompra.estado == "FINALIZADO").count()
    anulados = query_base.filter(ProcesoCompra.estado == "ANULADO").count()

    presupuesto_total = db.query(func.coalesce(func.sum(ProcesoCompra.presupuesto_referencial), 0))
    monto_adj = db.query(func.coalesce(func.sum(ProcesoCompra.monto_adjudicado), 0))
    if anio is not None:
        presupuesto_total = presupuesto_total.join(CarpetaAnual).filter(CarpetaAnual.anio == anio)
        monto_adj = monto_adj.join(CarpetaAnual).filter(CarpetaAnual.anio == anio)

    presupuesto_total_val = Decimal(str(presupuesto_total.scalar() or 0))
    monto_adj_val = Decimal(str(monto_adj.scalar() or 0))
    pct_ejecucion = float((monto_adj_val / presupuesto_total_val * 100) if presupuesto_total_val > 0 else 0)

    # Procesos con retraso (dias_retraso > 0)
    con_retraso = (
        db.query(func.count(SeguimientoProceso.id))
        .filter(SeguimientoProceso.dias_retraso > 0)
        .scalar()
        or 0
    )

    # Distribución por etapa
    etapas = (
        db.query(ProcesoCompra.etapa_actual, func.count(ProcesoCompra.id).label("cantidad"))
        .filter(ProcesoCompra.estado == "ACTIVO")
        .group_by(ProcesoCompra.etapa_actual)
        .all()
    )
    procesos_por_etapa = [{"etapa": e.etapa_actual or "SIN_ETAPA", "cantidad": e.cantidad} for e in etapas]

    # Distribución por tipo
    tipos = (
        db.query(ProcesoCompra.tipo_contratacion, func.count(ProcesoCompra.id).label("cantidad"))
        .group_by(ProcesoCompra.tipo_contratacion)
        .limit(10)
        .all()
    )
    procesos_por_tipo = [{"tipo": t.tipo_contratacion, "cantidad": t.cantidad} for t in tipos]

    # Semáforo plazos
    todos_plazos = db.query(PlazoProceso).all()
    verde = len([p for p in todos_plazos if p.dias_atraso == 0])
    amarillo = len([p for p in todos_plazos if 0 < p.dias_atraso <= 7])
    rojo = len([p for p in todos_plazos if p.dias_atraso > 7])

    return DashboardRespuesta(
        kpis=DashboardKPIs(
            total_procesos=total,
            procesos_activos=activos,
            procesos_finalizados=finalizados,
            procesos_anulados=anulados,
            presupuesto_total=presupuesto_total_val,
            monto_adjudicado_total=monto_adj_val,
            porcentaje_ejecucion=round(pct_ejecucion, 2),
            procesos_con_retraso=con_retraso,
        ),
        procesos_por_etapa=procesos_por_etapa,
        procesos_por_tipo=procesos_por_tipo,
        semaforo_plazos={"verde": verde, "amarillo": amarillo, "rojo": rojo},
    )
