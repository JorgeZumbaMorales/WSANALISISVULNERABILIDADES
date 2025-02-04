from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from app.core.base import Base

class ReporteGenerado(Base):
    __tablename__ = 'reportes_generados'
    __table_args__ = {'schema': 'reportes'}

    reporte_generado_id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_reporte_id = Column(Integer, ForeignKey('reportes.tipo_reportes.tipo_reporte_id'), nullable=False)
    nombre_reporte_generado = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    usuario_id = Column(Integer, ForeignKey('autenticacion.usuarios.usuario_id'))
    fecha_inicio = Column(TIMESTAMP, nullable=False)
    fecha_fin = Column(TIMESTAMP, nullable=False)
    contenido = Column(JSON)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
