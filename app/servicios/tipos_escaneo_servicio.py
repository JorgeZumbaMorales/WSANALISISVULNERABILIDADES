from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.modelos.tipos_escaneo import TipoEscaneo
from app.esquemas.tipos_escaneo_esquemas import TipoEscaneoCrear, TipoEscaneoActualizar

def crear_tipo_escaneo(datos: TipoEscaneoCrear, db: Session):
    """
    Crea un nuevo tipo de escaneo.
    """
    try:
        nuevo_tipo = TipoEscaneo(
            nombre_tipo=datos.nombre_tipo,
            descripcion=datos.descripcion,
            estado=datos.estado
        )

        db.add(nuevo_tipo)
        db.commit()
        db.refresh(nuevo_tipo)
        return nuevo_tipo

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en la base de datos: {str(e)}")

def actualizar_tipo_escaneo(tipo_escaneo_id: int, datos: TipoEscaneoActualizar, db: Session):
    """
    Actualiza un tipo de escaneo existente.
    """
    tipo_escaneo = db.query(TipoEscaneo).filter(TipoEscaneo.tipo_escaneo_id == tipo_escaneo_id).first()
    
    if not tipo_escaneo:
        raise HTTPException(status_code=404, detail="Tipo de escaneo no encontrado")

    if datos.nombre_tipo:
        tipo_escaneo.nombre_tipo = datos.nombre_tipo
    if datos.descripcion:
        tipo_escaneo.descripcion = datos.descripcion
    if datos.estado is not None:
        tipo_escaneo.estado = datos.estado

    db.commit()
    db.refresh(tipo_escaneo)
    return tipo_escaneo

def eliminar_tipo_escaneo(tipo_escaneo_id: int, db: Session):
    """
    Elimina un tipo de escaneo.
    """
    tipo_escaneo = db.query(TipoEscaneo).filter(TipoEscaneo.tipo_escaneo_id == tipo_escaneo_id).first()
    
    if not tipo_escaneo:
        raise HTTPException(status_code=404, detail="Tipo de escaneo no encontrado")
    
    db.delete(tipo_escaneo)
    db.commit()
    return {"message": "Tipo de escaneo eliminado exitosamente"}

def obtener_tipo_escaneo(tipo_escaneo_id: int, db: Session):
    """
    Obtiene un tipo de escaneo por su ID.
    """
    tipo_escaneo = db.query(TipoEscaneo).filter(TipoEscaneo.tipo_escaneo_id == tipo_escaneo_id).first()
    
    if not tipo_escaneo:
        raise HTTPException(status_code=404, detail="Tipo de escaneo no encontrado")
    
    return tipo_escaneo

def listar_tipos_escaneo(db: Session):
    """
    Lista todos los tipos de escaneo.
    """
    return db.query(TipoEscaneo).all()
