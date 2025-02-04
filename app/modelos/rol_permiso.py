from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.base import Base

class RolPermiso(Base):
    __tablename__ = 'rol_permiso'
    __table_args__ = {'schema': 'autenticacion'}

    rol_permiso_id = Column(Integer, primary_key=True, autoincrement=True)
    rol_id = Column(Integer, ForeignKey('autenticacion.roles.rol_id'), nullable=False)
    permiso_id = Column(Integer, ForeignKey('autenticacion.permisos.permiso_id'), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
