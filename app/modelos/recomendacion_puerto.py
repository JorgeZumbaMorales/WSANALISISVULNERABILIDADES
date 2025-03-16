from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base  

class RecomendacionPuerto(Base):
    __tablename__ = 'recomendaciones_puertos'
    __table_args__ = {'schema': 'analisis_vulnerabilidades'}

    recomendacion_id = Column(Integer, primary_key=True, autoincrement=True)
    puerto_id = Column(Integer, ForeignKey('analisis_vulnerabilidades.puertos_abiertos.puerto_id', ondelete="CASCADE"), nullable=False)
    recomendacion = Column(Text, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)

    # Relación con puertos abiertos
    puerto = relationship("PuertoAbierto", backref="recomendaciones_asociadas")
