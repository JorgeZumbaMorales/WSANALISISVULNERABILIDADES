from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.core.base import Base

class Dispositivo(Base):
    __tablename__ = 'dispositivos'
    __table_args__ = {'schema': 'gestion_dispositivos'}

    dispositivo_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_dispositivo = Column(String(100))
    ip_address = Column(String(50), nullable=False)
    sistema_operativo = Column(String(50))
    tipo = Column(String(50))
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
