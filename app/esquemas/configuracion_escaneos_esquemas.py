from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 📌 Esquema para CREAR configuración de escaneo
class ConfiguracionEscaneoCrear(BaseModel):
    nombre_configuracion_escaneo: str  
    tipo_escaneo_id: int
    frecuencia_minutos: Optional[int] = None
    hora_especifica: Optional[datetime] = None
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None

# 📌 Esquema para ACTUALIZAR configuración de escaneo
class ConfiguracionEscaneoActualizar(BaseModel):
    nombre_configuracion_escaneo: Optional[str]  
    frecuencia_minutos: Optional[int] = None
    hora_especifica: Optional[datetime] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado: Optional[bool] = None

# 📌 Esquema de RESPUESTA para configuración de escaneo
class ConfiguracionEscaneoRespuesta(BaseModel):
    configuracion_escaneo_id: int
    nombre_configuracion_escaneo: str  
    tipo_escaneo_id: int
    frecuencia_minutos: Optional[int]
    hora_especifica: Optional[datetime]
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    estado: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True

# 📌 Esquema para listar múltiples configuraciones
class ListaConfiguracionesEscaneo(BaseModel):
    configuraciones: list[ConfiguracionEscaneoRespuesta]
