"""
Rutas FastAPI — Módulo Presupuesto
Prefijo: /api/presupuesto
"""
from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api import deps
from app.models.user import User
from app.models.presupuesto import (
    PartidaPresupuestaria,
    PresupuestoAnual,
    AsignacionPresupuestaria,
    ReformaPresupuestaria,
    CertificadoPresupuestario,
    Compromiso,
    Devengado,
)
from app.schemas.presupuesto import (
    PartidaPresupuestariaCrear,
    PartidaPresupuestariaActualizar,
    PartidaPresupuestariaRespuesta,
    PresupuestoAnualCrear,
    PresupuestoAnualActualizar,
    PresupuestoAnualRespuesta,
    AsignacionPresupuestariaCrear,
    AsignacionPresupuestariaRespuesta,
    ReformaPresupuestariaCrear,
    ReformaPresupuestariaRespuesta,
    CertificadoPresupuestariaCrear,
    CertificadoPresupuestariaEstado,
    CertificadoPresupuestariaRespuesta,
    CompromisoCrear,
    CompromisoRespuesta,
    DevengadoCrear,
    DevengadoRespuesta,
    EjecucionPresupuestariaRespuesta,
)

router = APIRouter()


# ===========================================================================
# PARTIDAS PRESUPUESTARIAS
# ===========================================================================

@router.get("/partidas", response_model=List[PartidaPresupuestariaRespuesta], tags=["Presupuesto"])
def listar_partidas(
    tipo: Optional[str] = Query(None, description="INGRESO o GASTO"),
    solo_hojas: bool = Query(False),
    db: Session = Depends(deps.get_db),
):
    q = db.query(PartidaPresupuestaria)
    if tipo:
        q = q.filter(PartidaPresupuestaria.tipo == tipo)
    if solo_hojas:
        q = q.filter(PartidaPresupuestaria.es_hoja == True)
    return q.order_by(PartidaPresupuestaria.codigo).all()


@router.post("/partidas", response_model=PartidaPresupuestariaRespuesta, status_code=201, tags=["Presupuesto"])
def crear_partida(req: PartidaPresupuestariaCrear, db: Session = Depends(deps.get_db), _: User = Depends(deps.get_current_user)):
    if db.query(PartidaPresupuestaria).filter_by(codigo=req.codigo).first():
        raise HTTPException(status_code=400, detail=f"Partida con código {req.codigo} ya existe")
    obj = PartidaPresupuestaria(**req.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/partidas/{partida_id}", response_model=PartidaPresupuestariaRespuesta, tags=["Presupuesto"])
def obtener_partida(partida_id: int, db: Session = Depends(deps.get_db)):
    obj = db.query(PartidaPresupuestaria).get(partida_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    return obj


@router.put("/partidas/{partida_id}", response_model=PartidaPresupuestariaRespuesta, tags=["Presupuesto"])
def actualizar_partida(
    partida_id: int, req: PartidaPresupuestariaActualizar, db: Session = Depends(deps.get_db), _: User = Depends(deps.get_current_user)
):
    obj = db.query(PartidaPresupuestaria).get(partida_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    for k, v in req.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


# ===========================================================================
# PRESUPUESTO ANUAL
# ===========================================================================

@router.get("/presupuestos", response_model=List[PresupuestoAnualRespuesta], tags=["Presupuesto"])
def listar_presupuestos(
    anio: Optional[int] = Query(None),
    estado: Optional[str] = Query(None),
    db: Session = Depends(deps.get_db),
):
    q = db.query(PresupuestoAnual)
    if anio:
        q = q.filter(PresupuestoAnual.anio_fiscal == anio)
    if estado:
        q = q.filter(PresupuestoAnual.estado == estado)
    return q.order_by(PresupuestoAnual.anio_fiscal.desc()).all()


@router.post("/presupuestos", response_model=PresupuestoAnualRespuesta, status_code=201, tags=["Presupuesto"])
def crear_presupuesto(req: PresupuestoAnualCrear, db: Session = Depends(deps.get_db), _: User = Depends(deps.get_current_user)):
    existente = db.query(PresupuestoAnual).filter(
        PresupuestoAnual.anio_fiscal == req.anio_fiscal,
        PresupuestoAnual.estado == "APROBADO"
    ).first()
    if existente:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un presupuesto APROBADO para {req.anio_fiscal}"
        )
    obj = PresupuestoAnual(
        **req.model_dump(),
        monto_codificado=req.monto_inicial,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/presupuestos/{presupuesto_id}", response_model=PresupuestoAnualRespuesta, tags=["Presupuesto"])
def obtener_presupuesto(presupuesto_id: int, db: Session = Depends(deps.get_db)):
    obj = db.query(PresupuestoAnual).get(presupuesto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return obj


@router.patch("/presupuestos/{presupuesto_id}", response_model=PresupuestoAnualRespuesta, tags=["Presupuesto"])
def actualizar_presupuesto(
    presupuesto_id: int, req: PresupuestoAnualActualizar, db: Session = Depends(deps.get_db), _: User = Depends(deps.get_current_user)
):
    obj = db.query(PresupuestoAnual).get(presupuesto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    if obj.estado == "CERRADO":
        raise HTTPException(status_code=400, detail="No se puede modificar un presupuesto CERRADO")
    for k, v in req.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


# ===========================================================================
# ASIGNACIONES PRESUPUESTARIAS
# ===========================================================================

@router.get(
    "/presupuestos/{presupuesto_id}/asignaciones",
    response_model=List[AsignacionPresupuestariaRespuesta],
    tags=["Presupuesto"],
)
def listar_asignaciones(presupuesto_id: int, db: Session = Depends(deps.get_db)):
    return (
        db.query(AsignacionPresupuestaria)
        .filter_by(id_presupuesto=presupuesto_id)
        .all()
    )


@router.post(
    "/asignaciones",
    response_model=AsignacionPresupuestariaRespuesta,
    status_code=201,
    tags=["Presupuesto"],
)
def crear_asignacion(req: AsignacionPresupuestariaCrear, db: Session = Depends(deps.get_db), _: User = Depends(deps.get_current_user)):
    existente = db.query(AsignacionPresupuestaria).filter_by(
        id_presupuesto=req.id_presupuesto, id_partida=req.id_partida
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Esta partida ya está asignada a ese presupuesto")
    obj = AsignacionPresupuestaria(
        **req.model_dump(),
        monto_codificado=req.monto_inicial,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.post(
    "/asignaciones/{asignacion_id}/reformas",
    response_model=ReformaPresupuestariaRespuesta,
    status_code=201,
    tags=["Presupuesto"],
)
def crear_reforma(
    asignacion_id: int, req: ReformaPresupuestariaCrear, db: Session = Depends(deps.get_db), _: User = Depends(deps.get_current_user)
):
    asig = db.query(AsignacionPresupuestaria).get(asignacion_id)
    if not asig:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    reforma = ReformaPresupuestaria(**req.model_dump())
    asig.monto_codificado = Decimal(str(asig.monto_codificado)) + Decimal(str(req.monto))
    db.add(reforma)
    db.commit()
    db.refresh(reforma)
    return reforma


# ===========================================================================
# CERTIFICADOS PRESUPUESTARIOS
# ===========================================================================

def _generar_numero_certificado(db: Session, anio: int) -> str:
    """Genera número secuencial: CERT-YYYY-NNNNN"""
    total = (
        db.query(CertificadoPresupuestario)
        .join(AsignacionPresupuestaria)
        .join(PresupuestoAnual)
        .filter(PresupuestoAnual.anio_fiscal == anio)
        .count()
    )
    return f"CERT-{anio}-{total + 1:05d}"


@router.get("/certificados", response_model=List[CertificadoPresupuestariaRespuesta], tags=["Presupuesto"])
def listar_certificados(
    estado: Optional[str] = Query(None),
    anio: Optional[int] = Query(None),
    db: Session = Depends(deps.get_db),
):
    q = db.query(CertificadoPresupuestario)
    if estado:
        q = q.filter(CertificadoPresupuestario.estado == estado)
    if anio:
        q = (
            q.join(AsignacionPresupuestaria)
            .join(PresupuestoAnual)
            .filter(PresupuestoAnual.anio_fiscal == anio)
        )
    return q.order_by(CertificadoPresupuestario.id_certificado.desc()).all()


@router.post(
    "/certificados", response_model=CertificadoPresupuestariaRespuesta, status_code=201, tags=["Presupuesto"]
)
def crear_certificado(req: CertificadoPresupuestariaCrear, db: Session = Depends(deps.get_db), _: User = Depends(deps.get_current_user)):
    asig = db.query(AsignacionPresupuestaria).get(req.id_asignacion)
    if not asig:
        raise HTTPException(status_code=404, detail="Asignación presupuestaria no encontrada")

    saldo = Decimal(str(asig.monto_codificado)) - Decimal(str(asig.monto_comprometido))
    if req.monto_certificado > saldo:
        raise HTTPException(
            status_code=400,
            detail=f"Saldo insuficiente. Disponible: {saldo}, Solicitado: {req.monto_certificado}",
        )

    anio = db.query(PresupuestoAnual.anio_fiscal).filter(
        PresupuestoAnual.id_presupuesto == asig.id_presupuesto
    ).scalar()

    obj = CertificadoPresupuestario(
        **req.model_dump(),
        numero_certificado=_generar_numero_certificado(db, anio),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get(
    "/certificados/{cert_id}", response_model=CertificadoPresupuestariaRespuesta, tags=["Presupuesto"]
)
def obtener_certificado(cert_id: int, db: Session = Depends(deps.get_db)):
    obj = db.query(CertificadoPresupuestario).get(cert_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")
    return obj


@router.patch(
    "/certificados/{cert_id}/estado",
    response_model=CertificadoPresupuestariaRespuesta,
    tags=["Presupuesto"],
)
def cambiar_estado_certificado(
    cert_id: int, req: CertificadoPresupuestariaEstado, db: Session = Depends(deps.get_db), _: User = Depends(deps.get_current_user)
):
    obj = db.query(CertificadoPresupuestario).get(cert_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")
    if obj.estado in ("ANULADO", "LIQUIDADO"):
        raise HTTPException(status_code=400, detail=f"El certificado está en estado {obj.estado}, no modificable")
    obj.estado = req.estado
    if req.motivo_anulacion:
        obj.motivo_anulacion = req.motivo_anulacion
    if req.estado == "APROBADO":
        from datetime import date
        obj.fecha_certificacion = date.today()
    db.commit()
    db.refresh(obj)
    return obj


# ===========================================================================
# COMPROMISOS
# ===========================================================================

@router.get("/compromisos", response_model=List[CompromisoRespuesta], tags=["Presupuesto"])
def listar_compromisos(
    estado: Optional[str] = Query(None),
    db: Session = Depends(deps.get_db),
):
    q = db.query(Compromiso)
    if estado:
        q = q.filter(Compromiso.estado == estado)
    return q.order_by(Compromiso.id_compromiso.desc()).all()


@router.post("/compromisos", response_model=CompromisoRespuesta, status_code=201, tags=["Presupuesto"])
def crear_compromiso(req: CompromisoCrear, db: Session = Depends(deps.get_db), _: User = Depends(deps.get_current_user)):
    cert = db.query(CertificadoPresupuestario).get(req.id_certificado)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")
    if cert.estado != "APROBADO":
        raise HTTPException(
            status_code=400,
            detail="RN-03: El certificado debe estar APROBADO para crear un compromiso"
        )
    # Verificar que no exceda el monto del certificado
    comprometido_prev = sum(
        c.monto_comprometido
        for c in db.query(Compromiso).filter(
            Compromiso.id_certificado == req.id_certificado,
            Compromiso.estado != "ANULADO"
        ).all()
    )
    disponible = Decimal(str(cert.monto_certificado)) - Decimal(str(comprometido_prev))
    if req.monto_comprometido > disponible:
        raise HTTPException(
            status_code=400,
            detail=f"RN-PRES-02: Monto supera saldo del certificado. Disponible: {disponible}"
        )
    obj = Compromiso(**req.model_dump())
    # Actualizar monto comprometido en asignación
    asig = cert.asignacion
    asig.monto_comprometido = Decimal(str(asig.monto_comprometido)) + req.monto_comprometido
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/compromisos/{comp_id}/anular", response_model=CompromisoRespuesta, tags=["Presupuesto"])
def anular_compromiso(comp_id: int, motivo: str = Query(...), db: Session = Depends(deps.get_db), _: User = Depends(deps.get_current_user)):
    obj = db.query(Compromiso).get(comp_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Compromiso no encontrado")
    if obj.estado == "ANULADO":
        raise HTTPException(status_code=400, detail="Ya está anulado")
    obj.estado = "ANULADO"
    obj.motivo_anulacion = motivo
    # Liberar monto en asignación
    cert = obj.certificado
    asig = cert.asignacion
    asig.monto_comprometido = max(
        Decimal("0"),
        Decimal(str(asig.monto_comprometido)) - Decimal(str(obj.monto_comprometido))
    )
    db.commit()
    db.refresh(obj)
    return obj


# ===========================================================================
# DEVENGADOS
# ===========================================================================

@router.get("/devengados", response_model=List[DevengadoRespuesta], tags=["Presupuesto"])
def listar_devengados(
    estado: Optional[str] = Query(None),
    db: Session = Depends(deps.get_db),
):
    q = db.query(Devengado)
    if estado:
        q = q.filter(Devengado.estado == estado)
    return q.order_by(Devengado.id_devengado.desc()).all()


@router.post("/devengados", response_model=DevengadoRespuesta, status_code=201, tags=["Presupuesto"])
def crear_devengado(req: DevengadoCrear, db: Session = Depends(deps.get_db), _: User = Depends(deps.get_current_user)):
    comp = db.query(Compromiso).get(req.id_compromiso)
    if not comp:
        raise HTTPException(status_code=404, detail="Compromiso no encontrado")
    if comp.estado not in ("ACTIVO",):
        raise HTTPException(status_code=400, detail="El compromiso debe estar ACTIVO")

    # RN-PRES-04: validar que monto_devengado no supere el saldo disponible del compromiso
    devengado_previo = db.query(func.coalesce(func.sum(Devengado.monto_devengado), Decimal("0"))).filter(
        Devengado.id_compromiso == comp.id_compromiso,
        Devengado.estado != "ANULADO",
    ).scalar()
    saldo_compromiso = Decimal(str(comp.monto_comprometido)) - Decimal(str(devengado_previo))
    if Decimal(str(req.monto_devengado)) > saldo_compromiso:
        raise HTTPException(
            status_code=400,
            detail=(
                f"RN-PRES-04: Monto devengado ({req.monto_devengado}) supera el saldo disponible "
                f"del compromiso ({saldo_compromiso}). Sobregiro presupuestario no permitido."
            ),
        )

    obj = Devengado(**req.model_dump())
    comp.estado = "DEVENGADO"
    # Actualizar asignación
    cert = comp.certificado
    asig = cert.asignacion
    asig.monto_devengado = Decimal(str(asig.monto_devengado)) + req.monto_devengado
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ===========================================================================
# EJECUCIÓN PRESUPUESTARIA (REPORTE)
# ===========================================================================

@router.get(
    "/ejecucion/{anio_fiscal}",
    response_model=List[EjecucionPresupuestariaRespuesta],
    tags=["Presupuesto"],
)
def reporte_ejecucion(anio_fiscal: int, db: Session = Depends(deps.get_db)):
    rows = (
        db.query(
            PresupuestoAnual.anio_fiscal,
            PartidaPresupuestaria.codigo.label("codigo_partida"),
            PartidaPresupuestaria.nombre.label("nombre_partida"),
            AsignacionPresupuestaria.monto_inicial,
            AsignacionPresupuestaria.monto_codificado,
            AsignacionPresupuestaria.monto_comprometido,
            AsignacionPresupuestaria.monto_devengado,
            AsignacionPresupuestaria.monto_pagado,
        )
        .join(AsignacionPresupuestaria, PresupuestoAnual.id_presupuesto == AsignacionPresupuestaria.id_presupuesto)
        .join(PartidaPresupuestaria, AsignacionPresupuestaria.id_partida == PartidaPresupuestaria.id_partida)
        .filter(PresupuestoAnual.anio_fiscal == anio_fiscal)
        .order_by(PartidaPresupuestaria.codigo)
        .all()
    )

    result = []
    for r in rows:
        codificado = Decimal(str(r.monto_codificado))
        devengado = Decimal(str(r.monto_devengado))
        saldo = codificado - Decimal(str(r.monto_comprometido))
        porcentaje = (devengado / codificado * 100) if codificado > 0 else Decimal("0")
        result.append(
            EjecucionPresupuestariaRespuesta(
                anio_fiscal=r.anio_fiscal,
                codigo_partida=r.codigo_partida,
                nombre_partida=r.nombre_partida,
                monto_inicial=Decimal(str(r.monto_inicial)),
                monto_codificado=codificado,
                monto_comprometido=Decimal(str(r.monto_comprometido)),
                monto_devengado=devengado,
                monto_pagado=Decimal(str(r.monto_pagado)),
                saldo_disponible=saldo,
                porcentaje_ejecucion=round(porcentaje, 2),
            )
        )
    return result
