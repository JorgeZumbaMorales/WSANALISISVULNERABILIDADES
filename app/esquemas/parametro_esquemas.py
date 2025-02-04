from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Esquema para crear un parámetro
class ParametroCrear(BaseModel):
    nombre_parametro: str = Field(..., example="--verbose")
    descripcion: Optional[str] = Field(None, example="Activa el modo detallado")

# Esquema para actualizar un parámetro
class ParametroActualizar(BaseModel):
    nombre_parametro: Optional[str] = Field(None, example="--quiet")
    descripcion: Optional[str] = Field(None, example="Desactiva el modo detallado")

# Esquema para cambiar el estado de un parámetro
class ParametroActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

# Esquema para mostrar un parámetro
class ParametroMostrar(BaseModel):
    parametro_id: int
    nombre_parametro: str
    descripcion: Optional[str]
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
