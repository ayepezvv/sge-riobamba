from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.db.base_class import Base
from app.models.mixins import AuditMixin

# =====================================================================
# 1. INFRAESTRUCTURA FISICA
# =====================================================================
class Predio(AuditMixin, Base):
    __tablename__ = "predios"

    id = Column(Integer, primary_key=True, index=True)
    clave_catastral = Column(String(50), unique=True, index=True, nullable=False)
    barrio_id = Column(Integer, ForeignKey("barrios.id", ondelete="SET NULL"), nullable=True)
    calle_principal_id = Column(Integer, ForeignKey("calles.id", ondelete="SET NULL"), nullable=True)
    calle_secundaria_id = Column(Integer, ForeignKey("calles.id", ondelete="SET NULL"), nullable=True)
    numero_casa = Column(String(50), nullable=True)
    foto_fachada = Column(String(255), nullable=True)
    croquis = Column(String(255), nullable=True)
    
    # Geometria (Puede ser un poligono del lote o un punto si no hay catastro exacto)
    geometria = Column(Geometry(geometry_type='GEOMETRY', srid=4326), nullable=True)

    # Relaciones
    acometidas = relationship("Acometida", back_populates="predio", cascade="all, delete-orphan")


class Acometida(AuditMixin, Base):
    __tablename__ = "acometidas"

    id = Column(Integer, primary_key=True, index=True)
    predio_id = Column(Integer, ForeignKey("predios.id", ondelete="CASCADE"), nullable=False)
    ruta_id = Column(Integer, ForeignKey("rutas.id", ondelete="RESTRICT"), nullable=True)
    diametro = Column(Float, nullable=True) # Ej: 0.5, 0.75 pulgadas
    material = Column(String(50), nullable=True) # Ej: PVC, Cobre
    
    geometria = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)

    # Relaciones
    predio = relationship("Predio", back_populates="acometidas")
    ruta = relationship("Ruta")
    cuentas = relationship("Cuenta", back_populates="acometida")


# =====================================================================
# 2. ENTIDAD CENTRAL DEL NEGOCIO
# =====================================================================
class Cuenta(AuditMixin, Base):
    __tablename__ = "cuentas"

    id = Column(Integer, primary_key=True, index=True)
    acometida_id = Column(Integer, ForeignKey("acometidas.id", ondelete="RESTRICT"), nullable=False)
    
    # Separacion de roles (Dualidad Ciudadano)
    propietario_id = Column(Integer, ForeignKey("ciudadanos.id", ondelete="RESTRICT"), nullable=False)
    responsable_pago_id = Column(Integer, ForeignKey("ciudadanos.id", ondelete="RESTRICT"), nullable=False)

    # Logistica
    secuencial_lectura = Column(Integer, nullable=True) # Vital para el orden de la ruta mensual
    
    # Estados
    estado = Column(String(20), nullable=False, default="Activa") # Activa, Inactiva, Cortada, Suspendida
    tiene_alcantarillado = Column(Boolean, default=True)

    # Relaciones
    acometida = relationship("Acometida", back_populates="cuentas")
    propietario = relationship("Ciudadano", foreign_keys=[propietario_id])
    responsable_pago = relationship("Ciudadano", foreign_keys=[responsable_pago_id])
    
    historial_medidores = relationship("HistorialMedidorCuenta", back_populates="cuenta")
    historial_tarifas = relationship("HistorialTarifaCuenta", back_populates="cuenta")


# =====================================================================
# 3. TRAZABILIDAD HISTORICA
# =====================================================================
class Medidor(AuditMixin, Base):
    __tablename__ = "medidores"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String(50), nullable=True)
    serie = Column(String(50), unique=True, index=True, nullable=False)
    esferas = Column(Integer, default=4) # Cuantos digitos tiene el reloj (4, 5, 6)

    # Relaciones
    historial = relationship("HistorialMedidorCuenta", back_populates="medidor")


class HistorialMedidorCuenta(AuditMixin, Base):
    __tablename__ = "historial_medidor_cuenta"

    id = Column(Integer, primary_key=True, index=True)
    cuenta_id = Column(Integer, ForeignKey("cuentas.id", ondelete="CASCADE"), nullable=False)
    medidor_id = Column(Integer, ForeignKey("medidores.id", ondelete="RESTRICT"), nullable=False)
    
    fecha_instalacion = Column(Date, nullable=False)
    fecha_retiro = Column(Date, nullable=True)
    
    lectura_inicial = Column(Integer, nullable=False, default=0)
    lectura_retiro = Column(Integer, nullable=True)

    # Relaciones
    cuenta = relationship("Cuenta", back_populates="historial_medidores")
    medidor = relationship("Medidor", back_populates="historial")


class HistorialTarifaCuenta(AuditMixin, Base):
    __tablename__ = "historial_tarifa_cuenta"

    id = Column(Integer, primary_key=True, index=True)
    cuenta_id = Column(Integer, ForeignKey("cuentas.id", ondelete="CASCADE"), nullable=False)
    
    tipo_tarifa = Column(String(50), nullable=False) # Residencial, Comercial, Industrial, etc.
    
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)

    # Relaciones
    cuenta = relationship("Cuenta", back_populates="historial_tarifas")

