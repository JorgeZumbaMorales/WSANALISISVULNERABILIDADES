from sqlalchemy.orm import Session
from app.modelos.vulnerabilidad import Vulnerabilidad
from app.esquemas.vulnerabilidad_esquemas import (
    VulnerabilidadCrear,
    VulnerabilidadActualizar
)
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_vulnerabilidad(datos: VulnerabilidadCrear, db: Session):
    nueva_vulnerabilidad = Vulnerabilidad(
        dispositivo_id=datos.dispositivo_id,
        tipo=datos.tipo,
        severidad=datos.severidad,
        descripcion=datos.descripcion,
        fecha_deteccion=datos.fecha_deteccion
    )
    db.add(nueva_vulnerabilidad)
    db.commit()
    db.refresh(nueva_vulnerabilidad)
    return nueva_vulnerabilidad

def listar_vulnerabilidades(db: Session):
    return db.query(Vulnerabilidad).all()

def actualizar_vulnerabilidad(vulnerabilidad_id: int, datos: VulnerabilidadActualizar, db: Session):
    vulnerabilidad = db.query(Vulnerabilidad).filter(Vulnerabilidad.vulnerabilidad_id == vulnerabilidad_id).first()
    if not vulnerabilidad:
        excepcion_no_encontrado("Vulnerabilidad")

    vulnerabilidad.tipo = datos.tipo
    vulnerabilidad.severidad = datos.severidad
    vulnerabilidad.descripcion = datos.descripcion

    db.commit()
    db.refresh(vulnerabilidad)
    return vulnerabilidad

def actualizar_estado_vulnerabilidad(vulnerabilidad_id: int, estado: bool, db: Session):
    vulnerabilidad = db.query(Vulnerabilidad).filter(Vulnerabilidad.vulnerabilidad_id == vulnerabilidad_id).first()
    if not vulnerabilidad:
        excepcion_no_encontrado("Vulnerabilidad")

    vulnerabilidad.estado = estado
    db.commit()
    db.refresh(vulnerabilidad)
    return vulnerabilidad

def eliminar_vulnerabilidad(vulnerabilidad_id: int, db: Session):
    vulnerabilidad = db.query(Vulnerabilidad).filter(Vulnerabilidad.vulnerabilidad_id == vulnerabilidad_id).first()
    if not vulnerabilidad:
        excepcion_no_encontrado("Vulnerabilidad")

    db.delete(vulnerabilidad)
    db.commit()
    return respuesta_exitosa("Vulnerabilidad eliminada exitosamente")
