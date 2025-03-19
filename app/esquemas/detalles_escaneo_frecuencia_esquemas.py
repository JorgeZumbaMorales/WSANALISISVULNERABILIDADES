from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DetallesEscaneoFrecuenciaCrear(BaseModel):
    configuracion_escaneo_id: int = Field(..., example=1)
    frecuencia_minutos: int = Field(..., gt=0, example=30)
    fecha_inicio: datetime = Field(..., example="2024-03-18T12:00:00")
    fecha_fin: Optional[datetime] = Field(None, example="2024-06-01T12:00:00")

class DetallesEscaneoFrecuenciaActualizar(BaseModel):
    frecuencia_minutos: Optional[int] = Field(None, gt=0, example=60)
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado: Optional[bool] = Field(None, example=True)

class DetallesEscaneoFrecuenciaRespuesta(BaseModel):
    frecuencia_id: int
    configuracion_escaneo_id: int
    frecuencia_minutos: int
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    estado: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True
