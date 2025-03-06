from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base

class DispositivoSistemaOperativo(Base):
    __tablename__ = 'dispositivo_sistema_operativo'
    __table_args__ = {'schema': 'gestion_dispositivos'}

    dispositivo_so_id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('gestion_dispositivos.dispositivos.dispositivo_id'), nullable=False)
    sistema_operativo_id = Column(Integer, ForeignKey('gestion_dispositivos.sistemas_operativos.sistema_operativo_id'), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)

   
    dispositivo = relationship("Dispositivo", back_populates="sistema_operativo_relacion")

   
    sistema_operativo = relationship("SistemaOperativo", back_populates="dispositivos_relacion")
