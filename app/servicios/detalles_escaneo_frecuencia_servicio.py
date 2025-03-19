from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.detalles_escaneo_frecuencia import DetallesEscaneoFrecuencia
from app.esquemas.detalles_escaneo_frecuencia_esquemas import (
    DetallesEscaneoFrecuenciaCrear,
    DetallesEscaneoFrecuenciaActualizar
)

def crear_detalles_frecuencia(datos: DetallesEscaneoFrecuenciaCrear, db: Session):
    nueva_frecuencia = DetallesEscaneoFrecuencia(
        configuracion_escaneo_id=datos.configuracion_escaneo_id,
        frecuencia_minutos=datos.frecuencia_minutos,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin
    )
    db.add(nueva_frecuencia)
    db.commit()
    db.refresh(nueva_frecuencia)
    return nueva_frecuencia

def obtener_detalles_frecuencia(db: Session, frecuencia_id: int):
    frecuencia = db.query(DetallesEscaneoFrecuencia).filter(
        DetallesEscaneoFrecuencia.frecuencia_id == frecuencia_id
    ).first()
    
    if not frecuencia:
        raise HTTPException(status_code=404, detail="Configuración de frecuencia no encontrada")
    
    return frecuencia

def actualizar_detalles_frecuencia(frecuencia_id: int, datos: DetallesEscaneoFrecuenciaActualizar, db: Session):
    frecuencia = obtener_detalles_frecuencia(db, frecuencia_id)
    
    if datos.frecuencia_minutos is not None:
        frecuencia.frecuencia_minutos = datos.frecuencia_minutos
    if datos.fecha_inicio is not None:
        frecuencia.fecha_inicio = datos.fecha_inicio
    if datos.fecha_fin is not None:
        frecuencia.fecha_fin = datos.fecha_fin
    if datos.estado is not None:
        frecuencia.estado = datos.estado
    
    db.commit()
    db.refresh(frecuencia)
    return frecuencia

def eliminar_detalles_frecuencia(frecuencia_id: int, db: Session):
    frecuencia = obtener_detalles_frecuencia(db, frecuencia_id)
    db.delete(frecuencia)
    db.commit()
    return {"message": "Configuración de frecuencia eliminada exitosamente"}

def listar_detalles_frecuencia(db: Session):
    return db.query(DetallesEscaneoFrecuencia).all()
