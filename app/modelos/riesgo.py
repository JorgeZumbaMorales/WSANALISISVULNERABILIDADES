from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base  

class Riesgo(Base):
    __tablename__ = 'riesgos'
    __table_args__ = {'schema': 'gestion_dispositivos'}

    riesgo_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_riesgo = Column(String(20), unique=True, nullable=False)
    descripcion = Column(String, nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)

    # ✅ Relación con la tabla dispositivo_riesgo
    dispositivo_riesgo_relacion = relationship("DispositivoRiesgo", back_populates="riesgo")
