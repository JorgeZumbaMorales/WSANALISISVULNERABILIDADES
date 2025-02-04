from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Esquema para crear una relación herramienta-parámetro
class HerramientaParametroCrear(BaseModel):
    herramienta_id: int = Field(..., example=1)
    parametro_id: int = Field(..., example=2)

# Esquema para actualizar una relación herramienta-parámetro
class HerramientaParametroActualizar(BaseModel):
    herramienta_id: Optional[int] = Field(None, example=1)
    parametro_id: Optional[int] = Field(None, example=2)

# Esquema para cambiar el estado de una relación herramienta-parámetro
class HerramientaParametroActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

# Esquema para mostrar una relación herramienta-parámetro
class HerramientaParametroMostrar(BaseModel):
    herramienta_parametro_id: int
    herramienta_id: int
    parametro_id: int
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
