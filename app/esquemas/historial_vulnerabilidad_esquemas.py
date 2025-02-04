from pydantic import BaseModel, Field
from datetime import datetime

# Esquema para crear un registro en el historial de vulnerabilidades
class HistorialVulnerabilidadCrear(BaseModel):
    vulnerabilidad_id: int = Field(..., example=1)
    estado_anterior: bool = Field(..., example=True)
    estado_actual: bool = Field(..., example=False)

# Esquema para mostrar un historial de vulnerabilidades
class HistorialVulnerabilidadMostrar(BaseModel):
    historial_vulnerabilidad_id: int
    vulnerabilidad_id: int
    estado_anterior: bool
    estado_actual: bool
    fecha_cambio: datetime
    estado: bool

    class Config:
        from_attributes = True
