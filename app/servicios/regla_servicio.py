from sqlalchemy.orm import Session
from app.modelos.regla import Regla
from app.esquemas.regla_esquemas import (
    ReglaCrear,
    ReglaActualizar,
    ReglaActualizarEstado,
)
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_regla(datos: ReglaCrear, db: Session):
    nueva_regla = Regla(
        nombre_regla=datos.nombre_regla,
        descripcion=datos.descripcion,
        herramienta=datos.herramienta,
        parametros=datos.parametros
    )
    db.add(nueva_regla)
    db.commit()
    db.refresh(nueva_regla)
    return nueva_regla

def listar_reglas(db: Session):
    return db.query(Regla).all()

def actualizar_regla(regla_id: int, datos: ReglaActualizar, db: Session):
    regla = db.query(Regla).filter(Regla.regla_id == regla_id).first()
    if not regla:
        excepcion_no_encontrado("Regla")

    if datos.nombre_regla:
        regla.nombre_regla = datos.nombre_regla
    if datos.descripcion:
        regla.descripcion = datos.descripcion
    if datos.herramienta:
        regla.herramienta = datos.herramienta
    if datos.parametros:
        regla.parametros = datos.parametros

    db.commit()
    db.refresh(regla)
    return regla

def actualizar_estado_regla(regla_id: int, datos: ReglaActualizarEstado, db: Session):
    regla = db.query(Regla).filter(Regla.regla_id == regla_id).first()
    if not regla:
        excepcion_no_encontrado("Regla")

    regla.estado = datos.estado

    db.commit()
    db.refresh(regla)
    return regla

def eliminar_regla(regla_id: int, db: Session):
    regla = db.query(Regla).filter(Regla.regla_id == regla_id).first()
    if not regla:
        excepcion_no_encontrado("Regla")

    db.delete(regla)
    db.commit()
    return {"mensaje": "Regla eliminada exitosamente"}
