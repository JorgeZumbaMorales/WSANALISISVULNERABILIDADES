from sqlalchemy.orm import Session
from app.modelos.herramienta import Herramienta
from app.esquemas.herramienta_esquemas import (
    HerramientaCrear,
    HerramientaActualizar,
    HerramientaActualizarEstado,
)
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_herramienta(datos: HerramientaCrear, db: Session):
    nueva_herramienta = Herramienta(
        nombre_herramienta=datos.nombre_herramienta,
        descripcion=datos.descripcion
    )
    db.add(nueva_herramienta)
    db.commit()
    db.refresh(nueva_herramienta)
    return nueva_herramienta

def listar_herramientas(db: Session):
    return db.query(Herramienta).all()

def actualizar_herramienta(herramienta_id: int, datos: HerramientaActualizar, db: Session):
    herramienta = db.query(Herramienta).filter(Herramienta.herramienta_id == herramienta_id).first()
    if not herramienta:
        excepcion_no_encontrado("Herramienta")

    if datos.nombre_herramienta:
        herramienta.nombre_herramienta = datos.nombre_herramienta
    if datos.descripcion:
        herramienta.descripcion = datos.descripcion

    db.commit()
    db.refresh(herramienta)
    return herramienta

def actualizar_estado_herramienta(herramienta_id: int, datos: HerramientaActualizarEstado, db: Session):
    herramienta = db.query(Herramienta).filter(Herramienta.herramienta_id == herramienta_id).first()
    if not herramienta:
        excepcion_no_encontrado("Herramienta")

    herramienta.estado = datos.estado

    db.commit()
    db.refresh(herramienta)
    return herramienta

def eliminar_herramienta(herramienta_id: int, db: Session):
    herramienta = db.query(Herramienta).filter(Herramienta.herramienta_id == herramienta_id).first()
    if not herramienta:
        excepcion_no_encontrado("Herramienta")

    db.delete(herramienta)
    db.commit()
    return {"mensaje": "Herramienta eliminada exitosamente"}
