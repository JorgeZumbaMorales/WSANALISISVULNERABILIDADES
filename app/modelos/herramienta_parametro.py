from sqlalchemy import Column, Integer, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.base import Base

class HerramientaParametro(Base):
    __tablename__ = 'herramienta_parametro'
    __table_args__ = {'schema': 'configuracion'}

    herramienta_parametro_id = Column(Integer, primary_key=True, autoincrement=True)
    herramienta_id = Column(Integer, ForeignKey('configuracion.herramientas.herramienta_id'), nullable=False)
    parametro_id = Column(Integer, ForeignKey('configuracion.parametros.parametro_id'), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
