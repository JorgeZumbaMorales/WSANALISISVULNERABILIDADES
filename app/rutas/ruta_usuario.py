from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa
from app.esquemas.usuario_esquemas import UsuarioCrear, UsuarioActualizar, UsuarioActualizarEstado
from app.servicios.usuario_servicio import crear_usuario, listar_usuarios, actualizar_usuario, actualizar_estado_usuario, eliminar_usuario
from app.transacciones.transaccion_usuario_rol import crear_usuario_con_rol
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/crear_usuario")
def crear_usuario_endpoint(datos_usuario: UsuarioCrear, rol_id: int, db: Session = Depends(obtener_bd)):
    resultado = crear_usuario_con_rol(datos_usuario, rol_id, db)
    return respuesta_exitosa("Usuario y rol asignado correctamente", resultado)

@router.get("/listar_usuarios")
def listar_usuarios_endpoint(db: Session = Depends(obtener_bd)):
    usuarios = listar_usuarios(db)
    return respuesta_exitosa("Lista de usuarios obtenida exitosamente", usuarios)

@router.put("/actualizar_usuario/{usuario_id}")
def actualizar_usuario_endpoint(usuario_id: int, datos_usuario: UsuarioActualizar, db: Session = Depends(obtener_bd)):
    usuario = actualizar_usuario(usuario_id, datos_usuario, db)
    if not usuario:
        excepcion_no_encontrado("Usuario")
    return respuesta_exitosa("Usuario actualizado exitosamente", usuario)

@router.put("/actualizar_estado_usuario/{usuario_id}")
def actualizar_estado_usuario_endpoint(usuario_id: int, datos_estado: UsuarioActualizarEstado, db: Session = Depends(obtener_bd)):
    usuario = actualizar_estado_usuario(usuario_id, datos_estado, db)
    if not usuario:
        excepcion_no_encontrado("Usuario")
    return respuesta_exitosa("Estado del usuario actualizado exitosamente", usuario)

@router.delete("/eliminar_usuario/{usuario_id}")
def eliminar_usuario_endpoint(usuario_id: int, db: Session = Depends(obtener_bd)):
    eliminar_usuario(usuario_id, db)
    return respuesta_exitosa("Usuario eliminado exitosamente")
