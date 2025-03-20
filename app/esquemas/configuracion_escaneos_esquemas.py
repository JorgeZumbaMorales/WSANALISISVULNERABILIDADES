from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 📌 Esquema para CREAR configuración de escaneo
class ConfiguracionEscaneoCrear(BaseModel):
    nombre_configuracion_escaneo: str  
    tipo_escaneo_id: int
    frecuencia_minutos: Optional[int] = None
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    estado: Optional[bool] = False  # ✅ Ahora por defecto es False

# 📌 Esquema para ACTUALIZAR configuración de escaneo
class ConfiguracionEscaneoActualizar(BaseModel):
    nombre_configuracion_escaneo: Optional[str]  
    frecuencia_minutos: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado: Optional[bool] = None  

# 📌 Esquema para ACTUALIZAR SOLO EL ESTADO de una configuración
class ConfiguracionEscaneoActualizarEstado(BaseModel):
    estado: bool  # ✅ Solo se enviará el estado

# 📌 Esquema de RESPUESTA para configuración de escaneo
class ConfiguracionEscaneoRespuesta(BaseModel):
    configuracion_escaneo_id: int
    nombre_configuracion_escaneo: str  
    tipo_escaneo_id: int
    frecuencia_minutos: Optional[int]
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    estado: bool  
    fecha_creacion: datetime

    class Config:
        from_attributes = True
