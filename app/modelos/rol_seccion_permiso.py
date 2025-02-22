from sqlalchemy import Column, Integer, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.base import Base

class RolSeccionPermiso(Base):
    __tablename__ = "rol_seccion_permiso"
    __table_args__ = {'schema': 'autenticacion'}

    rol_seccion_permiso_id = Column(Integer, primary_key=True, autoincrement=True)
    rol_id = Column(Integer, ForeignKey("autenticacion.roles.rol_id", ondelete="CASCADE"), nullable=False)
    seccion_id = Column(Integer, ForeignKey("autenticacion.secciones.seccion_id", ondelete="CASCADE"), nullable=False)
    permiso_id = Column(Integer, ForeignKey("autenticacion.permisos.permiso_id", ondelete="CASCADE"), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
