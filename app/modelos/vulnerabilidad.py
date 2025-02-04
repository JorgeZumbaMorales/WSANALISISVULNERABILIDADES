from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.base import Base

class Vulnerabilidad(Base):
    __tablename__ = 'vulnerabilidades'
    __table_args__ = {'schema': 'analisis_vulnerabilidades'}

    vulnerabilidad_id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('gestion_dispositivos.dispositivos.dispositivo_id'), nullable=False)
    tipo = Column(String(50), nullable=False)
    severidad = Column(String(20))
    descripcion = Column(String(255))
    fecha_deteccion = Column(TIMESTAMP, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
