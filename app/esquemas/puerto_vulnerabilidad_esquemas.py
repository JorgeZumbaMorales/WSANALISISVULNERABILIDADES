from pydantic import BaseModel
from typing import Optional

class PuertoVulnerabilidadCrear(BaseModel):
    puerto_id: int
    vulnerabilidad_id: int
    exploit: Optional[bool] = False
    estado: Optional[bool] = True

class PuertoVulnerabilidadRespuesta(BaseModel):
    puerto_vuln_id: int
    puerto_id: int
    vulnerabilidad_id: int
    exploit: Optional[bool]
    estado: bool
    fecha_creacion: str

    class Config:
        from_attributes = True
