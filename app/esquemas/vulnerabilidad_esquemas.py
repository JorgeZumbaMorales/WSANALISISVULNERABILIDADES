from pydantic import BaseModel, Field
from typing import Optional

class VulnerabilidadCrear(BaseModel):
    cve_id: str = Field(..., max_length=50)
    score: Optional[float]
    url: Optional[str]
    estado: Optional[bool] = True

class VulnerabilidadActualizar(BaseModel):
    score: Optional[float]
    url: Optional[str]
    estado: Optional[bool]

class VulnerabilidadRespuesta(BaseModel):
    vulnerabilidad_id: int
    cve_id: str
    score: Optional[float]
    url: Optional[str]
    estado: bool
    fecha_creacion: str

    class Config:
        from_attributes = True
