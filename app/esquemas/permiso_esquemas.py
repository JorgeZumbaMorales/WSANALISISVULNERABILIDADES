from pydantic import BaseModel

class PermisoCrear(BaseModel):
    nombre_permiso: str
    descripcion: str

class PermisoActualizar(BaseModel):
    nombre_permiso: str
    descripcion: str

class PermisoActualizarEstado(BaseModel):
    estado: bool
