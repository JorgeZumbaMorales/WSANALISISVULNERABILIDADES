from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.base import Base

class Notificacion(Base):
    __tablename__ = 'notificaciones'
    __table_args__ = {'schema': 'alertas'}

    notificacion_id = Column(Integer, primary_key=True, autoincrement=True)
    mensaje_notificacion = Column(String(255), nullable=False)
    tipo_alerta_id = Column(Integer, ForeignKey('alertas.tipos_alerta.tipo_alerta_id'))
    canal_alerta_id = Column(Integer, ForeignKey('alertas.canales_alerta.canal_alerta_id'))
    usuario_id = Column(Integer, ForeignKey('autenticacion.usuarios.usuario_id'))
    dispositivo_id = Column(Integer, ForeignKey('gestion_dispositivos.dispositivos.dispositivo_id'))
    vulnerabilidad_id = Column(Integer, ForeignKey('analisis_vulnerabilidades.vulnerabilidades.vulnerabilidad_id'))
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_envio = Column(TIMESTAMP, nullable=True)
    estado = Column(Boolean, default=True)
