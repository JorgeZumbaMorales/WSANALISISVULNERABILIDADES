from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Esquema para crear una notificación
class NotificacionCrear(BaseModel):
    mensaje_notificacion: str = Field(..., example="Vulnerabilidad crítica detectada")
    tipo_alerta_id: int
    canal_alerta_id: int
    usuario_id: int
    dispositivo_id: int
    vulnerabilidad_id: int

# Esquema para actualizar una notificación
class NotificacionActualizar(BaseModel):
    mensaje_notificacion: Optional[str] = Field(None, example="Nueva actualización de vulnerabilidad")
    fecha_envio: Optional[datetime]

# Esquema para mostrar una notificación
class NotificacionMostrar(BaseModel):
    notificacion_id: int
    mensaje_notificacion: str
    tipo_alerta_id: int
    canal_alerta_id: int
    usuario_id: int
    dispositivo_id: int
    vulnerabilidad_id: int
    fecha_creacion: datetime
    fecha_envio: Optional[datetime]
    estado: bool

    class Config:
        from_attributes = True
