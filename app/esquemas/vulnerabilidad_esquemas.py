from pydantic import BaseModel, Field
from datetime import datetime

# Esquema para crear una vulnerabilidad
class VulnerabilidadCrear(BaseModel):
    dispositivo_id: int = Field(..., example=1)
    tipo: str = Field(..., example="SQL Injection")
    severidad: str = Field(..., example="Alta")
    descripcion: str = Field(None, example="Brecha de seguridad en el formulario de login")
    fecha_deteccion: datetime = Field(..., example="2024-06-01T12:00:00")

# Esquema para actualizar una vulnerabilidad
class VulnerabilidadActualizar(BaseModel):
    tipo: str = Field(..., example="Cross-Site Scripting")
    severidad: str = Field(..., example="Media")
    descripcion: str = Field(None, example="Brecha de seguridad en el formulario de contacto")

# Esquema para actualizar el estado de una vulnerabilidad
class VulnerabilidadActualizarEstado(BaseModel):
    estado: bool = Field(..., example=False)
