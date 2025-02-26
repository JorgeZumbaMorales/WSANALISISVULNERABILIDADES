from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.servicios.usuario_servicio import crear_usuario
from app.servicios.rol_usuario_servicio import crear_rol_usuario
from app.esquemas.usuario_esquemas import UsuarioCrear
from app.esquemas.rol_usuario_esquemas import RolUsuarioCrear

def crear_usuario_con_rol(datos_usuario: UsuarioCrear, rol_id: int, db: Session):

    """
    Crea un usuario y le asigna un rol dentro de una transacción.
    - Llama a `crear_usuario` para agregarlo a la tabla `usuarios`.
    - Usa `crear_rol_usuario` para asignarle un rol en `rol_usuario`.
    - Si algo falla, revierte toda la transacción.
    """

    try:
        # **1️⃣ Crear usuario usando la función existente**
        usuario_creado = crear_usuario(datos_usuario, db)

        # **2️⃣ Crear relación usuario-rol usando la función existente**
        datos_rol = RolUsuarioCrear(
            usuario_id=usuario_creado.usuario_id,
            rol_id=rol_id 
        )
        rol_usuario_creado = crear_rol_usuario(datos_rol, db)

        # **3️⃣ Confirmar transacción**
        db.commit()
        db.refresh(usuario_creado)
        db.refresh(rol_usuario_creado)

        return {
            "mensaje": "Usuario y rol asignados correctamente",
            "usuario": usuario_creado,
            "rol_usuario": rol_usuario_creado
        }

    except SQLAlchemyError as e:
        db.rollback()  # **❌ Si algo falla, revertimos la transacción**
        raise HTTPException(status_code=500, detail=f"Error en la transacción: {str(e)}")
