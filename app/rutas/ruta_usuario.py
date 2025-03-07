from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa
from app.esquemas.usuario_esquemas import UsuarioCrear, UsuarioActualizar, UsuarioActualizarEstado, UsuarioActualizarContrasena
from app.servicios.usuario_servicio import crear_usuario, listar_usuarios, actualizar_usuario, actualizar_estado_usuario, eliminar_usuario,buscar_usuario_por_nombre, buscar_usuario_por_correo, actualizar_contrasena_usuario
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

@router.get("/buscar_por_nombre/{nombre_usuario}")
def buscar_usuario_por_nombre_endpoint(nombre_usuario: str, db: Session = Depends(obtener_bd)):
    """
    📌 Endpoint para buscar un usuario por su nombre de usuario.
    """
    usuario = buscar_usuario_por_nombre(db, nombre_usuario)
    return respuesta_exitosa("Usuario encontrado exitosamente", usuario)

@router.get("/buscar_por_correo/{correo}")
def buscar_usuario_por_correo_endpoint(correo: str, db: Session = Depends(obtener_bd)):
    """
    📌 Endpoint para buscar un usuario por su correo electrónico.
    """
    usuario = buscar_usuario_por_correo(db, correo)
    return respuesta_exitosa("Usuario encontrado exitosamente", usuario)

@router.put("/actualizar_contrasena")
def actualizar_contrasena_endpoint(datos: UsuarioActualizarContrasena, db: Session = Depends(obtener_bd)):
    """
    📌 Endpoint para actualizar solo la contraseña de un usuario.
    """
    resultado = actualizar_contrasena_usuario(db, datos.usuario_id, datos.nueva_contrasena)
    return respuesta_exitosa("Contraseña actualizada exitosamente", resultado)