from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.recomendacion_puerto import RecomendacionPuerto
from app.esquemas.recomendacion_puerto_esquemas import RecomendacionPuertoCrear, RecomendacionPuertoActualizarEstado

def agregar_recomendacion_a_puerto(datos: RecomendacionPuertoCrear, db: Session):
    """📌 Agrega una recomendación para un puerto específico."""
    try:
        nueva_recomendacion = RecomendacionPuerto(
            puerto_id=datos.puerto_id,
            recomendacion=datos.recomendacion
        )

        db.add(nueva_recomendacion)
        db.commit()
        db.refresh(nueva_recomendacion)
        return nueva_recomendacion

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno al agregar recomendación: {str(e)}")

def obtener_recomendaciones_por_puerto(puerto_id: int, db: Session):
    """📌 Obtiene todas las recomendaciones asociadas a un puerto."""
    recomendaciones = db.query(RecomendacionPuerto).filter(RecomendacionPuerto.puerto_id == puerto_id).all()
    return recomendaciones

def actualizar_estado_recomendacion(recomendacion_id: int, datos_estado: RecomendacionPuertoActualizarEstado, db: Session):
    """📌 Actualiza el estado de una recomendación."""
    recomendacion_existente = db.query(RecomendacionPuerto).filter(RecomendacionPuerto.recomendacion_id == recomendacion_id).first()
    if not recomendacion_existente:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")

    recomendacion_existente.estado = datos_estado.estado
    db.commit()
    db.refresh(recomendacion_existente)
    return recomendacion_existente

def eliminar_recomendacion(recomendacion_id: int, db: Session):
    """📌 Elimina una recomendación de un puerto."""
    recomendacion_existente = db.query(RecomendacionPuerto).filter(RecomendacionPuerto.recomendacion_id == recomendacion_id).first()
    if not recomendacion_existente:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")

    db.delete(recomendacion_existente)
    db.commit()
    return {"message": "Recomendación eliminada exitosamente"}

def listar_todas_las_recomendaciones(db: Session):
    """📌 Lista todas las recomendaciones registradas en la base de datos."""
    return db.query(RecomendacionPuerto).all()
