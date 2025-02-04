from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.rol_usuario_esquemas import RolUsuarioCrear, RolUsuarioActualizar, RolUsuarioActualizarEstado
from app.servicios.rol_usuario_servicio import (
    crear_rol_usuario,
    listar_roles_usuarios,
    actualizar_rol_usuario,
    actualizar_estado_rol_usuario,
    eliminar_rol_usuario
)

router = APIRouter(
    prefix="/roles_usuarios",
    tags=["Roles-Usuarios"]
)

@router.post("/crear_rol_usuario")
def crear_rol_usuario_endpoint(datos: RolUsuarioCrear, db: Session = Depends(obtener_bd)):
    rol_usuario = crear_rol_usuario(datos, db)
    return respuesta_exitosa("Rol-Usuario creado exitosamente", rol_usuario)

@router.get("/listar_roles_usuarios")
def listar_roles_usuarios_endpoint(db: Session = Depends(obtener_bd)):
    roles_usuarios = listar_roles_usuarios(db)
    return respuesta_exitosa("Lista de roles-usuarios obtenida exitosamente", roles_usuarios)

@router.put("/actualizar_rol_usuario/{rol_usuario_id}")
def actualizar_rol_usuario_endpoint(rol_usuario_id: int, datos: RolUsuarioActualizar, db: Session = Depends(obtener_bd)):
    rol_usuario = actualizar_rol_usuario(rol_usuario_id, datos, db)
    return respuesta_exitosa("Rol-Usuario actualizado exitosamente", rol_usuario)

@router.put("/actualizar_estado_rol_usuario/{rol_usuario_id}")
def actualizar_estado_rol_usuario_endpoint(rol_usuario_id: int, datos: RolUsuarioActualizarEstado, db: Session = Depends(obtener_bd)):
    rol_usuario = actualizar_estado_rol_usuario(rol_usuario_id, datos, db)
    return respuesta_exitosa("Estado del Rol-Usuario actualizado exitosamente", rol_usuario)

@router.delete("/eliminar_rol_usuario/{rol_usuario_id}")
def eliminar_rol_usuario_endpoint(rol_usuario_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_rol_usuario(rol_usuario_id, db)
