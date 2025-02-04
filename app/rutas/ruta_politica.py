from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.politica_esquemas import (
    PoliticaCrear,
    PoliticaActualizar,
    PoliticaActualizarEstado,
)
from app.servicios.politica_servicio import (
    crear_politica,
    listar_politicas,
    actualizar_politica,
    actualizar_estado_politica,
    eliminar_politica,
)

router = APIRouter(
    prefix="/politicas",
    tags=["Políticas"]
)

@router.post("/crear_politica")
def crear_politica_endpoint(datos: PoliticaCrear, db: Session = Depends(obtener_bd)):
    politica = crear_politica(datos, db)
    return respuesta_exitosa("Política creada exitosamente", politica)

@router.get("/listar_politicas")
def listar_politicas_endpoint(db: Session = Depends(obtener_bd)):
    politicas = listar_politicas(db)
    return respuesta_exitosa("Lista de políticas obtenida exitosamente", politicas)

@router.put("/actualizar_politica/{politica_id}")
def actualizar_politica_endpoint(politica_id: int, datos: PoliticaActualizar, db: Session = Depends(obtener_bd)):
    politica = actualizar_politica(politica_id, datos, db)
    return respuesta_exitosa("Política actualizada exitosamente", politica)

@router.put("/actualizar_estado_politica/{politica_id}")
def actualizar_estado_politica_endpoint(politica_id: int, datos: PoliticaActualizarEstado, db: Session = Depends(obtener_bd)):
    politica = actualizar_estado_politica(politica_id, datos, db)
    return respuesta_exitosa("Estado de la política actualizado exitosamente", politica)

@router.delete("/eliminar_politica/{politica_id}")
def eliminar_politica_endpoint(politica_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_politica(politica_id, db)
