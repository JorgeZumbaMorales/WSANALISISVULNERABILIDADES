from pydantic import BaseModel
from typing import Optional

class RolSeccionPermisoCrear(BaseModel):
    rol_id: int
    seccion_id: int
    permiso_id: int
    estado: Optional[bool] = True

class RolSeccionPermisoActualizar(BaseModel):
    estado: Optional[bool]

class RolSeccionPermisoRespuesta(BaseModel):
    rol_seccion_permiso_id: int
    rol_id: int
    seccion_id: int
    permiso_id: int
    fecha_creacion: str
    estado: bool

    class Config:
        from_attributes = True
