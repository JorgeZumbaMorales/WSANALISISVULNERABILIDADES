from pydantic import BaseModel, Field
from typing import Optional

class SistemaOperativoCrear(BaseModel):
    nombre_so: str = Field(..., min_length=3, max_length=255)
    estado: bool = True

class SistemaOperativoActualizar(BaseModel):
    nombre_so: Optional[str] = Field(None, min_length=3, max_length=255)
    estado: Optional[bool]

class SistemaOperativoRespuesta(BaseModel):
    sistema_operativo_id: int
    nombre_so: str


    class Config:
        from_attributes = True

class SistemaOperativoBusqueda(BaseModel):
    sistema_operativo_id: int
    nombre_so: str

    class Config:
        from_attributes = True