from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base  

class ConfiguracionEscaneo(Base):
    __tablename__ = "configuracion_escaneo"
    __table_args__ = {"schema": "configuracion"}

    configuracion_escaneo_id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_escaneo_id = Column(Integer, ForeignKey("configuracion.tipos_escaneo.tipo_escaneo_id", ondelete="RESTRICT"), nullable=False)
    estado = Column(Boolean, default=True)  
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())  

    # Relaciones
    tipo_escaneo = relationship("TipoEscaneo", back_populates="configuraciones", lazy="joined")
    detalles_frecuencia = relationship("DetallesEscaneoFrecuencia", back_populates="configuracion", cascade="all, delete-orphan", lazy="joined")
    detalles_hora = relationship("DetallesEscaneoHora", back_populates="configuracion", cascade="all, delete-orphan", lazy="joined")
