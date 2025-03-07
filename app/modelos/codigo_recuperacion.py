from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.core.base import Base

class CodigoRecuperacion(Base):
    __tablename__ = "codigos_recuperacion"
    __table_args__ = {"schema": "autenticacion"}  

    codigo_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("autenticacion.usuarios.usuario_id", ondelete="CASCADE"), unique=True, nullable=False)
    codigo_hash = Column(String(255), nullable=False)  # 🟢 CAMBIO AQUÍ
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_expiracion = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10))  

    usuario = relationship("Usuario")
