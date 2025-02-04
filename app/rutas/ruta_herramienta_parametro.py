from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.herramienta_parametro_esquemas import (
    HerramientaParametroCrear,
    HerramientaParametroActualizar,
    HerramientaParametroActualizarEstado,
)
from app.servicios.herramienta_parametro_servicio import (
    crear_herramienta_parametro,
    listar_herramienta_parametro,
    actualizar_herramienta_parametro,
    actualizar_estado_herramienta_parametro,
    eliminar_herramienta_parametro,
)

router = APIRouter(
    prefix="/herramienta_parametros",
    tags=["Herramienta-Parámetro"]
)

@router.post("/crear_herramienta_parametro")
def crear_herramienta_parametro_endpoint(datos: HerramientaParametroCrear, db: Session = Depends(obtener_bd)):
    relacion = crear_herramienta_parametro(datos, db)
    return respuesta_exitosa("Relación Herramienta-Parámetro creada exitosamente", relacion)

@router.get("/listar_herramienta_parametros")
def listar_herramienta_parametros_endpoint(db: Session = Depends(obtener_bd)):
    relaciones = listar_herramienta_parametro(db)
    return respuesta_exitosa("Lista de relaciones Herramienta-Parámetro obtenida exitosamente", relaciones)

@router.put("/actualizar_herramienta_parametro/{relacion_id}")
def actualizar_herramienta_parametro_endpoint(relacion_id: int, datos: HerramientaParametroActualizar, db: Session = Depends(obtener_bd)):
    relacion = actualizar_herramienta_parametro(relacion_id, datos, db)
    return respuesta_exitosa("Relación Herramienta-Parámetro actualizada exitosamente", relacion)

@router.put("/actualizar_estado_herramienta_parametro/{relacion_id}")
def actualizar_estado_herramienta_parametro_endpoint(relacion_id: int, datos: HerramientaParametroActualizarEstado, db: Session = Depends(obtener_bd)):
    relacion = actualizar_estado_herramienta_parametro(relacion_id, datos, db)
    return respuesta_exitosa("Estado de la relación Herramienta-Parámetro actualizado exitosamente", relacion)

@router.delete("/eliminar_herramienta_parametro/{relacion_id}")
def eliminar_herramienta_parametro_endpoint(relacion_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_herramienta_parametro(relacion_id, db)
