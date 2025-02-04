from sqlalchemy.orm import Session
from app.modelos.politica_regla import PoliticaRegla
from app.esquemas.politica_regla_esquemas import (
    PoliticaReglaCrear,
    PoliticaReglaActualizar,
    PoliticaReglaActualizarEstado,
)
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_politica_regla(datos: PoliticaReglaCrear, db: Session):
    nueva_politica_regla = PoliticaRegla(
        politica_id=datos.politica_id,
        regla_id=datos.regla_id
    )
    db.add(nueva_politica_regla)
    db.commit()
    db.refresh(nueva_politica_regla)
    return nueva_politica_regla

def listar_politicas_reglas(db: Session):
    return db.query(PoliticaRegla).all()

def actualizar_politica_regla(politica_regla_id: int, datos: PoliticaReglaActualizar, db: Session):
    asociacion = db.query(PoliticaRegla).filter(PoliticaRegla.politica_regla_id == politica_regla_id).first()
    if not asociacion:
        excepcion_no_encontrado("Asociación Política-Regla")

    if datos.politica_id:
        asociacion.politica_id = datos.politica_id
    if datos.regla_id:
        asociacion.regla_id = datos.regla_id

    db.commit()
    db.refresh(asociacion)
    return asociacion

def actualizar_estado_politica_regla(politica_regla_id: int, datos: PoliticaReglaActualizarEstado, db: Session):
    asociacion = db.query(PoliticaRegla).filter(PoliticaRegla.politica_regla_id == politica_regla_id).first()
    if not asociacion:
        excepcion_no_encontrado("Asociación Política-Regla")

    asociacion.estado = datos.estado

    db.commit()
    db.refresh(asociacion)
    return asociacion

def eliminar_politica_regla(politica_regla_id: int, db: Session):
    asociacion = db.query(PoliticaRegla).filter(PoliticaRegla.politica_regla_id == politica_regla_id).first()
    if not asociacion:
        excepcion_no_encontrado("Asociación Política-Regla")

    db.delete(asociacion)
    db.commit()
    return {"mensaje": "Asociación eliminada exitosamente"}
