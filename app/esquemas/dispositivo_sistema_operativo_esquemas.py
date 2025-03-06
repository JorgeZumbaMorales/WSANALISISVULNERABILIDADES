from pydantic import BaseModel
from typing import Optional

class DispositivoSistemaOperativoCrear(BaseModel):
    dispositivo_id: int
    sistema_operativo_id: int
    estado: bool = True

class DispositivoSistemaOperativoActualizar(BaseModel):
    estado: Optional[bool]

class DispositivoSistemaOperativoRespuesta(BaseModel):
    dispositivo_so_id: int
    dispositivo_id: int
    sistema_operativo_id: int
    fecha_creacion: str
    estado: bool

    class Config:
        from_attributes = True
