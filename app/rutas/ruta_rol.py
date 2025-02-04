# app/rutas/ruta_rol.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.rol_esquemas import RolCrear, RolActualizar, RolActualizarEstado
from app.servicios.rol_servicio import crear_rol, listar_roles, actualizar_rol, actualizar_estado_rol, eliminar_rol

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.post("/crear_rol")
def crear_rol_endpoint(datos_rol: RolCrear, db: Session = Depends(obtener_bd)):
    rol = crear_rol(datos_rol, db)
    return respuesta_exitosa("Rol creado exitosamente", rol)

@router.get("/listar_roles")
def listar_roles_endpoint(db: Session = Depends(obtener_bd)):
    roles = listar_roles(db)
    return respuesta_exitosa("Lista de roles obtenida exitosamente", roles)

@router.put("/actualizar_rol/{rol_id}")
def actualizar_rol_endpoint(rol_id: int, datos_rol: RolActualizar, db: Session = Depends(obtener_bd)):
    rol = actualizar_rol(rol_id, datos_rol, db)
    return respuesta_exitosa("Rol actualizado exitosamente", rol)

@router.put("/actualizar_estado_rol/{rol_id}")
def actualizar_estado_rol_endpoint(rol_id: int, datos_estado: RolActualizarEstado, db: Session = Depends(obtener_bd)):
    rol = actualizar_estado_rol(rol_id, datos_estado, db)
    return respuesta_exitosa("Estado del rol actualizado exitosamente", rol)

@router.delete("/eliminar_rol/{rol_id}")
def eliminar_rol_endpoint(rol_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_rol(rol_id, db)
