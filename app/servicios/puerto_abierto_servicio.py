from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.puerto_abierto import PuertoAbierto
from app.esquemas.puerto_abierto_esquemas import PuertoAbiertoCrear, PuertoAbiertoActualizar, PuertosSeleccionadosPeticion
from sqlalchemy.orm import joinedload


def crear_puerto_abierto(datos_puerto: PuertoAbiertoCrear, db: Session):
    nuevo_puerto = PuertoAbierto(
        dispositivo_id=datos_puerto.dispositivo_id,
        puerto=datos_puerto.puerto,
        protocolo=datos_puerto.protocolo,
        servicio=datos_puerto.servicio,
        version=datos_puerto.version,
        estado=datos_puerto.estado
    )
    db.add(nuevo_puerto)
    db.flush()
    db.refresh(nuevo_puerto)
    return nuevo_puerto

def listar_puertos_abiertos(db: Session):
    return db.query(PuertoAbierto).all()

def actualizar_puerto_abierto(puerto_id: int, datos_puerto: PuertoAbiertoActualizar, db: Session):
    puerto_existente = db.query(PuertoAbierto).filter(PuertoAbierto.puerto_id == puerto_id).first()
    if not puerto_existente:
        raise HTTPException(status_code=404, detail="Puerto abierto no encontrado")
    
    for key, value in datos_puerto.dict(exclude_unset=True).items():
        setattr(puerto_existente, key, value)
    
    db.commit()
    db.refresh(puerto_existente)
    return puerto_existente

def eliminar_puerto_abierto(puerto_id: int, db: Session):
    puerto_existente = db.query(PuertoAbierto).filter(PuertoAbierto.puerto_id == puerto_id).first()
    if not puerto_existente:
        raise HTTPException(status_code=404, detail="Puerto abierto no encontrado")
    
    db.delete(puerto_existente)
    db.commit()
    return {"message": "Puerto abierto eliminado exitosamente"}

def obtener_recomendaciones_por_puertos(db: Session, request: PuertosSeleccionadosPeticion):
    """
    🔍 Obtiene las recomendaciones **solo para los puertos seleccionados**.
    """
    if not request.puertos_ids:
        raise HTTPException(status_code=400, detail="Debe proporcionar al menos un puerto para obtener recomendaciones.")

    puertos = db.query(PuertoAbierto).filter(PuertoAbierto.puerto_id.in_(request.puertos_ids)).options(joinedload(PuertoAbierto.recomendacion)).all()

    if not puertos:
        raise HTTPException(status_code=404, detail="No se encontraron puertos con recomendaciones para los IDs proporcionados.")

    resultado = []
    for puerto in puertos:
        resultado.append({
            "puerto_id": puerto.puerto_id,
            "numero": puerto.puerto,
            "protocolo": puerto.protocolo,
            "servicio": puerto.servicio,
            "version": puerto.version,
            "recomendacion": puerto.recomendacion.recomendacion if puerto.recomendacion else "No hay recomendación disponible"
        })

    return {"message": "Recomendaciones obtenidas con éxito.", "puertos": resultado}