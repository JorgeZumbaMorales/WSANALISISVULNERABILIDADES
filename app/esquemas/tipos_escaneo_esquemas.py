from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TiposEscaneoCrear(BaseModel):
    nombre_tipo: str = Field(..., min_length=3, max_length=20, example="Frecuencia")
    descripcion: Optional[str] = Field(None, max_length=255, example="Escaneo basado en una frecuencia de tiempo")

class TiposEscaneoActualizar(BaseModel):
    nombre_tipo: Optional[str] = Field(None, min_length=3, max_length=20, example="Hora específica")
    descripcion: Optional[str] = Field(None, max_length=255)
    estado: Optional[bool] = Field(None, example=True)

class TiposEscaneoRespuesta(BaseModel):
    tipo_escaneo_id: int
    nombre_tipo: str
    descripcion: Optional[str]
    estado: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True
