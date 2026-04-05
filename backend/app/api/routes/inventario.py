from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import List, Optional
from decimal import Decimal

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.inventario import (
    CuentaContableInventario, ArticuloInventario, Movimiento,
    MovimientoDetalle, Destino, Encargado, Proveedor, UnidadGestion
)
from app.schemas.inventario import (
    CuentaContableInventario as CuentaContableSchema,
    CuentaContableInventarioCrear,
    ArticuloInventario as ArticuloSchema,
    ArticuloInventarioCrear, ArticuloInventarioActualizar, ArticuloListado,
    Movimiento as MovimientoSchema,
    MovimientoCrear, MovimientoListado,
    MovimientoDetalle as MovimientoDetalleSchema,
    MovimientoDetalleCrear,
    Destino as DestinoSchema, DestinoCrear, DestinoActualizar,
    Encargado as EncargadoSchema, EncargadoCrear, EncargadoActualizar,
    Proveedor as ProveedorSchema, ProveedorCrear, ProveedorActualizar,
    UnidadGestion as UnidadGestionSchema, UnidadGestionCrear,
    ResumenAnualInventario,
)

router = APIRouter(tags=["Inventario / Existencias"])


def _crear_schema(db: Session):
    """Crea el schema inventario si no existe (idempotente)."""
    db.execute(text("CREATE SCHEMA IF NOT EXISTS inventario"))
    db.commit()


# ══════════════════════════════════════════════════════
# HEALTH / RESUMEN
# ══════════════════════════════════════════════════════

@router.get("/resumen", summary="Resumen del módulo inventario por año fiscal")
def resumen_inventario(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    """Devuelve conteos por año fiscal (2021-2025)."""
    resultado = []
    for anno in range(2021, 2026):
        total_art = db.query(func.count(ArticuloInventario.id)).filter(
            ArticuloInventario.anno_fiscal == anno
        ).scalar() or 0
        total_mov = db.query(func.count(Movimiento.id)).filter(
            Movimiento.anno_fiscal == anno
        ).scalar() or 0
        total_klin = db.query(func.count(MovimientoDetalle.id)).filter(
            MovimientoDetalle.anno_fiscal == anno
        ).scalar() or 0
        valor = db.query(func.sum(ArticuloInventario.valor_total)).filter(
            ArticuloInventario.anno_fiscal == anno
        ).scalar()
        resultado.append(ResumenAnualInventario(
            anno_fiscal=anno,
            total_articulos=total_art,
            total_movimientos=total_mov,
            total_lineas_kardex=total_klin,
            valor_inventario_total=valor,
        ))
    return resultado


# ══════════════════════════════════════════════════════
# CUENTAS CONTABLES
# ══════════════════════════════════════════════════════

@router.get("/cuentas", response_model=List[CuentaContableSchema],
            summary="Listar cuentas contables de inventario")
def listar_cuentas(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    return db.query(CuentaContableInventario).order_by(
        CuentaContableInventario.codigo_cuenta
    ).all()


@router.post("/cuentas", response_model=CuentaContableSchema, status_code=201,
             summary="Crear cuenta contable")
def crear_cuenta(
    datos: CuentaContableInventarioCrear,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    _crear_schema(db)
    existente = db.query(CuentaContableInventario).filter(
        CuentaContableInventario.codigo_cuenta == datos.codigo_cuenta
    ).first()
    if existente:
        raise HTTPException(400, f"Cuenta {datos.codigo_cuenta} ya existe")
    obj = CuentaContableInventario(**datos.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ══════════════════════════════════════════════════════
# ARTÍCULOS
# ══════════════════════════════════════════════════════

@router.get("/articulos", response_model=List[ArticuloListado],
            summary="Listar artículos del inventario")
def listar_articulos(
    anno: Optional[int] = Query(None, ge=2021, le=2025, description="Filtrar por año fiscal"),
    activo: Optional[bool] = Query(None),
    buscar: Optional[str] = Query(None, description="Buscar por nombre o código"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    q = db.query(ArticuloInventario)
    if anno:
        q = q.filter(ArticuloInventario.anno_fiscal == anno)
    if activo is not None:
        q = q.filter(ArticuloInventario.activo == activo)
    if buscar:
        like = f"%{buscar}%"
        q = q.filter(
            ArticuloInventario.nombre.ilike(like) |
            ArticuloInventario.codigo_articulo.ilike(like)
        )
    return q.order_by(ArticuloInventario.codigo_articulo).offset(skip).limit(limit).all()


@router.get("/articulos/{articulo_id}", response_model=ArticuloSchema,
            summary="Obtener artículo por ID")
def obtener_articulo(
    articulo_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    obj = db.query(ArticuloInventario).filter(ArticuloInventario.id == articulo_id).first()
    if not obj:
        raise HTTPException(404, "Artículo no encontrado")
    return obj


@router.get("/articulos/codigo/{codigo}", response_model=ArticuloSchema,
            summary="Obtener artículo por código")
def obtener_articulo_por_codigo(
    codigo: str,
    anno: Optional[int] = Query(2025, ge=2021, le=2025),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    obj = db.query(ArticuloInventario).filter(
        ArticuloInventario.codigo_articulo == codigo,
        ArticuloInventario.anno_fiscal == anno
    ).first()
    if not obj:
        raise HTTPException(404, f"Artículo {codigo} no encontrado en año {anno}")
    return obj


@router.post("/articulos", response_model=ArticuloSchema, status_code=201,
             summary="Crear artículo")
def crear_articulo(
    datos: ArticuloInventarioCrear,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    _crear_schema(db)
    existente = db.query(ArticuloInventario).filter(
        ArticuloInventario.codigo_articulo == datos.codigo_articulo,
        ArticuloInventario.anno_fiscal == datos.anno_fiscal
    ).first()
    if existente:
        raise HTTPException(400, f"Artículo {datos.codigo_articulo} ya existe en año {datos.anno_fiscal}")
    obj = ArticuloInventario(**datos.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/articulos/{articulo_id}", response_model=ArticuloSchema,
              summary="Actualizar artículo")
def actualizar_articulo(
    articulo_id: int,
    datos: ArticuloInventarioActualizar,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    obj = db.query(ArticuloInventario).filter(ArticuloInventario.id == articulo_id).first()
    if not obj:
        raise HTTPException(404, "Artículo no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(obj, campo, valor)
    db.commit()
    db.refresh(obj)
    return obj


# ══════════════════════════════════════════════════════
# MOVIMIENTOS
# ══════════════════════════════════════════════════════

@router.get("/movimientos", response_model=List[MovimientoListado],
            summary="Listar movimientos de inventario")
def listar_movimientos(
    anno: Optional[int] = Query(None, ge=2021, le=2025),
    tipo: Optional[str] = Query(None, description="ENTRADA o SALIDA"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    from sqlalchemy.orm import joinedload
    q = db.query(Movimiento).options(
        joinedload(Movimiento.proveedor),
        joinedload(Movimiento.destino),
        joinedload(Movimiento.encargado),
    )
    if anno:
        q = q.filter(Movimiento.anno_fiscal == anno)
    if tipo:
        q = q.filter(Movimiento.tipo_movimiento == tipo.upper())
    movs = q.order_by(Movimiento.fecha.desc()).offset(skip).limit(limit).all()
    resultado = []
    for m in movs:
        resultado.append(MovimientoListado(
            id=m.id,
            numero_movimiento=m.numero_movimiento,
            fecha=m.fecha,
            tipo_movimiento=m.tipo_movimiento,
            costo_total=m.costo_total,
            observacion=m.observacion,
            anno_fiscal=m.anno_fiscal,
            proveedor=m.proveedor.nombre if m.proveedor else None,
            destino=m.destino.nombre if m.destino else None,
            encargado=m.encargado.nombre if m.encargado else None,
        ))
    return resultado


@router.get("/movimientos/{movimiento_id}", response_model=MovimientoSchema,
            summary="Obtener movimiento por ID")
def obtener_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    from sqlalchemy.orm import joinedload
    obj = db.query(Movimiento).options(
        joinedload(Movimiento.proveedor),
        joinedload(Movimiento.destino),
        joinedload(Movimiento.encargado),
    ).filter(Movimiento.id == movimiento_id).first()
    if not obj:
        raise HTTPException(404, "Movimiento no encontrado")
    return obj


@router.get("/movimientos/{movimiento_id}/detalle",
            response_model=List[MovimientoDetalleSchema],
            summary="Obtener líneas del kardex de un movimiento")
def obtener_detalle_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    from sqlalchemy.orm import joinedload
    detalles = db.query(MovimientoDetalle).options(
        joinedload(MovimientoDetalle.articulo)
    ).filter(MovimientoDetalle.id_movimiento == movimiento_id).all()
    return detalles


# ══════════════════════════════════════════════════════
# KARDEX POR ARTÍCULO
# ══════════════════════════════════════════════════════

@router.get("/kardex/{articulo_id}", response_model=List[MovimientoDetalleSchema],
            summary="Kardex de movimientos de un artículo")
def kardex_articulo(
    articulo_id: int,
    anno: Optional[int] = Query(None, ge=2021, le=2025),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    q = db.query(MovimientoDetalle).filter(
        MovimientoDetalle.id_articulo == articulo_id
    )
    if anno:
        q = q.filter(MovimientoDetalle.anno_fiscal == anno)
    return q.order_by(MovimientoDetalle.fecha.desc()).offset(skip).limit(limit).all()


# ══════════════════════════════════════════════════════
# MAESTROS: DESTINOS, ENCARGADOS, PROVEEDORES, UG
# ══════════════════════════════════════════════════════

@router.get("/destinos", response_model=List[DestinoSchema],
            summary="Listar destinos/áreas receptoras")
def listar_destinos(
    activo: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    q = db.query(Destino)
    if activo is not None:
        q = q.filter(Destino.activo == activo)
    return q.order_by(Destino.nombre).all()


@router.post("/destinos", response_model=DestinoSchema, status_code=201)
def crear_destino(
    datos: DestinoCrear,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    _crear_schema(db)
    obj = Destino(**datos.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/encargados", response_model=List[EncargadoSchema],
            summary="Listar encargados de bodega")
def listar_encargados(
    activo: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    q = db.query(Encargado)
    if activo is not None:
        q = q.filter(Encargado.activo == activo)
    return q.order_by(Encargado.nombre).all()


@router.post("/encargados", response_model=EncargadoSchema, status_code=201)
def crear_encargado(
    datos: EncargadoCrear,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    _crear_schema(db)
    obj = Encargado(**datos.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/proveedores", response_model=List[ProveedorSchema],
            summary="Listar proveedores de inventario")
def listar_proveedores(
    activo: Optional[bool] = Query(None),
    buscar: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    q = db.query(Proveedor)
    if activo is not None:
        q = q.filter(Proveedor.activo == activo)
    if buscar:
        q = q.filter(Proveedor.nombre.ilike(f"%{buscar}%"))
    return q.order_by(Proveedor.nombre).all()


@router.post("/proveedores", response_model=ProveedorSchema, status_code=201)
def crear_proveedor(
    datos: ProveedorCrear,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    _crear_schema(db)
    obj = Proveedor(**datos.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/unidades-gestion", response_model=List[UnidadGestionSchema],
            summary="Listar unidades de gestión / estructura funcional")
def listar_unidades_gestion(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    return db.query(UnidadGestion).order_by(UnidadGestion.codigo).all()
