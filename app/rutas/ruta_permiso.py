from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.esquemas.permiso_esquemas import PermisoCrear, PermisoActualizar, PermisoActualizarEstado
from app.servicios.permiso_servicio import (
    crear_permiso, listar_permisos, actualizar_permiso, actualizar_estado_permiso, eliminar_permiso
)
from app.core.respuestas import respuesta_exitosa

router = APIRouter(
    prefix="/permisos",
    tags=["Permisos"]
)

@router.post("/crear_permiso")
def crear_permiso_endpoint(datos_permiso: PermisoCrear, db: Session = Depends(obtener_bd)):
    permiso = crear_permiso(datos_permiso, db)
    return respuesta_exitosa("Permiso creado exitosamente", permiso)

@router.get("/listar_permisos")
def listar_permisos_endpoint(db: Session = Depends(obtener_bd)):
    permisos = listar_permisos(db)
    return respuesta_exitosa("Lista de permisos obtenida exitosamente", permisos)

@router.put("/actualizar_permiso/{permiso_id}")
def actualizar_permiso_endpoint(permiso_id: int, datos_permiso: PermisoActualizar, db: Session = Depends(obtener_bd)):
    permiso = actualizar_permiso(permiso_id, datos_permiso, db)
    return respuesta_exitosa("Permiso actualizado exitosamente", permiso)

@router.put("/actualizar_estado_permiso/{permiso_id}")
def actualizar_estado_permiso_endpoint(permiso_id: int, datos_estado: PermisoActualizarEstado, db: Session = Depends(obtener_bd)):
    permiso = actualizar_estado_permiso(permiso_id, datos_estado, db)
    return respuesta_exitosa("Estado del permiso actualizado exitosamente", permiso)

@router.delete("/eliminar_permiso/{permiso_id}")
def eliminar_permiso_endpoint(permiso_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_permiso(permiso_id, db)
