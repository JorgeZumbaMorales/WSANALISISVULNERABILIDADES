from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Esquema para crear una asociación entre política y regla
class PoliticaReglaCrear(BaseModel):
    politica_id: int = Field(..., example=1)
    regla_id: int = Field(..., example=2)

# Esquema para actualizar una asociación entre política y regla
class PoliticaReglaActualizar(BaseModel):
    politica_id: Optional[int] = Field(None, example=1)
    regla_id: Optional[int] = Field(None, example=2)

# Esquema para cambiar el estado de una asociación
class PoliticaReglaActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

# Esquema para mostrar una asociación entre política y regla
class PoliticaReglaMostrar(BaseModel):
    politica_regla_id: int
    politica_id: int
    regla_id: int
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
