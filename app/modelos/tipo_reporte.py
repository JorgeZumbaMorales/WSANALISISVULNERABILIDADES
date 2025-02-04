from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.core.base import Base

class TipoReporte(Base):
    __tablename__ = 'tipo_reportes'
    __table_args__ = {'schema': 'reportes'}

    tipo_reporte_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo_reporte = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
