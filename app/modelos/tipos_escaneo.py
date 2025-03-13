from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.core.base import Base

class TipoEscaneo(Base):
    __tablename__ = "tipos_escaneo"
    __table_args__ = {"schema": "configuracion"}

    tipo_escaneo_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo = Column(String(20), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
