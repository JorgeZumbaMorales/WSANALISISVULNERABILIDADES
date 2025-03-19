from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base  

class DetallesEscaneoFrecuencia(Base):
    __tablename__ = "detalles_escaneo_frecuencia"
    __table_args__ = {"schema": "configuracion"}

    frecuencia_id = Column(Integer, primary_key=True, autoincrement=True)
    configuracion_escaneo_id = Column(Integer, ForeignKey("configuracion.configuracion_escaneo.configuracion_escaneo_id", ondelete="CASCADE"), nullable=False)
    frecuencia_minutos = Column(Integer, nullable=False)
    fecha_inicio = Column(TIMESTAMP, nullable=False)
    fecha_fin = Column(TIMESTAMP, nullable=True)  # Opcional
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relación con Configuración de Escaneo
    configuracion = relationship("ConfiguracionEscaneo", back_populates="detalles_frecuencia", lazy="joined")
