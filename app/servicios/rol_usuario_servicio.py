from sqlalchemy.orm import Session
from app.modelos.rol_usuario import RolUsuario
from app.esquemas.rol_usuario_esquemas import RolUsuarioCrear, RolUsuarioActualizar, RolUsuarioActualizarEstado
from fastapi import HTTPException
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_rol_usuario(datos: RolUsuarioCrear, db: Session):
    nuevo_rol_usuario = RolUsuario(
        usuario_id=datos.usuario_id,
        rol_id=datos.rol_id
    )
    db.add(nuevo_rol_usuario)
    db.commit()
    db.refresh(nuevo_rol_usuario)
    return nuevo_rol_usuario

def listar_roles_usuarios(db: Session):
    return db.query(RolUsuario).all()

def actualizar_rol_usuario(rol_usuario_id: int, datos: RolUsuarioActualizar, db: Session):
    rol_usuario = db.query(RolUsuario).filter(RolUsuario.rol_usuario_id == rol_usuario_id).first()
    if not rol_usuario:
        excepcion_no_encontrado("Rol-Usuario")

    rol_usuario.usuario_id = datos.usuario_id
    rol_usuario.rol_id = datos.rol_id

    db.commit()
    db.refresh(rol_usuario)
    return rol_usuario

def actualizar_estado_rol_usuario(rol_usuario_id: int, datos: RolUsuarioActualizarEstado, db: Session):
    rol_usuario = db.query(RolUsuario).filter(RolUsuario.rol_usuario_id == rol_usuario_id).first()
    if not rol_usuario:
        excepcion_no_encontrado("Rol-Usuario")

    rol_usuario.estado = datos.estado

    db.commit()
    db.refresh(rol_usuario)
    return rol_usuario

def eliminar_rol_usuario(rol_usuario_id: int, db: Session):
    rol_usuario = db.query(RolUsuario).filter(RolUsuario.rol_usuario_id == rol_usuario_id).first()
    if not rol_usuario:
        excepcion_no_encontrado("Rol-Usuario")

    db.delete(rol_usuario)
    db.commit()
    return respuesta_exitosa("Rol-Usuario eliminado exitosamente")
