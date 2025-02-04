from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.vulnerabilidad_esquemas import (
    VulnerabilidadCrear,
    VulnerabilidadActualizar,
    VulnerabilidadActualizarEstado
)
from app.servicios.vulnerabilidad_servicio import (
    crear_vulnerabilidad,
    listar_vulnerabilidades,
    actualizar_vulnerabilidad,
    actualizar_estado_vulnerabilidad,
    eliminar_vulnerabilidad
)

router = APIRouter(
    prefix="/vulnerabilidades",
    tags=["Vulnerabilidades"]
)

@router.post("/crear_vulnerabilidad")
def crear_vulnerabilidad_endpoint(datos: VulnerabilidadCrear, db: Session = Depends(obtener_bd)):
    vulnerabilidad = crear_vulnerabilidad(datos, db)
    return respuesta_exitosa("Vulnerabilidad creada exitosamente", vulnerabilidad)

@router.get("/listar_vulnerabilidades")
def listar_vulnerabilidades_endpoint(db: Session = Depends(obtener_bd)):
    vulnerabilidades = listar_vulnerabilidades(db)
    return respuesta_exitosa("Lista de vulnerabilidades obtenida exitosamente", vulnerabilidades)

@router.put("/actualizar_vulnerabilidad/{vulnerabilidad_id}")
def actualizar_vulnerabilidad_endpoint(vulnerabilidad_id: int, datos: VulnerabilidadActualizar, db: Session = Depends(obtener_bd)):
    vulnerabilidad = actualizar_vulnerabilidad(vulnerabilidad_id, datos, db)
    return respuesta_exitosa("Vulnerabilidad actualizada exitosamente", vulnerabilidad)

@router.put("/actualizar_estado_vulnerabilidad/{vulnerabilidad_id}")
def actualizar_estado_vulnerabilidad_endpoint(vulnerabilidad_id: int, datos: VulnerabilidadActualizarEstado, db: Session = Depends(obtener_bd)):
    vulnerabilidad = actualizar_estado_vulnerabilidad(vulnerabilidad_id, datos.estado, db)
    return respuesta_exitosa("Estado de la vulnerabilidad actualizado exitosamente", vulnerabilidad)

@router.delete("/eliminar_vulnerabilidad/{vulnerabilidad_id}")
def eliminar_vulnerabilidad_endpoint(vulnerabilidad_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_vulnerabilidad(vulnerabilidad_id, db)
