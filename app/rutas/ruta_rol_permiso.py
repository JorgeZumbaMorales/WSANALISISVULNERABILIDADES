from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.rol_permiso_esquemas import RolPermisoCrear, RolPermisoActualizar, RolPermisoActualizarEstado
from app.servicios.rol_permiso_servicio import (
    crear_rol_permiso,
    listar_roles_permisos,
    actualizar_rol_permiso,
    actualizar_estado_rol_permiso,
    eliminar_rol_permiso
)

router = APIRouter(
    prefix="/roles_permisos",
    tags=["Roles-Permisos"]
)

@router.post("/crear_rol_permiso")
def crear_rol_permiso_endpoint(datos: RolPermisoCrear, db: Session = Depends(obtener_bd)):
    rol_permiso = crear_rol_permiso(datos, db)
    return respuesta_exitosa("Rol-Permiso creado exitosamente", rol_permiso)

@router.get("/listar_roles_permisos")
def listar_roles_permisos_endpoint(db: Session = Depends(obtener_bd)):
    roles_permisos = listar_roles_permisos(db)
    return respuesta_exitosa("Lista de roles-permisos obtenida exitosamente", roles_permisos)

@router.put("/actualizar_rol_permiso/{rol_permiso_id}")
def actualizar_rol_permiso_endpoint(rol_permiso_id: int, datos: RolPermisoActualizar, db: Session = Depends(obtener_bd)):
    rol_permiso = actualizar_rol_permiso(rol_permiso_id, datos, db)
    return respuesta_exitosa("Rol-Permiso actualizado exitosamente", rol_permiso)

@router.put("/actualizar_estado_rol_permiso/{rol_permiso_id}")
def actualizar_estado_rol_permiso_endpoint(rol_permiso_id: int, datos: RolPermisoActualizarEstado, db: Session = Depends(obtener_bd)):
    rol_permiso = actualizar_estado_rol_permiso(rol_permiso_id, datos, db)
    return respuesta_exitosa("Estado del Rol-Permiso actualizado exitosamente", rol_permiso)

@router.delete("/eliminar_rol_permiso/{rol_permiso_id}")
def eliminar_rol_permiso_endpoint(rol_permiso_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_rol_permiso(rol_permiso_id, db)
