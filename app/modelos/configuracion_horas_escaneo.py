from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, Time, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base  

class ConfiguracionHorasEscaneo(Base):
    __tablename__ = "configuracion_horas_escaneo"
    __table_args__ = {"schema": "configuracion"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    configuracion_escaneo_id = Column(Integer, ForeignKey("configuracion.configuracion_escaneo.configuracion_escaneo_id", ondelete="CASCADE"), nullable=False)
    hora = Column(Time, nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relación con ConfiguracionEscaneo
    configuracion = relationship("ConfiguracionEscaneo", back_populates="horas_escaneo")
