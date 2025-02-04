from pydantic import BaseModel, Field
from typing import Optional

# Esquema para crear un dispositivo
class DispositivoCrear(BaseModel):
    nombre_dispositivo: Optional[str] = Field(None, example="Servidor Principal")
    ip_address: str = Field(..., example="192.168.1.10")
    sistema_operativo: Optional[str] = Field(None, example="Linux")
    tipo: Optional[str] = Field(None, example="Servidor")

# Esquema para actualizar un dispositivo
class DispositivoActualizar(BaseModel):
    nombre_dispositivo: Optional[str] = Field(None, example="Servidor Actualizado")
    sistema_operativo: Optional[str] = Field(None, example="Windows")
    tipo: Optional[str] = Field(None, example="Workstation")

# Esquema para actualizar el estado del dispositivo
class DispositivoActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)
