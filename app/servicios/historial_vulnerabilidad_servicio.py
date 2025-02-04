from sqlalchemy.orm import Session
from app.modelos.historial_vulnerabilidad import HistorialVulnerabilidad
from app.esquemas.historial_vulnerabilidad_esquemas import HistorialVulnerabilidadCrear
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_historial_vulnerabilidad(datos: HistorialVulnerabilidadCrear, db: Session):
    nuevo_historial = HistorialVulnerabilidad(
        vulnerabilidad_id=datos.vulnerabilidad_id,
        estado_anterior=datos.estado_anterior,
        estado_actual=datos.estado_actual
    )
    db.add(nuevo_historial)
    db.commit()
    db.refresh(nuevo_historial)
    return nuevo_historial

def listar_historial_vulnerabilidades(db: Session):
    return db.query(HistorialVulnerabilidad).all()

def obtener_historial_por_vulnerabilidad(vulnerabilidad_id: int, db: Session):
    historial = db.query(HistorialVulnerabilidad).filter(HistorialVulnerabilidad.vulnerabilidad_id == vulnerabilidad_id).all()
    if not historial:
        excepcion_no_encontrado("Historial de vulnerabilidad")
    return historial
