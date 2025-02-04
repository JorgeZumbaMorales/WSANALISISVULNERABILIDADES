from sqlalchemy.orm import Session
from app.modelos.notificacion import Notificacion
from app.esquemas.notificacion_esquemas import NotificacionCrear, NotificacionActualizar
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_notificacion(datos: NotificacionCrear, db: Session):
    nueva_notificacion = Notificacion(
        mensaje_notificacion=datos.mensaje_notificacion,
        tipo_alerta_id=datos.tipo_alerta_id,
        canal_alerta_id=datos.canal_alerta_id,
        usuario_id=datos.usuario_id,
        dispositivo_id=datos.dispositivo_id,
        vulnerabilidad_id=datos.vulnerabilidad_id
    )
    db.add(nueva_notificacion)
    db.commit()
    db.refresh(nueva_notificacion)
    return nueva_notificacion

def listar_notificaciones(db: Session):
    return db.query(Notificacion).all()

def actualizar_notificacion(notificacion_id: int, datos: NotificacionActualizar, db: Session):
    notificacion_existente = db.query(Notificacion).filter(Notificacion.notificacion_id == notificacion_id).first()
    if not notificacion_existente:
        excepcion_no_encontrado("Notificación")

    if datos.mensaje_notificacion:
        notificacion_existente.mensaje_notificacion = datos.mensaje_notificacion
    if datos.fecha_envio:
        notificacion_existente.fecha_envio = datos.fecha_envio

    db.commit()
    db.refresh(notificacion_existente)
    return notificacion_existente

def eliminar_notificacion(notificacion_id: int, db: Session):
    notificacion_existente = db.query(Notificacion).filter(Notificacion.notificacion_id == notificacion_id).first()
    if not notificacion_existente:
        excepcion_no_encontrado("Notificación")

    db.delete(notificacion_existente)
    db.commit()
    return {"mensaje": "Notificación eliminada exitosamente"}
