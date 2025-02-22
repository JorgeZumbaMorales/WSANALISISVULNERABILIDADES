from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.core.base import Base

class Seccion(Base):
    __tablename__ = 'secciones'
    __table_args__ = {'schema': 'autenticacion'}

    seccion_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_seccion = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))
    ruta = Column(String(100), unique=True, nullable=False)
    icono = Column(String(50))
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
