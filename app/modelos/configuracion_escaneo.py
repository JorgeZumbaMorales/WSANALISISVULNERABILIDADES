from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base  

class ConfiguracionEscaneo(Base):
    __tablename__ = "configuracion_escaneo"
    __table_args__ = {"schema": "configuracion"}

    configuracion_escaneo_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_configuracion_escaneo = Column(String(100), nullable=False, default="Configuración sin nombre")  
    tipo_escaneo_id = Column(Integer, ForeignKey("configuracion.tipos_escaneo.tipo_escaneo_id", ondelete="RESTRICT"), nullable=False)
    frecuencia_minutos = Column(Integer, nullable=True)
    fecha_inicio = Column(TIMESTAMP, nullable=False)
    fecha_fin = Column(TIMESTAMP, nullable=True)
    estado = Column(Boolean, default=False)  
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())  

    # Relaciones
    tipo_escaneo = relationship("TiposEscaneo", back_populates="configuraciones", lazy="joined")
    registros_escaneos = relationship("RegistroEscaneos", back_populates="configuracion", cascade="all, delete-orphan", lazy="joined")
    horas_escaneo = relationship("ConfiguracionHorasEscaneo", back_populates="configuracion", cascade="all, delete-orphan", lazy="joined")