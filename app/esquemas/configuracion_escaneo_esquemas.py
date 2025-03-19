from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ConfiguracionEscaneoCrear(BaseModel):
    tipo_escaneo_id: int = Field(..., example=1)

class ConfiguracionEscaneoActualizar(BaseModel):
    estado: Optional[bool] = Field(None, example=True)

class ConfiguracionEscaneoRespuesta(BaseModel):
    configuracion_escaneo_id: int
    tipo_escaneo_id: int
    estado: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True
