from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.modelos.riesgo import Riesgo
from app.esquemas.riesgo_esquemas import RiesgoCrear, RiesgoActualizar, RiesgoActualizarEstado

def crear_riesgo(datos_riesgo: RiesgoCrear, db: Session):
    """📌 Crea un nuevo riesgo en la base de datos."""
    try:
        nuevo_riesgo = Riesgo(
            nombre_riesgo=datos_riesgo.nombre_riesgo,
            descripcion=datos_riesgo.descripcion
        )
        db.add(nuevo_riesgo)
        db.commit()
        db.refresh(nuevo_riesgo)
        return nuevo_riesgo

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="El nombre de riesgo ya existe.")

def actualizar_riesgo(riesgo_id: int, datos_riesgo: RiesgoActualizar, db: Session):
    """📌 Actualiza la información de un riesgo."""
    riesgo_existente = db.query(Riesgo).filter(Riesgo.riesgo_id == riesgo_id).first()
    if not riesgo_existente:
        raise HTTPException(status_code=404, detail="Riesgo no encontrado")

    if datos_riesgo.descripcion:
        riesgo_existente.descripcion = datos_riesgo.descripcion

    db.commit()
    db.refresh(riesgo_existente)
    return riesgo_existente

def actualizar_estado_riesgo(riesgo_id: int, datos_estado: RiesgoActualizarEstado, db: Session):
    """📌 Actualiza el estado de un riesgo (activo/inactivo)."""
    riesgo_existente = db.query(Riesgo).filter(Riesgo.riesgo_id == riesgo_id).first()
    if not riesgo_existente:
        raise HTTPException(status_code=404, detail="Riesgo no encontrado")

    riesgo_existente.estado = datos_estado.estado

    db.commit()
    db.refresh(riesgo_existente)
    return riesgo_existente

def eliminar_riesgo(riesgo_id: int, db: Session):
    """📌 Elimina un riesgo de la base de datos."""
    riesgo_existente = db.query(Riesgo).filter(Riesgo.riesgo_id == riesgo_id).first()
    if not riesgo_existente:
        raise HTTPException(status_code=404, detail="Riesgo no encontrado")

    db.delete(riesgo_existente)
    db.commit()
    return {"message": "Riesgo eliminado exitosamente"}

def listar_riesgos(db: Session):
    """📌 Lista todos los riesgos disponibles."""
    return db.query(Riesgo).all()

def obtener_riesgo_por_id(riesgo_id: int, db: Session):
    """📌 Obtiene un riesgo por su ID."""
    riesgo = db.query(Riesgo).filter(Riesgo.riesgo_id == riesgo_id).first()
    if not riesgo:
        raise HTTPException(status_code=404, detail="Riesgo no encontrado")
    return riesgo
