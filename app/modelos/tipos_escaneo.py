from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.core.base import Base  
from sqlalchemy.orm import relationship
class TiposEscaneo(Base):
    __tablename__ = "tipos_escaneo"
    __table_args__ = {"schema": "configuracion"}

    tipo_escaneo_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo = Column(String(20), unique=True, nullable=False)  # Ejemplo: "Frecuencia", "Hora específica"
    descripcion = Column(String(255), nullable=True)  # Explicación del tipo de escaneo
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relación con Configuración de Escaneo
    configuraciones = relationship("ConfiguracionEscaneo", back_populates="tipo_escaneo", lazy="joined")
