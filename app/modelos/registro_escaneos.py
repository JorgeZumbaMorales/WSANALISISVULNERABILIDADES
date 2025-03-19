from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base  

class RegistroEscaneos(Base):
    __tablename__ = "registro_escaneos"
    __table_args__ = {"schema": "configuracion"}

    registro_escaneo_id = Column(Integer, primary_key=True, autoincrement=True)
    configuracion_escaneo_id = Column(Integer, ForeignKey("configuracion.configuracion_escaneo.configuracion_escaneo_id", ondelete="CASCADE"), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)  # 📌 Solo mantenemos esta

    # Relaciones
    configuracion = relationship("ConfiguracionEscaneo", back_populates="registros_escaneos", lazy="joined")
