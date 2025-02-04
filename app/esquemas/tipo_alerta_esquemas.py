from pydantic import BaseModel, Field
from datetime import datetime

# Esquema para crear un tipo de alerta
class TipoAlertaCrear(BaseModel):
    nombre_tipo: str = Field(..., example="Alerta Crítica")

# Esquema para actualizar un tipo de alerta
class TipoAlertaActualizar(BaseModel):
    nombre_tipo: str = Field(..., example="Alerta Informativa")

# Esquema para mostrar un tipo de alerta
class TipoAlertaMostrar(BaseModel):
    tipo_alerta_id: int
    nombre_tipo: str
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
