from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.dispositivo_riesgo_esquemas import DispositivoRiesgoCrear, DispositivoRiesgoActualizarEstado
from app.servicios.dispositivo_riesgo_servicio import (
    asignar_riesgo_a_dispositivo,
    obtener_riesgos_de_dispositivo,
    actualizar_estado_dispositivo_riesgo,
    eliminar_riesgo_de_dispositivo,
    listar_todas_las_relaciones
)

router = APIRouter(
    prefix="/dispositivo_riesgo",
    tags=["Dispositivo - Riesgo"]
)

@router.post("/asignar")
def asignar_riesgo_endpoint(datos: DispositivoRiesgoCrear, db: Session = Depends(obtener_bd)):
    """📌 Asigna un riesgo a un dispositivo."""
    resultado = asignar_riesgo_a_dispositivo(datos, db)
    return respuesta_exitosa("Riesgo asignado correctamente al dispositivo", resultado)

@router.get("/listar_por_dispositivo/{dispositivo_id}")
def obtener_riesgos_de_dispositivo_endpoint(dispositivo_id: int, db: Session = Depends(obtener_bd)):
    """📌 Obtiene los riesgos asignados a un dispositivo específico."""
    riesgos = obtener_riesgos_de_dispositivo(dispositivo_id, db)
    return respuesta_exitosa("Lista de riesgos del dispositivo obtenida", riesgos)

@router.put("/actualizar_estado/{dispositivo_riesgo_id}")
def actualizar_estado_dispositivo_riesgo_endpoint(dispositivo_riesgo_id: int, datos_estado: DispositivoRiesgoActualizarEstado, db: Session = Depends(obtener_bd)):
    """📌 Actualiza el estado de un riesgo asignado a un dispositivo."""
    resultado = actualizar_estado_dispositivo_riesgo(dispositivo_riesgo_id, datos_estado, db)
    return respuesta_exitosa("Estado del riesgo en el dispositivo actualizado correctamente", resultado)

@router.delete("/eliminar/{dispositivo_riesgo_id}")
def eliminar_riesgo_de_dispositivo_endpoint(dispositivo_riesgo_id: int, db: Session = Depends(obtener_bd)):
    """📌 Elimina un riesgo asignado a un dispositivo."""
    eliminar_riesgo_de_dispositivo(dispositivo_riesgo_id, db)
    return respuesta_exitosa("Riesgo eliminado del dispositivo correctamente")

@router.get("/listar_todas")
def listar_todas_relaciones_endpoint(db: Session = Depends(obtener_bd)):
    """📌 Obtiene todas las relaciones dispositivo-riesgo registradas."""
    relaciones = listar_todas_las_relaciones(db)
    return respuesta_exitosa("Lista de todas las relaciones dispositivo-riesgo obtenida", relaciones)
