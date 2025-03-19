from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.detalles_escaneo_hora import DetallesEscaneoHora
from app.esquemas.detalles_escaneo_hora_esquemas import (
    DetallesEscaneoHoraCrear,
    DetallesEscaneoHoraActualizar
)

def crear_detalles_hora(datos: DetallesEscaneoHoraCrear, db: Session):
    nueva_hora = DetallesEscaneoHora(
        configuracion_escaneo_id=datos.configuracion_escaneo_id,
        hora_especifica=datos.hora_especifica,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin
    )
    db.add(nueva_hora)
    db.commit()
    db.refresh(nueva_hora)
    return nueva_hora

def obtener_detalles_hora(db: Session, hora_id: int):
    hora = db.query(DetallesEscaneoHora).filter(
        DetallesEscaneoHora.hora_id == hora_id
    ).first()
    
    if not hora:
        raise HTTPException(status_code=404, detail="Configuración de hora no encontrada")
    
    return hora

def actualizar_detalles_hora(hora_id: int, datos: DetallesEscaneoHoraActualizar, db: Session):
    hora = obtener_detalles_hora(db, hora_id)
    
    if datos.hora_especifica is not None:
        hora.hora_especifica = datos.hora_especifica
    if datos.fecha_inicio is not None:
        hora.fecha_inicio = datos.fecha_inicio
    if datos.fecha_fin is not None:
        hora.fecha_fin = datos.fecha_fin
    if datos.estado is not None:
        hora.estado = datos.estado
    
    db.commit()
    db.refresh(hora)
    return hora

def eliminar_detalles_hora(hora_id: int, db: Session):
    hora = obtener_detalles_hora(db, hora_id)
    db.delete(hora)
    db.commit()
    return {"message": "Configuración de hora eliminada exitosamente"}

def listar_detalles_hora(db: Session):
    return db.query(DetallesEscaneoHora).all()
