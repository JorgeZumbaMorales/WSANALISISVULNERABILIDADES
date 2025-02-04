from sqlalchemy.orm import Session
from app.modelos.rol_permiso import RolPermiso
from app.esquemas.rol_permiso_esquemas import RolPermisoCrear, RolPermisoActualizar, RolPermisoActualizarEstado
from fastapi import HTTPException
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_rol_permiso(datos: RolPermisoCrear, db: Session):
    nuevo_rol_permiso = RolPermiso(
        rol_id=datos.rol_id,
        permiso_id=datos.permiso_id
    )
    db.add(nuevo_rol_permiso)
    db.commit()
    db.refresh(nuevo_rol_permiso)
    return nuevo_rol_permiso

def listar_roles_permisos(db: Session):
    return db.query(RolPermiso).all()

def actualizar_rol_permiso(rol_permiso_id: int, datos: RolPermisoActualizar, db: Session):
    rol_permiso = db.query(RolPermiso).filter(RolPermiso.rol_permiso_id == rol_permiso_id).first()
    if not rol_permiso:
        excepcion_no_encontrado("Rol-Permiso")

    rol_permiso.rol_id = datos.rol_id
    rol_permiso.permiso_id = datos.permiso_id

    db.commit()
    db.refresh(rol_permiso)
    return rol_permiso

def actualizar_estado_rol_permiso(rol_permiso_id: int, datos: RolPermisoActualizarEstado, db: Session):
    rol_permiso = db.query(RolPermiso).filter(RolPermiso.rol_permiso_id == rol_permiso_id).first()
    if not rol_permiso:
        excepcion_no_encontrado("Rol-Permiso")

    rol_permiso.estado = datos.estado

    db.commit()
    db.refresh(rol_permiso)
    return rol_permiso

def eliminar_rol_permiso(rol_permiso_id: int, db: Session):
    rol_permiso = db.query(RolPermiso).filter(RolPermiso.rol_permiso_id == rol_permiso_id).first()
    if not rol_permiso:
        excepcion_no_encontrado("Rol-Permiso")

    db.delete(rol_permiso)
    db.commit()
    return respuesta_exitosa("Rol-Permiso eliminado exitosamente")
