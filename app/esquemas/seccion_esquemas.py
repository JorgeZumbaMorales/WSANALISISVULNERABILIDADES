from pydantic import BaseModel
from typing import Optional

# 📌 Esquema para crear una sección
class SeccionCrear(BaseModel):
    nombre_seccion: str
    descripcion: Optional[str] = None
    ruta: str
    icono: Optional[str] = None

# 📌 Esquema para actualizar una sección
class SeccionActualizar(BaseModel):
    nombre_seccion: Optional[str] = None
    descripcion: Optional[str] = None
    ruta: Optional[str] = None
    icono: Optional[str] = None

# 📌 Esquema para cambiar el estado de una sección
class SeccionActualizarEstado(BaseModel):
    estado: bool

# 📌 Esquema de respuesta con información completa de la sección
class SeccionRespuesta(BaseModel):
    seccion_id: int
    nombre_seccion: str
    descripcion: Optional[str]
    ruta: str
    icono: Optional[str]
    fecha_creacion: str
    estado: bool

    class Config:
        from_attributes = True
