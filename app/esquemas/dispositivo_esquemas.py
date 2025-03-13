from pydantic import BaseModel, Field
from typing import Optional

class DispositivoCrear(BaseModel):
    nombre_dispositivo: Optional[str] = Field(None, example="Servidor Principal")
    mac_address: str = Field(..., example="60:83:E7:B9:CE:78")

class DispositivoActualizar(BaseModel):
    nombre_dispositivo: Optional[str] = Field(None, example="Servidor Actualizado")
    estado: Optional[bool]

class DispositivoActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

class DispositivoRespuesta(BaseModel):
    dispositivo_id: int
    nombre_dispositivo: Optional[str]
    mac_address: str
    fecha_creacion: str
    estado: bool

    class Config:
        from_attributes = True

