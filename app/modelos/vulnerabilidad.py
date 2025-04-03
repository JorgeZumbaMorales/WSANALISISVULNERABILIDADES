from sqlalchemy import Column, Integer, String, Float, Text, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.core.base import Base
from sqlalchemy.orm import relationship

class Vulnerabilidad(Base):
    __tablename__ = "vulnerabilidades"
    __table_args__ = {"schema": "analisis_vulnerabilidades"}

    vulnerabilidad_id = Column(Integer, primary_key=True, autoincrement=True)
    cve_id = Column(String(50), unique=True, nullable=False)
    score = Column(Float)
    url = Column(Text)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    
    # Relación con PuertoVulnerabilidad
    puertos_afectados = relationship("PuertoVulnerabilidad", back_populates="vulnerabilidad", lazy="joined", cascade="all, delete-orphan", uselist=True)

