from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any

# Esquema para crear un reporte generado
class ReporteGeneradoCrear(BaseModel):
    tipo_reporte_id: int = Field(..., example=1)
    nombre_reporte_generado: str = Field(..., example="Reporte de Vulnerabilidades Semanal")
    descripcion: Optional[str] = Field(None, example="Informe detallado de vulnerabilidades detectadas")
    usuario_id: Optional[int] = Field(None, example=1)
    fecha_inicio: datetime = Field(..., example="2024-05-01T00:00:00")
    fecha_fin: datetime = Field(..., example="2024-05-07T23:59:59")
    contenido: Any = Field(..., example={"detalles": "Datos del reporte en formato JSON"})

# Esquema para actualizar un reporte generado
class ReporteGeneradoActualizar(BaseModel):
    nombre_reporte_generado: Optional[str] = Field(None, example="Nuevo nombre del reporte")
    descripcion: Optional[str] = Field(None, example="Descripción actualizada del reporte")
    contenido: Optional[Any] = Field(None, example={"detalles": "Contenido actualizado"})

# Esquema para cambiar el estado de un reporte generado
class ReporteGeneradoActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)

# Esquema para mostrar un reporte generado
class ReporteGeneradoMostrar(BaseModel):
    reporte_generado_id: int
    tipo_reporte_id: int
    nombre_reporte_generado: str
    descripcion: Optional[str]
    usuario_id: Optional[int]
    fecha_inicio: datetime
    fecha_fin: datetime
    contenido: Any
    fecha_creacion: datetime
    estado: bool

    class Config:
        from_attributes = True
