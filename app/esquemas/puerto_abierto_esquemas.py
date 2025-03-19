from pydantic import BaseModel, Field
from typing import Optional
from typing import List
class PuertoAbiertoCrear(BaseModel):
    dispositivo_id: int
    puerto: int
    protocolo: str = Field(..., min_length=3, max_length=10)
    servicio: str = Field(..., min_length=3, max_length=100)
    version: Optional[str] = Field(None, max_length=100)
    estado: bool = True

class PuertoAbiertoActualizar(BaseModel):
    puerto: Optional[int]
    protocolo: Optional[str] = Field(None, min_length=3, max_length=10)
    servicio: Optional[str] = Field(None, min_length=3, max_length=100)
    version: Optional[str] = Field(None, max_length=100)
    estado: Optional[bool]

class PuertoAbiertoRespuesta(BaseModel):
    puerto_id: int
    dispositivo_id: int
    puerto: int
    protocolo: str
    servicio: str
    version: Optional[str]
    fecha_creacion: str
    estado: bool

    class Config:
        from_attributes = True

class PuertosSeleccionadosPeticion(BaseModel):
    puertos_ids: List[int]