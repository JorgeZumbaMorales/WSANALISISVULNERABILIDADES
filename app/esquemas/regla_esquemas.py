from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Esquema para crear una regla
class ReglaCrear(BaseModel):
    nombre_regla: str = Field(..., example="Escaneo de puertos")
    descripcion: Optional[str] = Field(None, example="Escaneo de puertos abiertos en una red")
    herramienta: str = Field(..., example="nmap")
    parametros: Optional[str] = Field(None, example="-p 80,443")

# Esquema para actualizar una regla
class ReglaActualizar(BaseModel):
    nombre_regla: Optional[str] = Field(None, example="Escaneo de vulnerabilidades")
    descripcion: Optional[str] = Field(None, example="Escaneo de vulnerabilidades críticas")
    herramienta: Optional[str] = Field(None, example="tcpdump")
    parametros: Optional[str] = Field(None, example="-i eth0")

# Esquema para cambiar el estado de una regla
class ReglaActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

# Esquema para mostrar una regla
class ReglaMostrar(BaseModel):
    regla_id: int
    nombre_regla: str
    descripcion: Optional[str]
    herramienta: str
    parametros: Optional[str]
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
