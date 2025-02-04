from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RolUsuarioCrear(BaseModel):
    usuario_id: int
    rol_id: int

class RolUsuarioActualizar(BaseModel):
    usuario_id: int
    rol_id: int

class RolUsuarioActualizarEstado(BaseModel):
    estado: bool

class RolUsuarioRespuesta(BaseModel):
    rol_usuario_id: int
    usuario_id: int
    rol_id: int
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
