from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base

class IpAsignacion(Base):
    __tablename__ = 'ip_asignaciones'
    __table_args__ = {'schema': 'gestion_dispositivos'}

    ip_asignacion_id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('gestion_dispositivos.dispositivos.dispositivo_id', ondelete="CASCADE"), nullable=False)
    ip_address = Column(String(50), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
