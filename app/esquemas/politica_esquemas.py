from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Esquema para crear una política
class PoliticaCrear(BaseModel):
    nombre_politica: str = Field(..., example="Política de Seguridad")
    descripcion: Optional[str] = Field(None, example="Política de seguridad para la red")

# Esquema para actualizar una política
class PoliticaActualizar(BaseModel):
    nombre_politica: Optional[str] = Field(None, example="Política de Seguridad Actualizada")
    descripcion: Optional[str] = Field(None, example="Descripción actualizada de la política")

# Esquema para cambiar el estado de una política
class PoliticaActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

# Esquema para mostrar una política
class PoliticaMostrar(BaseModel):
    politica_id: int
    nombre_politica: str
    descripcion: Optional[str]
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
