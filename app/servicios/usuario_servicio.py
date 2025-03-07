import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modelos.usuario import Usuario
from app.esquemas.usuario_esquemas import UsuarioCrear, UsuarioActualizar, UsuarioActualizarEstado
from fastapi import HTTPException
from app.esquemas.usuario_esquemas import UsuarioLogin

def encriptar_contrasena(contrasena: str) -> str:
    """Hashea la contraseña antes de guardarla en la base de datos."""
    salt = bcrypt.gensalt()
    contrasena_hasheada = bcrypt.hashpw(contrasena.encode('utf-8'), salt)
    return contrasena_hasheada.decode('utf-8')

def verificar_existencia_usuario(db: Session, nombre_usuario: str, email: str, telefono: str):
    """
    Verifica si el nombre de usuario, email o teléfono ya están en uso de forma independiente.
    Retorna un mensaje específico según el campo duplicado.
    """
    if db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")

    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    if db.query(Usuario).filter(Usuario.telefono == telefono).first():
        raise HTTPException(status_code=400, detail="El número de teléfono ya está en uso.")

def crear_usuario(datos_usuario: UsuarioCrear, db: Session):
    verificar_existencia_usuario(db, datos_usuario.nombre_usuario, datos_usuario.email, datos_usuario.telefono)

    try:
        contrasena_segura = encriptar_contrasena(datos_usuario.contrasena)

        nuevo_usuario = Usuario(
            nombre_usuario=datos_usuario.nombre_usuario,
            contrasena=contrasena_segura,
            nombres_completos=datos_usuario.nombres_completos,
            apellidos_completos=datos_usuario.apellidos_completos,
            email=datos_usuario.email,
            telefono=datos_usuario.telefono
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en la base de datos: {str(e)}")
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno al crear usuario: {str(e)}")

def actualizar_usuario(usuario_id: int, datos_usuario: UsuarioActualizar, db: Session):
    usuario_existente = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos_usuario.nombre_usuario and datos_usuario.nombre_usuario != usuario_existente.nombre_usuario:
        if db.query(Usuario).filter(Usuario.nombre_usuario == datos_usuario.nombre_usuario).first():
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")

    if datos_usuario.email and datos_usuario.email != usuario_existente.email:
        if db.query(Usuario).filter(Usuario.email == datos_usuario.email).first():
            raise HTTPException(status_code=400, detail="El email ya está registrado.")

    if datos_usuario.telefono and datos_usuario.telefono != usuario_existente.telefono:
        if db.query(Usuario).filter(Usuario.telefono == datos_usuario.telefono).first():
            raise HTTPException(status_code=400, detail="El número de teléfono ya está en uso.")

    # 🔹 Se actualizan todos los campos EXCEPTO la contraseña
    if datos_usuario.nombre_usuario:
        usuario_existente.nombre_usuario = datos_usuario.nombre_usuario
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


def buscar_usuario_por_nombre(db: Session, nombre_usuario: str):
    """
    Busca un usuario en la base de datos por su nombre de usuario.
    Retorna el usuario si existe, o lanza un error 404 si no se encuentra.
    """
    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario

def buscar_usuario_por_correo(db: Session, correo: str):
    """
    Busca un usuario en la base de datos por su correo electrónico.
    Retorna el usuario si existe, o lanza un error 404 si no se encuentra.
    """
    usuario = db.query(Usuario).filter(Usuario.email == correo).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Correo no encontrado")
    
    return usuario

def listar_usuarios(db: Session):
    return db.query(Usuario).all()

def verificar_credenciales(db: Session, datos: UsuarioLogin):
    """Verifica si el usuario y la contraseña son correctos."""
    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == datos.nombre_usuario).first()
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    if not usuario.estado:
        raise HTTPException(status_code=403, detail="Cuenta desactivada")

    # Comparar contraseña ingresada con la contraseña hasheada en la BD
    if not bcrypt.checkpw(datos.contrasena.encode('utf-8'), usuario.contrasena.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    return usuario  # Si pasa todas las verificaciones, devuelve el usuario

def actualizar_contrasena_usuario(db: Session, usuario_id: int, nueva_contrasena: str):
    """
    📌 Actualiza solo la contraseña de un usuario.
    """
    usuario = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Encriptar la nueva contraseña antes de guardarla
    usuario.contrasena = encriptar_contrasena(nueva_contrasena)

    db.commit()
    db.refresh(usuario)

    return {"message": "Contraseña actualizada correctamente"}
