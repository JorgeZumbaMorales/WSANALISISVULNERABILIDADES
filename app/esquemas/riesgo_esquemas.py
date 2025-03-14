from pydantic import BaseModel, Field
from typing import Optional

class RiesgoCrear(BaseModel):
    nombre_riesgo: str = Field(..., example="Alto")
    descripcion: Optional[str] = Field(None, example="Nivel de riesgo alto para un dispositivo.")

class RiesgoActualizar(BaseModel):
    descripcion: Optional[str] = Field(None, example="Nueva descripción actualizada.")

class RiesgoActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

class RiesgoRespuesta(BaseModel):
    riesgo_id: int
    nombre_riesgo: str
    descripcion: Optional[str]
    fecha_creacion: str
    estado: bool

    class Config:
        from_attributes = True
