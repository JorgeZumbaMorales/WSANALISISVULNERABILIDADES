from sqlalchemy.orm import Session
from app.modelos.tipo_alerta import TipoAlerta
from app.esquemas.tipo_alerta_esquemas import TipoAlertaCrear, TipoAlertaActualizar
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_tipo_alerta(datos: TipoAlertaCrear, db: Session):
    nuevo_tipo_alerta = TipoAlerta(
        nombre_tipo=datos.nombre_tipo
    )
    db.add(nuevo_tipo_alerta)
    db.commit()
    db.refresh(nuevo_tipo_alerta)
    return nuevo_tipo_alerta

def listar_tipos_alerta(db: Session):
    return db.query(TipoAlerta).all()

def actualizar_tipo_alerta(tipo_alerta_id: int, datos: TipoAlertaActualizar, db: Session):
    tipo_alerta_existente = db.query(TipoAlerta).filter(TipoAlerta.tipo_alerta_id == tipo_alerta_id).first()
    if not tipo_alerta_existente:
        excepcion_no_encontrado("Tipo de alerta")

    tipo_alerta_existente.nombre_tipo = datos.nombre_tipo

    db.commit()
    db.refresh(tipo_alerta_existente)
    return tipo_alerta_existente

def eliminar_tipo_alerta(tipo_alerta_id: int, db: Session):
    tipo_alerta_existente = db.query(TipoAlerta).filter(TipoAlerta.tipo_alerta_id == tipo_alerta_id).first()
    if not tipo_alerta_existente:
        excepcion_no_encontrado("Tipo de alerta")

    db.delete(tipo_alerta_existente)
    db.commit()
    return {"mensaje": "Tipo de alerta eliminado exitosamente"}
