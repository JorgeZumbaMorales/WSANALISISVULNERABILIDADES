from sqlalchemy.orm import Session
from app.modelos.permiso import Permiso
from app.esquemas.permiso_esquemas import PermisoCrear, PermisoActualizar, PermisoActualizarEstado
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_permiso(datos_permiso: PermisoCrear, db: Session):
    nuevo_permiso = Permiso(
        nombre_permiso=datos_permiso.nombre_permiso,
        descripcion=datos_permiso.descripcion
    )
    db.add(nuevo_permiso)
    db.commit()
    db.refresh(nuevo_permiso)
    return nuevo_permiso

def listar_permisos(db: Session):
    return db.query(Permiso).all()

def actualizar_permiso(permiso_id: int, datos_permiso: PermisoActualizar, db: Session):
    permiso_existente = db.query(Permiso).filter(Permiso.permiso_id == permiso_id).first()
    if not permiso_existente:
        excepcion_no_encontrado("Permiso")

    permiso_existente.nombre_permiso = datos_permiso.nombre_permiso
    permiso_existente.descripcion = datos_permiso.descripcion

    db.commit()
    db.refresh(permiso_existente)
    return permiso_existente

def actualizar_estado_permiso(permiso_id: int, datos_estado: PermisoActualizarEstado, db: Session):
    permiso_existente = db.query(Permiso).filter(Permiso.permiso_id == permiso_id).first()
    if not permiso_existente:
        excepcion_no_encontrado("Permiso")

    permiso_existente.estado = datos_estado.estado
    db.commit()
    db.refresh(permiso_existente)
    return permiso_existente

def eliminar_permiso(permiso_id: int, db: Session):
    permiso_existente = db.query(Permiso).filter(Permiso.permiso_id == permiso_id).first()
    if not permiso_existente:
        excepcion_no_encontrado("Permiso")

    db.delete(permiso_existente)
    db.commit()
    return respuesta_exitosa("Permiso eliminado exitosamente")
