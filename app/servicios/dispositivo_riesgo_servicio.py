from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.dispositivo_riesgo import DispositivoRiesgo
from app.esquemas.dispositivo_riesgo_esquemas import DispositivoRiesgoCrear, DispositivoRiesgoActualizarEstado

def asignar_riesgo_a_dispositivo(datos: DispositivoRiesgoCrear, db: Session):
    """📌 Asigna un riesgo a un dispositivo en la base de datos."""
    try:
        nuevo_dispositivo_riesgo = DispositivoRiesgo(
            dispositivo_id=datos.dispositivo_id,
            riesgo_id=datos.riesgo_id
        )

        db.add(nuevo_dispositivo_riesgo)
        db.commit()
        db.refresh(nuevo_dispositivo_riesgo)
        return nuevo_dispositivo_riesgo

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno al asignar riesgo: {str(e)}")

def obtener_riesgos_de_dispositivo(dispositivo_id: int, db: Session):
    """📌 Obtiene todos los riesgos asignados a un dispositivo."""
    riesgos = db.query(DispositivoRiesgo).filter(DispositivoRiesgo.dispositivo_id == dispositivo_id).all()
    return riesgos

def actualizar_estado_dispositivo_riesgo(dispositivo_riesgo_id: int, datos_estado: DispositivoRiesgoActualizarEstado, db: Session):
    """📌 Actualiza el estado de un riesgo asignado a un dispositivo."""
    relacion_existente = db.query(DispositivoRiesgo).filter(DispositivoRiesgo.dispositivo_riesgo_id == dispositivo_riesgo_id).first()
    if not relacion_existente:
        raise HTTPException(status_code=404, detail="Relación dispositivo-riesgo no encontrada")

    relacion_existente.estado = datos_estado.estado
    db.commit()
    db.refresh(relacion_existente)
    return relacion_existente

def eliminar_riesgo_de_dispositivo(dispositivo_riesgo_id: int, db: Session):
    """📌 Elimina un riesgo asignado a un dispositivo."""
    relacion_existente = db.query(DispositivoRiesgo).filter(DispositivoRiesgo.dispositivo_riesgo_id == dispositivo_riesgo_id).first()
    if not relacion_existente:
        raise HTTPException(status_code=404, detail="Relación dispositivo-riesgo no encontrada")

    db.delete(relacion_existente)
    db.commit()
    return {"message": "Relación dispositivo-riesgo eliminada exitosamente"}

def listar_todas_las_relaciones(db: Session):
    """📌 Lista todas las relaciones entre dispositivos y riesgos."""
    return db.query(DispositivoRiesgo).all()
