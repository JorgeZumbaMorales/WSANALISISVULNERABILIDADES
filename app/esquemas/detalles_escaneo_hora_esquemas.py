from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, time

class DetallesEscaneoHoraCrear(BaseModel):
    configuracion_escaneo_id: int = Field(..., example=1)
    hora_especifica: time = Field(..., example="12:00:00")
    fecha_inicio: datetime = Field(..., example="2024-03-18T12:00:00")
    fecha_fin: Optional[datetime] = Field(None, example="2024-06-01T12:00:00")

class DetallesEscaneoHoraActualizar(BaseModel):
    hora_especifica: Optional[time] = Field(None, example="14:00:00")
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado: Optional[bool] = Field(None, example=True)

class DetallesEscaneoHoraRespuesta(BaseModel):
    hora_id: int
    configuracion_escaneo_id: int
    hora_especifica: time
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    estado: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True
