from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.core.base import Base

class Permiso(Base):
    __tablename__ = 'permisos'
    __table_args__ = {'schema': 'autenticacion'}

    permiso_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_permiso = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
