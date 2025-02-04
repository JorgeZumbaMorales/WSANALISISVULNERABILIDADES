from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.base import Base

class HistorialVulnerabilidad(Base):
    __tablename__ = 'historial_vulnerabilidades'
    __table_args__ = {'schema': 'analisis_vulnerabilidades'}

    historial_vulnerabilidad_id = Column(Integer, primary_key=True, autoincrement=True)
    vulnerabilidad_id = Column(Integer, ForeignKey('analisis_vulnerabilidades.vulnerabilidades.vulnerabilidad_id'), nullable=False)
    estado_anterior = Column(Boolean)
    estado_actual = Column(Boolean)
    fecha_cambio = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
