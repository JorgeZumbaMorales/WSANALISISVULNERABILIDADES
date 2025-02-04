from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.tipo_alerta_esquemas import TipoAlertaCrear, TipoAlertaActualizar
from app.servicios.tipo_alerta_servicio import (
    crear_tipo_alerta,
    listar_tipos_alerta,
    actualizar_tipo_alerta,
    eliminar_tipo_alerta
)

router = APIRouter(
    prefix="/tipos_alerta",
    tags=["Tipos de Alerta"]
)

@router.post("/crear_tipo_alerta")
def crear_tipo_alerta_endpoint(datos: TipoAlertaCrear, db: Session = Depends(obtener_bd)):
    tipo_alerta = crear_tipo_alerta(datos, db)
    return respuesta_exitosa("Tipo de alerta creado exitosamente", tipo_alerta)

@router.get("/listar_tipos_alerta")
def listar_tipos_alerta_endpoint(db: Session = Depends(obtener_bd)):
    tipos_alerta = listar_tipos_alerta(db)
    return respuesta_exitosa("Lista de tipos de alerta obtenida exitosamente", tipos_alerta)

@router.put("/actualizar_tipo_alerta/{tipo_alerta_id}")
def actualizar_tipo_alerta_endpoint(tipo_alerta_id: int, datos: TipoAlertaActualizar, db: Session = Depends(obtener_bd)):
    tipo_alerta = actualizar_tipo_alerta(tipo_alerta_id, datos, db)
    return respuesta_exitosa("Tipo de alerta actualizado exitosamente", tipo_alerta)

@router.delete("/eliminar_tipo_alerta/{tipo_alerta_id}")
def eliminar_tipo_alerta_endpoint(tipo_alerta_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_tipo_alerta(tipo_alerta_id, db)
