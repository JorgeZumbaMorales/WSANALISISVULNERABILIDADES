from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa, excepcion_no_encontrado
from app.esquemas.configuracion_escaneo_esquemas import (
    ConfiguracionEscaneoCrear,
    ConfiguracionEscaneoActualizar
)
from app.servicios.configuracion_escaneo_servicio import (
    crear_configuracion_escaneo,
    obtener_configuracion_escaneo,
    actualizar_configuracion_escaneo,
    eliminar_configuracion_escaneo,
    listar_configuraciones
)

router = APIRouter(
    prefix="/configuracion_escaneo",
    tags=["Configuración de Escaneos"]
)

@router.post("/crear")
def crear_configuracion_endpoint(datos: ConfiguracionEscaneoCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_configuracion_escaneo(datos, db)
    return respuesta_exitosa("Configuración creada exitosamente", resultado)

@router.get("/listar")
def listar_configuraciones_endpoint(db: Session = Depends(obtener_bd)):
    configuraciones = listar_configuraciones(db)
    return respuesta_exitosa("Lista de configuraciones obtenida", configuraciones)

@router.get("/{configuracion_id}")
def obtener_configuracion_endpoint(configuracion_id: int, db: Session = Depends(obtener_bd)):
    configuracion = obtener_configuracion_escaneo(db, configuracion_id)
    if not configuracion:
        excepcion_no_encontrado("Configuración")
    return respuesta_exitosa("Configuración encontrada", configuracion)

@router.put("/actualizar/{configuracion_id}")
def actualizar_configuracion_endpoint(configuracion_id: int, datos: ConfiguracionEscaneoActualizar, db: Session = Depends(obtener_bd)):
    resultado = actualizar_configuracion_escaneo(configuracion_id, datos, db)
    return respuesta_exitosa("Configuración actualizada correctamente", resultado)

@router.delete("/eliminar/{configuracion_id}")
def eliminar_configuracion_endpoint(configuracion_id: int, db: Session = Depends(obtener_bd)):
    eliminar_configuracion_escaneo(configuracion_id, db)
    return respuesta_exitosa("Configuración eliminada exitosamente")
