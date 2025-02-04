from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioCrear(BaseModel):
    nombre_usuario: str
    contrasena: str
    nombres_completos: str
    apellidos_completos: str
    email: EmailStr
    telefono: Optional[str] = None

class UsuarioActualizar(BaseModel):
    nombre_usuario: Optional[str] = None
    contrasena: Optional[str] = None
    nombres_completos: Optional[str] = None
    apellidos_completos: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

class UsuarioActualizarEstado(BaseModel):
    estado: bool

class UsuarioRespuesta(BaseModel):
    usuario_id: int
    nombre_usuario: str
    nombres_completos: str
    apellidos_completos: str
    email: str
    telefono: Optional[str]
    fecha_creacion: str
    estado: bool

    class Config:
        from_attributes = True
