from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.regla_esquemas import (
    ReglaCrear,
    ReglaActualizar,
    ReglaActualizarEstado,
)
from app.servicios.regla_servicio import (
    crear_regla,
    listar_reglas,
    actualizar_regla,
    actualizar_estado_regla,
    eliminar_regla,
)

router = APIRouter(
    prefix="/reglas",
    tags=["Reglas"]
)

@router.post("/crear_regla")
def crear_regla_endpoint(datos: ReglaCrear, db: Session = Depends(obtener_bd)):
    regla = crear_regla(datos, db)
    return respuesta_exitosa("Regla creada exitosamente", regla)

@router.get("/listar_reglas")
def listar_reglas_endpoint(db: Session = Depends(obtener_bd)):
    reglas = listar_reglas(db)
    return respuesta_exitosa("Lista de reglas obtenida exitosamente", reglas)

@router.put("/actualizar_regla/{regla_id}")
def actualizar_regla_endpoint(regla_id: int, datos: ReglaActualizar, db: Session = Depends(obtener_bd)):
    regla = actualizar_regla(regla_id, datos, db)
    return respuesta_exitosa("Regla actualizada exitosamente", regla)

@router.put("/actualizar_estado_regla/{regla_id}")
def actualizar_estado_regla_endpoint(regla_id: int, datos: ReglaActualizarEstado, db: Session = Depends(obtener_bd)):
    regla = actualizar_estado_regla(regla_id, datos, db)
    return respuesta_exitosa("Estado de la regla actualizado exitosamente", regla)

@router.delete("/eliminar_regla/{regla_id}")
def eliminar_regla_endpoint(regla_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_regla(regla_id, db)
