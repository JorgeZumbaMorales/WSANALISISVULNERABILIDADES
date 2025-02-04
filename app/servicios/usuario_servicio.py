from sqlalchemy.orm import Session
from app.modelos.usuario import Usuario
from app.esquemas.usuario_esquemas import UsuarioCrear, UsuarioActualizar, UsuarioActualizarEstado
from fastapi import HTTPException

def crear_usuario(datos_usuario: UsuarioCrear, db: Session):
    nuevo_usuario = Usuario(
        nombre_usuario=datos_usuario.nombre_usuario,
        contrasena=datos_usuario.contrasena,
        nombres_completos=datos_usuario.nombres_completos,
        apellidos_completos=datos_usuario.apellidos_completos,
        email=datos_usuario.email,
        telefono=datos_usuario.telefono
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def listar_usuarios(db: Session):
    return db.query(Usuario).all()

def actualizar_usuario(usuario_id: int, datos_usuario: UsuarioActualizar, db: Session):
    usuario_existente = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if datos_usuario.nombre_usuario:
        usuario_existente.nombre_usuario = datos_usuario.nombre_usuario
    if datos_usuario.contrasena:
        usuario_existente.contrasena = datos_usuario.contrasena
    if datos_usuario.nombres_completos:
        usuario_existente.nombres_completos = datos_usuario.nombres_completos
    if datos_usuario.apellidos_completos:
        usuario_existente.apellidos_completos = datos_usuario.apellidos_completos
    if datos_usuario.email:
        usuario_existente.email = datos_usuario.email
    if datos_usuario.telefono:
        usuario_existente.telefono = datos_usuario.telefono

    db.commit()
    db.refresh(usuario_existente)
    return usuario_existente

def actualizar_estado_usuario(usuario_id: int, datos_estado: UsuarioActualizarEstado, db: Session):
    usuario_existente = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario_existente.estado = datos_estado.estado

    db.commit()
    db.refresh(usuario_existente)
    return usuario_existente

def eliminar_usuario(usuario_id: int, db: Session):
    usuario_existente = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario_existente)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}
