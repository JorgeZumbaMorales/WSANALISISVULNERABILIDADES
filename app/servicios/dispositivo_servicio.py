from sqlalchemy.orm import Session
from app.modelos.dispositivo import Dispositivo
from app.esquemas.dispositivo_esquemas import DispositivoCrear, DispositivoActualizar
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_dispositivo(datos_dispositivo: DispositivoCrear, db: Session):
    nuevo_dispositivo = Dispositivo(
        nombre_dispositivo=datos_dispositivo.nombre_dispositivo,
        ip_address=datos_dispositivo.ip_address,
        sistema_operativo=datos_dispositivo.sistema_operativo,
        tipo=datos_dispositivo.tipo
    )
    db.add(nuevo_dispositivo)
    db.commit()
    db.refresh(nuevo_dispositivo)
    return nuevo_dispositivo

def listar_dispositivos(db: Session):
    return db.query(Dispositivo).all()

def actualizar_dispositivo(dispositivo_id: int, datos_dispositivo: DispositivoActualizar, db: Session):
    dispositivo = db.query(Dispositivo).filter(Dispositivo.dispositivo_id == dispositivo_id).first()
    if not dispositivo:
        excepcion_no_encontrado("Dispositivo")

    for key, value in datos_dispositivo.dict(exclude_unset=True).items():
        setattr(dispositivo, key, value)

    db.commit()
    db.refresh(dispositivo)
    return dispositivo

def actualizar_estado_dispositivo(dispositivo_id: int, estado: bool, db: Session):
    dispositivo = db.query(Dispositivo).filter(Dispositivo.dispositivo_id == dispositivo_id).first()
    if not dispositivo:
        excepcion_no_encontrado("Dispositivo")

    dispositivo.estado = estado
    db.commit()
    db.refresh(dispositivo)
    return dispositivo

def eliminar_dispositivo(dispositivo_id: int, db: Session):
    dispositivo = db.query(Dispositivo).filter(Dispositivo.dispositivo_id == dispositivo_id).first()
    if not dispositivo:
        excepcion_no_encontrado("Dispositivo")

    db.delete(dispositivo)
    db.commit()
    return respuesta_exitosa("Dispositivo eliminado exitosamente")
