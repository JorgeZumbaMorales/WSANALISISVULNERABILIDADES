from pydantic import BaseModel
from datetime import time, datetime
from typing import List, Optional

# 📌 Esquema para CREAR una nueva hora de escaneo
class ConfiguracionHorasEscaneoCrear(BaseModel):
    configuracion_escaneo_id: int
    hora: time

# 📌 Esquema para ACTUALIZAR una hora de escaneo
class ConfiguracionHorasEscaneoActualizar(BaseModel):
    hora: Optional[time] = None
    estado: Optional[bool] = None

# 📌 Esquema de RESPUESTA para una hora de escaneo
class ConfiguracionHorasEscaneoRespuesta(BaseModel):
    id: int
    configuracion_escaneo_id: int
    hora: time
    estado: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True

# 📌 Esquema para listar múltiples horas asociadas a una configuración
class ListaConfiguracionHorasEscaneo(BaseModel):
    horas: List[ConfiguracionHorasEscaneoRespuesta]
