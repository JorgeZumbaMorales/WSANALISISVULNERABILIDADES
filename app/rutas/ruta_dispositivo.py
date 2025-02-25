from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.dispositivo_esquemas import (
    DispositivoCrear, 
    DispositivoActualizar, 
    IpAsignacionCrear
)
from app.servicios.dispositivo_servicio import (
    crear_dispositivo,
    listar_dispositivos,
    asignar_ip,
    obtener_historial_ips
)

router = APIRouter(
    prefix="/dispositivos",
    tags=["Dispositivos"]
)

@router.post("/crear_dispositivo")
def crear_dispositivo_endpoint(datos_dispositivo: DispositivoCrear, db: Session = Depends(obtener_bd)):
    dispositivo = crear_dispositivo(datos_dispositivo, db)
    return respuesta_exitosa("Dispositivo creado exitosamente", dispositivo)

@router.get("/listar_dispositivos")
def listar_dispositivos_endpoint(db: Session = Depends(obtener_bd)):
    dispositivos = listar_dispositivos(db)
    return respuesta_exitosa("Lista de dispositivos obtenida exitosamente", dispositivos)

@router.post("/asignar_ip")
def asignar_ip_endpoint(datos_ip: IpAsignacionCrear, db: Session = Depends(obtener_bd)):
    return asignar_ip(datos_ip, db)

@router.get("/historial_ips/{dispositivo_id}")
def historial_ips_endpoint(dispositivo_id: int, db: Session = Depends(obtener_bd)):
    historial = obtener_historial_ips(dispositivo_id, db)
    return respuesta_exitosa("Historial de IPs obtenido exitosamente", historial)
