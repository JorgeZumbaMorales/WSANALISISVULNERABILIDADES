from pydantic import BaseModel
from datetime import datetime

# 📌 Esquema para CREAR un nuevo registro de escaneo
class RegistroEscaneoCrear(BaseModel):
    configuracion_escaneo_id: int  # La configuración usada para el escaneo

# 📌 Esquema para ACTUALIZAR un registro de escaneo (ejemplo: desactivarlo)
class RegistroEscaneoActualizarEstado(BaseModel):
    estado: bool  # Permite activar o desactivar el registro

# 📌 Esquema de RESPUESTA para devolver registros
class RegistroEscaneoRespuesta(BaseModel):
    registro_escaneo_id: int
    configuracion_escaneo_id: int
    estado: bool
    fecha_creacion: datetime  # 📌 Solo se mantiene este campo de tiempo

    class Config:
        from_attributes = True
