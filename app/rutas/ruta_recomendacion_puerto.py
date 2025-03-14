from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.recomendacion_puerto_esquemas import RecomendacionPuertoCrear, RecomendacionPuertoActualizarEstado
from app.servicios.recomendacion_puerto_servicio import (
    agregar_recomendacion_a_puerto,
    obtener_recomendaciones_por_puerto,
    actualizar_estado_recomendacion,
    eliminar_recomendacion,
    listar_todas_las_recomendaciones
)

router = APIRouter(
    prefix="/recomendaciones_puertos",
    tags=["Recomendaciones de Puertos"]
)

@router.post("/agregar")
def agregar_recomendacion_endpoint(datos: RecomendacionPuertoCrear, db: Session = Depends(obtener_bd)):
    """📌 Agrega una recomendación para un puerto."""
    resultado = agregar_recomendacion_a_puerto(datos, db)
    return respuesta_exitosa("Recomendación agregada correctamente", resultado)

@router.get("/listar_por_puerto/{puerto_id}")
def obtener_recomendaciones_por_puerto_endpoint(puerto_id: int, db: Session = Depends(obtener_bd)):
    """📌 Obtiene todas las recomendaciones asociadas a un puerto específico."""
    recomendaciones = obtener_recomendaciones_por_puerto(puerto_id, db)
    return respuesta_exitosa("Lista de recomendaciones obtenida", recomendaciones)

@router.put("/actualizar_estado/{recomendacion_id}")
def actualizar_estado_recomendacion_endpoint(recomendacion_id: int, datos_estado: RecomendacionPuertoActualizarEstado, db: Session = Depends(obtener_bd)):
    """📌 Actualiza el estado de una recomendación."""
    resultado = actualizar_estado_recomendacion(recomendacion_id, datos_estado, db)
    return respuesta_exitosa("Estado de la recomendación actualizado correctamente", resultado)

@router.delete("/eliminar/{recomendacion_id}")
def eliminar_recomendacion_endpoint(recomendacion_id: int, db: Session = Depends(obtener_bd)):
    """📌 Elimina una recomendación de un puerto."""
    eliminar_recomendacion(recomendacion_id, db)
    return respuesta_exitosa("Recomendación eliminada correctamente")

@router.get("/listar_todas")
def listar_todas_recomendaciones_endpoint(db: Session = Depends(obtener_bd)):
    """📌 Obtiene todas las recomendaciones registradas."""
    recomendaciones = listar_todas_las_recomendaciones(db)
    return respuesta_exitosa("Lista de todas las recomendaciones obtenida", recomendaciones)
