from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.core.base import Base

class Parametro(Base):
    __tablename__ = 'parametros'
    __table_args__ = {'schema': 'configuracion'}

    parametro_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_parametro = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
