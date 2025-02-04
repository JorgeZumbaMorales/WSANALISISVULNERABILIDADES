from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Esquema para crear una herramienta
class HerramientaCrear(BaseModel):
    nombre_herramienta: str = Field(..., example="Nmap")
    descripcion: Optional[str] = Field(None, example="Herramienta de escaneo de red")

# Esquema para actualizar una herramienta
class HerramientaActualizar(BaseModel):
    nombre_herramienta: Optional[str] = Field(None, example="Tcpdump")
    descripcion: Optional[str] = Field(None, example="Herramienta para capturar tráfico de red")

# Esquema para cambiar el estado de una herramienta
class HerramientaActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

# Esquema para mostrar una herramienta
class HerramientaMostrar(BaseModel):
    herramienta_id: int
    nombre_herramienta: str
    descripcion: Optional[str]
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
