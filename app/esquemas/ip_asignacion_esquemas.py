from pydantic import BaseModel, Field
from typing import Optional

class IpAsignacionCrear(BaseModel):
    dispositivo_id: int
    ip_address: str = Field(..., min_length=7, max_length=50)
    estado: bool = True

class IpAsignacionActualizar(BaseModel):
    estado: Optional[bool]

class IpAsignacionRespuesta(BaseModel):
    ip_asignacion_id: int
    dispositivo_id: int
    ip_address: str
    fecha_creacion: str
    estado: bool

    class Config:
        from_attributes = True
