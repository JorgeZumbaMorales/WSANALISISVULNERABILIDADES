from sqlalchemy.orm import Session
from app.modelos.canal_alerta import CanalAlerta
from app.esquemas.canal_alerta_esquemas import CanalAlertaCrear, CanalAlertaActualizar
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_canal_alerta(datos: CanalAlertaCrear, db: Session):
    nuevo_canal_alerta = CanalAlerta(
        nombre_canal=datos.nombre_canal
    )
    db.add(nuevo_canal_alerta)
    db.commit()
    db.refresh(nuevo_canal_alerta)
    return nuevo_canal_alerta

def listar_canales_alerta(db: Session):
    return db.query(CanalAlerta).all()

def actualizar_canal_alerta(canal_alerta_id: int, datos: CanalAlertaActualizar, db: Session):
    canal_alerta_existente = db.query(CanalAlerta).filter(CanalAlerta.canal_alerta_id == canal_alerta_id).first()
    if not canal_alerta_existente:
        excepcion_no_encontrado("Canal de alerta")

    canal_alerta_existente.nombre_canal = datos.nombre_canal

    db.commit()
    db.refresh(canal_alerta_existente)
    return canal_alerta_existente

def eliminar_canal_alerta(canal_alerta_id: int, db: Session):
    canal_alerta_existente = db.query(CanalAlerta).filter(CanalAlerta.canal_alerta_id == canal_alerta_id).first()
    if not canal_alerta_existente:
        excepcion_no_encontrado("Canal de alerta")

    db.delete(canal_alerta_existente)
    db.commit()
    return {"mensaje": "Canal de alerta eliminado exitosamente"}
