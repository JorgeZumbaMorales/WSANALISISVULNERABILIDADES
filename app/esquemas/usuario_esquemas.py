from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioLogin(BaseModel):
    nombre_usuario: str = Field(..., min_length=4, max_length=50, example="admin")
    contrasena: str = Field(..., min_length=8, max_length=50, example="password123")
class UsuarioCrear(BaseModel):
    nombre_usuario: str = Field(..., min_length=4, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    contrasena: str = Field(..., min_length=8, max_length=50)
    nombres_completos: str = Field(..., min_length=2, max_length=100)
    apellidos_completos: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, pattern="^[0-9]{10,15}$")  # Solo números de 10 a 15 dígitos

class UsuarioActualizar(BaseModel):
    nombre_usuario: Optional[str] = Field(None, min_length=4, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    contrasena: Optional[str] = Field(None, min_length=8, max_length=50)
    nombres_completos: Optional[str] = Field(None, min_length=2, max_length=100)
    apellidos_completos: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, pattern="^[0-9]{10,15}$")

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
