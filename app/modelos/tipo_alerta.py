from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.core.base import Base

class TipoAlerta(Base):
    __tablename__ = 'tipos_alerta'
    __table_args__ = {'schema': 'alertas'}

    tipo_alerta_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo = Column(String(50), unique=True, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
