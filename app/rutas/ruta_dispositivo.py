from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.dispositivo_esquemas import (
    DispositivoCrear, 
    DispositivoActualizar, 
    DispositivoActualizarEstado
)
from app.servicios.dispositivo_servicio import (
    crear_dispositivo,
    listar_dispositivos,
    actualizar_dispositivo,
    actualizar_estado_dispositivo,
    eliminar_dispositivo
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

@router.put("/actualizar_dispositivo/{dispositivo_id}")
def actualizar_dispositivo_endpoint(dispositivo_id: int, datos_dispositivo: DispositivoActualizar, db: Session = Depends(obtener_bd)):
    dispositivo = actualizar_dispositivo(dispositivo_id, datos_dispositivo, db)
    return respuesta_exitosa("Dispositivo actualizado exitosamente", dispositivo)

@router.put("/actualizar_estado_dispositivo/{dispositivo_id}")
def actualizar_estado_dispositivo_endpoint(dispositivo_id: int, datos_estado: DispositivoActualizarEstado, db: Session = Depends(obtener_bd)):
    dispositivo = actualizar_estado_dispositivo(dispositivo_id, datos_estado.estado, db)
    return respuesta_exitosa("Estado del dispositivo actualizado exitosamente", dispositivo)

@router.delete("/eliminar_dispositivo/{dispositivo_id}")
def eliminar_dispositivo_endpoint(dispositivo_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_dispositivo(dispositivo_id, db)
