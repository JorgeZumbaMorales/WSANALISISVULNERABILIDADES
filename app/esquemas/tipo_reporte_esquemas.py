from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Esquema para crear un tipo de reporte
class TipoReporteCrear(BaseModel):
    nombre_tipo_reporte: str = Field(..., example="Reporte de Vulnerabilidades")
    descripcion: Optional[str] = Field(None, example="Informe detallado de vulnerabilidades detectadas")

# Esquema para actualizar un tipo de reporte
class TipoReporteActualizar(BaseModel):
    nombre_tipo_reporte: Optional[str] = Field(None, example="Reporte de Dispositivos")
    descripcion: Optional[str] = Field(None, example="Informe actualizado sobre dispositivos conectados")

# Esquema para cambiar el estado de un tipo de reporte
class TipoReporteActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

# Esquema para mostrar un tipo de reporte
class TipoReporteMostrar(BaseModel):
    tipo_reporte_id: int
    nombre_tipo_reporte: str
    descripcion: Optional[str]
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
