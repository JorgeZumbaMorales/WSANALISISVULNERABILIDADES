from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base

class Dispositivo(Base):
    __tablename__ = 'dispositivos'
    __table_args__ = {'schema': 'gestion_dispositivos'}

    dispositivo_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_dispositivo = Column(String(100), nullable=True)
    mac_address = Column(String(50), nullable=False, unique=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)

   
    sistema_operativo_relacion = relationship("DispositivoSistemaOperativo", back_populates="dispositivo", lazy="joined")
    
    
    ips_relacion = relationship("IpAsignacion", back_populates="dispositivo", lazy="joined")
