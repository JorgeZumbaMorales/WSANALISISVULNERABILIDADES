from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa, excepcion_no_encontrado
from app.esquemas.detalles_escaneo_hora_esquemas import (
    DetallesEscaneoHoraCrear,
    DetallesEscaneoHoraActualizar
)
from app.servicios.detalles_escaneo_hora_servicio import (
    crear_detalles_hora,
    obtener_detalles_hora,
    actualizar_detalles_hora,
    eliminar_detalles_hora,
    listar_detalles_hora
)

router = APIRouter(
    prefix="/detalles_escaneo_hora",
    tags=["Detalles de Escaneo por Hora"]
)

@router.post("/crear")
def crear_detalles_hora_endpoint(datos: DetallesEscaneoHoraCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_detalles_hora(datos, db)
    return respuesta_exitosa("Configuración de hora creada exitosamente", resultado)

@router.get("/listar")
def listar_detalles_hora_endpoint(db: Session = Depends(obtener_bd)):
    configuraciones = listar_detalles_hora(db)
    return respuesta_exitosa("Lista de configuraciones de hora obtenida", configuraciones)

@router.get("/{hora_id}")
def obtener_detalles_hora_endpoint(hora_id: int, db: Session = Depends(obtener_bd)):
    configuracion = obtener_detalles_hora(db, hora_id)
    if not configuracion:
        excepcion_no_encontrado("Configuración de Hora")
    return respuesta_exitosa("Configuración de hora encontrada", configuracion)

@router.put("/actualizar/{hora_id}")
def actualizar_detalles_hora_endpoint(hora_id: int, datos: DetallesEscaneoHoraActualizar, db: Session = Depends(obtener_bd)):
    resultado = actualizar_detalles_hora(hora_id, datos, db)
    return respuesta_exitosa("Configuración de hora actualizada correctamente", resultado)

@router.delete("/eliminar/{hora_id}")
def eliminar_detalles_hora_endpoint(hora_id: int, db: Session = Depends(obtener_bd)):
    eliminar_detalles_hora(hora_id, db)
    return respuesta_exitosa("Configuración de hora eliminada exitosamente")
