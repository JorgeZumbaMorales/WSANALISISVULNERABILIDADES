from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.historial_vulnerabilidad_esquemas import HistorialVulnerabilidadCrear
from app.servicios.historial_vulnerabilidad_servicio import (
    crear_historial_vulnerabilidad,
    listar_historial_vulnerabilidades,
    obtener_historial_por_vulnerabilidad
)

router = APIRouter(
    prefix="/historial_vulnerabilidades",
    tags=["Historial Vulnerabilidades"]
)

@router.post("/crear_historial_vulnerabilidad")
def crear_historial_vulnerabilidad_endpoint(datos: HistorialVulnerabilidadCrear, db: Session = Depends(obtener_bd)):
    historial = crear_historial_vulnerabilidad(datos, db)
    return respuesta_exitosa("Historial de vulnerabilidad creado exitosamente", historial)

@router.get("/listar_historial_vulnerabilidades")
def listar_historial_vulnerabilidades_endpoint(db: Session = Depends(obtener_bd)):
    historial = listar_historial_vulnerabilidades(db)
    return respuesta_exitosa("Lista del historial de vulnerabilidades obtenida exitosamente", historial)

@router.get("/obtener_historial_por_vulnerabilidad/{vulnerabilidad_id}")
def obtener_historial_por_vulnerabilidad_endpoint(vulnerabilidad_id: int, db: Session = Depends(obtener_bd)):
    historial = obtener_historial_por_vulnerabilidad(vulnerabilidad_id, db)
    return respuesta_exitosa(f"Historial de vulnerabilidad {vulnerabilidad_id} obtenido exitosamente", historial)
