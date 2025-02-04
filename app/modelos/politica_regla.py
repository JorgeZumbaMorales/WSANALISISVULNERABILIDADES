from sqlalchemy import Column, Integer, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.base import Base

class PoliticaRegla(Base):
    __tablename__ = 'politica_regla'
    __table_args__ = {'schema': 'configuracion'}

    politica_regla_id = Column(Integer, primary_key=True, autoincrement=True)
    politica_id = Column(Integer, ForeignKey('configuracion.politicas.politica_id'), nullable=False)
    regla_id = Column(Integer, ForeignKey('configuracion.reglas.regla_id'), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
