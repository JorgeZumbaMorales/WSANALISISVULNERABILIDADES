from pydantic import BaseModel, Field
from typing import Optional
from datetime import time

class ConfiguracionEscaneoBase(BaseModel):
    tipo_escaneo_id: int = Field(..., example=1)
    frecuencia_minutos: Optional[int] = Field(None, gt=0, example=30)
    hora_especifica: Optional[time] = Field(None, example="03:00:00")
    estado: Optional[bool] = Field(default=True)

class ConfiguracionEscaneoCrear(ConfiguracionEscaneoBase):
    pass

class ConfiguracionEscaneoActualizar(BaseModel):
    frecuencia_minutos: Optional[int] = Field(None, gt=0, example=30)
    hora_especifica: Optional[time] = Field(None, example="03:00:00")
    estado: Optional[bool] = Field(None)

class ConfiguracionEscaneoRespuesta(ConfiguracionEscaneoBase):
    configuracion_escaneo_id: int
    fecha_creacion: str

    class Config:
        from_attributes = True
