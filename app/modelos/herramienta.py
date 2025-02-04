from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.core.base import Base

class Herramienta(Base):
    __tablename__ = 'herramientas'
    __table_args__ = {'schema': 'configuracion'}

    herramienta_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_herramienta = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
