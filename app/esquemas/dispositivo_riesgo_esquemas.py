from pydantic import BaseModel, Field
from typing import Optional

class DispositivoRiesgoCrear(BaseModel):
    dispositivo_id: int = Field(..., example=1)
    riesgo_id: int = Field(..., example=2)

class DispositivoRiesgoActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

class DispositivoRiesgoRespuesta(BaseModel):
    dispositivo_riesgo_id: int
    dispositivo_id: int
    riesgo_id: int
    fecha_evaluacion: str
    estado: bool

    class Config:
        from_attributes = True
