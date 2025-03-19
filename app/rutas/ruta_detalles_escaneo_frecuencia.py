from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa, excepcion_no_encontrado
from app.esquemas.detalles_escaneo_frecuencia_esquemas import (
    DetallesEscaneoFrecuenciaCrear,
    DetallesEscaneoFrecuenciaActualizar
)
from app.servicios.detalles_escaneo_frecuencia_servicio import (
    crear_detalles_frecuencia,
    obtener_detalles_frecuencia,
    actualizar_detalles_frecuencia,
    eliminar_detalles_frecuencia,
    listar_detalles_frecuencia
)

router = APIRouter(
    prefix="/detalles_escaneo_frecuencia",
    tags=["Detalles de Escaneo por Frecuencia"]
)

@router.post("/crear")
def crear_detalles_frecuencia_endpoint(datos: DetallesEscaneoFrecuenciaCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_detalles_frecuencia(datos, db)
    return respuesta_exitosa("Configuración de frecuencia creada exitosamente", resultado)

@router.get("/listar")
def listar_detalles_frecuencia_endpoint(db: Session = Depends(obtener_bd)):
    configuraciones = listar_detalles_frecuencia(db)
    return respuesta_exitosa("Lista de configuraciones de frecuencia obtenida", configuraciones)

@router.get("/{frecuencia_id}")
def obtener_detalles_frecuencia_endpoint(frecuencia_id: int, db: Session = Depends(obtener_bd)):
    configuracion = obtener_detalles_frecuencia(db, frecuencia_id)
    if not configuracion:
        excepcion_no_encontrado("Configuración de Frecuencia")
    return respuesta_exitosa("Configuración de frecuencia encontrada", configuracion)

@router.put("/actualizar/{frecuencia_id}")
def actualizar_detalles_frecuencia_endpoint(frecuencia_id: int, datos: DetallesEscaneoFrecuenciaActualizar, db: Session = Depends(obtener_bd)):
    resultado = actualizar_detalles_frecuencia(frecuencia_id, datos, db)
    return respuesta_exitosa("Configuración de frecuencia actualizada correctamente", resultado)

@router.delete("/eliminar/{frecuencia_id}")
def eliminar_detalles_frecuencia_endpoint(frecuencia_id: int, db: Session = Depends(obtener_bd)):
    eliminar_detalles_frecuencia(frecuencia_id, db)
    return respuesta_exitosa("Configuración de frecuencia eliminada exitosamente")
