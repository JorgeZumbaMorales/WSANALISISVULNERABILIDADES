from pydantic import BaseModel, Field
from typing import Optional

class RecomendacionPuertoCrear(BaseModel):
    puerto_id: int = Field(..., example=1)
    recomendacion: str = Field(..., min_length=5, example="Se recomienda cerrar este puerto debido a vulnerabilidades conocidas.")

class RecomendacionPuertoActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

class RecomendacionPuertoRespuesta(BaseModel):
    recomendacion_id: int
    puerto_id: int
    recomendacion: str
    fecha_creacion: str
    estado: bool

    class Config:
        from_attributes = True
