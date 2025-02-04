from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RolPermisoCrear(BaseModel):
    rol_id: int
    permiso_id: int

class RolPermisoActualizar(BaseModel):
    rol_id: int
    permiso_id: int

class RolPermisoActualizarEstado(BaseModel):
    estado: bool

class RolPermisoRespuesta(BaseModel):
    rol_permiso_id: int
    rol_id: int
    permiso_id: int
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
