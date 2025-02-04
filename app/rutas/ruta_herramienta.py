from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.herramienta_esquemas import (
    HerramientaCrear,
    HerramientaActualizar,
    HerramientaActualizarEstado,
)
from app.servicios.herramienta_servicio import (
    crear_herramienta,
    listar_herramientas,
    actualizar_herramienta,
    actualizar_estado_herramienta,
    eliminar_herramienta,
)

router = APIRouter(
    prefix="/herramientas",
    tags=["Herramientas"]
)

@router.post("/crear_herramienta")
def crear_herramienta_endpoint(datos: HerramientaCrear, db: Session = Depends(obtener_bd)):
    herramienta = crear_herramienta(datos, db)
    return respuesta_exitosa("Herramienta creada exitosamente", herramienta)

@router.get("/listar_herramientas")
def listar_herramientas_endpoint(db: Session = Depends(obtener_bd)):
    herramientas = listar_herramientas(db)
    return respuesta_exitosa("Lista de herramientas obtenida exitosamente", herramientas)

@router.put("/actualizar_herramienta/{herramienta_id}")
def actualizar_herramienta_endpoint(herramienta_id: int, datos: HerramientaActualizar, db: Session = Depends(obtener_bd)):
    herramienta = actualizar_herramienta(herramienta_id, datos, db)
    return respuesta_exitosa("Herramienta actualizada exitosamente", herramienta)

@router.put("/actualizar_estado_herramienta/{herramienta_id}")
def actualizar_estado_herramienta_endpoint(herramienta_id: int, datos: HerramientaActualizarEstado, db: Session = Depends(obtener_bd)):
    herramienta = actualizar_estado_herramienta(herramienta_id, datos, db)
    return respuesta_exitosa("Estado de la herramienta actualizado exitosamente", herramienta)

@router.delete("/eliminar_herramienta/{herramienta_id}")
def eliminar_herramienta_endpoint(herramienta_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_herramienta(herramienta_id, db)
