from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey, Time, CheckConstraint
from sqlalchemy.sql import func
from app.core.base import Base

class ConfiguracionEscaneo(Base):
    __tablename__ = "configuracion_escaneo"
    __table_args__ = {"schema": "configuracion"}

    configuracion_escaneo_id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_escaneo_id = Column(Integer, ForeignKey("configuracion.tipos_escaneo.tipo_escaneo_id", ondelete="RESTRICT"), nullable=False)
    frecuencia_minutos = Column(Integer, CheckConstraint("frecuencia_minutos > 0"), nullable=True)
    hora_especifica = Column(Time, nullable=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
