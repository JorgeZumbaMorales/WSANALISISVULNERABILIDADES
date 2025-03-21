from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.core.base import Base

class CanalAlerta(Base):
    __tablename__ = 'canales_alerta'
    __table_args__ = {'schema': 'alertas'}

    canal_alerta_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_canal = Column(String(50), unique=True, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
