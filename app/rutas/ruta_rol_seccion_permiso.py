from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa
from app.esquemas.rol_seccion_permiso_esquemas import RolSeccionPermisoCrear, RolSeccionPermisoActualizar
from app.servicios.rol_seccion_permiso_servicio import (
    crear_rol_seccion_permiso, listar_rol_seccion_permisos, 
    actualizar_estado_rol_seccion_permiso, eliminar_rol_seccion_permiso
)

router = APIRouter(
    prefix="/rol_seccion_permiso",
    tags=["Rol Sección Permiso"]
)

@router.post("/crear_rol_seccion_permiso")
def crear_registro(datos: RolSeccionPermisoCrear, db: Session = Depends(obtener_bd)):
    registro = crear_rol_seccion_permiso(datos, db)
    return respuesta_exitosa("Registro creado exitosamente", registro)

@router.get("/listar_rol_seccion_permiso")
def listar_registros(db: Session = Depends(obtener_bd)):
    registros = listar_rol_seccion_permisos(db)
    return respuesta_exitosa("Lista de registros obtenida exitosamente", registros)

@router.put("/actualizar_estado_rol_seccion_permiso/{rol_seccion_permiso_id}")
def actualizar_estado(rol_seccion_permiso_id: int, datos: RolSeccionPermisoActualizar, db: Session = Depends(obtener_bd)):
    registro = actualizar_estado_rol_seccion_permiso(rol_seccion_permiso_id, datos, db)
    if not registro:
        excepcion_no_encontrado("Registro")
    return respuesta_exitosa("Estado actualizado exitosamente", registro)

@router.delete("/eliminar_rol_seccion_permiso/{rol_seccion_permiso_id}")
def eliminar_registro(rol_seccion_permiso_id: int, db: Session = Depends(obtener_bd)):
    eliminar_rol_seccion_permiso(rol_seccion_permiso_id, db)
    return respuesta_exitosa("Registro eliminado exitosamente")
