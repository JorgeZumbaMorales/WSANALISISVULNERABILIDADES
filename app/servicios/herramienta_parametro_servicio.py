from sqlalchemy.orm import Session
from app.modelos.herramienta_parametro import HerramientaParametro
from app.esquemas.herramienta_parametro_esquemas import (
    HerramientaParametroCrear,
    HerramientaParametroActualizar,
    HerramientaParametroActualizarEstado,
)
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_herramienta_parametro(datos: HerramientaParametroCrear, db: Session):
    nueva_relacion = HerramientaParametro(
        herramienta_id=datos.herramienta_id,
        parametro_id=datos.parametro_id
    )
    db.add(nueva_relacion)
    db.commit()
    db.refresh(nueva_relacion)
    return nueva_relacion

def listar_herramienta_parametro(db: Session):
    return db.query(HerramientaParametro).all()

def actualizar_herramienta_parametro(relacion_id: int, datos: HerramientaParametroActualizar, db: Session):
    relacion = db.query(HerramientaParametro).filter(HerramientaParametro.herramienta_parametro_id == relacion_id).first()
    if not relacion:
        excepcion_no_encontrado("Relación Herramienta-Parámetro")

    if datos.herramienta_id:
        relacion.herramienta_id = datos.herramienta_id
    if datos.parametro_id:
        relacion.parametro_id = datos.parametro_id

    db.commit()
    db.refresh(relacion)
    return relacion

def actualizar_estado_herramienta_parametro(relacion_id: int, datos: HerramientaParametroActualizarEstado, db: Session):
    relacion = db.query(HerramientaParametro).filter(HerramientaParametro.herramienta_parametro_id == relacion_id).first()
    if not relacion:
        excepcion_no_encontrado("Relación Herramienta-Parámetro")

    relacion.estado = datos.estado

    db.commit()
    db.refresh(relacion)
    return relacion

def eliminar_herramienta_parametro(relacion_id: int, db: Session):
    relacion = db.query(HerramientaParametro).filter(HerramientaParametro.herramienta_parametro_id == relacion_id).first()
    if not relacion:
        excepcion_no_encontrado("Relación Herramienta-Parámetro")

    db.delete(relacion)
    db.commit()
    return {"mensaje": "Relación Herramienta-Parámetro eliminada exitosamente"}
