from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.notificacion_esquemas import NotificacionCrear, NotificacionActualizar
from app.servicios.notificacion_servicio import (
    crear_notificacion,
    listar_notificaciones,
    actualizar_notificacion,
    eliminar_notificacion
)

router = APIRouter(
    prefix="/notificaciones",
    tags=["Notificaciones"]
)

@router.post("/crear_notificacion")
def crear_notificacion_endpoint(datos: NotificacionCrear, db: Session = Depends(obtener_bd)):
    notificacion = crear_notificacion(datos, db)
    return respuesta_exitosa("Notificación creada exitosamente", notificacion)

@router.get("/listar_notificaciones")
def listar_notificaciones_endpoint(db: Session = Depends(obtener_bd)):
    notificaciones = listar_notificaciones(db)
    return respuesta_exitosa("Lista de notificaciones obtenida exitosamente", notificaciones)

@router.put("/actualizar_notificacion/{notificacion_id}")
def actualizar_notificacion_endpoint(notificacion_id: int, datos: NotificacionActualizar, db: Session = Depends(obtener_bd)):
    notificacion = actualizar_notificacion(notificacion_id, datos, db)
    return respuesta_exitosa("Notificación actualizada exitosamente", notificacion)

@router.delete("/eliminar_notificacion/{notificacion_id}")
def eliminar_notificacion_endpoint(notificacion_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_notificacion(notificacion_id, db)
