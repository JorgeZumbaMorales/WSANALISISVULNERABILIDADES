from sqlalchemy.orm import Session
from app.modelos.politica import Politica
from app.esquemas.politica_esquemas import (
    PoliticaCrear,
    PoliticaActualizar,
    PoliticaActualizarEstado,
)
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_politica(datos: PoliticaCrear, db: Session):
    nueva_politica = Politica(
        nombre_politica=datos.nombre_politica,
        descripcion=datos.descripcion
    )
    db.add(nueva_politica)
    db.commit()
    db.refresh(nueva_politica)
    return nueva_politica

def listar_politicas(db: Session):
    return db.query(Politica).all()

def actualizar_politica(politica_id: int, datos: PoliticaActualizar, db: Session):
    politica = db.query(Politica).filter(Politica.politica_id == politica_id).first()
    if not politica:
        excepcion_no_encontrado("Política")

    if datos.nombre_politica:
        politica.nombre_politica = datos.nombre_politica
    if datos.descripcion:
        politica.descripcion = datos.descripcion

    db.commit()
    db.refresh(politica)
    return politica

def actualizar_estado_politica(politica_id: int, datos: PoliticaActualizarEstado, db: Session):
    politica = db.query(Politica).filter(Politica.politica_id == politica_id).first()
    if not politica:
        excepcion_no_encontrado("Política")

    politica.estado = datos.estado

    db.commit()
    db.refresh(politica)
    return politica

def eliminar_politica(politica_id: int, db: Session):
    politica = db.query(Politica).filter(Politica.politica_id == politica_id).first()
    if not politica:
        excepcion_no_encontrado("Política")

    db.delete(politica)
    db.commit()
    return {"mensaje": "Política eliminada exitosamente"}
