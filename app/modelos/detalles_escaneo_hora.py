from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, Time, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base  

class DetallesEscaneoHora(Base):
    __tablename__ = "detalles_escaneo_hora"
    __table_args__ = {"schema": "configuracion"}

    hora_id = Column(Integer, primary_key=True, autoincrement=True)
    configuracion_escaneo_id = Column(Integer, ForeignKey("configuracion.configuracion_escaneo.configuracion_escaneo_id", ondelete="CASCADE"), nullable=False)
    hora_especifica = Column(Time, nullable=False)  # Guarda la hora exacta del escaneo
    fecha_inicio = Column(TIMESTAMP, nullable=False)  # Desde cuándo empieza la configuración
    fecha_fin = Column(TIMESTAMP, nullable=True)  # Opcional: Hasta cuándo se repite el escaneo
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relación con Configuración de Escaneo
    configuracion = relationship("ConfiguracionEscaneo", back_populates="detalles_hora", lazy="joined")
