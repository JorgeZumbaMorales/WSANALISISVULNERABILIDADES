from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.base import Base  
from sqlalchemy.orm import relationship
class PuertoAbierto(Base):
    __tablename__ = 'puertos_abiertos'
    __table_args__ = {'schema': 'analisis_vulnerabilidades'}

    puerto_id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('gestion_dispositivos.dispositivos.dispositivo_id'), nullable=False)
    puerto = Column(Integer, nullable=False)
    protocolo = Column(String(10), nullable=False)
    servicio = Column(String(100), nullable=False)
    version = Column(String(100))
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    estado = Column(Boolean, default=True)

    recomendacion = relationship("RecomendacionPuerto", uselist=False, back_populates="puerto")