from sqlalchemy import Column, Integer, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.base import Base

class DispositivoCategoria(Base):
    __tablename__ = 'dispositivo_categoria'
    __table_args__ = {'schema': 'gestion_dispositivos'}

    dispositivo_categoria_id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('gestion_dispositivos.dispositivos.dispositivo_id'), nullable=False)
    categoria_id = Column(Integer, ForeignKey('gestion_dispositivos.categorias.categoria_id'), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
