from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.parametro_esquemas import (
    ParametroCrear,
    ParametroActualizar,
    ParametroActualizarEstado,
)
from app.servicios.parametro_servicio import (
    crear_parametro,
    listar_parametros,
    actualizar_parametro,
    actualizar_estado_parametro,
    eliminar_parametro,
)

router = APIRouter(
    prefix="/parametros",
    tags=["Parámetros"]
)

@router.post("/crear_parametro")
def crear_parametro_endpoint(datos: ParametroCrear, db: Session = Depends(obtener_bd)):
    parametro = crear_parametro(datos, db)
    return respuesta_exitosa("Parámetro creado exitosamente", parametro)

@router.get("/listar_parametros")
def listar_parametros_endpoint(db: Session = Depends(obtener_bd)):
    parametros = listar_parametros(db)
    return respuesta_exitosa("Lista de parámetros obtenida exitosamente", parametros)

@router.put("/actualizar_parametro/{parametro_id}")
def actualizar_parametro_endpoint(parametro_id: int, datos: ParametroActualizar, db: Session = Depends(obtener_bd)):
    parametro = actualizar_parametro(parametro_id, datos, db)
    return respuesta_exitosa("Parámetro actualizado exitosamente", parametro)

@router.put("/actualizar_estado_parametro/{parametro_id}")
def actualizar_estado_parametro_endpoint(parametro_id: int, datos: ParametroActualizarEstado, db: Session = Depends(obtener_bd)):
    parametro = actualizar_estado_parametro(parametro_id, datos, db)
    return respuesta_exitosa("Estado del parámetro actualizado exitosamente", parametro)

@router.delete("/eliminar_parametro/{parametro_id}")
def eliminar_parametro_endpoint(parametro_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_parametro(parametro_id, db)
