from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.core.base import Base

class Politica(Base):
    __tablename__ = 'politicas'
    __table_args__ = {'schema': 'configuracion'}

    politica_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_politica = Column(String(50), nullable=False)
    descripcion = Column(String(255))
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
