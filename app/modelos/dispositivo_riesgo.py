from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base  

class DispositivoRiesgo(Base):
    __tablename__ = 'dispositivo_riesgo'
    __table_args__ = {'schema': 'analisis_vulnerabilidades'}

    dispositivo_riesgo_id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('gestion_dispositivos.dispositivos.dispositivo_id', ondelete="CASCADE"), nullable=False)
    riesgo_id = Column(Integer, ForeignKey('analisis_vulnerabilidades.riesgos.riesgo_id', ondelete="CASCADE"), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)

    # Relaciones
    dispositivo = relationship("Dispositivo", back_populates="riesgos_relacion", lazy="joined")
    riesgo = relationship("Riesgo", back_populates="dispositivo_riesgo_relacion", lazy="joined")
