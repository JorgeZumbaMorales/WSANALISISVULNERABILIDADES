from pydantic import BaseModel, Field
from typing import Optional

class TipoEscaneoBase(BaseModel):
    nombre_tipo: str = Field(..., min_length=3, max_length=20, example="frecuencia")
    descripcion: Optional[str] = Field(None, example="Escaneo basado en una frecuencia específica.")
    estado: Optional[bool] = Field(default=True)

class TipoEscaneoCrear(TipoEscaneoBase):
    pass

class TipoEscaneoActualizar(BaseModel):
    nombre_tipo: Optional[str] = Field(None, min_length=3, max_length=20)
    descripcion: Optional[str] = Field(None)
    estado: Optional[bool] = Field(None)

class TipoEscaneoRespuesta(TipoEscaneoBase):
    tipo_escaneo_id: int
    fecha_creacion: str

    class Config:
        from_attributes = True
