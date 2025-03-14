from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa, excepcion_no_encontrado
from app.esquemas.riesgo_esquemas import RiesgoCrear, RiesgoActualizar, RiesgoActualizarEstado
from app.servicios.riesgo_servicio import (
    crear_riesgo, listar_riesgos, actualizar_riesgo, 
    actualizar_estado_riesgo, eliminar_riesgo, obtener_riesgo_por_id
)

router = APIRouter(
    prefix="/riesgos",
    tags=["Riesgos"]
)

@router.post("/crear_riesgo")
def crear_riesgo_endpoint(datos_riesgo: RiesgoCrear, db: Session = Depends(obtener_bd)):
    """📌 Crea un nuevo riesgo en la base de datos."""
    resultado = crear_riesgo(datos_riesgo, db)
    return respuesta_exitosa("Riesgo creado exitosamente", resultado)

@router.get("/listar_riesgos")
def listar_riesgos_endpoint(db: Session = Depends(obtener_bd)):
    """📌 Obtiene la lista de todos los riesgos."""
    riesgos = listar_riesgos(db)
    return respuesta_exitosa("Lista de riesgos obtenida exitosamente", riesgos)

@router.get("/obtener_riesgo/{riesgo_id}")
def obtener_riesgo_endpoint(riesgo_id: int, db: Session = Depends(obtener_bd)):
    """📌 Obtiene un riesgo específico por ID."""
    riesgo = obtener_riesgo_por_id(riesgo_id, db)
    return respuesta_exitosa("Riesgo encontrado exitosamente", riesgo)

@router.put("/actualizar_riesgo/{riesgo_id}")
def actualizar_riesgo_endpoint(riesgo_id: int, datos_riesgo: RiesgoActualizar, db: Session = Depends(obtener_bd)):
    """📌 Actualiza un riesgo específico."""
    riesgo = actualizar_riesgo(riesgo_id, datos_riesgo, db)
    return respuesta_exitosa("Riesgo actualizado exitosamente", riesgo)

@router.put("/actualizar_estado_riesgo/{riesgo_id}")
def actualizar_estado_riesgo_endpoint(riesgo_id: int, datos_estado: RiesgoActualizarEstado, db: Session = Depends(obtener_bd)):
    """📌 Actualiza el estado de un riesgo (activo/inactivo)."""
    riesgo = actualizar_estado_riesgo(riesgo_id, datos_estado, db)
    return respuesta_exitosa("Estado del riesgo actualizado exitosamente", riesgo)

@router.delete("/eliminar_riesgo/{riesgo_id}")
def eliminar_riesgo_endpoint(riesgo_id: int, db: Session = Depends(obtener_bd)):
    """📌 Elimina un riesgo de la base de datos."""
    eliminar_riesgo(riesgo_id, db)
    return respuesta_exitosa("Riesgo eliminado exitosamente")
