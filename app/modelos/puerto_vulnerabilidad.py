from sqlalchemy import Column, Integer, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.core.base import Base
from sqlalchemy.orm import relationship
class PuertoVulnerabilidad(Base):
    __tablename__ = "puerto_vulnerabilidad"
    __table_args__ = {"schema": "analisis_vulnerabilidades"}

    puerto_vuln_id = Column(Integer, primary_key=True, autoincrement=True)
    puerto_id = Column(Integer, ForeignKey('analisis_vulnerabilidades.puertos_abiertos.puerto_id', ondelete="CASCADE"), nullable=False)
    vulnerabilidad_id = Column(Integer, ForeignKey('analisis_vulnerabilidades.vulnerabilidades.vulnerabilidad_id', ondelete="CASCADE"), nullable=False)
    exploit = Column(Boolean)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    
    
    # Relación hacia PuertoAbierto
    puerto = relationship("PuertoAbierto", back_populates="vulnerabilidades")

    # Relación hacia Vulnerabilidad
    vulnerabilidad = relationship("Vulnerabilidad", back_populates="puertos_afectados")
