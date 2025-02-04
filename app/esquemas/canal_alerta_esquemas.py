from pydantic import BaseModel, Field
from datetime import datetime

# Esquema para crear un canal de alerta
class CanalAlertaCrear(BaseModel):
    nombre_canal: str = Field(..., example="Correo Electrónico")

# Esquema para actualizar un canal de alerta
class CanalAlertaActualizar(BaseModel):
    nombre_canal: str = Field(..., example="SMS")

# Esquema para mostrar un canal de alerta
class CanalAlertaMostrar(BaseModel):
    canal_alerta_id: int
    nombre_canal: str
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
