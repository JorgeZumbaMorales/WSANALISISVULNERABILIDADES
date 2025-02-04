from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.core.base import Base

class Regla(Base):
    __tablename__ = 'reglas'
    __table_args__ = {'schema': 'configuracion'}

    regla_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_regla = Column(String(50), nullable=False)
    descripcion = Column(String(255))
    herramienta = Column(String(50), nullable=False)  # Ejemplo: 'nmap', 'tcpdump'
    parametros = Column(String(255))                  # Ejemplo: '-p 80,443'
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
