from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.core.base import Base  

class Usuario(Base):
    __tablename__ = 'usuarios'
    __table_args__ = {'schema': 'autenticacion'}

    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    nombres_completos = Column(String(100), nullable=False)
    apellidos_completos = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20), unique=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Boolean, default=True)
