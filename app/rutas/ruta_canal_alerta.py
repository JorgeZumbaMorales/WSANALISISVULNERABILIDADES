from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.canal_alerta_esquemas import CanalAlertaCrear, CanalAlertaActualizar
from app.servicios.canal_alerta_servicio import (
    crear_canal_alerta,
    listar_canales_alerta,
    actualizar_canal_alerta,
    eliminar_canal_alerta
)

router = APIRouter(
    prefix="/canales_alerta",
    tags=["Canales de Alerta"]
)

@router.post("/crear_canal_alerta")
def crear_canal_alerta_endpoint(datos: CanalAlertaCrear, db: Session = Depends(obtener_bd)):
    canal_alerta = crear_canal_alerta(datos, db)
    return respuesta_exitosa("Canal de alerta creado exitosamente", canal_alerta)

@router.get("/listar_canales_alerta")
def listar_canales_alerta_endpoint(db: Session = Depends(obtener_bd)):
    canales_alerta = listar_canales_alerta(db)
    return respuesta_exitosa("Lista de canales de alerta obtenida exitosamente", canales_alerta)

@router.put("/actualizar_canal_alerta/{canal_alerta_id}")
def actualizar_canal_alerta_endpoint(canal_alerta_id: int, datos: CanalAlertaActualizar, db: Session = Depends(obtener_bd)):
    canal_alerta = actualizar_canal_alerta(canal_alerta_id, datos, db)
    return respuesta_exitosa("Canal de alerta actualizado exitosamente", canal_alerta)

@router.delete("/eliminar_canal_alerta/{canal_alerta_id}")
def eliminar_canal_alerta_endpoint(canal_alerta_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_canal_alerta(canal_alerta_id, db)
