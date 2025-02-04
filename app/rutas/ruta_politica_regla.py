from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.politica_regla_esquemas import (
    PoliticaReglaCrear,
    PoliticaReglaActualizar,
    PoliticaReglaActualizarEstado,
)
from app.servicios.politica_regla_servicio import (
    crear_politica_regla,
    listar_politicas_reglas,
    actualizar_politica_regla,
    actualizar_estado_politica_regla,
    eliminar_politica_regla,
)

router = APIRouter(
    prefix="/politicas_reglas",
    tags=["Políticas-Reglas"]
)

@router.post("/crear_politica_regla")
def crear_politica_regla_endpoint(datos: PoliticaReglaCrear, db: Session = Depends(obtener_bd)):
    asociacion = crear_politica_regla(datos, db)
    return respuesta_exitosa("Asociación Política-Regla creada exitosamente", asociacion)

@router.get("/listar_politicas_reglas")
def listar_politicas_reglas_endpoint(db: Session = Depends(obtener_bd)):
    asociaciones = listar_politicas_reglas(db)
    return respuesta_exitosa("Lista de asociaciones obtenida exitosamente", asociaciones)

@router.put("/actualizar_politica_regla/{politica_regla_id}")
def actualizar_politica_regla_endpoint(politica_regla_id: int, datos: PoliticaReglaActualizar, db: Session = Depends(obtener_bd)):
    asociacion = actualizar_politica_regla(politica_regla_id, datos, db)
    return respuesta_exitosa("Asociación actualizada exitosamente", asociacion)

@router.put("/actualizar_estado_politica_regla/{politica_regla_id}")
def actualizar_estado_politica_regla_endpoint(politica_regla_id: int, datos: PoliticaReglaActualizarEstado, db: Session = Depends(obtener_bd)):
    asociacion = actualizar_estado_politica_regla(politica_regla_id, datos, db)
    return respuesta_exitosa("Estado de la asociación actualizado exitosamente", asociacion)

@router.delete("/eliminar_politica_regla/{politica_regla_id}")
def eliminar_politica_regla_endpoint(politica_regla_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_politica_regla(politica_regla_id, db)
