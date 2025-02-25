from pydantic import BaseModel, Field
from typing import Optional, List

# Esquema para crear un dispositivo
class DispositivoCrear(BaseModel):
    nombre_dispositivo: Optional[str] = Field(None, example="Servidor Principal")
    mac_address: str = Field(..., example="60:83:E7:B9:CE:78")
    fabricante: Optional[str] = Field(None, example="TP-LINK CORPORATION PTE. LTD.")
    ip_address: str = Field(..., example="192.168.1.10")  # La IP inicial

# Esquema para actualizar un dispositivo
class DispositivoActualizar(BaseModel):
    nombre_dispositivo: Optional[str] = Field(None, example="Servidor Actualizado")
    fabricante: Optional[str] = Field(None, example="Cisco Systems")

# Esquema para asignación de IPs
class IpAsignacionCrear(BaseModel):
    dispositivo_id: int
    ip_address: str = Field(..., example="192.168.1.15")

# Esquema de respuesta para dispositivo con historial de IPs
class DispositivoConIps(BaseModel):
    dispositivo_id: int
    nombre_dispositivo: Optional[str]
    mac_address: str
    fabricante: Optional[str]
    ips: List[str]  # Lista de direcciones IP asociadas
