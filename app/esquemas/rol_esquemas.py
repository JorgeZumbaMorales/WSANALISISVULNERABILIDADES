# app/esquemas/rol_esquemas.py
from pydantic import BaseModel
from typing import Optional

class RolCrear(BaseModel):
    nombre_rol: str
    descripcion: Optional[str] = None

class RolActualizar(BaseModel):
    nombre_rol: str
    descripcion: Optional[str] = None

class RolActualizarEstado(BaseModel):
    estado: bool

class RolRespuesta(BaseModel):
    rol_id: int
    nombre_rol: str
    descripcion: Optional[str]
    fecha_creacion: str
    estado: bool

    class Config:
        from_attributes = True
