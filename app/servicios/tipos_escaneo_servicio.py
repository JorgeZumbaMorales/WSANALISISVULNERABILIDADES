from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.tipos_escaneo import TiposEscaneo
from app.esquemas.tipos_escaneo_esquemas import (
    TiposEscaneoCrear,
    TiposEscaneoActualizar
)

def crear_tipo_escaneo(datos: TiposEscaneoCrear, db: Session):
    nuevo_tipo = TiposEscaneo(
        nombre_tipo=datos.nombre_tipo,
        descripcion=datos.descripcion
    )
    db.add(nuevo_tipo)
    db.commit()
    db.refresh(nuevo_tipo)
    return nuevo_tipo

def obtener_tipo_escaneo(db: Session, tipo_escaneo_id: int):
    tipo = db.query(TiposEscaneo).filter(
        TiposEscaneo.tipo_escaneo_id == tipo_escaneo_id
    ).first()
    
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de escaneo no encontrado")
    
    return tipo

def actualizar_tipo_escaneo(tipo_escaneo_id: int, datos: TiposEscaneoActualizar, db: Session):
    tipo = obtener_tipo_escaneo(db, tipo_escaneo_id)

    if datos.nombre_tipo is not None:
        tipo.nombre_tipo = datos.nombre_tipo
    if datos.descripcion is not None:
        tipo.descripcion = datos.descripcion
    if datos.estado is not None:
        tipo.estado = datos.estado

    db.commit()
    db.refresh(tipo)
    return tipo

def eliminar_tipo_escaneo(tipo_escaneo_id: int, db: Session):
    tipo = obtener_tipo_escaneo(db, tipo_escaneo_id)
    db.delete(tipo)
    db.commit()
    return {"message": "Tipo de escaneo eliminado exitosamente"}

def listar_tipos_escaneo(db: Session):
    return db.query(TiposEscaneo).all()
