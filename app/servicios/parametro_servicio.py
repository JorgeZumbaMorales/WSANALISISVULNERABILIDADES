from sqlalchemy.orm import Session
from app.modelos.parametro import Parametro
from app.esquemas.parametro_esquemas import (
    ParametroCrear,
    ParametroActualizar,
    ParametroActualizarEstado,
)
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_parametro(datos: ParametroCrear, db: Session):
    nuevo_parametro = Parametro(
        nombre_parametro=datos.nombre_parametro,
        descripcion=datos.descripcion
    )
    db.add(nuevo_parametro)
    db.commit()
    db.refresh(nuevo_parametro)
    return nuevo_parametro

def listar_parametros(db: Session):
    return db.query(Parametro).all()

def actualizar_parametro(parametro_id: int, datos: ParametroActualizar, db: Session):
    parametro = db.query(Parametro).filter(Parametro.parametro_id == parametro_id).first()
    if not parametro:
        excepcion_no_encontrado("Parámetro")

    if datos.nombre_parametro:
        parametro.nombre_parametro = datos.nombre_parametro
    if datos.descripcion:
        parametro.descripcion = datos.descripcion

    db.commit()
    db.refresh(parametro)
    return parametro

def actualizar_estado_parametro(parametro_id: int, datos: ParametroActualizarEstado, db: Session):
    parametro = db.query(Parametro).filter(Parametro.parametro_id == parametro_id).first()
    if not parametro:
        excepcion_no_encontrado("Parámetro")

    parametro.estado = datos.estado

    db.commit()
    db.refresh(parametro)
    return parametro

def eliminar_parametro(parametro_id: int, db: Session):
    parametro = db.query(Parametro).filter(Parametro.parametro_id == parametro_id).first()
    if not parametro:
        excepcion_no_encontrado("Parámetro")

    db.delete(parametro)
    db.commit()
    return {"mensaje": "Parámetro eliminado exitosamente"}
