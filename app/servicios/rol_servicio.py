# app/servicios/rol_servicio.py
from sqlalchemy.orm import Session
from app.modelos.rol import Rol
from app.esquemas.rol_esquemas import RolCrear, RolActualizar, RolActualizarEstado
from fastapi import HTTPException
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_rol(datos_rol: RolCrear, db: Session):
    nuevo_rol = Rol(
        nombre_rol=datos_rol.nombre_rol,
        descripcion=datos_rol.descripcion
    )
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return nuevo_rol

def listar_roles(db: Session):
    return db.query(Rol).all()

def actualizar_rol(rol_id: int, datos_rol: RolActualizar, db: Session):
    rol_existente = db.query(Rol).filter(Rol.rol_id == rol_id).first()
    if not rol_existente:
        excepcion_no_encontrado("Rol")

    rol_existente.nombre_rol = datos_rol.nombre_rol
    rol_existente.descripcion = datos_rol.descripcion

    db.commit()
    db.refresh(rol_existente)
    return rol_existente

def actualizar_estado_rol(rol_id: int, datos_estado: RolActualizarEstado, db: Session):
    rol_existente = db.query(Rol).filter(Rol.rol_id == rol_id).first()
    if not rol_existente:
        excepcion_no_encontrado("Rol")

    rol_existente.estado = datos_estado.estado

    db.commit()
    db.refresh(rol_existente)
    return rol_existente

def eliminar_rol(rol_id: int, db: Session):
    rol_existente = db.query(Rol).filter(Rol.rol_id == rol_id).first()
    if not rol_existente:
        excepcion_no_encontrado("Rol")

    db.delete(rol_existente)
    db.commit()
    return respuesta_exitosa("Rol eliminado exitosamente")
