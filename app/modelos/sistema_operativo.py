from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base

class SistemaOperativo(Base):
    __tablename__ = 'sistemas_operativos'
    __table_args__ = {'schema': 'gestion_dispositivos'}

    sistema_operativo_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_so = Column(String(255), nullable=False, unique=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)

    # ✅ Relación con DispositivoSistemaOperativo (evitamos import circular usando string)
    dispositivos_relacion = relationship("DispositivoSistemaOperativo", back_populates="sistema_operativo")
