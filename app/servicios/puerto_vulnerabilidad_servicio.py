from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.puerto_vulnerabilidad import PuertoVulnerabilidad
from app.esquemas.puerto_vulnerabilidad_esquemas import PuertoVulnerabilidadCrear

def asignar_vulnerabilidad_a_puerto(datos: PuertoVulnerabilidadCrear, db: Session):
    existente = db.query(PuertoVulnerabilidad).filter(
        PuertoVulnerabilidad.puerto_id == datos.puerto_id,
        PuertoVulnerabilidad.vulnerabilidad_id == datos.vulnerabilidad_id
    ).first()

    if existente:
        return existente  # Ya está asignado

    nueva_asignacion = PuertoVulnerabilidad(
        puerto_id=datos.puerto_id,
        vulnerabilidad_id=datos.vulnerabilidad_id,
        exploit=datos.exploit,
        estado=datos.estado
    )
    db.add(nueva_asignacion)
    db.commit()
    db.refresh(nueva_asignacion)
    return nueva_asignacion

def listar_vulnerabilidades_por_puerto(puerto_id: int, db: Session):
    return db.query(PuertoVulnerabilidad).filter(
        PuertoVulnerabilidad.puerto_id == puerto_id
    ).all()
