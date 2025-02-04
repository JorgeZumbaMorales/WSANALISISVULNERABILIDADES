from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.base import Base

class RolUsuario(Base):
    __tablename__ = 'rol_usuario'
    __table_args__ = {'schema': 'autenticacion'}

    rol_usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('autenticacion.usuarios.usuario_id'), nullable=False)
    rol_id = Column(Integer, ForeignKey('autenticacion.roles.rol_id'), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
