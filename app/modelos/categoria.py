from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.core.base import Base

class Categoria(Base):
    __tablename__ = 'categorias'
    __table_args__ = {'schema': 'gestion_dispositivos'}

    categoria_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_categoria = Column(String(50), nullable=False)
    descripcion = Column(String(255))
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
